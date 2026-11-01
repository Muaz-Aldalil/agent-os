#!/usr/bin/env python3
"""
PreToolUse Safety Hook for Antigravity Agent.
Intercepts run_command, view_file, write_to_file, and replace_file_content tool calls to enforce:
1. Workspace Boundary & Danger Zone isolation
2. Secret Leak prevention (.env, SSH keys, cloud credentials across shell & file tools)
3. Destructive command gating (hard git resets with -C flags, PowerShell/POSIX directory wipeouts, force pushes, DB drops)
4. Self-protection of safety_hook.py, hooks.json, and .git/hooks/*
5. Fail-closed evaluation on malformed/null payloads
"""

import sys
import json
import re
import os
from pathlib import Path
from typing import Any, Dict, Tuple

# Ensure clean UTF-8 encoding across Windows console environments
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_READ_VERBS = r"(?:cat|type|Get-Content|gc|head|tail|more|less|Select-String|sls|rg|grep|findstr|Get-Item|gi|Get-ChildItem|gci|ReadAllText|ReadAllBytes|ReadAllLines|ReadLines|OpenRead|OpenText|StreamReader)"
_ENV_TARGET = r"(?:\.env(?!\.(?:example|sample|template)\b)(?:\.[a-zA-Z0-9_-]+)?\b|\.e['\"\s+]+\+\s*['\"]?nv\b)"
_KEY_TARGET = r"(?:id_rsa|id_ed25519|id_ecdsa|\.pem\b|\.key\b)"
_CLOUD_TARGET = r"(?:\.aws[\\/]credentials|\.docker[\\/]config\.json|\.kube[\\/]config|\.gcloud[\\/](?:credentials|application_default_credentials\.json)|\.npmrc\b|\.pypirc\b)"

# Patterns indicating attempts to dump sensitive secrets
SECRET_LEAK_PATTERNS = [
    (
        rf"(?:\b{_READ_VERBS}\b|\[(?:System\.)?IO\.File\]).*{_ENV_TARGET}",
        "Attempt to dump or search plaintext environment file containing secrets or API tokens",
    ),
    (
        rf"(?:\b{_READ_VERBS}\b|\[(?:System\.)?IO\.File\]).*{_KEY_TARGET}",
        "Attempt to dump or search private SSH or TLS encryption keys",
    ),
    (
        rf"(?:\b{_READ_VERBS}\b|\[(?:System\.)?IO\.File\]).*{_CLOUD_TARGET}",
        "Attempt to dump or search cloud provider authentication credentials",
    ),
    (
        rf"(?:python\d*(?:\.exe)?\s+.*-c|node(?:\.exe)?\s+.*-e|php(?:\.exe)?\s+.*-r|agent_os\.py\s+(?:eval|py|probe|logs)|repl_sandbox\.py|runtime_observer\.py).*(?:{_ENV_TARGET}|{_KEY_TARGET}|{_CLOUD_TARGET})",
        "Attempt to read sensitive secret or credential file via inline script or CLI observer",
    ),
    (
        r"\bprobe\s+file:",
        "Attempt to probe local filesystem via file:// URI scheme",
    ),
]

