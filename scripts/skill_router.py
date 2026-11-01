#!/usr/bin/env python3
"""
scripts/skill_router.py
Dynamic Full-Catalog & 4-Phase Conflict-Free Routing Engine for Agent OS.

Guarantees that every task across all indexed custom skills, active Web/AI plugin skills,
CLI tools, and registered MCP servers (dynamically loaded from SKILL_INDEX.json) is paired with:
1. Accurate task sizing (Level 1 to Level 4)
2. Conflict-free Stack & Tool resolution (Single-Winner Authority per domain)
3. Dynamic live discovery from SKILL_INDEX.json & mcp_config.json (auto-detects new additions)
4. 4-Phase Engineering Loadout (1. THINK -> 2. PLAN -> 3. BUILD -> 4. VERIFY)
5. Active implementation skills, in-flight tools, resilient fallbacks, and completion guards
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SKILL_INDEX_PATH = WORKSPACE_ROOT / "SKILL_INDEX.json"

# Comprehensive domain profiles covering the entire Web, Backend, Data, AI, Cloud & QA Arsenal
DOMAIN_PROFILES: Dict[str, Dict[str, Any]] = {
    "WEB_PRECODE": {
        "description": "Pre-Coding Specification & Architecture Blueprint (6 Pillars)",
        "file_patterns": [r"0[1-6]-.*\.md$", r"docs[\\/]precode[\\/]", r"specs[\\/].*?[\\/]precode[\\/]"],
        "keywords": [
            "precode", "prd", "trd", "app flow", "user flow", "design brief",
            "backend schema", "implementation plan", "spec", "blueprint",
            "specification", "start-project",
        ],
        "think_skills": ["engineering-workflow", "intake", "plan-daily"],
        "plan_skills": ["web-precode", "critique", "spec-kit", "muaz-skill", "design-md", "site-md", "taste-design"],
        "implementation_skills": ["web-precode", "spec-kit", "muaz-skill", "design-md", "site-md", "database"],
        "in_flight_tools": [
            "agent_os precode init",
            "agent_os precode audit",
            "StitchMCP + Google Stitch Skills (design-md, site-md, manage-design-system, generate-design)",
            "repl_sandbox sql",
            "sequential-thinking (sequentialthinking)",
            "github MCP (search_issues, list_commits)",
        ],
        "completion_guards": ["agent_os precode audit", "clean-code-guard"],
        "fallbacks": {
            "github MCP": "local git log & file review",
            "sequential-thinking": "structured internal hypothesis tree in thought",
        },
    },
    "SPEC_KIT_SDD": {
        "description": "Specification-Driven Development (Spec-Kit Lifecycle Phases)",
        "file_patterns": [r"\.specify[\\/]", r"specs[\\/]\d+-", r"tasks\.md$", r"spec\.md$", r"plan\.md$"],
        "keywords": [
            "spec-kit", "speckit", "speckit-specify", "speckit-clarify",
            "speckit-plan", "speckit-tasks", "speckit-checklist",
            "speckit-analyze", "speckit-implement", "speckit-converge",
            "speckit-constitution", "speckit-taskstoissues",
        ],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["spec-kit", "speckit-specify", "speckit-clarify", "speckit-plan", "speckit-tasks"],
        "implementation_skills": ["spec-kit", "speckit-implement", "web-precode"],
        "in_flight_tools": [
            "code_graph outline",
            "sequential-thinking (sequentialthinking)",
            "github MCP (create_issue, search_issues)",
        ],
        "completion_guards": ["speckit-analyze", "speckit-converge", "clean-code-guard"],
        "fallbacks": {
            "github MCP": "local specs/<feature>/tasks.md tracking",
        },
    },
    "FRONTEND_UI": {
        "description": "User Interface, Frontend Components, Google Stitch Design & Bilingual RTL Layout",
        "file_patterns": [
            r"\.tsx$", r"\.jsx$", r"\.vue$", r"\.svelte$",
            r"\.css$", r"\.scss$", r"components[\\/]", r"app[\\/].*?page\.",
            r"DESIGN\.md$", r"SITE\.md$",
        ],
        "keywords": [
            "ui", "component", "button", "layout", "design", "css", "tailwind",
            "modal", "page", "frontend", "bilingual", "rtl", "navbar", "sidebar",
            "form", "table", "screen", "ui audit", "audit ui", "stitch",
            "feature-fe", "fix-ui", "generate-design", "design-md", "taste-design",
            "stitch-loop", "shadcn", "remotion", "react-native",
        ],
        "think_skills": ["engineering-workflow", "intake"],
        "plan_skills": [
            "muaz-skill",
            "critique",
            "design-md",
            "taste-design",
            "enhance-prompt",
            "manage-design-system",
            "extract-design-md",
            "site-md",
        ],
        "implementation_skills": [
            "muaz-skill",
            "generate-design",
            "stitch-loop",
            "react-components",
            "shadcn-ui",
            "react-vite-dashboard",
            "code-to-design",
            "upload-to-stitch",
            "extract-static-html",
            "nextjs-fullstack",
            "ui-audit",
            "modern-web-guidance",
        ],
        "in_flight_tools": [
            "StitchMCP + Google Stitch Skills (generate-design, design-md, taste-design, manage-design-system, stitch-loop, react-components, shadcn-ui)",
            "chrome-devtools-mcp (evaluate_script, get_css_styles, take_screenshot, list_console_messages)",
            "code_graph outline",
            "repl_sandbox regex",
            "playwright browser_navigate",
        ],
        "completion_guards": [
            "rtl-logical-guard",
            "ui-review-loop",
            "chrome-devtools-mcp (lighthouse_audit)",
            "clean-code-guard",
            "list_console_messages",
            "chaos-audit",
        ],
        "fallbacks": {
            "StitchMCP": "muaz-skill + Google Stitch local skills (design-md, taste-design, shadcn-ui, react-components)",
            "chrome-devtools-mcp": "playwright (browser_navigate, browser_snapshot) or agent_os probe",
            "playwright": "agent_os probe <url> + manual DOM inspection",
        },
    },
    "PERFORMANCE_A11Y_DEBUG": {
        "description": "Core Web Vitals (LCP), Accessibility (a11y) & Memory Leak Debugging",
        "file_patterns": [r"lighthouse", r"heapsnapshot"],
        "keywords": [
            "lcp", "largest contentful paint", "core web vitals", "cwv",
            "a11y", "accessibility", "aria", "contrast", "keyboard navigation",
            "memory leak", "heapsnapshot", "oom", "slow page",
        ],
        "think_skills": ["chrome-devtools", "troubleshooting"],
        "plan_skills": ["modern-web-guidance"],
        "implementation_skills": [
            "debug-optimize-lcp",
            "a11y-debugging",
            "memory-leak-debugging",
            "chrome-devtools",
            "fix-ui",
        ],
        "in_flight_tools": [
            "chrome-devtools-mcp (performance_start_trace, performance_stop_trace, lighthouse_audit, take_heapsnapshot)",
            "agent_os ui-audit",
        ],
        "completion_guards": ["chrome-devtools-mcp (lighthouse_audit)", "ui-review-loop", "clean-code-guard"],
        "fallbacks": {
            "chrome-devtools-mcp": "agent_os ui-audit + playwright snapshot inspection",
        },
    },
    "PAYMENTS_BILLING": {
        "description": "Stripe Payments, Invoices, Subscriptions & Webhooks",
        "file_patterns": [r"stripe", r"billing", r"checkout", r"webhook", r"subscription", r"invoice"],
        "keywords": ["stripe", "payment", "billing", "checkout", "subscription", "invoice", "webhook", "refund", "card"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["backend-api", "database"],
        "implementation_skills": ["backend-api", "database"],
        "in_flight_tools": [
            "stripe MCP (stripe_api_search, stripe_api_read, search_stripe_documentation, stripe_implementation_planner)",
            "context7 (resolve-library-id, query-docs)",
        ],
        "completion_guards": ["Danger Zone 1 (zero float math, mandatory idempotency keys)", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "stripe MCP": "Official Stripe docs via web search; enforce Danger Zone 1 integer rules",
            "context7": "read_url_content / search_web for Stripe API docs",
        },
    },
    "DEVOPS_DEPLOYMENT": {
        "description": "Netlify Hosting, Docker Containers, CI/CD & GitHub PR Workflows",
        "file_patterns": [r"netlify\.toml$", r"Dockerfile$", r"docker-compose\.ya?ml$", r"deploy", r"\.github[\\/]workflows[\\/]"],
        "keywords": [
            "deploy", "deployment", "netlify", "preview", "ci", "cd", "pipeline",
            "release", "hosting", "production", "pr", "pull request",
            "docker", "dockerfile", "container", "nginx",
        ],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["devops-deploy"],
        "implementation_skills": ["devops-deploy", "backend-ops"],
        "in_flight_tools": [
            "netlify MCP (netlify-deploy-services-reader, netlify-project-services-reader)",
            "github MCP (create_pull_request, push_files, list_pull_requests)",
            "docker MCP (run_command)",
        ],
        "completion_guards": ["netlify preview verification", "diff_reviewer", "clean-code-guard"],
        "fallbacks": {
            "netlify MCP": "git push + GitHub Actions CI/CD deployment logs",
            "github MCP": "local git CLI (git status, git log, git diff)",
            "docker MCP": "local docker CLI via run_command",
        },
    },
    "NEXTJS_SERVER_ACTIONS": {
        "description": "Next.js Server Actions & App Router Endpoints",
        "file_patterns": [r"actions\.(?:ts|js)$", r"actions[\\/]", r"route\.(?:ts|js)$"],
        "keywords": ["server action", "use server", "safeparse", "idor", "auth derivation", "action", "nextjs", "app router"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["nextjs-fullstack"],
        "implementation_skills": ["next-server-action-guard", "nextjs-fullstack", "backend-api"],
        "in_flight_tools": ["code_graph find", "repl_sandbox py", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["next-server-action-guard", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "context7": "search_web for Next.js 15 Server Action docs",
        },
    },
    "BACKEND_LARAVEL_PHP": {
        "description": "Laravel 11+ & PHP 8 Modern Backend Services",
        "file_patterns": [r"\.php$", r"\.phtml$", r"app[\\/]Http[\\/]", r"routes[\\/]"],
        "keywords": ["laravel", "php", "artisan", "pest", "eloquent", "blade", "livewire", "controller"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["laravel-mastery"],
        "implementation_skills": ["laravel-mastery", "backend-http", "backend-api"],
        "in_flight_tools": ["code_graph outline", "repl_sandbox sql", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["pest-security-guard", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "context7": "search_web for Laravel 11 / Pest 3 documentation",
        },
    },
    "BACKEND_CORE_API": {
        "description": "REST/GraphQL APIs, Auth/RBAC/JWT, Queues, Workers & Server Logic",
        "file_patterns": [r"controllers[\\/]", r"services[\\/]", r"middleware[\\/]", r"auth[\\/]"],
        "keywords": [
            "api", "endpoint", "rest", "graphql", "webhook", "websocket", "sse",
            "jwt", "oauth", "rbac", "session", "auth", "authentication",
            "queue", "worker", "job", "fix-backend", "feature-febe", "feature-full",
        ],
        "think_skills": ["engineering-workflow", "intake"],
        "plan_skills": ["backend-api", "critique"],
        "implementation_skills": ["backend-api", "backend-http", "backend-identity", "backend-ops"],
        "in_flight_tools": ["code_graph symbol", "code_graph trace", "context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["clean-code-guard", "test-guard", "sentinel", "chaos-audit"],
        "fallbacks": {
            "context7": "local codebase patterns + official framework docs",
        },
    },
    "SECURITY_AUDIT_PENTEST": {
        "description": "Full-Stack Bug Hunting, Security Auditing, Authorized Pentesting & Cookie/Auth Debugging",
        "file_patterns": [r"security", r"pentest", r"cookie"],
        "keywords": [
            "security audit", "pentest", "pen test", "bug-hunter", "bug hunter",
            "vulnerability", "bola", "bfla", "cookie-debugging", "samesite",
            "reverse-engineer-anything",
        ],
        "think_skills": ["engineering-workflow", "security-audit"],
        "plan_skills": ["security-audit", "bug-hunter", "cookie-debugging"],
        "implementation_skills": ["security-audit", "bug-hunter", "pentest", "cookie-debugging"],
        "in_flight_tools": [
            "agent_os scan",
            "agent_os sentinel",
            "chrome-devtools-mcp (get_network_request, list_network_requests)",
        ],
        "completion_guards": ["security-audit", "clean-code-guard", "sentinel"],
        "fallbacks": {
            "chrome-devtools-mcp": "agent_os probe <url> + static source inspection",
        },
    },
    "WORDPRESS_WOOCOMMERCE": {
        "description": "WordPress Themes/Plugins/Blocks & WooCommerce HPOS Extensions",
        "file_patterns": [r"wp-content[\\/]", r"functions\.php$", r"woocommerce[\\/]"],
        "keywords": [
            "wordpress", "wp", "woocommerce", "woo", "hpos", "shortcode",
            "wp_query", "wpdb", "wc_get_order", "feature-wp", "wp-guard", "woo-guard",
        ],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["feature-wp"],
        "implementation_skills": ["feature-wp", "wp-guard", "woo-guard"],
        "in_flight_tools": ["code_graph symbol", "repl_sandbox sql"],
        "completion_guards": ["wp-guard", "woo-guard", "rtl-logical-guard", "clean-code-guard"],
        "fallbacks": {},
    },
    "DATABASE_PERSISTENCE": {
        "description": "Database Schemas, Migrations, Indexes & Queries",
        "file_patterns": [r"\.sql$", r"migrations[\\/]", r"schema\.prisma$", r"models[\\/]"],
        "keywords": ["database", "sql", "migration", "prisma", "table", "index", "schema", "foreign key", "acid", "query"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["database"],
        "implementation_skills": ["database", "backend-data"],
        "in_flight_tools": ["repl_sandbox sql (in-memory SQLite sandbox)"],
        "completion_guards": ["antipattern AP-001 (raw SQL injection)", "sentinel (unbounded query & index check)", "clean-code-guard"],
        "fallbacks": {
            "repl_sandbox": "manual schema review against existing migrations",
        },
    },
    "AI_GEMINI_INTEGRATION": {
        "description": "Google Gemini API, Multimodal Live API, Omni Flash Video & Agy SDK",
        "file_patterns": [r"gemini", r"genai"],
        "keywords": [
            "gemini", "google-genai", "live api", "multimodal", "omni flash",
            "text-to-video", "tts", "function calling", "structured output",
            "antigravity sdk", "agy sdk",
        ],
        "think_skills": ["retrieving-developer-knowledge"],
        "plan_skills": ["gemini-api-dev"],
        "implementation_skills": [
            "gemini-api-dev",
            "gemini-live-api-dev",
            "gemini-omni-flash-api",
            "google-antigravity-sdk",
            "firebase-ai-logic-basics",
        ],
        "in_flight_tools": [
            "gemini-api-docs MCP (gemini_search_docs, gemini_get_doc)",
            "context7 (resolve-library-id, query-docs)",
        ],
        "completion_guards": ["clean-code-guard", "test-guard"],
        "fallbacks": {
            "gemini-api-docs MCP": "search_web on ai.google.dev/gemini-api/docs",
        },
    },
    "FIREBASE_CLOUD": {
        "description": "Firebase Hosting, App Hosting, Auth, Firestore, Data Connect & Security Rules",
        "file_patterns": [r"firestore\.rules$", r"firebase\.json$", r"apphosting\.yaml$", r"\.firebaserc$"],
        "keywords": [
            "firebase", "firestore", "firestore.rules", "data connect",
            "app hosting", "remote config", "crashlytics",
        ],
        "think_skills": ["firebase-basics"],
        "plan_skills": ["firebase-firestore", "firestore-rules-creation"],
        "implementation_skills": [
            "firebase-firestore",
            "firebase-auth-basics",
            "firebase-hosting-basics",
            "firebase-app-hosting-basics",
            "firebase-data-connect",
            "firestore-rules-creation",
        ],
        "in_flight_tools": ["context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["firebase-security-rules-auditor", "clean-code-guard"],
        "fallbacks": {},
    },
    "MAPS_GEOLOCATION": {
        "description": "Google Maps Platform, Places, Geocoding, Routes & 3D Maps",
        "file_patterns": [r"google.*maps", r"mapbox", r"geocod"],
        "keywords": ["google maps", "geocoding", "places api", "marker clustering", "geofencing", "street view", "routing eta"],
        "think_skills": ["retrieving-developer-knowledge"],
        "plan_skills": ["google-maps-platform"],
        "implementation_skills": ["google-maps-platform"],
        "in_flight_tools": ["context7 (resolve-library-id, query-docs)"],
        "completion_guards": ["clean-code-guard", "rtl-logical-guard"],
        "fallbacks": {},
    },
    "CHROME_EXTENSIONS": {
        "description": "Chrome Extensions Manifest V3, Content Scripts, Service Workers & Side Panels",
        "file_patterns": [r"manifest\.json$", r"content_script", r"side_panel"],
        "keywords": ["chrome extension", "browser extension", "manifest v3", "declarativenetrequest", "content script", "side panel"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["chrome-extensions"],
        "implementation_skills": ["chrome-extensions", "modern-web-guidance"],
        "in_flight_tools": ["chrome-devtools-mcp (list_console_messages, evaluate_script)"],
        "completion_guards": ["clean-code-guard", "test-guard"],
        "fallbacks": {},
    },
    "WEBMCP": {
        "description": "In-Browser WebMCP (document.modelContext) Tools & Declarative Forms",
        "file_patterns": [r"webmcp", r"modelContext", r"registerTool"],
        "keywords": [
            "webmcp", "modelcontext", "registertool", "gettools", "executetool",
            "toolchange", "toolautosubmit", "in-browser tool", "browser tool",
        ],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["webmcp"],
        "implementation_skills": ["webmcp", "muaz-skill", "clean-code-guard"],
        "in_flight_tools": [
            "chrome-devtools-mcp (evaluate_script, list_console_messages)",
            "playwright (browser_navigate, browser_evaluate)",
            "context7 (resolve-library-id, query-docs)",
        ],
        "completion_guards": ["clean-code-guard", "test-guard", "chaos-audit"],
        "fallbacks": {
            "chrome-devtools-mcp": "playwright or local mock harness (MockModelContext)",
            "context7": "skills/webmcp/references/spec-idl.md and official W3C webmachinelearning/webmcp repository",
        },
    },
    "TESTING_QA_VERIFICATION": {
        "description": "Unit, Integration & E2E Testing, Test-Guard & Two-Model Debate Review",
        "file_patterns": [r"\.test\.(?:ts|tsx|js)$", r"\.spec\.(?:ts|tsx|js)$", r"tests[\\/]", r"Test\.php$"],
        "keywords": [
            "test", "tests", "unit test", "integration test", "e2e", "vitest",
            "jest", "pytest", "phpunit", "test-guard", "testing-qa",
            "check-all", "debate-review", "ui-review-loop",
        ],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["testing-qa"],
        "implementation_skills": ["testing-qa", "test-guard", "ui-review-loop"],
        "in_flight_tools": ["agent_os test", "agent_os review", "playwright (browser_navigate, browser_snapshot)"],
        "completion_guards": ["test-guard", "clean-code-guard", "debate-review", "check-all"],
        "fallbacks": {},
    },
    "DOCUMENTATION_ARCHITECTURE": {
        "description": "Project README, Architecture Docs, API Reference & Docs-vs-Code Drift Guard",
        "file_patterns": [r"README\.md$", r"docs[\\/]ARCHITECTURE\.md$", r"docs[\\/]API\.md$", r"CHANGELOG\.md$"],
        "keywords": ["document", "documentation", "readme", "docstring", "changelog", "doc-project", "docs-guard", "project-documentation"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["doc-project"],
        "implementation_skills": ["doc-project", "project-documentation", "docs-guard"],
        "in_flight_tools": ["code_graph outline", "code_graph symbol"],
        "completion_guards": ["docs-guard", "agent_os audit"],
        "fallbacks": {},
    },
    "PONYTAIL_SIMPLICITY": {
        "description": "Anti-Overengineering, YAGNI, Minimalist Code & Technical Debt Ledger",
        "file_patterns": [],
        "keywords": [
            "ponytail", "ponytail-review", "ponytail-audit", "ponytail-debt",
            "ponytail-gain", "ponytail-help", "over-engineering", "overengineered",
            "yagni", "bloat", "simplify",
        ],
        "think_skills": ["ponytail"],
        "plan_skills": ["ponytail"],
        "implementation_skills": ["ponytail", "ponytail-review", "ponytail-audit", "ponytail-debt"],
        "in_flight_tools": ["code_graph outline", "agent_os review"],
        "completion_guards": ["ponytail-review", "clean-code-guard"],
        "fallbacks": {},
    },
    "OPENCODE_DELEGATION": {
        "description": "OpenCode CLI Background Delegation & Fleet Lane Configuration",
        "file_patterns": [r"relay\.mjs$"],
        "keywords": ["opencode", "opencode-delegate", "delegate-setup", "delegation lane"],
        "think_skills": ["delegate-setup"],
        "plan_skills": ["opencode-delegate"],
        "implementation_skills": ["opencode-delegate", "delegate-setup"],
        "in_flight_tools": ["node skills/opencode-delegate/scripts/relay.mjs"],
        "completion_guards": ["clean-code-guard", "test-guard"],
        "fallbacks": {},
    },
    "BANDWIDTH_DATA_SAVER": {
        "description": "Low-Bandwidth Data-Saver Profile, Offline Package Caching & Caveman Token Mode",
        "file_patterns": [r"bandwidth_guard\.py$"],
        "keywords": ["data-saver", "save-data", "bandwidth", "caveman", "low bandwidth", "metered connection", "offline cache"],
        "think_skills": ["save-data", "data-saver", "caveman"],
        "plan_skills": ["data-saver"],
        "implementation_skills": ["save-data", "data-saver", "caveman"],
        "in_flight_tools": ["agent_os data-saver status", "agent_os data-saver apply"],
        "completion_guards": ["agent_os data-saver status"],
        "fallbacks": {},
    },
    "CROSS_SESSION_CONTINUITY": {
        "description": "Cross-Session Working Memory, Daily Triage & Decision Tracking",
        "file_patterns": [r"PROGRESS\.md$", r"DECISIONS\.md$", r"SESSION_SNAPSHOT\.md$", r"release-tracker\.md$"],
        "keywords": [
            "continuity", "resume", "checkpoint", "memory", "graph", "session",
            "recall", "past decision", "plan-daily", "daily plan", "plan daily",
        ],
        "think_skills": ["plan-daily", "engineering-workflow"],
        "plan_skills": ["plan-daily"],
        "implementation_skills": ["plan-daily", "engineering-workflow"],
        "in_flight_tools": [
            "agent_os plan-daily",
            "memory MCP (search_nodes, open_nodes, create_entities, add_observations)",
            "agent_os snapshot resume",
            "agent_os snapshot freeze",
        ],
        "completion_guards": ["agent_os snapshot freeze", "clean-code-guard"],
        "fallbacks": {
            "memory MCP": "SESSION_SNAPSHOT.md + PROGRESS.md + DECISIONS.md in project root",
        },
    },
    "PYTHON_SYSTEMS": {
        "description": "Python Utilities, Agent OS Scripts & Automation",
        "file_patterns": [r"\.py$"],
        "keywords": ["python", "script", "agent", "daemon", "cli", "regex", "repl"],
        "think_skills": ["engineering-workflow"],
        "plan_skills": ["engineering-workflow"],
        "implementation_skills": ["clean-code-guard", "engineering-workflow"],
        "in_flight_tools": ["repl_sandbox eval", "code_graph symbol"],
        "completion_guards": ["python-security-guard", "sentinel", "clean-code-guard", "chaos-audit"],
        "fallbacks": {
            "code_graph": "view_file / grep search",
        },
    },
}

# Single-Winner Authority Hierarchy (prevents Skill vs Tool vs MCP conflicts)
SINGLE_WINNER_AUTHORITY: Dict[str, str] = {
    "design_tokens_and_layout": "muaz-skill (design_system.py + anti_slop.py) + rtl-logical-guard",
    "visual_screen_generation": "StitchMCP (ONLY for visual mockup/variant generation; never overrides RTL/CMS tokens)",
    "local_codebase_navigation": "agent_os.py symbol / outline / trace (AST lookup before broad file reads)",
    "live_framework_docs": "context7 MCP (gemini-api-docs for Gemini SDK; stripe MCP for Stripe billing)",
    "live_browser_debugging": "chrome-devtools-mcp (DOM, CSS, console, LCP, a11y inspection)",
    "automated_e2e_user_flows": "ui-review-loop / playwright MCP (multi-viewport 375px/768px/1440px verification)",
}


def load_live_catalog() -> Dict[str, Any]:
    """Loads SKILL_INDEX.json (custom skills, active plugin skills, MCP servers) for dynamic discovery."""
    if SKILL_INDEX_PATH.exists():
        try:
            return json.loads(SKILL_INDEX_PATH.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            _ = exc  # Fallback to live build_index() if SKILL_INDEX.json is malformed
    try:
        from scripts.skill_indexer import build_index
        return build_index()
    except Exception:
        return {"skills": [], "plugin_skills": [], "mcp_servers": []}


def discover_dynamic_catalog_matches(input_target: str, catalog: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Dynamically matches any custom skill, active plugin skill, or MCP server in SKILL_INDEX.json
    whose exact name or slash-command appears in input_target, ensuring future skills/MCPs are auto-routed.
    """
    lower_input = input_target.lower()
    matched_by_phase: Dict[str, List[str]] = {"THINK": [], "PLAN": [], "BUILD": [], "VERIFY": []}
    matched_mcps: List[str] = []

    all_skills = list(catalog.get("skills", [])) + list(catalog.get("plugin_skills", []))
    for item in all_skills:
        s_name = item.get("name", "")
        if not s_name:
            continue
        # Match explicit skill name or /skill-name mention
        pat = r"(?:^|[\s/\"'])" + re.escape(s_name.lower()) + r"(?:$|[\s.,\"'])"
        if re.search(pat, lower_input):
            phase = item.get("phase", "BUILD")
            if s_name not in matched_by_phase.get(phase, []):
                matched_by_phase.setdefault(phase, []).append(s_name)

    for srv in catalog.get("mcp_servers", []):
        srv_name = srv.get("name", "")
        if srv_name and srv_name.lower() in lower_input:
            matched_mcps.append(f"{srv_name} MCP ({srv.get('domain', '')})")

    return {
        "THINK": matched_by_phase["THINK"],
        "PLAN": matched_by_phase["PLAN"],
        "BUILD": matched_by_phase["BUILD"],
        "VERIFY": matched_by_phase["VERIFY"],
        "MCPS": matched_mcps,
    }


