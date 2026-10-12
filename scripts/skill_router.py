#!/usr/bin/env python3
"""
scripts/skill_router.py
Deterministic Task-to-Skill & Tool Routing Engine for Agent OS.

Guarantees that every task is paired with:
1. Accurate task sizing (Level 1 to Level 4)
2. Active implementation skills
3. Required in-flight tools and MCP servers
4. Resilient fallbacks if an external MCP is unavailable
5. Mandatory verification guards
6. Clear delegation vs direct execution guidance
"""

import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Domain definitions mapping intent keywords and file patterns to skills/tools
DOMAIN_PROFILES = {
    "WEB_PRECODE": {
        "description": "Pre-Coding Specification & Architecture Blueprint (6 Pillars)",
        "file_patterns": [r"0[1-6]-.*\.md$", r"docs[\\/]precode[\\/]", r"specs[\\/].*?[\\/]precode[\\/]"],
        "keywords": ["precode", "prd", "trd", "app flow", "user flow", "design brief", "backend schema", "implementation plan", "spec", "blueprint", "specification"],
        "implementation_skills": ["web-precode", "spec-kit", "muaz-skill", "database"],
        "in_flight_tools": ["agent_os precode init", "agent_os precode audit", "repl_sandbox sql", "sequential-thinking (sequentialthinking)", "github MCP (search_issues, list_commits)"],
        "completion_guards": ["agent_os precode audit", "clean-code-guard"],
        "fallbacks": {
            "github MCP": "local git log & file review",
            "sequential-thinking": "structured internal hypothesis tree in thought"
        }
    },
    "FRONTEND_UI": {
        "description": "User Interface, Frontend Components, Design & Layout",
        "file_patterns": [r"\.tsx$", r"\.jsx$", r"\.vue$", r"\.svelte$", r"\.css$", r"\.scss$", r"components[\\/]", r"app[\\/].*?page\."],
        "keywords": ["ui", "component", "button", "layout", "design", "css", "tailwind", "modal", "page", "frontend", "bilingual", "rtl", "navbar", "form", "screen", "ui audit", "audit ui"],
        "implementation_skills": ["muaz-skill", "nextjs-fullstack", "ui-audit"],
        "in_flight_tools": ["StitchMCP (generate_screen_from_text, create_design_system, generate_variants)", "chrome-devtools-mcp (evaluate_script, get_css_styles, take_screenshot, list_console_messages)", "code_graph outline", "repl_sandbox regex", "playwright browser_navigate"],
        "completion_guards": ["rtl-logical-guard", "chrome-devtools-mcp (lighthouse_audit)", "clean-code-guard", "list_console_messages", "chaos-audit"],
        "fallbacks": {
            "StitchMCP": "muaz-skill design tokens and Tailwind primitives",
            "chrome-devtools-mcp": "playwright (browser_navigate, browser_snapshot) or agent_os probe",
            "playwright": "agent_os probe <url> + manual DOM inspection"
        }
    },
    "PAYMENTS_BILLING": {
        "description": "Stripe Payments, Invoices, Subscriptions & Webhooks",
        "file_patterns": [r"stripe", r"billing", r"checkout", r"webhook", r"subscription", r"invoice"],
        "keywords": ["stripe", "payment", "billing", "checkout", "subscription", "invoice", "webhook", "refund", "card"],
        "implementation_skills": ["backend-api", "database"],
        "in_flight_tools": ["stripe MCP (stripe_api_search, stripe_api_read, search_stripe_documentation, stripe_implementation_planner)", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["Danger Zone 1 (zero float math, mandatory idempotency keys)", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "stripe MCP": "Official Stripe docs via web search; enforce Danger Zone 1 integer rules",
            "context7": "read_url_content / search_web for Stripe API docs"
        }
    },
    "DEVOPS_DEPLOYMENT": {
        "description": "Netlify Hosting, CI/CD, Releases & GitHub PR Workflows",
        "file_patterns": [r"netlify\.toml$", r"deploy", r"\.github[\\/]workflows[\\/]"],
        "keywords": ["deploy", "netlify", "preview", "ci", "cd", "pipeline", "release", "hosting", "build", "production", "pr", "pull request"],
        "implementation_skills": ["devops-deploy"],
        "in_flight_tools": ["netlify MCP (netlify-deploy-services-reader, netlify-project-services-reader)", "github MCP (create_pull_request, push_files, list_pull_requests)"],
        "completion_guards": ["netlify preview verification", "diff_reviewer", "clean-code-guard"],
        "fallbacks": {
            "netlify MCP": "git push + GitHub Actions CI/CD deployment logs",
            "github MCP": "local git CLI (git status, git log, git diff)"
        }
    },
    "NEXTJS_SERVER_ACTIONS": {
        "description": "Next.js Server Actions & App Router Endpoints",
        "file_patterns": [r"actions\.(?:ts|js)$", r"actions[\\/]", r"route\.(?:ts|js)$"],
        "keywords": ["server action", "use server", "safeparse", "idor", "auth derivation", "action"],
        "implementation_skills": ["next-server-action-guard", "backend-api"],
        "in_flight_tools": ["code_graph find", "repl_sandbox py", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["next-server-action-guard", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "context7": "search_web for Next.js 15 Server Action docs"
        }
    },
    "BACKEND_LARAVEL_PHP": {
        "description": "Laravel 11+ & PHP 8 Modern Backend Services",
        "file_patterns": [r"\.php$", r"\.phtml$", r"app[\\/]Http[\\/]", r"routes[\\/]"],
        "keywords": ["laravel", "php", "artisan", "pest", "eloquent", "blade", "controller"],
        "implementation_skills": ["laravel-mastery", "backend-http"],
        "in_flight_tools": ["code_graph outline", "repl_sandbox sql", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["pest-security-guard", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "context7": "search_web for Laravel 11 / Pest 3 documentation"
        }
    },
    "DATABASE_PERSISTENCE": {
        "description": "Database Schemas, Migrations, Indexes & Queries",
        "file_patterns": [r"\.sql$", r"migrations[\\/]", r"schema\.prisma$", r"models[\\/]"],
        "keywords": ["database", "sql", "migration", "prisma", "table", "index", "schema", "foreign key", "acid"],
        "implementation_skills": ["database", "backend-data"],
        "in_flight_tools": ["repl_sandbox sql (in-memory SQLite sandbox)"],
        "completion_guards": ["antipattern AP-001 (raw SQL injection)", "sentinel (unbounded query & index check)", "clean-code-guard"],
        "fallbacks": {
            "repl_sandbox": "manual schema review against existing migrations"
        }
    },
    "PYTHON_SYSTEMS": {
        "description": "Python Utilities, Agent OS Scripts & Automation",
        "file_patterns": [r"\.py$"],
        "keywords": ["python", "script", "agent", "daemon", "cli", "regex", "repl"],
        "implementation_skills": ["clean-code-guard", "engineering-workflow"],
        "in_flight_tools": ["repl_sandbox eval", "code_graph symbol"],
        "completion_guards": ["python-security-guard", "sentinel", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "code_graph": "view_file / grep search"
        }
    },
    "CROSS_SESSION_CONTINUITY": {
        "description": "Cross-Session Working Memory & Decision Tracking",
        "file_patterns": [r"PROGRESS\.md$", r"DECISIONS\.md$", r"SESSION_SNAPSHOT\.md$"],
        "keywords": ["continuity", "resume", "checkpoint", "memory", "graph", "session", "recall", "past decision"],
        "implementation_skills": ["engineering-workflow"],
        "in_flight_tools": ["memory MCP (search_nodes, open_nodes, create_entities, add_observations)", "agent_os snapshot resume", "agent_os snapshot freeze"],
        "completion_guards": ["agent_os snapshot freeze", "clean-code-guard"],
        "fallbacks": {
            "memory MCP": "SESSION_SNAPSHOT.md + PROGRESS.md + DECISIONS.md in project root"
        }
    },
    "WEBMCP": {
        "description": "In-Browser WebMCP (document.modelContext) Tools & Declarative Forms",
        "file_patterns": [r"webmcp", r"modelContext", r"registerTool"],
        "keywords": ["webmcp", "modelcontext", "registertool", "gettools", "executetool", "toolchange", "toolautosubmit", "in-browser tool", "browser tool"],
        "implementation_skills": ["webmcp", "muaz-skill", "clean-code-guard"],
        "in_flight_tools": ["chrome-devtools-mcp (evaluate_script, list_console_messages)", "playwright (browser_navigate, browser_evaluate)", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["clean-code-guard", "test-guard", "chaos-audit"],
        "fallbacks": {
            "chrome-devtools-mcp": "playwright or local mock harness (MockModelContext)",
            "context7": "skills/webmcp/references/spec-idl.md and official W3C webmachinelearning/webmcp repository"
        }
    }
}

def determine_task_level(input_target: str) -> Dict[str, str]:
    """Classifies task sizing into Levels 1-4 with ceremony guidelines."""
    lower = input_target.lower()
    
    # Level 1: Trivial edits
    if any(k in lower for k in ["typo", "fix typo", "rename", "single line", "quick fix", "comment", "docstring", "lint"]):
        return {
            "level": "Level 1: Trivial Edit",
            "ceremony": "Zero ceremony. Inspect -> Surgical edit -> Run test/lint -> Done."
        }
    
    # Level 4: Greenfield or cross-cutting overhaul
    if any(k in lower for k in ["architectural overhaul", "greenfield", "precode", "prd", "trd", "6 pillars", "spec-kit", "complete overhaul"]):
        return {
            "level": "Level 4: Architectural Overhaul / Cross-Cutting",
            "ceremony": "Formal Pre-Coding Pillars (01-PRD to 06-PLAN) or Spec Kit workflow. Gated approval required."
        }
        
    # Level 2: Focused defect/bug fix
    if any(k in lower for k in ["bug", "defect", "fix", "error", "failing", "crash", "regression", "broken"]):
        return {
            "level": "Level 2: Focused Bug Fix",
            "ceremony": "Reproduce -> Diagnose root cause -> Targeted fix -> Regression test -> Done."
        }
        
    # Level 3: Standard feature or refactor
    return {
        "level": "Level 3: Moderate Feature / Refactor",
        "ceremony": "Context reconstruction -> Bounded plan -> Direct execution lock -> Verify with tests & guards."
    }

def determine_delegation(input_target: str) -> str:
    """Recommends whether to delegate to a subagent or execute directly."""
    lower = input_target.lower()
    if "firestore.rules" in lower or "firestore rules" in lower:
        return "DELEGATE: Mandatory specialist subagent 'firestore-rules-author'."
    if "flutter" in lower and ("a11y" in lower or "accessibility" in lower):
        return "DELEGATE: Specialized subagent 'flutter_a11y_agent'."
    if any(k in lower for k in ["wide survey", "explore entire repo", "survey all directories"]):
        return "DELEGATE: Subagent 'research' (read-only context preservation)."
    return "DIRECT EXECUTION LOCK: Primary agent executes directly (No subagent delegation needed)."

def resolve_task_routing(input_target: str) -> Dict[str, Any]:
    matched_domains: List[str] = []
    lower_input = input_target.lower()

    for domain_key, profile in DOMAIN_PROFILES.items():
        # Check file pattern match
        pattern_match = any(re.search(pat, input_target, re.IGNORECASE) for pat in profile["file_patterns"])
        # Check keyword match
        keyword_match = any(re.search(r"\b" + re.escape(kw) + r"\b", lower_input) for kw in profile["keywords"])

        if pattern_match or keyword_match:
            matched_domains.append(domain_key)

    if not matched_domains:
        # Default to general engineering workflow
        matched_domains = ["PYTHON_SYSTEMS"] if input_target.endswith(".py") else ["FRONTEND_UI" if any(input_target.endswith(ext) for ext in [".tsx", ".css", ".jsx"]) else "GENERAL_ENGINEERING"]

    impl_skills = set()
    tools = set()
    guards = set()
    fallbacks = {}

    for d in matched_domains:
        prof = DOMAIN_PROFILES.get(d)
        if prof:
            impl_skills.update(prof["implementation_skills"])
            tools.update(prof["in_flight_tools"])
            guards.update(prof["completion_guards"])
            if "fallbacks" in prof:
                fallbacks.update(prof["fallbacks"])

    if not guards:
        guards = {"clean-code-guard", "chaos-audit"}

    task_sizing = determine_task_level(input_target)
    delegation_advice = determine_delegation(input_target)

    return {
        "input": input_target,
        "task_level": task_sizing["level"],
        "ceremony": task_sizing["ceremony"],
        "delegation": delegation_advice,
        "domains": matched_domains,
        "implementation_skills": sorted(list(impl_skills)),
        "in_flight_tools": sorted(list(tools)),
        "completion_guards": sorted(list(guards)),
        "fallbacks": fallbacks
    }

def print_routing_manifest(result: Dict[str, Any]):
    print("=" * 65)
    print("      ANTIGRAVITY AGENT OS - TASK & TOOL ROUTING MANIFEST      ")
    print("=" * 65)
    print(f"Target Input:        {result['input']}")
    print(f"Task Sizing:         {result['task_level']}")
    print(f"Ceremony Protocol:   {result['ceremony']}")
    print(f"Delegation Guidance: {result['delegation']}")
    print(f"Matched Domain(s):   {', '.join(result['domains'])}")
    print("-" * 65)
    print("[1. WHILE IMPLEMENTING - ACTIVE SKILLS TO CONSULT]:")
    for s in result["implementation_skills"]:
        print(f"  * {s}")
    print("\n[2. WHILE IMPLEMENTING - IN-FLIGHT TOOLS]:")
    for t in result["in_flight_tools"]:
        print(f"  * {t}")
    if result["fallbacks"]:
        print("\n[3. IF TOOLS UNAVAILABLE - RESILIENT FALLBACKS]:")
        for tool, fallback in result["fallbacks"].items():
            print(f"  * {tool:<20} -> {fallback}")
    print("\n[4. WHEN FINISHED - MANDATORY COMPLETION GUARDS]:")
    for g in result["completion_guards"]:
        print(f"  * {g}")
    print("=" * 65)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/skill_router.py <task description or file path>")
        sys.exit(1)

    input_target = " ".join(sys.argv[1:])
    result = resolve_task_routing(input_target)
    print_routing_manifest(result)
    sys.exit(0)

if __name__ == "__main__":
    main()