# Patterns for destructive or dangerous system/git operations
DESTRUCTIVE_PATTERNS = [
    (
        r"\bgit\b(?:\s+\S+)*?\s+reset\b(?:\s+\S+)*?\s+--hard\b",
        "Hard git reset would discard all uncommitted changes and modified files",
    ),
    (
        r"\bgit\b(?:\s+\S+)*?\s+clean\b(?:\s+\S+)*?\s+(?:-[a-zA-Z]*f|--force\b)",
        "Untracked file wipeout would permanently delete new files",
    ),
    (
        r"\bgit\b(?:\s+\S+)*?\s+checkout\b(?:\s+\S+)*?\s+(?:-f\b|--force\b)",
    "Forced git checkout discards local uncommitted modifications",
    ),
    (
        r"\bgit\b(?:\s+\S+)*?\s+push\b(?:\s+\S+)*?\s+(?:-[a-zA-Z]*f\b|--force\b|--force-with-lease\b)",
        "Force-pushing may overwrite remote team commit history",
    ),
    (
        r"\b(?:rmdir|rd)\s+/[sS]\s+/[qQ]\b",
        "Recursive directory deletion destroys filesystem or version control data",
    ),
    (
        r"\b(?:del|erase)\b(?:\s+/[a-zA-Z])*(?:\s+/[sS]\b)(?:\s+/[a-zA-Z])*\s+\S+",
        "Recursive Windows file deletion (del /s) destroys directory trees",
    ),
    (
        r"\b(?:Remove-Item|ri|del|erase|rmdir|rd)\b.*(?:\.git\b|-Recurse\b|-Force\b|\s-r\b|\s-fo\b)",
        "Destructive PowerShell/shell item removal targeting .git or using recursive/force flags",
    ),
    (
        r"\brm\b(?:\s+-[a-zA-Z]+)+\s+.*(?:\.git\b|[/~*])",
        "Recursive or forced rm targeting .git, root, home, or wildcard paths",
    ),
    (
        r"\bmigrate:(?:fresh|reset|refresh)\b",
        "Destructive migration command drops or rolls back all database tables",
    ),
    (
        r"\bdb:wipe\b",
        "db:wipe drops all database tables, views, and types",
    ),
    (
        r"\bprisma\s+migrate\s+reset\b",
        "prisma migrate reset drops and recreates the database",
    ),
    (
        r"\bDROP\s+(?:DATABASE|SCHEMA|TABLE)\b",
        "DROP DATABASE/SCHEMA/TABLE destroys application schemas and data",
    ),
    (
        r"\bTRUNCATE\s+TABLE\b",
        "TRUNCATE TABLE wipes all rows in target table",
    ),
    (
        r"\b(?:curl|wget)\s+.*\|\s*(?:bash|sh|zsh|powershell|pwsh|cmd)\b",
        "Piping unverified remote web script directly into shell interpreter",
    ),
    (
        r"\b(?:iwr|Invoke-WebRequest|irm|Invoke-RestMethod|curl|wget)\b.*\|\s*(?:iex|Invoke-Expression)\b",
        "Piping unverified remote download directly into PowerShell Invoke-Expression",
    ),
    (
        r"\b(?:iex|Invoke-Expression)\s*\(.*(?:iwr|Invoke-WebRequest|curl|irm|Invoke-RestMethod)\b",
        "Executing unverified remote download directly in PowerShell",
    ),
    (
        r"\b(?:taskkill\b.*(?:/im\s+node(?:\.exe)?\b)|Get-Process\s+node\b.*\|\s*(?:Stop-Process|spps|kill)\b|(?:Stop-Process|spps)\b.*\b-Name\s+['\"]?node\b)",
        "Blanket termination of all node.exe processes across ports is prohibited (Multi-Server Port Safety)",
    ),
]

# Authorized projects (owner-granted full access; boundary lock lifted, 2026-10-06, ADR-022):
#   - KNZiN Project (D:\Work Projects\Knzin Project)
# Secret-leak and destructive-command guards below STILL apply inside authorized projects.
# Danger Zones - strictly isolated foreign paths / projects (add (regex, reason) tuples here)
DANGER_ZONE_KEYWORDS = []

SENSITIVE_FILE_REGEX = re.compile(
    r"(?:^|[\\/]|^[a-zA-Z]:)(?:\.env(?:\.(?!example$|sample$|template$)[a-zA-Z0-9_-]+)?|id_rsa|id_ed25519|id_ecdsa|.*\.(?:pem|key)|\.aws[\\/]credentials|\.docker[\\/]config\.json|\.kube[\\/]config|\.gcloud[\\/](?:credentials|application_default_credentials\.json)|\.npmrc|\.pypirc)$",
    re.IGNORECASE,
)

PROTECTED_HOOK_FILE_REGEX = re.compile(
    r"(?:^|[\\/]|^[a-zA-Z]:)(?:safety_hook\.py|hooks\.json|mcp_config\.json|\.git[\\/]hooks[\\/].*)$",
    re.IGNORECASE,
)


def evaluate_command(cmd: str, cwd: str) -> Tuple[str, str]:
    """
    Evaluates command line and current working directory against security rules.
    Returns (decision, reason).
    """
    if not isinstance(cmd, str) or not isinstance(cwd, str):
        return ("force_ask", "SAFETY GUARD BLOCKED: CommandLine and Cwd must be valid strings.")

    normalized_cmd = cmd.strip()
    if not normalized_cmd:
        return ("force_ask", "SAFETY GUARD BLOCKED: Empty or null CommandLine is not permitted.")

    normalized_cwd = os.path.normpath(cwd) if cwd else ""

    # 1. Check Cwd and CommandLine for Danger Zone isolation
    for keyword_regex, reason in DANGER_ZONE_KEYWORDS:
        if re.search(keyword_regex, normalized_cwd, re.IGNORECASE):
            return (
                "force_ask",
                f"WORKSPACE BOUNDARY VIOLATION: Execution directory '{normalized_cwd}' is restricted. {reason}",
            )
        if re.search(keyword_regex, normalized_cmd, re.IGNORECASE):
            return (
                "force_ask",
                f"WORKSPACE BOUNDARY VIOLATION: Command references restricted entity. {reason}",
            )

    # 2. Check Secret Leak Patterns
    for pattern, reason in SECRET_LEAK_PATTERNS:
        if re.search(pattern, normalized_cmd, re.IGNORECASE):
            return ("force_ask", f"SECRET LEAK PREVENTION: {reason} ('{normalized_cmd}')")

    # 3. Check Destructive Patterns
    for pattern, reason in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, normalized_cmd, re.IGNORECASE):
            return ("force_ask", f"SAFETY GUARD BLOCKED: {reason} ('{normalized_cmd}')")

    return ("allow", "")