def resolve_stack_conflicts(
    matched_domains: List[str],
    lower_input: str,
    skills_set: Set[str],
    guards_set: Set[str],
) -> None:
    """
    Eliminates cross-stack skill collisions in-place so mutually exclusive stacks
    (Next.js vs Laravel/PHP vs WordPress) never pollute each other unless both are requested.
    """
    has_laravel = "BACKEND_LARAVEL_PHP" in matched_domains
    has_wp = "WORDPRESS_WOOCOMMERCE" in matched_domains
    has_nextjs = "NEXTJS_SERVER_ACTIONS" in matched_domains or any(
        k in lower_input for k in ["nextjs", "next.js", "tsx", "react", "app router"]
    )

    if has_laravel and not has_nextjs:
        skills_set.discard("nextjs-fullstack")
        skills_set.discard("next-server-action-guard")
        guards_set.discard("next-server-action-guard")
    if has_laravel and not has_wp:
        skills_set.discard("wp-guard")
        skills_set.discard("woo-guard")
        skills_set.discard("feature-wp")
        guards_set.discard("wp-guard")
        guards_set.discard("woo-guard")

    if has_wp and not has_nextjs:
        skills_set.discard("nextjs-fullstack")
        skills_set.discard("next-server-action-guard")
        guards_set.discard("next-server-action-guard")
    if has_wp and not has_laravel:
        skills_set.discard("laravel-mastery")
        guards_set.discard("pest-security-guard")

    if has_nextjs and not has_laravel and not has_wp:
        skills_set.discard("laravel-mastery")
        skills_set.discard("wp-guard")
        skills_set.discard("woo-guard")
        guards_set.discard("pest-security-guard")
        guards_set.discard("wp-guard")
        guards_set.discard("woo-guard")


