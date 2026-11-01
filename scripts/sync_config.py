#!/usr/bin/env python3
"""
Agent OS Tri-Target Configuration & Skill Parity Engine.
Maintains deterministic parity across:
1. Workspace root: D:/Skills/.agents
2. Global Antigravity config root: C:/Users/HP/.gemini/config
3. Global OpenCode config root: C:/Users/HP/.config/opencode

Synchronizes:
- All custom Agent OS skills (85), active Antigravity plugin skills (76), and Antigravity built-in skills (9)
  into OpenCode skills/ (<canonical-name>/SKILL.md + companion folders)
- Slash command wrappers in OpenCode commands/ (<canonical-name>.md) while preserving existing speckit.*.md files
- Rules, scripts, hooks.json, and GEMINI.md between Workspace and Antigravity Global Config
"""

import sys
import os
import re
import json
import hashlib
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
GLOBAL_ROOT = Path(os.path.expanduser("~/.gemini/config"))
BUILTIN_SKILLS_ROOT = Path(os.path.expanduser("~/.gemini/antigravity/builtin/skills"))
OPENCODE_ROOT = Path(os.path.expanduser("~/.config/opencode"))

EXCLUDE_PATTERNS = {
    ".git",
    "__pycache__",
    ".gitignore",
    "tests",
    "SKILL_INDEX.json",
    "SKILLS_DIRECTORY.md",
    "node_modules",
    ".venv",
}

PRESERVED_OPENCODE_COMMANDS = {
    "speckit.analyze.md",
    "speckit.checklist.md",
    "speckit.clarify.md",
    "speckit.constitution.md",
    "speckit.converge.md",
    "speckit.implement.md",
    "speckit.init.md",
    "speckit.plan.md",
    "speckit.specify.md",
    "speckit.tasks.md",
    "speckit.taskstoissues.md",
}

RETAINED_SCIENCE_SKILLS = {"credentials", "uv", "workflow_skill_creator"}


def archive_unused_science_skills(global_root: Path = GLOBAL_ROOT) -> int:
    """
    Moves unused biology/chemistry/genomics skills from plugins/science to plugins_archive/science
    (retaining credentials, uv, and workflow_skill_creator) so custom Agent OS skills are never evicted.
    """
    science_dir = global_root / "plugins" / "science"
    if not science_dir.exists():
        return 0

    archive_dir = global_root / "plugins_archive" / "science"
    moved = 0

    science_skills = science_dir / "skills"
    if science_skills.exists():
        archive_skills = archive_dir / "skills"
        archive_skills.mkdir(parents=True, exist_ok=True)
        for item in sorted(science_skills.iterdir()):
            if item.is_dir() and item.name not in RETAINED_SCIENCE_SKILLS:
                dest = archive_skills / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.move(str(item), str(dest))
                moved += 1

    science_rules = science_dir / "rules"
    if science_rules.exists():
        dest_rules = archive_dir / "rules"
        dest_rules.parent.mkdir(parents=True, exist_ok=True)
        if dest_rules.exists():
            shutil.rmtree(dest_rules)
        shutil.move(str(science_rules), str(dest_rules))
        moved += 1

    # Also archive duplicate plugin skills already promoted to custom workspace/global skills
    duplicate_plugin_skills = [
        ("chrome-devtools-plugin", "cookie-debugging"),
        ("firebase", "firebase_security_rules_auditor"),
    ]
    for plugin_name, skill_folder in duplicate_plugin_skills:
        dup_src = global_root / "plugins" / plugin_name / "skills" / skill_folder
        if dup_src.exists():
            dup_dest = global_root / "plugins_archive" / plugin_name / "skills" / skill_folder
            dup_dest.parent.mkdir(parents=True, exist_ok=True)
            if dup_dest.exists():
                shutil.rmtree(dup_dest)
            shutil.move(str(dup_src), str(dup_dest))
            moved += 1

    return moved