def evaluate_tool_call(tool_name: str, args: Dict[str, Any]) -> Tuple[str, str]:
    """Evaluates PreToolUse payloads across run_command, view_file, write_to_file, and replace_file_content."""
    if not isinstance(tool_name, str) or not isinstance(args, dict):
        return ("force_ask", "SAFETY GUARD BLOCKED: Malformed toolCall payload.")

    if tool_name == "run_command":
        raw_cmd = args.get("CommandLine")
        raw_cwd = args.get("Cwd", "")
        if not isinstance(raw_cmd, str) or not raw_cmd.strip():
            return ("force_ask", "SAFETY GUARD BLOCKED: Missing, null, or non-string CommandLine.")
        return evaluate_command(raw_cmd, str(raw_cwd or ""))

    if tool_name == "view_file":
        abs_path = str(args.get("AbsolutePath") or "").strip()
        if not abs_path:
            return ("force_ask", "SAFETY GUARD BLOCKED: Missing AbsolutePath in view_file.")
        norm_path = os.path.normpath(abs_path)
        for candidate in (abs_path, norm_path):
            for keyword_regex, reason in DANGER_ZONE_KEYWORDS:
                if re.search(keyword_regex, candidate, re.IGNORECASE):
                    return ("force_ask", f"WORKSPACE BOUNDARY VIOLATION: '{abs_path}' is restricted. {reason}")
            if SENSITIVE_FILE_REGEX.search(candidate):
                return (
                    "force_ask",
                    f"SECRET LEAK PREVENTION: Direct file view of sensitive secret/key file '{abs_path}' requires explicit owner approval.",
                )
        return ("allow", "")

    if tool_name in ("write_to_file", "replace_file_content"):
        target_file = str(args.get("TargetFile") or "").strip()
        if not target_file:
            return ("force_ask", f"SAFETY GUARD BLOCKED: Missing TargetFile in {tool_name}.")
        norm_target = os.path.normpath(target_file)
        for candidate in (target_file, norm_target):
            for keyword_regex, reason in DANGER_ZONE_KEYWORDS:
                if re.search(keyword_regex, candidate, re.IGNORECASE):
                    return ("force_ask", f"WORKSPACE BOUNDARY VIOLATION: '{target_file}' is restricted. {reason}")
            if PROTECTED_HOOK_FILE_REGEX.search(candidate) or SENSITIVE_FILE_REGEX.search(candidate):
                return (
                    "force_ask",
                    f"SAFETY GUARD BLOCKED: Modifying protected security or credential file ('{target_file}') requires explicit owner confirmation.",
                )
        return ("allow", "")

    return ("allow", "")


def main() -> int:
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            print(json.dumps({
                "decision": "force_ask",
                "reason": "Safety hook received empty stdin payload (fail-closed)."
            }))
            return 0

        data = json.loads(raw_input)
        if not isinstance(data, dict):
            print(json.dumps({
                "decision": "force_ask",
                "reason": "Safety hook received non-object JSON payload (fail-closed)."
            }))
            return 0

        tool_call = data.get("toolCall")
        if not isinstance(tool_call, dict):
            print(json.dumps({
                "decision": "force_ask",
                "reason": "Safety hook received missing or invalid toolCall object (fail-closed)."
            }))
            return 0

        tool_name = str(tool_call.get("name") or "")
        args = tool_call.get("args")
        if not isinstance(args, dict):
            print(json.dumps({
                "decision": "force_ask",
                "reason": "Safety hook received non-dict toolCall.args (fail-closed)."
            }))
            return 0

        decision, reason = evaluate_tool_call(tool_name, args)
        if decision != "allow":
            print(json.dumps({
                "decision": decision,
                "reason": reason
            }))
            return 0

        print(json.dumps({"decision": "allow"}))
        return 0
    except Exception as e:
        # Fail-closed on any unexpected exception so malformed payloads cannot bypass the hook
        print(json.dumps({
            "decision": "force_ask",
            "reason": f"Safety hook evaluation error (fail-closed): {str(e)}"
        }))
        return 0


if __name__ == "__main__":
    sys.exit(main())
