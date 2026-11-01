#!/usr/bin/env python3
"""
scripts/daily_planner.py
Autonomous Daily / Session Triage & Skill-Evolution Planner for Antigravity Agent OS.

Handles two core modes autonomously so the Owner never has to write a manual daily plan:
1. Daily / Session Triage Mode (`python scripts/agent_os.py plan-daily [focus_hint]`):
   - Inspects git branch, working tree status, and recent commit history.
   - Scans PROGRESS.md, DECISIONS.md, SESSION_SNAPSHOT.md, tasks.md, and docs/release-tracker.md.
   - Auto-detects project stack (Next.js/TS, Laravel/PHP, WordPress/Woo, Python, Agent OS).
   - Selects ONE Primary Focus for the session (breaking down large tasks) and parks the rest in "Up Next".
   - Attaches non-negotiable architectural & layer boundary guardrails and local quality gates
     (strictly halting before git commit/push per GEMINI.md Constitutional Rule 5).
2. Skill / Tool Evolution Mode (`python scripts/agent_os.py plan-daily --skill <name> [description]`):
   - Plans and scaffolds a new or upgraded skill/tool across skills/, scripts/, tests/, and global config sync.
"""

import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def get_git_context(project_dir: Path) -> Dict[str, Any]:
    """Extracts current git branch, head SHA, dirty files, and recent commits."""
    ctx: Dict[str, Any] = {
        "branch": "unknown",
        "sha": "unknown",
        "dirty_files": [],
        "recent_commits": [],
    }
    try:
        ctx["branch"] = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=project_dir,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or "HEAD"
        ctx["sha"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_dir,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        status_out = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=project_dir,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if status_out:
            ctx["dirty_files"] = [line.strip() for line in status_out.splitlines() if line.strip()]
        log_out = subprocess.check_output(
            ["git", "log", "-n", "5", "--oneline"],
            cwd=project_dir,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if log_out:
            ctx["recent_commits"] = [line.strip() for line in log_out.splitlines() if line.strip()]
    except (subprocess.SubprocessError, OSError):
        ctx["branch"] = ctx.get("branch") or "uninitialized"
    return ctx


def detect_project_stack(project_dir: Path) -> Dict[str, Any]:
    """Detects project stack, mandatory guards, and local quality gate commands."""
    stacks: List[str] = []
    guards: List[str] = ["clean-code-guard (Rules 1-27 + Layer/Domain Boundaries)", "test-guard"]
    quality_gates: List[str] = []

    has_pkg = (project_dir / "package.json").exists() or (project_dir / "frontend" / "package.json").exists()
    has_composer = (project_dir / "composer.json").exists() or (project_dir / "backend" / "composer.json").exists()
    has_wp = any((project_dir / p).exists() for p in ["wp-config.php", "wp-content", "style.css"])
    is_agent_os = (project_dir / "scripts" / "agent_os.py").exists() and (project_dir / "skills").exists()

    if is_agent_os:
        stacks.append("Antigravity Agent OS (Python CLI + Skills Ecosystem)")
        guards.extend(["engineering-workflow", "docs-guard"])
        quality_gates.extend([
            "python scripts/agent_os.py test",
            "python scripts/agent_os.py audit",
            "python scripts/agent_os.py sync --apply",
        ])

    if has_pkg:
        stacks.append("Next.js / React / TypeScript Frontend")
        guards.extend(["nextjs-fullstack", "next-server-action-guard", "rtl-logical-guard", "muaz-skill"])
        quality_gates.extend([
            "npm run lint && npm run typecheck",
            "npm test -- --watch=false",
            "npm run build",
        ])

    if has_composer:
        stacks.append("Laravel / PHP Backend")
        guards.extend(["laravel-mastery", "pest-security-guard", "backend-api", "database"])
        quality_gates.extend([
            "php artisan test",
            "python D:/Skills/.agents/scripts/agent_os.py sentinel",
        ])

    if has_wp and not has_composer:
        stacks.append("WordPress / WooCommerce")
        guards.extend(["wp-guard", "woo-guard", "rtl-logical-guard"])

    if not stacks:
        stacks.append("General Software Project")
        quality_gates.append("python D:/Skills/.agents/scripts/agent_os.py sentinel")

    return {
        "stacks": stacks,
        "guards": list(dict.fromkeys(guards)),
        "quality_gates": list(dict.fromkeys(quality_gates)),
    }


def extract_Candidate_tasks(project_dir: Path, focus_hint: str = "") -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Scans project tracking files for unchecked tasks or next actions.
    Returns (tasks_list, discovered_tracker_files).
    """
    candidate_files = [
        "PROGRESS.md",
        "tasks.md",
        "SESSION_SNAPSHOT.md",
        "docs/release-tracker.md",
        "docs/IMPLEMENTATION_PLAN.md",
        "docs/06-IMPLEMENTATION-PLAN.md",
        "TODO.md",
    ]
    # Also check specs/*/tasks.md if present
    specs_dir = project_dir / "specs"
    if specs_dir.exists() and specs_dir.is_dir():
        for p in sorted(specs_dir.glob("*/tasks.md")):
            rel = str(p.relative_to(project_dir)).replace("\\", "/")
            if rel not in candidate_files:
                candidate_files.append(rel)

    discovered_files: List[str] = []
    extracted_tasks: List[Dict[str, str]] = []

    checkbox_pat = re.compile(r"^\s*[-*]\s*\[\s*\]\s+(.+)$")
    numbered_next_pat = re.compile(r"^\s*\d+\.\s+(.+)$")

    for rel_path in candidate_files:
        fp = project_dir / rel_path
        if not fp.exists() or not fp.is_file():
            continue
        discovered_files.append(rel_path)
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        in_next_section = False
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                heading_lower = stripped.lower()
                in_next_section = any(
                    k in heading_lower
                    for k in ["next", "todo", "pending", "remaining", "action", "backlog"]
                )
                continue

            m_cb = checkbox_pat.match(line)
            if m_cb:
                task_text = m_cb.group(1).strip()
                extracted_tasks.append({"source": rel_path, "task": task_text})
                continue

            if in_next_section:
                m_num = numbered_next_pat.match(line)
                if m_num:
                    task_text = m_num.group(1).strip()
                    extracted_tasks.append({"source": rel_path, "task": task_text})

    # Filter or prioritize by focus_hint if provided
    if focus_hint:
        hint_lower = focus_hint.lower()
        matching = [t for t in extracted_tasks if hint_lower in t["task"].lower()]
        non_matching = [t for t in extracted_tasks if hint_lower not in t["task"].lower()]
        if matching:
            extracted_tasks = matching + non_matching
        else:
            extracted_tasks.insert(0, {
                "source": "Owner Focus Directive",
                "task": focus_hint.strip(),
            })

    return extracted_tasks, discovered_files


def build_daily_plan(project_dir: Path, focus_hint: str = "", skill_mode: Optional[str] = None) -> Dict[str, Any]:
    """Builds the structured autonomous daily/session plan dictionary."""
    git_ctx = get_git_context(project_dir)
    stack_ctx = detect_project_stack(project_dir)
    tasks, tracker_files = extract_Candidate_tasks(
        project_dir,
        focus_hint="" if skill_mode else focus_hint,
    )

    if skill_mode:
        primary_focus = {
            "source": "Skill & Tool Evolution Factory",
            "task": f"Design, implement, test, and globally sync skill/tool: '{skill_mode}'"
            + (f" ({focus_hint})" if focus_hint else ""),
        }
        execution_steps = [
            f"1. [Context & Deduplication]: Inspect existing skills/scripts in D:/Skills/.agents to avoid duplication and verify GEMINI.md Constitutional compliance.",
            f"2. [Skill Specification]: Create or update skills/{skill_mode}/SKILL.md (and references/) with strict rules, triggers, and self-checks.",
            f"3. [Deterministic CLI Engine]: Implement or extend the Python engine in scripts/ and wire command routing in scripts/agent_os.py & scripts/skill_router.py.",
            f"4. [Verification Battery]: Add unit tests in tests/ covering both positive/compliant and negative/adversarial cases.",
            f"5. [Audit & Global Sync]: Run `python scripts/agent_os.py test`, `python scripts/agent_os.py audit`, and `python scripts/agent_os.py sync --apply`.",
        ]
        up_next = [t["task"] for t in tasks[:4]]
    else:
        if tasks:
            primary_focus = tasks[0]
            up_next = [f"{t['task']} ({t['source']})" for t in tasks[1:6]]
        elif git_ctx["dirty_files"]:
            primary_focus = {
                "source": "Working Tree (git status)",
                "task": f"Complete, verify, and guard-audit in-progress modifications ({len(git_ctx['dirty_files'])} touched file(s))",
            }
            up_next = ["Run full regression & guard audit once working tree changes are verified."]
        else:
            primary_focus = {
                "source": "Repository Baseline Triage",
                "task": "Run proactive architectural & UI audit to select next high-leverage feature or defect fix",
            }
            up_next = ["Inspect DECISIONS.md / backlog or await Owner feature directive."]

        execution_steps = [
            "1. [Context Reconstruction]: Inspect target files, contracts, and adjacent neighbors before editing (Zero Blind Code Writing).",
            "2. [Ambiguity & Authority Check]: Verify upstream business/product rules; ask Owner ONLY if a policy gap exists.",
            "3. [Surgical Implementation]: Implement the primary focus while enforcing Layer/Domain/Shell boundaries and RTL logical properties.",
            "4. [Adversarial Self-Audit]: Run `clean-code-guard` (Imperatives 1-27) + `agent_os.py scan` on all modified files.",
            "5. [Quality Gate & Handoff]: Execute local lint, typecheck, unit tests, and build; present Edited-File Traceability Manifest.",
        ]

    try:
        from scripts.skill_router import resolve_task_routing
    except ImportError:
        from skill_router import resolve_task_routing

    routing = resolve_task_routing(primary_focus["task"])

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "project_dir": str(project_dir.resolve()),
        "git": git_ctx,
        "stack": stack_ctx,
        "tracker_files": tracker_files,
        "primary_focus": primary_focus,
        "phase_loadout": routing.get("phase_loadout", {}),
        "execution_steps": execution_steps,
        "up_next": up_next,
        "non_negotiable_rules": [
            "RULE 1 (One Primary Focus): Complete and verify the Primary Focus before touching 'Up Next' items.",
            "RULE 2 (Architectural Boundaries): Never skip layers (Controller/UI -> Service/Action -> Repository/DB). Never import server/DB modules in 'use client' or mix Public/Admin shells.",
            "RULE 3 (6-State UI & RTL): Cover Idle, Loading, Empty, Success, Error, and RTL logical properties (ms-*, me-*, ps-*, pe-*).",
            "RULE 4 (Git & Deploy Quota Safety): NEVER auto-commit, auto-push, or auto-merge. Stop after local Quality Gate passes and wait for explicit Owner instruction.",
        ],
    }


def format_daily_plan_report(plan: Dict[str, Any]) -> str:
    """Formats the daily/session plan as a clear, structured terminal report."""
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append(f"  ANTIGRAVITY AGENT OS - AUTONOMOUS SESSION & DAILY PLAN ({plan['date']})")
    lines.append("=" * 72)
    lines.append(f"Project Workspace : {plan['project_dir']}")
    lines.append(
        f"Git State         : Branch '{plan['git']['branch']}' @ [{plan['git']['sha']}] "
        f"| Dirty Files: {len(plan['git']['dirty_files'])}"
    )
    lines.append(f"Detected Stack    : {', '.join(plan['stack']['stacks'])}")
    lines.append(
        f"Trackers Read     : {', '.join(plan['tracker_files']) if plan['tracker_files'] else 'None (derived from Git state)'}"
    )
    lines.append("-" * 72)

    lines.append("\n[1] PRIMARY FOCUS FOR THIS SESSION (One Primary Focus Rule)")
    lines.append(f"  * Objective : {plan['primary_focus']['task']}")
    lines.append(f"  * Source    : {plan['primary_focus']['source']}")

    if plan.get("phase_loadout"):
        lines.append("\n[2] 4-PHASE CONFLICT-FREE LOADOUT (THINK -> PLAN -> BUILD -> VERIFY)")
        for phase_key, pdata in plan["phase_loadout"].items():
            lines.append(
                f"  * {phase_key:<9}: Skills={', '.join(pdata.get('skills', []))} "
                f"| CLI={', '.join(pdata.get('cli_tools', []))} "
                f"| MCPs={', '.join(pdata.get('mcps', []))}"
            )

    lines.append("\n[3] ORDERED EXECUTION TRAJECTORY")
    for step in plan["execution_steps"]:
        lines.append(f"  {step}")

    lines.append("\n[4] NON-NEGOTIABLE ARCHITECTURAL & GUARDRAIL STANDARDS")
    for rule in plan["non_negotiable_rules"]:
        lines.append(f"  - {rule}")
    lines.append(f"  - Active Guards: {', '.join(plan['stack']['guards'])}")

    lines.append("\n[5] LOCAL QUALITY GATE (Must Pass Before Handoff — No Auto-Commit/Push)")
    for cmd in plan["stack"]["quality_gates"]:
        lines.append(f"  $ {cmd}")

    if plan["up_next"]:
        lines.append("\n[6] UP NEXT (Parked to Prevent Scope Creep)")
        for item in plan["up_next"]:
            lines.append(f"  - [ ] {item}")

    lines.append("\n" + "=" * 72)
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    project_dir = Path.cwd()
    skill_mode: Optional[str] = None
    focus_parts: List[str] = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ["--skill", "--create-skill", "--tool"] and i + 1 < len(args):
            skill_mode = args[i + 1]
            i += 2
        elif arg in ["--path", "--cwd"] and i + 1 < len(args):
            project_dir = Path(args[i + 1]).resolve()
            i += 2
        else:
            focus_parts.append(arg)
            i += 1

    focus_hint = " ".join(focus_parts).strip()
    plan = build_daily_plan(project_dir, focus_hint=focus_hint, skill_mode=skill_mode)
    print(format_daily_plan_report(plan))


if __name__ == "__main__":
    main()
