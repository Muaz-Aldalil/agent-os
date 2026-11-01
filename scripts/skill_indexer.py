#!/usr/bin/env python3
"""
Agent OS Skill Indexer & Full-Ecosystem Discovery Engine.
Parses, indexes, and categorizes all custom Agent OS skills, active Web/AI plugin skills,
and registered MCP servers to enable:
1. Instant semantic & keyword search (< 20 tokens) instead of reading full SKILL.md files
2. Role classification (master-command, domain-skill, sub-module, phase-skill, guard)
3. 4-Phase Engineering Lifecycle mapping (THINK -> PLAN -> BUILD -> VERIFY)
4. Auto-generated SKILL_INDEX.json & SKILLS_DIRECTORY.md for deterministic routing
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = WORKSPACE_ROOT / "skills"
GLOBAL_CONFIG_ROOT = Path(os.path.expanduser("~/.gemini/config"))

CATEGORIES = {
    "Quality & Security Guards": [
        "next-server-action-guard",
        "pest-security-guard",
        "rtl-logical-guard",
        "clean-code-guard",
        "test-guard",
        "docs-guard",
        "woo-guard",
        "wp-guard",
        "bug-hunter",
        "cookie-debugging",
        "firebase-security-rules-auditor",
        "pentest",
        "reverse-engineer-anything",
        "security-audit",
    ],
    "Core Architecture & Workflow": [
        "engineering-workflow",
        "agentic-workflows",
        "intake",
        "critique",
        "plan-daily",
        "debate-review",
        "ui-review-loop",
        "delegate-setup",
        "opencode-delegate",
        "find-skills",
        "project-documentation",
        "data-saver",
    ],
    "Backend & Data Systems": [
        "laravel-mastery",
        "backend-api",
        "backend-data",
        "backend-http",
        "backend-identity",
        "backend-ops",
        "database",
        "devops-deploy",
    ],
    "Frontend & User Experience": [
        "nextjs-fullstack",
        "muaz-skill",
        "ui-audit",
        "webmcp",
    ],
    "Testing & QA Automation": [
        "testing-qa",
    ],
    "Specification-Driven Development (Spec-Kit)": [
        "web-precode",
        "spec-kit",
        "speckit-constitution",
        "speckit-specify",
        "speckit-clarify",
        "speckit-plan",
        "speckit-tasks",
        "speckit-checklist",
        "speckit-analyze",
        "speckit-implement",
        "speckit-converge",
        "speckit-taskstoissues",
    ],
    "Simplicity & Anti-Bloat (Ponytail)": [
        "ponytail",
        "ponytail-audit",
        "ponytail-debt",
        "ponytail-gain",
        "ponytail-help",
        "ponytail-review",
        "caveman",
    ],
    "Beginner Situation Combos (All-in-One)": [
        "start-project",
        "smart-feature",
        "feature-fe",
        "feature-febe",
        "feature-full",
        "feature-wp",
        "fix-ui",
        "fix-backend",
        "check-all",
        "doc-project",
        "save-data",
    ],
    "Google Stitch Design & UI Suite": [
        "generate-design",
        "design-md",
        "taste-design",
        "manage-design-system",
        "extract-design-md",
        "extract-static-html",
        "code-to-design",
        "upload-to-stitch",
        "enhance-prompt",
        "site-md",
        "stitch-loop",
        "react-components",
        "react-native",
        "react-vite-dashboard",
        "remotion",
        "shadcn-ui",
    ],
}

ROLE_MAP = {
    "master-command": {
        "start-project",
        "smart-feature",
        "feature-fe",
        "feature-febe",
        "feature-full",
        "feature-wp",
        "fix-ui",
        "fix-backend",
        "check-all",
        "doc-project",
        "save-data",
        "plan-daily",
        "spec-kit",
    },
    "phase-skill": {
        "intake",
        "web-precode",
        "speckit-constitution",
        "speckit-specify",
        "speckit-clarify",
        "speckit-plan",
        "speckit-tasks",
        "speckit-checklist",
        "speckit-analyze",
        "speckit-implement",
        "speckit-converge",
        "speckit-taskstoissues",
    },
    "sub-module": {
        "backend-data",
        "backend-http",
        "backend-identity",
        "backend-ops",
        "delegate-setup",
        "project-documentation",
        "ponytail-audit",
        "ponytail-debt",
        "ponytail-gain",
        "ponytail-help",
        "ponytail-review",
        "enhance-prompt",
        "extract-static-html",
        "upload-to-stitch",
    },
    "guard": {
        "critique",
        "clean-code-guard",
        "rtl-logical-guard",
        "next-server-action-guard",
        "pest-security-guard",
        "test-guard",
        "docs-guard",
        "wp-guard",
        "woo-guard",
        "ui-audit",
        "ui-review-loop",
        "debate-review",
    },
}

PHASE_MAP = {
    "THINK": {
        "engineering-workflow",
        "agentic-workflows",
        "intake",
        "plan-daily",
        "find-skills",
        "data-saver",
        "save-data",
        "caveman",
        "ponytail-help",
        "ponytail-gain",
    },
    "PLAN": {
        "start-project",
        "web-precode",
        "spec-kit",
        "speckit-constitution",
        "speckit-specify",
        "speckit-clarify",
        "speckit-plan",
        "speckit-tasks",
        "speckit-checklist",
        "speckit-taskstoissues",
        "delegate-setup",
        "design-md",
        "site-md",
        "taste-design",
        "enhance-prompt",
        "extract-design-md",
        "manage-design-system",
    },
    "BUILD": {
        "smart-feature",
        "feature-fe",
        "feature-febe",
        "feature-full",
        "feature-wp",
        "fix-ui",
        "fix-backend",
        "muaz-skill",
        "nextjs-fullstack",
        "laravel-mastery",
        "backend-api",
        "backend-data",
        "backend-http",
        "backend-identity",
        "backend-ops",
        "database",
        "devops-deploy",
        "webmcp",
        "opencode-delegate",
        "speckit-implement",
        "doc-project",
        "project-documentation",
        "testing-qa",
        "ponytail",
        "generate-design",
        "stitch-loop",
        "code-to-design",
        "upload-to-stitch",
        "extract-static-html",
        "react-components",
        "react-native",
        "react-vite-dashboard",
        "remotion",
        "shadcn-ui",
    },
    "VERIFY": {
        "check-all",
        "clean-code-guard",
        "rtl-logical-guard",
        "next-server-action-guard",
        "pest-security-guard",
        "test-guard",
        "docs-guard",
        "wp-guard",
        "woo-guard",
        "ui-audit",
        "ui-review-loop",
        "debate-review",
        "ponytail-review",
        "ponytail-audit",
        "ponytail-debt",
        "speckit-analyze",
        "speckit-converge",
    },
}


def infer_role_and_phase(name: str, description: str, category: str) -> Tuple[str, str]:
    """Determines (role, phase) for known skills and auto-infers for newly added skills."""
    role = "domain-skill"
    for r_key, members in ROLE_MAP.items():
        if name in members:
            role = r_key
            break
    else:
        desc_lower = f"{name} {description}".lower()
        if name.endswith("-guard") or "guard" in desc_lower or "audit" in desc_lower:
            role = "guard"
        elif "all-in-one" in desc_lower or category == "Beginner Situation Combos (All-in-One)":
            role = "master-command"

    phase = "BUILD"
    for p_key, members in PHASE_MAP.items():
        if name in members:
            phase = p_key
            break
    else:
        desc_lower = f"{name} {description}".lower()
        if role == "guard" or any(k in desc_lower for k in ["review", "audit", "verify", "security"]):
            phase = "VERIFY"
        elif any(k in desc_lower for k in ["plan", "spec", "precode", "architecture", "prd", "blueprint"]):
            phase = "PLAN"
        elif any(k in desc_lower for k in ["discover", "triage", "workflow", "search", "bandwidth"]):
            phase = "THINK"

    return role, phase


def parse_frontmatter(content: str):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    yaml_text = parts[1]
    body = parts[2]
    data = {}
    current_key = None
    current_val_lines = []

    for line in yaml_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # If indented, it's a continuation of current_key
        if line.startswith("  ") or line.startswith("\t"):
            if current_key:
                current_val_lines.append(stripped)
            continue

        # If new key-value pair
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

    return data, body


def discover_active_plugin_skills(plugins_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Scans active (non-disabled) plugin directories for Web/AI SKILL.md files."""
    target_dir = plugins_dir or (GLOBAL_CONFIG_ROOT / "plugins")
    plugin_skills: List[Dict[str, Any]] = []
    if not target_dir.exists():
        return plugin_skills

    for skill_file in sorted(target_dir.rglob("SKILL.md")):
        try:
            rel_parts = skill_file.relative_to(target_dir).parts
            plugin_name = rel_parts[0] if rel_parts else "plugin"
            content = skill_file.read_text(encoding="utf-8", errors="ignore")
            fm, _ = parse_frontmatter(content)
            skill_name = fm.get("name") or skill_file.parent.name
            if skill_name == "skills" and len(rel_parts) >= 2:
                skill_name = plugin_name.replace("_", "-")
            description = fm.get("description", "")
            _, phase = infer_role_and_phase(skill_name, description, plugin_name)
            plugin_skills.append({
                "name": skill_name,
                "plugin": plugin_name,
                "phase": phase,
                "description": description,
                "search_corpus": f"{skill_name} {plugin_name} {description}".lower(),
            })
        except OSError:
            continue

    plugin_skills.sort(key=lambda s: s["name"])
    return plugin_skills


