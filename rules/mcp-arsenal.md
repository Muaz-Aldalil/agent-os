# THE 8-MCP ARSENAL & LIFECYCLE ORCHESTRATION PROTOCOL (`mcp-arsenal.md`)

MCP servers are **live external & runtime bridges**—not replacements for local AST/file inspection. Invoke them purposefully at the lifecycle stage where external documentation, design assets, or live browser/API state is required.

---

## 1. The 8-MCP Lifecycle Matrix

| Lifecycle Stage | Active MCP Server | Primary Tools & Mandate |
| :--- | :--- | :--- |
| **Stage 1: External Docs & APIs** | `context7`, `gemini-api-docs`, `stripe` | Resolve library docs via `resolve-library-id` -> `query-docs`; query official Gemini SDK docs via `gemini_search_docs` -> `gemini_get_doc`; verify Stripe APIs via `search_stripe_documentation`. |
| **Stage 2: UI Design & Tokens** | `StitchMCP` | Generate/edit UI screens (`generate_screen_from_text`, `edit_screens`), manage design systems (`list_design_systems`, `apply_design_system`), and sync `DESIGN.md`. |
| **Stage 3: Live Runtime & DOM** | `chrome-devtools-mcp`, `playwright` | Inspect live DOM, computed CSS, console errors, network requests, and LCP/performance (*only when browser testing is permitted by the Owner*). |
| **Stage 4: Repo & Issue Ops** | `github`, `jira` | Inspect PRs, issues, commits, and review comments when managing remote repositories or issue trackers. |
| **Stage 5: Cloud & Deploy** | `netlify`, `docker` | Inspect deploy statuses, build logs, or container state when diagnosing infrastructure. |

---

## 2. Mandatory MCP Operating Rules

1. **Local First, MCP Second**:
   - Always check local repository code, `package.json` / `composer.json`, and local AST (`agent_os.py symbol` / `outline`) before calling external documentation MCPs.
2. **Context7 Two-Step Lookup (`resolve-library-id` -> `query-docs`)**:
   - Whenever verifying unfamiliar third-party library APIs (Next.js 15/16, Tailwind v4, TanStack, Prisma, Laravel 11/12), call `resolve-library-id` first, then `query-docs` with a specific question.
3. **Browser MCP Gate**:
   - If the Owner states *"don't open/test in the browser"*, strictly refrain from calling `playwright` or `chrome-devtools-mcp` tools; validate via CLI tests and provide a Manual Browser Acceptance Checklist.
4. **Resilient Fallback Protocol**:
   - If an MCP server times out or is offline (common on metered/Sudan connections), do not retry in a loop. Emit the single-line recovery notice from `execution-transparency.md` and fall back immediately to local deterministic scripts (`agent_os.py`) or local codebase inspection.