def file_hash(path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def parse_skill_frontmatter(skill_md_path: Path) -> Tuple[str, str]:
    """Extracts (canonical_name, one_line_description) from a SKILL.md file."""
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return skill_md_path.parent.name.replace("_", "-"), ""

    fallback_name = skill_md_path.parent.name
    if fallback_name == "skills" and skill_md_path.parent.parent.name:
        fallback_name = skill_md_path.parent.parent.name
    fallback_name = fallback_name.replace("_", "-")

    if not content.startswith("---"):
        return fallback_name, ""

    parts = content.split("---", 2)
    if len(parts) < 3:
        return fallback_name, ""

    yaml_text = parts[1]
    data: Dict[str, str] = {}
    current_key: Optional[str] = None
    current_val_lines: List[str] = []

    for line in yaml_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  ") or line.startswith("\t"):
            if current_key:
                current_val_lines.append(stripped)
            continue
        if ":" in line:
            if current_key:
                data[current_key] = " ".join(current_val_lines).strip("\"' ")
            k, v = line.split(":", 1)
            current_key = k.strip()
            v_clean = v.strip().strip("\"'")
            if v_clean in [">-", ">", "|", "|-"]:
                current_val_lines = []
            else:
                current_val_lines = [v_clean] if v_clean else []

    if current_key and current_val_lines:
        data[current_key] = " ".join(current_val_lines).strip("\"' ")

    raw_name = data.get("name", fallback_name).strip()
    canonical_name = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw_name).replace("_", "-").strip("-") or fallback_name
    desc = re.sub(r"\s+", " ", data.get("description", "")).strip()
    return canonical_name, desc


def discover_all_antigravity_skills(
    workspace_root: Path = WORKSPACE_ROOT,
    global_root: Path = GLOBAL_ROOT,
    builtin_root: Path = BUILTIN_SKILLS_ROOT,
) -> Dict[str, Dict[str, Any]]:
    """
    Discovers all skills across:
    1. Workspace skills (highest priority)
    2. Global Antigravity skills
    3. Active Antigravity Plugin skills
    4. Antigravity Built-in skills
    Returns a dict keyed by canonical hyphenated skill name.
    """
    catalog: Dict[str, Dict[str, Any]] = {}

    sources = [
        ("workspace", workspace_root / "skills"),
        ("global", global_root / "skills"),
        ("plugin", global_root / "plugins"),
        ("builtin", builtin_root),
    ]

    for tier, root_dir in sources:
        if not root_dir.exists():
            continue
        for skill_md in sorted(root_dir.rglob("SKILL.md")):
            # Skip any nested node_modules, .git, or test fixtures
            rel_parts = set(skill_md.relative_to(root_dir).parts)
            if rel_parts & EXCLUDE_PATTERNS:
                continue
            canonical_name, description = parse_skill_frontmatter(skill_md)
            if canonical_name not in catalog:
                catalog[canonical_name] = {
                    "name": canonical_name,
                    "tier": tier,
                    "source_dir": skill_md.parent,
                    "skill_md": skill_md,
                    "description": description or f"Execute the {canonical_name} skill workflow.",
                }

    return catalog


def render_opencode_command_md(skill_name: str, description: str, opencode_root: Path = OPENCODE_ROOT) -> str:
    """Generates an OpenCode slash command markdown wrapper for a skill."""
    short_desc = description[:220] + ("..." if len(description) > 220 else "")
    safe_desc = json.dumps(short_desc, ensure_ascii=False)
    skill_path = (opencode_root / "skills" / skill_name / "SKILL.md").as_posix()
    return (
        f"---\n"
        f"description: {safe_desc}\n"
        f"---\n\n"
        f"## Skill Activation: `/{skill_name}`\n\n"
        f"You **MUST** load and follow the `{skill_name}` skill instructions at:\n"
        f"`{skill_path}`\n\n"
        f"Also enforce the Agent OS CLI & Engineering Constitution (`D:/Skills/.agents/scripts/agent_os.py`) when applicable.\n\n"
        f"## User Input\n\n"
        f"```text\n"
        f"$ARGUMENTS\n"
        f"```\n\n"
        f"Read `{skill_path}` first (or load `{skill_name}` via the `skill` tool) and execute the user's request following all rules and verification gates in that skill.\n"
    )