def discover_mcp_servers(mcp_config_path: Optional[Path] = None) -> List[Dict[str, str]]:
    """Discovers registered MCP servers from mcp_config.json and built-in Antigravity MCPs."""
    builtin_mcps = {
        "StitchMCP": {
            "phase": "PLAN",
            "domain": "Visual UI Generation & Design Systems (Mockups/Variants)",
        },
        "chrome-devtools-mcp": {
            "phase": "VERIFY",
            "domain": "Live Browser DOM, CSS, Console, LCP & Accessibility Debugging",
        },
        "playwright": {
            "phase": "VERIFY",
            "domain": "Automated Multi-Viewport E2E User Flows & UI Review Loop",
        },
        "gemini-api-docs": {
            "phase": "BUILD",
            "domain": "Official Google Gemini SDK & API Documentation Lookup",
        },
        "context7": {
            "phase": "BUILD",
            "domain": "Up-to-Date Framework & Library Documentation (Next.js, Laravel, React, Tailwind)",
        },
        "sequential-thinking": {
            "phase": "THINK",
            "domain": "Structured Multi-Step Architectural Tradeoff & Root-Cause Analysis",
        },
        "memory": {
            "phase": "THINK",
            "domain": "Persistent Knowledge Graph for Cross-Session Entities & Decisions",
        },
        "stripe": {
            "phase": "BUILD",
            "domain": "Stripe Billing, Checkout, Subscriptions & Webhook Integration",
        },
        "github": {
            "phase": "PLAN",
            "domain": "GitHub Repositories, Pull Requests, Issues & Code Search",
        },
        "netlify": {
            "phase": "VERIFY",
            "domain": "Netlify Previews, Deploys & Hosting Management",
        },
        "docker": {
            "phase": "BUILD",
            "domain": "Container Runtime & Service Orchestration",
        },
        "jira": {
            "phase": "PLAN",
            "domain": "Jira Issue Tracking, Sprints & Project Workflows",
        },
    }

    cfg_path = mcp_config_path or (GLOBAL_CONFIG_ROOT / "mcp_config.json")
    if cfg_path.exists():
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
            for srv_name in raw.get("mcpServers", {}).keys():
                if srv_name not in builtin_mcps:
                    builtin_mcps[srv_name] = {
                        "phase": "BUILD",
                        "domain": f"Custom Configured MCP Server ({srv_name})",
                    }
        except (OSError, ValueError) as exc:
            _ = exc  # Preserve builtin_mcps defaults when mcp_config.json is unreadable

    servers = [
        {"name": k, "phase": v["phase"], "domain": v["domain"]}
        for k, v in sorted(builtin_mcps.items())
    ]
    return servers