def determine_task_level(input_target: str) -> Dict[str, str]:
    """Classifies task sizing into Levels 1-4 with ceremony guidelines."""
    lower = input_target.lower()

    # Level 1: Trivial edits
    if any(k in lower for k in ["typo", "fix typo", "rename", "single line", "quick fix", "comment", "docstring", "lint"]):
        return {
            "level": "Level 1: Trivial Edit",
            "ceremony": "Zero ceremony. Inspect -> Surgical edit -> Run test/lint -> Done.",
        }

    # Level 4: Greenfield or cross-cutting overhaul
    if any(k in lower for k in ["architectural overhaul", "greenfield", "precode", "prd", "trd", "6 pillars", "spec-kit", "complete overhaul", "start-project"]):
        return {
            "level": "Level 4: Architectural Overhaul / Cross-Cutting",
            "ceremony": "Formal Pre-Coding Pillars (01-PRD to 06-PLAN) or Spec Kit workflow. Gated approval required.",
        }

    # Level 2: Focused defect/bug fix
    if any(k in lower for k in ["bug", "defect", "fix", "error", "failing", "crash", "regression", "broken"]):
        return {
            "level": "Level 2: Focused Bug Fix",
            "ceremony": "Reproduce -> Diagnose root cause -> Targeted fix -> Regression test -> Done.",
        }

    # Level 3: Standard feature or refactor
    return {
        "level": "Level 3: Moderate Feature / Refactor",
        "ceremony": "Context reconstruction -> Bounded plan -> Direct execution lock -> Verify with tests & guards.",
    }