def scan_sync_drift(
    team_mode: bool = False,
    include_opencode: bool = True,
    workspace_root: Path = WORKSPACE_ROOT,
    global_root: Path = GLOBAL_ROOT,
    opencode_root: Path = OPENCODE_ROOT,
    builtin_root: Path = BUILTIN_SKILLS_ROOT,
) -> List[Dict[str, Any]]:
    """Compares files between workspace, Antigravity global config, and OpenCode global config."""
    drift_items: List[Dict[str, Any]] = []

    # 1. Track items to sync from workspace to Antigravity global config
    sync_dirs = ["skills", "rules", "scripts"]
    sync_files = ["hooks.json"]

    for d in sync_dirs:
        ws_dir = workspace_root / d
        if not ws_dir.exists():
            continue

        for root, dirs, files in os.walk(ws_dir):
            dirs[:] = [sub for sub in dirs if sub not in EXCLUDE_PATTERNS]
            for fname in files:
                if fname.endswith(".pyc") or fname in EXCLUDE_PATTERNS:
                    continue
                ws_file = Path(root) / fname
                rel_path = ws_file.relative_to(workspace_root)
                gl_file = global_root / rel_path

                if not gl_file.exists():
                    drift_items.append({
                        "rel_path": str(rel_path),
                        "status": "MISSING_IN_GLOBAL",
                        "source": ws_file,
                        "target": gl_file,
                    })
                elif file_hash(ws_file) != file_hash(gl_file):
                    drift_items.append({
                        "rel_path": str(rel_path),
                        "status": "MODIFIED_IN_WORKSPACE",
                        "source": ws_file,
                        "target": gl_file,
                    })

    for f_rel in sync_files:
        ws_f = workspace_root / f_rel
        gl_f = global_root / f_rel
        if ws_f.exists():
            if not gl_f.exists():
                drift_items.append({
                    "rel_path": f_rel,
                    "status": "MISSING_IN_GLOBAL",
                    "source": ws_f,
                    "target": gl_f,
                })
            elif file_hash(ws_f) != file_hash(gl_f):
                drift_items.append({
                    "rel_path": f_rel,
                    "status": "MODIFIED_IN_WORKSPACE",
                    "source": ws_f,
                    "target": gl_f,
                })

    # Sync GEMINI.team.md (when --team is passed) or GEMINI.md (default) to ~/.gemini/GEMINI.md
    gemini_src_name = "GEMINI.team.md" if team_mode and (workspace_root / "GEMINI.team.md").exists() else "GEMINI.md"
    ws_gemini = workspace_root / gemini_src_name
    gl_gemini = global_root.parent / "GEMINI.md"
    if ws_gemini.exists():
        if not gl_gemini.exists():
            drift_items.append({
                "rel_path": f"{gemini_src_name} (~/.gemini/GEMINI.md)",
                "status": "MISSING_IN_GLOBAL",
                "source": ws_gemini,
                "target": gl_gemini,
            })
        elif file_hash(ws_gemini) != file_hash(gl_gemini):
            drift_items.append({
                "rel_path": f"{gemini_src_name} (~/.gemini/GEMINI.md)",
                "status": "MODIFIED_IN_WORKSPACE",
                "source": ws_gemini,
                "target": gl_gemini,
            })

    # 2. Sync all discovered skills, slash commands, and rules into OpenCode config
    if include_opencode and opencode_root.exists():
        catalog = discover_all_antigravity_skills(
            workspace_root=workspace_root,
            global_root=global_root,
            builtin_root=builtin_root,
        )

        for skill_name, info in sorted(catalog.items()):
            src_dir: Path = info["source_dir"]
            oc_skill_dir = opencode_root / "skills" / skill_name

            for root, dirs, files in os.walk(src_dir):
                dirs[:] = [sub for sub in dirs if sub not in EXCLUDE_PATTERNS]
                for fname in files:
                    if fname.endswith(".pyc") or fname in EXCLUDE_PATTERNS:
                        continue
                    src_file = Path(root) / fname
                    rel_inside = src_file.relative_to(src_dir)
                    oc_target = oc_skill_dir / rel_inside

                    if not oc_target.exists():
                        drift_items.append({
                            "rel_path": f"opencode/skills/{skill_name}/{rel_inside}",
                            "status": "MISSING_IN_OPENCODE",
                            "source": src_file,
                            "target": oc_target,
                        })
                    elif file_hash(src_file) != file_hash(oc_target):
                        drift_items.append({
                            "rel_path": f"opencode/skills/{skill_name}/{rel_inside}",
                            "status": "MODIFIED_FOR_OPENCODE",
                            "source": src_file,
                            "target": oc_target,
                        })

            # Slash command wrapper in opencode/commands/<skill_name>.md
            cmd_filename = f"{skill_name}.md"
            if cmd_filename not in PRESERVED_OPENCODE_COMMANDS:
                oc_cmd_file = opencode_root / "commands" / cmd_filename
                expected_content = render_opencode_command_md(
                    skill_name, info["description"], opencode_root=opencode_root
                )
                if not oc_cmd_file.exists():
                    drift_items.append({
                        "rel_path": f"opencode/commands/{cmd_filename}",
                        "status": "MISSING_IN_OPENCODE",
                        "content": expected_content,
                        "target": oc_cmd_file,
                    })
                else:
                    current_content = oc_cmd_file.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")
                    if current_content != expected_content.replace("\r\n", "\n"):
                        drift_items.append({
                            "rel_path": f"opencode/commands/{cmd_filename}",
                            "status": "MODIFIED_FOR_OPENCODE",
                            "content": expected_content,
                            "target": oc_cmd_file,
                        })

        # Sync workspace rules/*.md into opencode/rules/*.md
        ws_rules = workspace_root / "rules"
        if ws_rules.exists():
            for rule_file in sorted(ws_rules.glob("*.md")):
                oc_rule = opencode_root / "rules" / rule_file.name
                if not oc_rule.exists():
                    drift_items.append({
                        "rel_path": f"opencode/rules/{rule_file.name}",
                        "status": "MISSING_IN_OPENCODE",
                        "source": rule_file,
                        "target": oc_rule,
                    })
                elif file_hash(rule_file) != file_hash(oc_rule):
                    drift_items.append({
                        "rel_path": f"opencode/rules/{rule_file.name}",
                        "status": "MODIFIED_FOR_OPENCODE",
                        "source": rule_file,
                        "target": oc_rule,
                    })

    return drift_items