def build_index() -> Dict[str, Any]:
    skills = []

    for skill_path in sorted(SKILLS_DIR.iterdir()):
        if not skill_path.is_dir():
            continue
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        fm, _ = parse_frontmatter(content)
        name = fm.get("name", skill_path.name)
        description = fm.get("description", "")

        # Determine category
        cat = "General Customizations"
        for category_name, member_skills in CATEGORIES.items():
            if name in member_skills or skill_path.name in member_skills:
                cat = category_name
                break

        role, phase = infer_role_and_phase(name, description, cat)

        # Token extraction for search
        search_corpus = f"{name} {description} {cat} {role} {phase}".lower()

        skills.append({
            "name": name,
            "category": cat,
            "role": role,
            "phase": phase,
            "description": description,
            "file": f"skills/{skill_path.name}/SKILL.md",
            "search_corpus": search_corpus,
        })

    # Sort skills alphabetically by name for deterministic prompt caching
    skills.sort(key=lambda s: s["name"])
    plugin_skills = discover_active_plugin_skills()
    mcp_servers = discover_mcp_servers()

    return {
        "skills": skills,
        "total_skills": len(skills),
        "plugin_skills": plugin_skills,
        "total_plugin_skills": len(plugin_skills),
        "mcp_servers": mcp_servers,
        "total_mcp_servers": len(mcp_servers),
    }


