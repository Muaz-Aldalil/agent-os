#!/usr/bin/env python3
"""
Cognitive Memory, 60%-70% Context Handover & State Snapshot Engine (100X Power Suite).
Eliminates context compaction amnesia by capturing and restoring
high-density session state:
- Empirical live transcript telemetry (steps, size in KB, context % vs ~600 KB compaction cap)
- Active Objective & Execution Mode
- Locked Owner Decisions (settled choices not to re-open)
- Rejected Ideas & Debate Outcomes (why rejected paths were ruled out)
- Git branch, commit, dirty files, diff statistics
- Active scientific hypotheses & trace ledger
- Immediate Next Executable Step ([Step] -> verify: [check])
Stores persistent snapshot in .agent_snapshot.json and SESSION_SNAPSHOT.md.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_JSON = WORKSPACE_ROOT / ".agent_snapshot.json"
SNAPSHOT_MD = WORKSPACE_ROOT / "SESSION_SNAPSHOT.md"
COMPACTION_BUDGET_KB = 600.0


def _load_previous_handover() -> Dict[str, Any]:
    if SNAPSHOT_JSON.exists():
        try:
            data = json.loads(SNAPSHOT_JSON.read_text(encoding="utf-8"))
            return data.get("handover", {}) or {}
        except Exception:
            return {}
    return {}


def _measure_live_transcript() -> Dict[str, Any]:
    """Measures empirical step count, transcript size (KB), and estimated context % from the active conversation transcript."""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    try:
        if brain_dir.exists():
            transcripts = list(brain_dir.glob("*/.system_generated/logs/transcript.jsonl"))
            if transcripts:
                latest = max(transcripts, key=lambda p: p.stat().st_mtime)
                size_bytes = latest.stat().st_size
                size_kb = round(size_bytes / 1024.0, 1)
                with open(latest, "r", encoding="utf-8", errors="ignore") as f:
                    steps = sum(1 for _ in f)
                pct = min(99, max(1, int(round((size_kb / COMPACTION_BUDGET_KB) * 100))))
                return {
                    "conversation_id": latest.parent.parent.parent.name,
                    "steps": steps,
                    "transcript_kb": size_kb,
                    "estimated_pct": pct,
                }
    except (OSError, ValueError):
        return {
            "conversation_id": "unknown",
            "steps": 0,
            "transcript_kb": 0.0,
            "estimated_pct": 0,
        }
    return {
        "conversation_id": "unknown",
        "steps": 0,
        "transcript_kb": 0.0,
        "estimated_pct": 0,
    }


def freeze_session(
    label: str = "Active Working State",
    objective: Optional[str] = None,
    mode: Optional[str] = None,
    decisions: Optional[List[str]] = None,
    rejected: Optional[List[str]] = None,
    next_step: Optional[str] = None,
    context_pct: Optional[int] = None,
) -> Dict[str, Any]:
    print("[*] Freezing cognitive state and active session handover snapshot...")

    # 1. Git State
    branch = "unknown"
    sha = "unknown"
    dirty_files: List[str] = []
    diff_stat = ""
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=WORKSPACE_ROOT, text=True
        ).strip()
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=WORKSPACE_ROOT, text=True
        ).strip()
        status_out = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=WORKSPACE_ROOT, text=True
        ).strip()
        if status_out:
            dirty_files = sorted([line.strip() for line in status_out.splitlines()])
        diff_stat = subprocess.check_output(
            ["git", "diff", "--stat"], cwd=WORKSPACE_ROOT, text=True
        ).strip()
    except Exception as err:
        print(f"[!] Notice: Git status query failed during snapshot: {err}", file=sys.stderr)

    # 2. Active Traces
    active_trace = None
    trace_path = WORKSPACE_ROOT / ".agent_trace.json"
    if trace_path.exists():
        try:
            with open(trace_path, "r", encoding="utf-8") as f:
                trace_data = json.load(f)
                active_trace = trace_data.get("current_investigation")
        except Exception as err:
            print(f"[!] Notice: Failed to parse trace ledger during snapshot: {err}", file=sys.stderr)

    # 3. Measure live transcript & preserve/update structured 60%-70% Chat Handover state
    live_metrics = _measure_live_transcript()
    prev_handover = _load_previous_handover()
    resolved_pct = (
        context_pct
        if context_pct is not None
        else (live_metrics["estimated_pct"] or prev_handover.get("context_pct", 0))
    )

    handover = {
        "context_pct": resolved_pct,
        "conversation_id": live_metrics["conversation_id"],
        "decisions": decisions if decisions is not None else prev_handover.get("decisions", []),
        "mode": mode or prev_handover.get("mode", "ACTIVE_EXECUTION"),
        "next_step": next_step
        or prev_handover.get(
            "next_step",
            "Run `python D:\\Skills\\.agents\\scripts\\agent_os.py status` -> verify: all checks GREEN",
        ),
        "objective": objective or prev_handover.get("objective", label),
        "rejected": rejected if rejected is not None else prev_handover.get("rejected", []),
        "transcript_kb": live_metrics["transcript_kb"],
        "transcript_steps": live_metrics["steps"],
    }

    snapshot_data: Dict[str, Any] = {
        "active_trace": active_trace,
        "git": {
            "branch": branch,
            "commit": sha,
            "diff_stat": diff_stat,
            "dirty_files": dirty_files,
        },
        "handover": handover,
        "label": label,
        "timestamp": datetime.now().isoformat(),
    }

    # Save JSON with deterministic key sorting and LF line endings
    json_text = json.dumps(snapshot_data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    SNAPSHOT_JSON.write_text(json_text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")

    # Generate Markdown (SESSION_SNAPSHOT.md)
    md_lines = [
        f"# Session Cognitive Snapshot & 60%–70% Context Handover ({label})",
        f"- **Captured At**: {snapshot_data['timestamp']}",
        f"- **Live Context Telemetry**: `~{handover['context_pct']}%` (`{handover['transcript_kb']} KB` / `{handover['transcript_steps']} steps` in conversation `{handover['conversation_id']}`; handover threshold: `60%–70%`)",
        f"- **Execution Mode**: `{handover['mode']}`",
        f"- **Git Status**: Branch `{branch}` at commit `[{sha}]` ({len(dirty_files)} modified/untracked file(s))",
        "",
        "## 1. Active Objective",
        f"- {handover['objective']}",
        "",
        "## 2. Locked Owner Decisions (Do Not Re-Open Without New Evidence)",
    ]
    if handover["decisions"]:
        for dec in handover["decisions"]:
            md_lines.append(f"- {dec}")
    else:
        md_lines.append("- Follow active ADRs in `DECISIONS.md` and `GEMINI.md` rules.")
    md_lines.append("")

    md_lines.append("## 3. Rejected Ideas & Debate Outcomes")
    if handover["rejected"]:
        for rej in handover["rejected"]:
            md_lines.append(f"- {rej}")
    else:
        md_lines.append("- None recorded in this checkpoint.")
    md_lines.append("")

    md_lines.append("## 4. Immediate Next Step (`[Step] -> verify: [check]`)")
    md_lines.append(f"- {handover['next_step']}")
    md_lines.append("")

    if dirty_files:
        md_lines.append("## 5. Working Tree Diff State")
        for df in dirty_files:
            md_lines.append(f"- `{df}`")
        md_lines.append("")

    if diff_stat:
        md_lines.append("```text")
        md_lines.append(diff_stat)
        md_lines.append("```\n")

    if active_trace:
        md_lines.append(f"## 6. Active Investigation: {active_trace.get('title')}")
        for h in active_trace.get("hypotheses", []):
            v_str = f"[{h.get('verdict')}]" if h.get("verdict") else f"[{h.get('status')}]"
            md_lines.append(f"- **Hypothesis #{h.get('id')} {v_str}**: {h.get('statement')}")
            if h.get("notes"):
                md_lines.append(f"  * Conclusion: {h.get('notes')}")
        md_lines.append("")

    md_content = "\n".join(md_lines).replace("\r\n", "\n") + "\n"
    SNAPSHOT_MD.write_text(md_content, encoding="utf-8", newline="\n")

    print("[SUCCESS] Cognitive state frozen successfully.")
    print(f"  - Machine: {SNAPSHOT_JSON}")
    print(f"  - Markdown: {SNAPSHOT_MD}")
    print(
        f"  - Live Context: ~{handover['context_pct']}% "
        f"({handover['transcript_kb']} KB, {handover['transcript_steps']} steps)"
    )
    if handover["context_pct"] >= 60:
        print(
            f"  - [HANDOVER READY] Context at ~{handover['context_pct']}%. "
            "You can safely run `/compact` or start a fresh chat and run `snapshot resume`."
        )
    return snapshot_data


def restore_session() -> Dict[str, Any]:
    if not SNAPSHOT_JSON.exists():
        print("[!] No active session snapshot found. Run 'snapshot freeze' first.")
        return {}

    with open(SNAPSHOT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    git = data.get("git", {})
    trace = data.get("active_trace", {})
    handover = data.get("handover", {})

    print("=" * 68)
    print("      ANTIGRAVITY 100X ENGINE - SESSION HANDOVER RESUME          ")
    print("=" * 68)
    print(f"Snapshot Label:  {data.get('label')}")
    print(f"Captured:        {data.get('timestamp', '')[:19]}")
    print(
        f"Mode / Load:     {handover.get('mode', 'ACTIVE')} "
        f"(~{handover.get('context_pct', 0)}% context, "
        f"{handover.get('transcript_kb', 0)} KB / {handover.get('transcript_steps', 0)} steps)"
    )
    print(f"Git Head:        Branch '{git.get('branch')}' at [{git.get('commit')}]")
    print(f"Uncommitted:     {len(git.get('dirty_files', []))} file(s)")
    print("-" * 68)

    if handover.get("objective"):
        print(f"Objective:       {handover['objective']}")
    if handover.get("decisions"):
        print("Locked Decisions:")
        for d in handover["decisions"]:
            print(f"  + {d}")
    if handover.get("rejected"):
        print("Rejected / Ruled Out:")
        for r in handover["rejected"]:
            print(f"  - {r}")
    if handover.get("next_step"):
        print(f"Next Step:       {handover['next_step']}")

    if git.get("dirty_files"):
        print("\nActive Changes:")
        for df in git["dirty_files"][:8]:
            print(f"  * {df}")
        if len(git["dirty_files"]) > 8:
            print(f"  ... and {len(git['dirty_files']) - 8} more")

    if trace:
        print("\nActive Investigation:")
        print(f"  Title: {trace.get('title')}")
        for h in trace.get("hypotheses", []):
            v = h.get("verdict") or h.get("status")
            print(f"  * Hypo #{h.get('id')} [{v}]: {h.get('statement')[:70]}...")

    print("=" * 68)
    print("[READY] Cognitive context restored. Zero amnesia.")
    print("=" * 68)
    return data


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/snapshot.py <freeze [label] [--objective ...] "
            "[--decision ...] [--rejected ...] [--next ...] [--context-pct N] | resume>"
        )
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "freeze":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("label_words", nargs="*")
        parser.add_argument("--objective", default=None)
        parser.add_argument("--mode", default=None)
        parser.add_argument("--decision", action="append", dest="decisions", default=None)
        parser.add_argument("--rejected", action="append", dest="rejected", default=None)
        parser.add_argument("--next", dest="next_step", default=None)
        parser.add_argument("--context-pct", type=int, default=None)
        args, unknown = parser.parse_known_args(sys.argv[2:])
        label_parts = args.label_words + unknown
        label = " ".join(label_parts).strip() if label_parts else "Active Working State"
        freeze_session(
            label=label,
            objective=args.objective,
            mode=args.mode,
            decisions=args.decisions,
            rejected=args.rejected,
            next_step=args.next_step,
            context_pct=args.context_pct,
        )
    elif cmd in ["resume", "restore"]:
        restore_session()
    else:
        print(f"Unknown command: '{cmd}'. Available: freeze [label], resume")


if __name__ == "__main__":
    main()