def apply_sync(drift_items: List[Dict[str, Any]]) -> int:
    """Copies or writes drifting files to Antigravity and OpenCode global configs."""
    applied = 0
    for item in drift_items:
        target: Path = item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if "content" in item:
            target.write_text(item["content"].replace("\r\n", "\n"), encoding="utf-8", newline="\n")
        else:
            shutil.copy2(item["source"], target)
        applied += 1
    return applied


def main() -> int:
    apply_mode = "--apply" in sys.argv
    team_mode = "--team" in sys.argv
    no_opencode = "--no-opencode" in sys.argv
    drift = scan_sync_drift(team_mode=team_mode, include_opencode=not no_opencode)

    print("=" * 65)
    print("      ANTIGRAVITY + OPENCODE AGENT OS - PARITY SYNC       ")
    print("=" * 65)
    print(f"Workspace Root: {WORKSPACE_ROOT}")
    print(f"Global Root:    {GLOBAL_ROOT}")
    print(f"OpenCode Root:  {OPENCODE_ROOT}")
    print("-" * 65)

    if not drift:
        print("[PASS] Parity verified: Antigravity & OpenCode configs are 100% in sync.")
        print("=" * 65)
        return 0

    print(f"Detected {len(drift)} file drift item(s):")
    for item in drift[:40]:
        tag = "[NEW]" if "MISSING" in item["status"] else "[MOD]"
        print(f"  {tag} {item['rel_path']}")
    if len(drift) > 40:
        print(f"  ... and {len(drift) - 40} more item(s)")

    print("-" * 65)
    if apply_mode:
        archived_science = archive_unused_science_skills(GLOBAL_ROOT)
        if archived_science:
            print(f"[BUDGET] Archived {archived_science} unused science biology items to prevent <skills> eviction.")
        count = apply_sync(drift)
        print(f"[SUCCESS] Applied synchronization: {count} file(s) synced across Antigravity & OpenCode.")
    else:
        print("[NOTICE] Running in dry-run mode. Run with '--apply' to sync changes.")
    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(main())