def determine_delegation(input_target: str) -> str:
    """Recommends whether to delegate to a subagent or execute directly."""
    lower = input_target.lower()
    if "firestore.rules" in lower or "firestore rules" in lower:
        return "DELEGATE: Mandatory specialist subagent 'firestore-rules-author'."
    if "opencode" in lower:
        return "DELEGATE: OpenCode background implementer CLI via 'opencode-delegate' (relay.mjs)."
    if any(k in lower for k in ["wide survey", "explore entire repo", "survey all directories"]):
        return "DELEGATE: Subagent 'research' (read-only context preservation)."
    return "DIRECT EXECUTION LOCK: Primary agent executes directly (No subagent delegation needed)."


def resolve_task_routing(input_target: str) -> Dict[str, Any]:
    matched_domains: List[str] = []
    lower_input = input_target.lower()

    for domain_key, profile in DOMAIN_PROFILES.items():
        pattern_match = any(re.search(pat, input_target, re.IGNORECASE) for pat in profile["file_patterns"])
        keyword_match = any(re.search(r"\b" + re.escape(kw) + r"\b", lower_input) for kw in profile["keywords"])

        if pattern_match or keyword_match:
            matched_domains.append(domain_key)

    if not matched_domains:
        if input_target.endswith(".py"):
            matched_domains = ["PYTHON_SYSTEMS"]
        elif any(input_target.endswith(ext) for ext in [".tsx", ".css", ".jsx"]):
            matched_domains = ["FRONTEND_UI"]
        else:
            matched_domains = ["BACKEND_CORE_API"]

    think_skills: Set[str] = {"engineering-workflow"}
    plan_skills: Set[str] = set()
    impl_skills: Set[str] = set()
    tools: Set[str] = set()
    guards: Set[str] = set()
    fallbacks: Dict[str, str] = {}

    for d in matched_domains:
        prof = DOMAIN_PROFILES.get(d)
        if prof:
            think_skills.update(prof.get("think_skills", []))
            plan_skills.update(prof.get("plan_skills", []))
            impl_skills.update(prof.get("implementation_skills", []))
            tools.update(prof.get("in_flight_tools", []))
            guards.update(prof.get("completion_guards", []))
            if "fallbacks" in prof:
                fallbacks.update(prof["fallbacks"])

    # Dynamic live discovery across SKILL_INDEX.json (custom skills, plugin skills, and MCP servers)
    catalog = load_live_catalog()
    dyn = discover_dynamic_catalog_matches(input_target, catalog)
    think_skills.update(dyn["THINK"])
    plan_skills.update(dyn["PLAN"])
    impl_skills.update(dyn["BUILD"])
    guards.update(dyn["VERIFY"])
    for mcp_entry in dyn["MCPS"]:
        srv_prefix = mcp_entry.split(" ")[0].lower()
        if not any(srv_prefix in existing.lower() for existing in tools):
            tools.add(mcp_entry)

    # Also include explicitly mentioned THINK/PLAN/VERIFY skills in implementation_skills for backward compatibility
    for explicit_skill in dyn["THINK"] + dyn["PLAN"] + dyn["VERIFY"]:
        impl_skills.add(explicit_skill)

    # Resolve cross-stack conflicts so mutually exclusive stacks never collide
    resolve_stack_conflicts(matched_domains, lower_input, impl_skills, guards)

    if not guards:
        guards = {"clean-code-guard", "chaos-audit"}
    if not plan_skills:
        plan_skills = {"plan-daily"}

    task_sizing = determine_task_level(input_target)
    delegation_advice = determine_delegation(input_target)

    mcp_markers = ("mcp", "context7", "chrome-devtools", "playwright", "sequential-thinking", "memory")
    phase_loadout = {
        "1_THINK": {
            "skills": sorted(list(think_skills)),
            "cli_tools": ["agent_os symbol", "agent_os outline", "agent_os scan"],
            "mcps": ["sequential-thinking", "memory"],
        },
        "2_PLAN": {
            "skills": sorted(list(plan_skills)),
            "cli_tools": ["agent_os plan-daily", "agent_os precode", "muaz-skill design_system.py"],
            "mcps": [t for t in sorted(list(tools)) if any(m in t for m in ["StitchMCP", "github MCP", "jira", "sequential-thinking"])]
            or ["context7 (resolve-library-id, query-docs)"],
        },
        "3_BUILD": {
            "skills": sorted(list(impl_skills)),
            "cli_tools": [t for t in sorted(list(tools)) if not any(m in t.lower() for m in mcp_markers)]
            or ["code_graph symbol", "repl_sandbox"],
            "mcps": [t for t in sorted(list(tools)) if any(m in t for m in ["context7", "stripe MCP", "gemini-api-docs", "docker MCP", "StitchMCP"])]
            or ["context7 (resolve-library-id, query-docs)"],
        },
        "4_VERIFY": {
            "skills": sorted(list(guards)),
            "cli_tools": ["agent_os review", "agent_os sentinel", "agent_os test"],
            "mcps": [t for t in sorted(list(tools)) if any(m in t for m in ["chrome-devtools-mcp", "playwright", "netlify MCP"])]
            or ["chrome-devtools-mcp (list_console_messages, lighthouse_audit)"],
        },
    }

    return {
        "input": input_target,
        "task_level": task_sizing["level"],
        "ceremony": task_sizing["ceremony"],
        "delegation": delegation_advice,
        "domains": matched_domains,
        "phase_loadout": phase_loadout,
        "authority_winners": SINGLE_WINNER_AUTHORITY,
        "implementation_skills": sorted(list(impl_skills)),
        "in_flight_tools": sorted(list(tools)),
        "completion_guards": sorted(list(guards)),
        "fallbacks": fallbacks,
    }


