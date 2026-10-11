# The 6-MCP Engineering Arsenal & Lifecycle Orchestration Matrix

## 1. Overview & Mandate
Antigravity is equipped with a 6-pillar Model Context Protocol (MCP) tool suite. These tools are not passive utilities—they are active operational instruments bound directly to the **Autonomous Senior Engineering Workflow** and the **6 Pre-Coding Pillars**.

When executing engineering tasks, the agent must orchestrate each MCP server at its designated lifecycle phase.

```
┌────────────────────────────────────────────────────────────────────────┐
│               THE 6-MCP LIFECYCLE ORCHESTRATION PIPELINE               │
├───────────────────┬──────────────────────────┬─────────────────────────┤
│ Lifecycle Phase   │ Active MCP Server        │ Primary Capabilities    │
├───────────────────┼──────────────────────────┼─────────────────────────┤
│ 1. Architecture   │ sequential-thinking      │ Multi-step logic trees, │
│    & Discovery    │ github                   │ issue/PR context        │
├───────────────────┼──────────────────────────┼─────────────────────────┤
│ 2. Visual Design  │ StitchMCP                │ Generative screens,     │
│    & Prototyping  │                          │ design systems, variants│
├───────────────────┼──────────────────────────┼─────────────────────────┤
│ 3. Domain & Auth  │ stripe                   │ Authoritative API docs, │
│    Implementation │                          │ intents, customer ops   │
├───────────────────┼──────────────────────────┼─────────────────────────┤
│ 4. Live UI & DOM  │ chrome-devtools-mcp      │ DOM inspection, CSS,    │
│    Verification   │                          │ network trace, consoles │
├───────────────────┼──────────────────────────┼─────────────────────────┤
│ 5. Deployment &   │ netlify                  │ Preview deploys, envs   │
│    Release Gate   │ github                   │ PR creation, code sync  │
│                   │ chrome-devtools-mcp      │ Lighthouse & CWV audits │
└───────────────────┴──────────────────────────┴─────────────────────────┘
```

---

## 2. Phase-by-Phase Tool Orchestration

### Phase 1: Architecture & Intent Clarification (Stages 1–3 / Pre-Code PRD & TRD)
* **`sequential-thinking`**:
  - Activates when decomposing complex architectural trade-offs, database migrations, or distributed flows.
  - Generates hypothesis trees, tests edge assumptions, and prevents hasty design decisions before drafting `01-PRD.md` or `02-TRD.md`.
* **`github`**:
  - `search_issues`, `list_issues`: Fetch user stories, bug reports, and acceptance criteria from GitHub.
  - `list_commits`, `get_pull_request`: Reconstruct recent development history and avoid redundant reimplementation.

### Phase 2: Visual Blueprint & Generative UI (Pre-Code App Flow & Design Brief)
* **`StitchMCP`**:
  - `generate_screen_from_text`: Rapidly prototype visual screens corresponding to routes defined in `03-APP_FLOW.md`.
  - `create_design_system_from_design_md`: Translate color tokens, typography scales, and component guidelines from `04-DESIGN_BRIEF.md` directly into Stitch design systems.
  - `generate_variants`: Explore responsive layout variants (mobile vs. desktop) and bidirectional RTL/LTR adaptations before writing front-end code.

### Phase 3: High-Stakes Domain & In-Flight Implementation (Stage 5)
* **`stripe`**:
  - `search_stripe_documentation`: Look up exact, authoritative Stripe API schemas and parameters (Zero Blind Code).
  - `stripe_implementation_planner`: Validate checkout architectures and subscription lifecycles.
  - `stripe_api_search`, `stripe_api_read`: Inspect live customer records, payment intents, and price IDs to eliminate configuration drift.
  - Mandatory compliance with **Danger Zone 1** (zero float arithmetic, strict idempotency keys, ACID ledger balance).

### Phase 4: Live DOM & Responsive In-Flight Verification (Stage 7)
* **`chrome-devtools-mcp`**:
  - `navigate_page`, `evaluate_script`: Inspect live web applications running in local dev environments.
  - `get_css_styles`: Empirically verify computed CSS Logical Properties (`padding-inline`, `margin-inline`, `inset-inline-start`) under RTL and LTR.
  - `get_console_message`, `get_network_request`: Catch silent JavaScript runtime errors, unhandled rejections, and failed API calls.
  - `take_screenshot`: Capture visual confirmation of completed UI states.

### Phase 5: Release Verification & Deployment Gate (Stages 8–9)
* **`chrome-devtools-mcp` (Lighthouse & Core Web Vitals)**:
  - `lighthouse_audit`: Run automated accessibility (a11y) and performance audits prior to merging.
  - Performance trace: Verify Largest Contentful Paint (LCP < 2.5s) and Cumulative Layout Shift (CLS < 0.1).
* **`netlify`**:
  - `netlify-deploy-services-reader`: Verify build logs and automated preview deployment URLs.
  - `netlify-project-services-reader`: Verify production environment variables and site redirects (`netlify.toml`).
* **`github`**:
  - `create_pull_request`: Generate atomic, descriptive PRs linking back to feature specs.
  - `create_pull_request_review`: Post structured architectural reviews and verification summaries.

---

## 3. Operational Invariants
1. **Zero Blind Guessing**: If an entity exists in GitHub, Stripe, or Netlify, query it via MCP before hardcoding assumptions.
2. **Deterministic Task Routing**: The agent must invoke `python scripts/agent_os.py route "<task>"` to identify mandatory MCP tools and verification guards.
3. **Evidence Precedes Claims**: Never claim a deployment or UI fix succeeded without concrete output from `chrome-devtools-mcp` or `netlify`.
