#!/usr/bin/env python3
"""
scripts/runtime_observer.py
Runtime Log Ingestion & Server Health Probe for Agent OS.

Bridges the gap between static code inspection and live runtime observability.
Provides log tailing with stack trace extraction and zero-dependency HTTP server health probing.
"""

import os
import sys
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AGENT_OS_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(os.environ.get("AGENT_OS_PROJECT_ROOT") or Path.cwd()).resolve()
WORKSPACE_ROOT = PROJECT_ROOT

COMMON_LOG_GLOBS = [
    "storage/logs/*.log",
    "logs/*.log",
    ".next/*.log",
    "var/log/*.log",
    "*.log"
]

FORBIDDEN_LOG_FILE_REGEX = re.compile(
    r"(?:^|[\\/]|^[a-zA-Z]:)(?:\.env(?:\..+)?|id_rsa.*|id_ed25519.*|id_ecdsa.*|.*\.(?:pem|key)|credentials\.json|\.kube[\\/]config|\.gcloud[\\/](?:credentials|application_default_credentials\.json)|\.npmrc|\.pypirc)$",
    re.IGNORECASE,
)

SECRET_REDACTION_PATTERNS = [
    (re.compile(r"(Bearer\s+)[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE), r"\1[REDACTED]"),
    (re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{10,}\b"), "[REDACTED_STRIPE_KEY]"),
    (re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"), "[REDACTED_GOOGLE_KEY]"),
    (re.compile(r"\bAQ\.Ab[0-9A-Za-z\-_]{20,}\b"), "[REDACTED_STITCH_KEY]"),
    (re.compile(r"(X-Goog-Api-Key\s*[:=]\s*)([^\s,;\"']+)", re.IGNORECASE), r"\1[REDACTED_STITCH_KEY]"),
    (re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"), "[REDACTED_GITHUB_PAT]"),
    (re.compile(r"\bnfp_[A-Za-z0-9]{20,}\b"), "[REDACTED_NETLIFY_PAT]"),
    (
        re.compile(r"((?:password|passwd|secret|api_key|apikey|token|access_token)\s*[=:]\s*)([^\s,;\"']+)", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
]


def _is_forbidden_secret_path(path: Path) -> bool:
    return bool(FORBIDDEN_LOG_FILE_REGEX.search(str(path)))


def _redact_secrets(line: str) -> str:
    redacted = line
    for pat, repl in SECRET_REDACTION_PATTERNS:
        redacted = pat.sub(repl, redacted)
    return redacted


def find_latest_log_file(custom_path: Optional[str] = None) -> Optional[Path]:
    if custom_path:
        p = Path(custom_path)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        if _is_forbidden_secret_path(p):
            return None
        return p if p.is_file() else None

    candidates: List[Path] = []
    for pattern in COMMON_LOG_GLOBS:
        for p in PROJECT_ROOT.glob(pattern):
            if p.is_file() and not _is_forbidden_secret_path(p) and p.stat().st_size > 0:
                candidates.append(p)

    if not candidates:
        return None

    # Return most recently modified log file
    candidates.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return candidates[0]


def tail_log(log_path: Path, lines_count: int = 50) -> Dict[str, Any]:
    if _is_forbidden_secret_path(log_path):
        return {
            "error": f"SecurityViolation: Refusing to ingest sensitive secret/key file '{log_path.name}' as a log.",
            "lines": [],
            "errors_detected": 0,
        }
    try:
        content = log_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": f"Failed to read log file: {e}", "lines": [], "errors_detected": 0}

    all_lines = content.splitlines()
    raw_recent = all_lines[-lines_count:] if len(all_lines) > lines_count else all_lines
    recent = [_redact_secrets(l) for l in raw_recent]

    # Detect errors / stack traces
    error_patterns = [
        re.compile(r"\b(?:FATAL|ERROR|CRITICAL|EXCEPTION|Exception|Traceback)\b"),
        re.compile(r"^\s*at\s+[\w\.<>]+(?:\s*\(.*?\))?"),  # JS / Node stack trace
        re.compile(r"^\s*#\d+\s+"),  # PHP stack trace
        re.compile(r"^\s*File \".*?\", line \d+"),  # Python stack trace
    ]

    error_lines = []
    for l in recent:
        for pat in error_patterns:
            if pat.search(l):
                error_lines.append(l)
                break

    return {
        "file": str(log_path.relative_to(PROJECT_ROOT) if log_path.is_relative_to(PROJECT_ROOT) else log_path),
        "total_file_lines": len(all_lines),
        "lines_returned": len(recent),
        "lines": recent,
        "errors_detected": len(error_lines),
        "error_snippets": error_lines[:15]
    }


def probe_endpoint(url: str, timeout: float = 3.0) -> Dict[str, Any]:
    start_time = time.perf_counter()
    parsed = urllib.parse.urlparse(str(url or "").strip())
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        return {
            "url": url,
            "reachable": False,
            "status_code": 0,
            "latency_ms": 0.0,
            "error": f"SecurityViolation: Only http:// and https:// URLs are permitted (got scheme '{parsed.scheme or 'none'}').",
            "body_preview": "",
        }

    headers = {"User-Agent": "Antigravity-AgentOS-Probe/1.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            status_code = response.getcode() or 200
            headers_dict = dict(response.info())
            raw_body = response.read(1024)
            body_preview = _redact_secrets(raw_body.decode("utf-8", errors="replace"))

            return {
                "url": url,
                "reachable": True,
                "status_code": int(status_code),
                "latency_ms": latency_ms,
                "headers": {k: headers_dict[k] for k in list(headers_dict.keys())[:5]},
                "body_preview": body_preview[:300]
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        raw_body = e.read(1024) if hasattr(e, "read") else b""
        body_preview = _redact_secrets(raw_body.decode("utf-8", errors="replace")) if raw_body else ""
        return {
            "url": url,
            "reachable": True,
            "status_code": int(e.code or 500),
            "latency_ms": latency_ms,
            "error": f"HTTP {e.code}: {e.reason}",
            "body_preview": body_preview[:300]
        }
    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "url": url,
            "reachable": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "error": str(e),
            "body_preview": ""
        }


def print_log_summary(res: Dict[str, Any]):
    print("=" * 65)
    print("      ANTIGRAVITY AGENT OS - RUNTIME LOG INGESTION REPORT     ")
    print("=" * 65)
    if "error" in res:
        print(f"[ERROR] {res['error']}")
        print("=" * 65)
        return

    print(f"Log File:        {res.get('file')}")
    print(f"Total Lines:     {res.get('total_file_lines')} lines")
    print(f"Errors Found:    {res.get('errors_detected')} error lines in last {res.get('lines_returned')} lines")
    print("-" * 65)

    if res.get("error_snippets"):
        print("[CRITICAL STACK TRACES & EXCEPTIONS DETECTED]:")
        for snip in res["error_snippets"]:
            print(f"  > {snip}")
    else:
        print("[INFO] Zero recent stack traces or fatal errors detected.")
        print("[RECENT LOG TAIL]:")
        for l in res.get("lines", [])[-10:]:
            print(f"  | {l}")
    print("=" * 65)


def print_probe_summary(res: Dict[str, Any]):
    print("=" * 65)
    print("       ANTIGRAVITY AGENT OS - RUNTIME SERVER HEALTH PROBE     ")
    print("=" * 65)
    print(f"Target URL:    {res.get('url')}")
    print(f"Reachable:     {res.get('reachable')}")
    print(f"Latency:       {res.get('latency_ms')} ms")
    if res.get("reachable"):
        print(f"Status Code:   {res.get('status_code')}")
        if res.get("error"):
            print(f"Notice:        {res.get('error')}")
        print("-" * 65)
        print("[RESPONSE PREVIEW]:")
        print(res.get("body_preview", "")[:200])
    else:
        print(f"[CONNECTION FAILED]: {res.get('error')}")
    print("=" * 65)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/runtime_observer.py <logs|probe> [args...]")
        print("  logs [--tail N] [--file <path>]")
        print("  probe <url> [--timeout S]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "logs":
        lines_count = 50
        file_path = None
        idx = 2
        while idx < len(sys.argv):
            if sys.argv[idx] == "--tail" and idx + 1 < len(sys.argv):
                lines_count = int(sys.argv[idx + 1])
                idx += 2
            elif sys.argv[idx] == "--file" and idx + 1 < len(sys.argv):
                file_path = sys.argv[idx + 1]
                idx += 2
            else:
                idx += 1

        if file_path and _is_forbidden_secret_path(Path(file_path)):
            print(f"[ERROR] SecurityViolation: Refusing to read sensitive file '{file_path}'.")
            sys.exit(1)

        log_file = find_latest_log_file(file_path)
        if not log_file:
            print("[INFO] No log files found in workspace (checked storage/logs, logs/, *.log).")
            sys.exit(0)
        res = tail_log(log_file, lines_count)
        print_log_summary(res)
        sys.exit(1 if "error" in res else 0)

    elif cmd == "probe":
        if len(sys.argv) < 3:
            print("Error: 'probe' requires a URL (e.g. http://localhost:3000)")
            sys.exit(1)
        url = sys.argv[2]
        timeout = 3.0
        if "--timeout" in sys.argv:
            t_idx = sys.argv.index("--timeout")
            if t_idx + 1 < len(sys.argv):
                timeout = float(sys.argv[t_idx + 1])
        res = probe_endpoint(url, timeout)
        print_probe_summary(res)
        status_code = int(res.get("status_code") or 0)
        sys.exit(0 if res.get("reachable") and 0 < status_code < 500 else 1)
    else:
        print(f"Unknown command: '{cmd}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