def print_routing_manifest(result: Dict[str, Any]):
    print("=" * 72)
    print("   ANTIGRAVITY AGENT OS - 4-PHASE CONFLICT-FREE ROUTING MANIFEST   ")
    print("=" * 72)
    print(f"Target Input:        {result['input']}")
    print(f"Task Sizing:         {result['task_level']}")
    print(f"Ceremony Protocol:   {result['ceremony']}")
    print(f"Delegation Guidance: {result['delegation']}")
    print(f"Matched Domain(s):   {', '.join(result['domains'])}")
    print("-" * 72)

    loadout = result.get("phase_loadout", {})
    if loadout:
        print("[4-PHASE ENGINEERING LOADOUT (THINK -> PLAN -> BUILD -> VERIFY)]:")
        for phase_key, pdata in loadout.items():
            print(f"  [{phase_key}]")
            print(f"    * Skills   : {', '.join(pdata.get('skills', []))}")
            print(f"    * CLI Tools: {', '.join(pdata.get('cli_tools', []))}")
            print(f"    * MCPs     : {', '.join(pdata.get('mcps', []))}")
        print("-" * 72)

    print("[1. WHILE IMPLEMENTING - ACTIVE SKILLS TO CONSULT]:")
    for s in result["implementation_skills"]:
        print(f"  * {s}")
    print("\n[2. WHILE IMPLEMENTING - IN-FLIGHT TOOLS & MCPS]:")
    for t in result["in_flight_tools"]:
        print(f"  * {t}")
    if result["fallbacks"]:
        print("\n[3. IF TOOLS UNAVAILABLE - RESILIENT FALLBACKS]:")
        for tool, fallback in result["fallbacks"].items():
            print(f"  * {tool:<20} -> {fallback}")
    print("\n[4. WHEN FINISHED - MANDATORY COMPLETION GUARDS]:")
    for g in result["completion_guards"]:
        print(f"  * {g}")
    print("=" * 72)


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