def generate_markdown_directory(index_data: Dict[str, Any]) -> str:
    md = ["# Antigravity Agent OS - Skills & Capabilities Directory\n"]
    md.append(
        f"> Auto-indexed registry of **{index_data['total_skills']} custom engineering skills**, "
        f"**{index_data.get('total_plugin_skills', 0)} active Web/AI plugin skills**, and "
        f"**{index_data.get('total_mcp_servers', 0)} MCP servers** organized by domain and lifecycle phase (`THINK -> PLAN -> BUILD -> VERIFY`).\n"
    )

    # Group by category (sorted category names)
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for item in index_data["skills"]:
        c = item["category"]
        by_cat.setdefault(c, []).append(item)

    for cat_name in sorted(by_cat.keys()):
        items = by_cat[cat_name]
        md.append(f"## {cat_name}\n")
        for s in sorted(items, key=lambda x: x["name"]):
            phase_badge = s.get("phase", "BUILD")
            role_badge = s.get("role", "domain-skill")
            md.append(
                f"- **[`{s['name']}`](file:///D:/Skills/.agents/{s['file']})** "
                f"`[{phase_badge} | {role_badge}]`: {s['description']}"
            )
        md.append("")

    if index_data.get("mcp_servers"):
        md.append("## Active MCP Servers (Single-Winner Domain Registry)\n")
        for srv in index_data["mcp_servers"]:
            md.append(f"- **`{srv['name']}`** `[{srv['phase']}]`: {srv['domain']}")
        md.append("")

    return "\n".join(md)


def search_skills(
    query: str,
    index_data: Optional[Dict[str, Any]] = None,
    limit: int = 5,
    include_plugins: bool = False,
) -> List[Dict[str, Any]]:
    if not index_data:
        index_data = build_index()

    raw_terms = re.findall(r"[a-zA-Z0-9]+", query.lower())
    matches = []

    pool = list(index_data["skills"])
    if include_plugins:
        pool.extend(index_data.get("plugin_skills", []))

    for s in pool:
        score = 0
        corpus = s["search_corpus"]
        name = s["name"].lower()

        for t in raw_terms:
            if len(t) < 2:
                continue
            if t == name:
                score += 20
            elif t in name:
                score += 10
            elif t in corpus:
                score += 3

        if score > 0:
            matches.append((score, s))

    matches.sort(key=lambda x: (x[0], x[1]["name"]), reverse=True)
    return [m[1] for m in matches[:limit]]


def main():
    index_data = build_index()

    # 1. Save SKILL_INDEX.json with sorted keys and normalized LF endings
    json_path = WORKSPACE_ROOT / "SKILL_INDEX.json"
    json_text = json.dumps(index_data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    json_path.write_text(json_text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")

    # 2. Save SKILLS_DIRECTORY.md with LF endings
    md_content = generate_markdown_directory(index_data)
    md_path = WORKSPACE_ROOT / "SKILLS_DIRECTORY.md"
    md_path.write_text(md_content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")

    print(
        f"[SUCCESS] Indexed {index_data['total_skills']} custom skills, "
        f"{index_data['total_plugin_skills']} Web/AI plugin skills, and "
        f"{index_data['total_mcp_servers']} MCP servers."
    )
    print(f"  - Machine index: {json_path}")
    print(f"  - Human catalog: {md_path}")

    if len(sys.argv) > 1 and sys.argv[1] != "--build-only":
        q = " ".join(sys.argv[1:])
        results = search_skills(q, index_data, include_plugins=True)
        print(f"\nSearch results for '{q}':")
        for r in results:
            cat_label = r.get("category") or f"plugin:{r.get('plugin', '')}"
            print(f"  * {r['name']} [{r.get('phase', 'BUILD')}] ({cat_label}): {r['description'][:90]}...")


if __name__ == "__main__":
    main()
