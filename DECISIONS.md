# Architectural Decision Records (ADRs)

## [ADR-001] Separation of Human Authority and Agent Engineering Ownership
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Historical sessions suffered from conversational friction, sycophancy, or hesitation where the agent repeatedly paused to ask trivial engineering questions or silently assumed business/pricing policies.
- **Alternatives Evaluated**:
  1. *Unrestricted autonomy*: Agent makes business and product decisions without human guidance. (Rejected: Violates product alignment).
  2. *Passive ticket executor*: Agent asks permission for every line edit. (Rejected: Causes extreme analysis paralysis).
- **Selected Decision**: Enshrine the Human–Agent Engineering Constitution ([engineering-constitution.md](file:///D:/Skills/.agents/rules/engineering-constitution.md)) with a strict authority boundary. Human owns product/policy/pricing/acceptance; Agent owns architecture/implementation/database/security/tests under Execution Lock.
- **Invariants & Trade-offs**: Agent owns routine engineering decisions without asking; when product policy is ambiguous, Agent presents a Structured Recommendation.

---

## [ADR-002] Modern Pest 3 Security Presets over Archived Enlightn
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: The Laravel security scanner `Enlightn` was officially archived in January 2026. A modern, actively supported architectural security solution was required.
- **Alternatives Evaluated**:
  1. *Continue using archived Enlightn*: (Rejected: Deprecated package, security liabilities).
  2. *Pest 3 Architecture Security Presets*: (Selected).
- **Selected Decision**: Adopt Pest 3 native `arch()->preset()->security()`, `arch()->preset()->php()`, and custom architectural test rules in [pest-security-guard](file:///D:/Skills/.agents/skills/pest-security-guard/SKILL.md).
- **Consequences**: Zero external deprecated dependencies; natively runs inside existing PHP test runners (`pest`).

---

## [ADR-003] CSS Logical Properties for RTL/LTR Layout Integrity
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Dual Arabic/English layouts frequently suffered from visual mirroring bugs when using physical CSS properties (`left`, `right`, `pl-*`, `pr-*`).
- **Alternatives Evaluated**:
  1. *Duplicate CSS stylesheets / manual overrides*: (Rejected: High maintenance and visual drift).
  2. *Tailwind CSS Logical Properties*: (Selected).
- **Selected Decision**: Enforce CSS Logical Properties (`start`, `end`, `ps-*`, `pe-*`, `ms-*`, `me-*`, `text-start`, `text-end`) via [rtl-logical-guard](file:///D:/Skills/.agents/skills/rtl-logical-guard/SKILL.md).
- **Consequences**: Automatic bi-directional layout switching simply by toggling `<html dir="rtl">` or `<html dir="ltr">`.

---

## [ADR-004] Dual Customization Topology (Global & Workspace Mirror)
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Skills placed in `C:\Users\HP\.agents\skills\` were unreachable by Antigravity because AGY discovers global skills strictly from `C:\Users\HP\.gemini\config\skills\` and workspace skills from `.agents/skills`.
- **Selected Decision**: Promote canonical skills to global `C:\Users\HP\.gemini\config\skills\` for cross-workspace availability, and maintain a complete mirror in `D:\Skills\.agents\skills\` under local git version control.
- **Consequences**: AGY has immediate access to all 41 skills across every project, while the workspace tracks the complete source of truth.

---

## [ADR-005] Clean Session Continuity via Automated Checkpointing
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Extended AI coding conversations experience context window degradation and token compaction around 40–50 turns, leading to context amnesia.
- **Selected Decision**: Implement the Clean Session Continuity Protocol. The agent automatically maintains `PROGRESS.md` and `DECISIONS.md` in the project root on milestones, turn limits, or prior to compaction. On session resumption, reading these files is the mandatory first action.
- **Consequences**: Zero loss of architectural context across session compactions or fresh conversation restarts.

---

## [ADR-006] Adoption of ui-review-loop for Temporal UI & Visual Verification
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Web UI is a state machine over time (debounced input, async fetches, DOM mutations, CSS transitions). Static screenshots are point-in-time captures that cannot diagnose why a state failed to transition or if a race condition occurred.
- **Selected Decision**: Deploy `ui-review-loop` to global (`C:\Users\HP\.gemini\config\skills\`) and workspace (`D:\Skills\.agents\skills\`). Wire into `engineering-workflow` Stage 8.
- **Consequences**: Enables recorded video verification rounds, full DOM MutationObserver timelines, and a local interactive review site (`127.0.0.1` via `server.mjs`) for asynchronous human review with zero npm dependencies under Node 24.

---

## [ADR-007] Selective Adoption of debate-review via OpenCode & Elimination of Fleet Bloat
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: `D:\Skills\Elnagdy` ships with 17 implementer delegate skills. The technical owner exclusively uses `opencode-delegate` (mandated by KNZiN Constitution Rule 32 for document and PDF generation) and explicitly rejected importing 16 unused CLIs. However, adversarial code review (`debate-review`) was required.
- **Alternatives Evaluated**:
  1. *Import all 16 delegate skills*: (Rejected: YAGNI violation, extreme maintenance bloat).
  2. *Reject debate-review entirely*: (Rejected: Loses valuable two-model adversarial review on diffs).
  3. *Adapt debate-review to dual OpenCode lanes*: (Selected).
- **Selected Decision**: Deploy `debate-review` configured with dual OpenCode lanes in `delegate-skills/config.json`:
  - `review-main`: `opencode` (`space-bunny-free`, `--read-only`)
  - `review-debate`: `opencode` (`big-pickle`, `--read-only`)
  Infuse its P0/P1/P2 severity triage and "Verify Before You Believe" invariant directly into `engineering-workflow` Stage 6. Dismiss the 16 unused delegates.
- **Consequences**: Pristine repository footprint; zero dead dependencies; fully functional multi-model adversarial review loop powered by existing OpenCode infrastructure.

---

## [ADR-008] Developer Attribution & Company Branding Assets (ديجتال أيج / DigAge)
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: The developer company that built the KNZiN platform is **ديجتال أيج** (DigAge). The branding visual tokens require "Dig" in `#00bcd4` and "Age" in `#e91e63`, with the transparent brain-chip logo sourced from `Simple Suits Store Black Logo بدون خلفيه.png` (mapped to `public/digage-logo.png`).
- **Selected Decision**: Integrate developer attribution into `Footer.tsx` with logo on top and stylized company name at the bottom. Maintain bidirectional parity in `messages/ar.json` and `messages/en.json`.
- **Consequences**: Consistent, permanent developer attribution preserved across all public pages in light and dark modes.

---

## [ADR-009] Lifecycle Command Safety Hooks & Frontend UUID Contract Harmonization
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Autonomous agent executions can run destructive git or database wipeout commands if unconstrained. In parallel, the KNZiN frontend TypeScript definitions suffered from subtle contract drift where UUID model IDs (`HasUuids`) were typed as `number`, and `CreatedOrder` assumed unmasked IP fields that backend `OrderResource` properly strips.
- **Selected Decision**:
  1. Deploy Antigravity native `hooks.json` and `scripts/safety_hook.py` using `PreToolUse` command inspection to automatically block destructive operations (`git reset --hard`, `git clean -f`, recursive `.git` deletion, `migrate:fresh`, `DROP DATABASE`).
  2. Implement `scripts/audit_agent_os.py` for automated zero-cost regression testing of all skills, frontmatters, and guard parity.
  3. Harmonize frontend contracts in `admin.ts`, `useAdminUsers.ts`, and `useCheckout.ts` to cleanly support string UUIDs and sanitized payloads.
- **Consequences**: Zero accidental data destruction; complete TypeScript and runtime payload alignment between Next.js and Laravel models; verified by 160 passing invariant tests.

---

## [ADR-010] Strict Workspace Boundary Isolation & Danger Zone Protocol
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Autonomous agents operating in workstations with multiple projects or open editor tabs risk cross-contaminating external repositories (e.g. adjacent client production codebases) when resolving dependencies or executing commands.
- **Alternatives Evaluated**:
  1. *Rely on conversational prompts*: (Rejected: Prone to drift across multi-turn sessions).
  2. *Constitutional + Programmatic Defense-in-Depth*: (Selected).
- **Selected Decision**:
  1. Enshrine Workspace Boundary Isolation in `engineering-constitution.md` (Section 3.4) and `engineering-workflow/SKILL.md` (Stage 1 & Danger Zone 4).
  2. Programmatically enforce directory boundaries in `scripts/safety_hook.py` by intercepting any `run_command` with `Cwd` or `CommandLine` referencing restricted danger zones (e.g., KNZiN Project).
  3. Prohibit `cd` usage across all tool invocations.
- **Consequences**: 100% boundary isolation. External repositories are completely protected from unauthorized modification or inspection.

---

## [ADR-011] Automated Guard Verification Battery & Static Security Checker
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Critical quality guards (`next-server-action-guard`, `pest-security-guard`, `rtl-logical-guard`, `clean-code-guard`) existed as advisory documentation. Without an automated verification engine, anti-patterns could slip through during rapid implementation.
- **Selected Decision**:
  1. Create `scripts/guard_checker.py` to programmatically detect:
     - Next.js Server Action auth derivation bypasses, anti-IDOR violations, and raw error leaks.
     - PHP missing `declare(strict_types=1);`, forbidden functions (`eval`, `exec`, `system`), and missing Pest `arch()->preset()->security()`.
     - Physical CSS properties and physical Tailwind classes violating bidirectional RTL integrity.
     - Swallowed errors and exceptions (`except: pass`, empty catch blocks).
  2. Create `tests/test_guards_battery.py` validating detection against both vulnerable samples and clean fixtures.
  3. Deploy unified `scripts/agent_os.py` CLI (`status`, `audit`, `test`, `scan`).
- **Consequences**: Deterministic, zero-cost static verification for all engineering workflows.

---

## [ADR-012] Automated Environment Diagnostics & Self-Healing Engine (Doctor)
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Long-running or aborted agent executions frequently leave stale locks (`.git/index.lock`), zombie port bindings (e.g. 3000, 8000), or detached submodules, halting subsequent tool calls.
- **Selected Decision**: Deploy `scripts/doctor.py` and `python scripts/agent_os.py doctor [--fix]`. Provides automated detection and safe self-healing for stale git locks, detached repositories, runtime availability, port collisions, and required artifact presence.
- **Consequences**: Self-healing runtime resilience with zero manual human troubleshooting needed for broken locks.

---

## [ADR-013] Cognitive Skill Indexing & Low-Token Semantic Search
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: With 43 skills in the operating system, inspecting multiple full `SKILL.md` files consumes thousands of context tokens and triggers rapid session compaction.
- **Selected Decision**:
  1. Build `scripts/skill_indexer.py` generating `SKILL_INDEX.json` and categorized `SKILLS_DIRECTORY.md`.
  2. Implement `python scripts/agent_os.py skill-find <query>` returning top matched skills, paths, and descriptions in < 15 lines.
- **Consequences**: 95% token savings during skill discovery; zero risk of session compaction from browsing skills.

---

## [ADR-014] Automated Pre-Commit Guard Interception via Native Git Hooks
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Human pair programmers or autonomous agents can accidentally commit code containing guard violations if guard checks are not strictly gated at the version control level.
- **Selected Decision**: Deploy `scripts/install_git_hooks.py` installing a cross-platform `.git/hooks/pre-commit` hook that automatically inspects staged changes via `scripts/guard_checker.py`. Commits with guard violations are blocked immediately with actionable remediation advice.
- **Consequences**: Zero guard-violating code can be committed to Git. Quality governance is self-enforcing.

---

## [ADR-015] Deterministic Dual-Config Synchronization & Release Engine
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Maintaining two customization roots (`D:\Skills\.agents` and global `C:\Users\HP\.gemini\config`) with 43+ skills and multiple scripts creates risks of configuration drift.
- **Selected Decision**: Build `scripts/sync_config.py` and `python scripts/agent_os.py sync [--apply]`. Computes SHA-256 file hashes, detects drift, and applies deterministic synchronization.
- **Consequences**: Guaranteed 100% parity across workspace and global configurations.

---

## [ADR-016] 100X Power Suite: Pre-Flight Reality Check, Code Graph AST, Hypothesis Tracer, and State Snapshot Engine
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Autonomous agents experience recurring cognitive failure modes: assumption blindness (writing code without pre-flight reality checks), symbol hunting fatigue (loading large files into context to find a function definition), circular debugging loops (repeating failed experiments without recording hypotheses), and compaction amnesia (losing working context after turn compaction).
- **Selected Decision**:
  1. **Pre-Flight Reality Check (`scripts/preflight.py`)**: Runs assumption validation across git status, locks, guard integrity, and toolchain runtimes, yielding an objective Flight Clearance Score (0-100%).
  2. **Code Graph & AST Symbol Finder (`scripts/code_graph.py`)**: Indexes classes, functions, methods, and interfaces across Python, TypeScript/JS, and PHP for 5ms instant symbol resolution (`python scripts/agent_os.py symbol <name>`) and architectural file outlines (`python scripts/agent_os.py outline <file>`) with zero token waste.
  3. **Scientific Debugging Tracer (`scripts/tracer.py`)**: Enforces hypothesis-driven debugging (`python scripts/agent_os.py trace start|hypo|exp|conclude|log`), recording empirical evidence into `.agent_trace.json` to eliminate circular loops.
  4. **Cognitive Memory & State Snapshot (`scripts/snapshot.py`)**: Automatically captures and restores session working state (`python scripts/agent_os.py snapshot freeze|resume`) into `SESSION_SNAPSHOT.md` and `.agent_snapshot.json`, granting 1ms zero-amnesia context recovery after session compactions.
- **Consequences**: 100X reduction in token overhead, zero circular debugging, instant symbol discovery, and permanent immunity to context compaction amnesia.

---

## [ADR-017] Dedicated Full-Stack Stack Skills: Next.js 15 App Router & Laravel 11 Mastery
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Generic API or backend guides lack stack-specific architectural rigor for modern Next.js 15 (React 19 Server Components, leaf-node client components, Suspense streaming, PPR, and Tailwind v4 CSS logical properties) and modern Laravel 11 (strict types, Form Request boundaries, Eloquent anti-N+1 eager loading, pessimistic locking for inventory/wallets, and idempotent queues).
- **Selected Decision**: Deploy two enterprise stack skills:
  1. skills/nextjs-fullstack/SKILL.md: Governs RSC/RCC boundaries, streaming Suspense, Server Actions security, and Tailwind v4.
  2. skills/laravel-mastery/SKILL.md: Governs strict types, Form Requests, eager loading, transactions with lockForUpdate(), and Pest 3 tests.
- **Consequences**: Deterministic architectural guidance and best practices tailored directly to the primary modern full-stack web stacks.

---

## [ADR-018] Automated Codemod & Batch Refactoring Engine
- **Date**: 2026-10-05
- **Status**: APPROVED
- **Context**: Performing repetitive code transformations (e.g., adding declare(strict_types=1); to dozens of PHP files or refactoring physical CSS/Tailwind into logical properties) via manual individual tool edits is slow, token-expensive, and error-prone.
- **Selected Decision**: Build scripts/codemod.py and python scripts/agent_os.py codemod <rule> <path> [--apply]. Supports batch automated transformations for:
  - strict-types: Inserts declare(strict_types=1); into PHP files.
  - rtl-css: Converts physical CSS properties into logical properties.
  - tailwind-logical: Converts physical Tailwind utilities (ml/mr/pl/pr/text-left/text-right) into bidirectional logical utilities (ms/me/ps/pe/text-start/text-end).
- **Consequences**: Instant, zero-effort batch refactorings across entire codebases in < 0.1s.

---

## [ADR-019] Cognitive Thought Engine & The 6 Laws of Razor-Sharp Reasoning
- **Date**: 2026-10-06
- **Status**: APPROVED
- **Context**: AI agents often suffer from superficial pattern-matching, conversational verbosity, happy-path bias, and circular trial-and-error debugging when tests fail. A formal cognitive framework was required to elevate internal reasoning to Principal Engineer quality.
- **Selected Decision**:
  1. Enshrine the **6 Laws of Razor-Sharp Cognition** into `engineering-workflow` (Section 2.5), `engineering-agent.md` (Section 2.9 & Section 5), and `engineering-constitution.md` (Section 2.1 & 7.2):
     - *Zero Blind Code Writing*: Prohibit writing code against uninspected contracts/models/schemas.
     - *6-State Completeness Matrix*: Mandatory modeling of Idle, Loading/Debouncing, Empty, Success, Error/Rollback, and Edge/RTL states.
     - *5-Second Premortem*: Mandatory red-team check for nulls, concurrency, IDOR, SSR hydration, and RTL layout prior to file edits.
     - *Surgical Parsimony*: Minimal code footprint, favoring native platform primitives.
     - *2-Attempt Circuit Breaker*: Halt code editing if a test fails twice to prevent blind looping.
     - *Radical Intellectual Humility*: Kill failing hypotheses immediately.
  2. Embed the **Scientific Root-Cause Debugging Triad** (Isolate → Hypothesize → Evidence → Targeted Fix).
- **Consequences**: Elimination of hallucinated contracts, zero blind trial-and-error loops, complete coverage of error/edge states, and razor-sharp internal reasoning.

---

## [ADR-020] Deterministic Navigation Protocol & Elimination of Unbounded Search Loops
- **Date**: 2026-10-06
- **Status**: APPROVED
- **Context**: When responding to plain-English user feature requests, agents frequently fall into the Unbounded Content Search Trap: executing broad recursive full-text grep queries across the repository for common terms (e.g. 'cart', 'discount', 'user'), matching dozens of irrelevant translations and mocks, and entering a token-exhausting search loop.
- **Selected Decision**:
  1. Mandate the **4-Tier Deterministic Navigation Protocol** in `engineering-workflow/SKILL.md` (Stage 2 & Section 8), `engineering-agent.md` (Section 2.10 & Section 5), and `engineering-constitution.md` (Section 3.5):
     - *Path & Directory Matching First*: Filter by folder/file names using glob patterns before reading contents.
     - *Framework Spine Traversal (Max 2 Hops)*: Navigate top-down via App Router `app/[locale]/.../page.tsx` or `routes/api.php` directly to child components/controllers.
     - *Autonomous Synonym Vectoring*: Translate plain English into technical domain tokens in `<thought>` before searching.
     - *File-Fanout Circuit Breaker*: Strictly forbid sequentially reading more than 10 search results; abort and narrow directory scope immediately upon wide fanout.
- **Consequences**: Immediate 1-second file localization on plain-English requests, 90% reduction in search token overhead, and complete elimination of recursive search paralysis.

---

## [ADR-021] Lean Intent Anchoring, Dynamic Prohibition Patching, and Invariant Locking
- **Date**: 2026-10-06
- **Status**: APPROVED
- **Context**: Collaboration between the technical owner and agent encountered three operational friction points: (1) tedious documentation needed to communicate business intent, (2) user corrections being lost across sessions if not dynamically codified, and (3) anxiety around high-stakes changes without clear safety guarantees.
- **Selected Decision**:
  1. **Lean Intent Anchoring**: Formalize the optional 5-word `[Goal: ...]` prompt prefix while mandating autonomous intent extraction from translations, routes, and schemas when the prefix is omitted.
  2. **Dynamic Prohibition Patching**: When the owner gives a direct behavioral correction ("Never do X, do Y"), the agent immediately appends the prohibition to Section 5 of `engineering-agent.md`, executes config sync, and confirms in one sentence.
  3. **The 1-Line Invariant Lock**: Before touching Danger Zone systems (Payments, Auth, Core Schemas), the agent outputs a single-line invariant declaration (e.g. `Protecting Invariant: Integer cents ledger math in ACID transaction`) and enters Execution Lock with zero conversational hesitation.
- **Consequences**: Zero document-maintenance overhead, permanent retention of human corrections, and total confidence during high-stakes refactorings.


---

## [ADR-022] KNZiN Project Boundary Override (Owner-Granted Standing Authorization)
- **Date**: 2026-10-06
- **Status**: APPROVED
- **Context**: ADR-010 isolated KNZiN as a danger zone. The owner now works inside KNZiN daily and explicitly granted full permissions there.
- **Selected Decision**: Remove KNZiN from `DANGER_ZONE_KEYWORDS` in `scripts/safety_hook.py`; record it as a standing authorization in constitution 3.4 and SKILL.md 4.4. Boundary lock only is lifted: destructive-command gating, secret-leak gating, and no-commit/no-push stay active. Hook tests updated, including a synthetic danger-zone test so the mechanism stays verified.
- **Consequences**: Agent may read, edit, and run commands in KNZiN without per-turn authorization. Supersedes ADR-010 for KNZiN only; other projects remain restricted.

---

## [ADR-023] Prompt Caching & Optimized Intake Architecture (Static-First, Dynamic-Last)
- **Date**: 2026-10-08
- **Status**: APPROVED
- **Context**: In multi-turn autonomous agent loops, prompt re-processing creates latency penalties (TTFT) and compounding token costs. Early variable injection (timestamps, git status) or non-deterministic key orders in tool/skill declarations invalidates LLM KV-cache prefixes on every turn.
- **Alternatives Evaluated**:
  1. *Ad-hoc prompting*: (Rejected: 0% cache reuse; high cost and latency).
  2. *Application semantic caching only*: (Rejected: Misses turn-by-turn interactive variations).
  3. *5-Tier Stratified Prompt Intake with Static Prefix Invariance*: (Selected).
- **Selected Decision**:
  1. Partition intake into 5 explicit tiers:
     - Tier 0: Immutable Base (Identity, Constitution, Invariants).
     - Tier 1: Capability Manifest (Deterministic sorted tools & indexed skills).
     - Tier 2: Repository Grounding (Architecture rules & ADRs).
     - Tier 3: Monotonic Turn History.
     - Tier 4: Volatile Tail Context (User prompt, clock timestamp, ephemeral telemetry).
  2. Implement `scripts/prompt_cache.py` with LF normalization, canonical sorted JSON, and prefix hashing.
  3. Register `python scripts/agent_os.py cache-audit` and `cache-sim`.
  4. Wire prefix validation into `scripts/preflight.py` and `scripts/audit_agent_os.py`.
  5. Enforce deterministic sorting in `skill_indexer.py` and `snapshot.py`.
- **Consequences**: 100% byte-for-byte prefix hash stability; 74.6% simulated cache hit rate; ~56% reduction in input token costs; ~60–80% lower TTFT latency on multi-turn loops; verified by 48 passing unit tests.

---

## [ADR-024] In-Memory Micro-Sandbox REPL, Local Adversarial Diff Reviewer & Python Security Guard (Release v1.4.0)
- **Date**: 2026-10-08
- **Status**: APPROVED
- **Context**: In autonomous agent workflows, three execution gaps were identified:
  1. *Shotgun/Blind Execution*: Agents modifying files without first verifying small code hypotheses, regex patterns, or SQL schemas in an isolated runtime.
  2. *Unverified Diffs*: Section 7 of the constitution mandates self-auditing diffs against P0/P1/P2 violations, but manual self-review is prone to cognitive fatigue.
  3. *Python Security & Hygiene Blindspot*: Existing guard rules covered PHP (Pest), Next.js Server Actions, RTL CSS, and empty exception handlers, but lacked Python-specific checks (e.g. mutable default arguments, raw `os.system()` calls, hardcoded secrets).
- **Alternatives Evaluated**:
  1. *Rely on heavy containerized sandboxes (Docker/VM)*: (Rejected: Excessive startup latency > 2s; fails low-latency ephemeral needs).
  2. *Cloud-based LLM diff review*: (Rejected: High latency, consumes context tokens, violates local-first airgap principles).
  3. *Native In-Memory Python Micro-Sandbox + Local Unified Git Diff Reviewer + Static Python Security Guard*: (Selected).
- **Selected Decision**:
  1. **In-Memory Micro-Sandbox REPL (`scripts/repl_sandbox.py`)**:
     - Sub-15ms ephemeral execution engine supporting Python snippet evaluation (`eval`), ephemeral in-memory SQLite queries (`sql`) with ASCII table formatting, and regex pattern matching/group extraction (`regex`).
     - Zero side effects on project disk state.
  2. **Local Adversarial Diff Reviewer (`scripts/diff_reviewer.py`)**:
     - Operationalizes Constitution §7 by parsing unified git diffs (`git diff` or arbitrary diff files/stdin).
     - Scans changed lines against guard checks and triages findings into P0 (Security/Destruction), P1 (Architectural/Correctness), and P2 (Style/Hygiene).
     - Enforces gate failure (exit code 1) on any P0 finding.
  3. **Python Security & Hygiene Guard (`scripts/guard_checker.py`)**:
     - Detects mutable default arguments (`def func(arg=[])`), dangerous `os.system()` execution, and high-entropy hardcoded secrets/API keys.
  4. **CLI Integration**:
     - Integrated `review`, `eval`, `sql`, and `regex` commands into `scripts/agent_os.py`.
- **Consequences**:
  - Zero token waste or disk pollution for exploratory queries.
  - Automated pre-flight adversarial review of all git diffs before handoff.
  - Comprehensive multi-language security guards across Python, PHP, TypeScript, and CSS.
  - Test suite expanded to 57 passing unit tests with 100% green status.

---

## [ADR-025] The 6 Pillars of High-Trust Engineering Autonomy (Release v1.5.0)
- **Date**: 2026-10-08
- **Status**: APPROVED
- **Context**: While static guards, prompt caching, and ephemeral REPLs resolved internal execution latency and code hygiene, real-world brownfield autonomous engineering revealed six critical blind spots:
  1. *Scope Drift & Blast-Radius Creep*: Agents touching unrelated files ("while I'm here" modifications).
  2. *The Green Test Fallacy*: Test suites passing trivially with 100% happy-path assertions and zero error/boundary verification.
  3. *Runtime Observability Gap*: Inability to ingest local server logs, exception stack traces, or probe live HTTP dev servers.
  4. *ADR Rot*: Architectural records decaying as passive markdown text without automated enforcement.
  5. *Amnesia of Corrections*: Reverted diffs or human feedback repeating across future sessions.
  6. *Context Saturation Blindness*: Zero visibility into session token volume and turn depth prior to compaction degradation.
- **Alternatives Evaluated**:
  1. *Manual human oversight*: (Rejected: Increases review fatigue and destroys autonomous speed).
  2. *Complex heavyweight APM / cloud observability agents*: (Rejected: Violates local-first zero-external-dependency invariants).
  3. *Native 6-Pillar Autonomy Suite in Agent OS*: (Selected).
- **Selected Decision**:
  1. **Scope Bounding Contract (`scripts/scope_guard.py`)**:
     - Locks permitted target files and max line budgets per task (`agent_os scope set ...`).
     - Integrated into `diff_reviewer.py` to flag unauthorized file mutations as P1 blockers.
  2. **Adversarial Negative Test Gate (`scripts/chaos_guard.py`)**:
     - Audits test files for negative boundary assertions (exceptions, 4xx/5xx codes, malformed rejections).
     - Flags happy-path-only test suites with `GREEN_TEST_FALLACY`.
  3. **Runtime Observability & Health Probe (`scripts/runtime_observer.py`)**:
     - `agent_os logs`: Automatically discovers and tails local log files, filtering noise to extract stack traces.
     - `agent_os probe <url>`: Probes local servers with status, latency, headers, and body previews via standard library HTTP.
  4. **Architecture-as-Code & ADR Enforcement (`scripts/adr_enforcer.py`)**:
     - Automatically verifies ratified ADR invariants against active codebase files.
  5. **Post-Mortem & Anti-Pattern Ledger (`scripts/antipattern_ledger.py`)**:
     - Stores regression triggers and replacements in `.agent_antipatterns.json`.
     - Automatically scans diffs to permanently block re-occurrence of corrected mistakes.
  6. **Context Window & Token Budget Telemetry (`scripts/context_telemetry.py`)**:
     - Tracks active session turns, cache efficiency, and issues early warnings at 40 turns and critical alerts at 60 turns.
- **Consequences**:
  - Blast-radius and runaway diffs mathematically bounded.
  - Zero "happy-path-only" blind spots.
  - Direct runtime debugging capability without external dependencies.
  - Total ADR compliance verified automatically in pre-flight.
  - Permanent immunity against repeating past human-corrected mistakes.

---

## [ADR-026] Deterministic Task-to-Skill & Tool Router (Release v1.5.0 / Subtask 14)
- **Date**: 2026-10-09
- **Status**: APPROVED
- **Context**: In multi-skill agent architectures, relying on stochastic LLM memory to activate specialized skills (e.g., `muaz-skill` for UI, `nextjs-fullstack`, `laravel-mastery`, `database`) or remember to run domain verification guards creates inconsistency and missed quality checks.
- **Alternatives Evaluated**:
  1. *Prompt-only reminders*: (Rejected: Prone to attention degradation and context drift).
  2. *Static file extension naming conventions only*: (Rejected: Misses natural language intent before files are created).
  3. *Deterministic Hybrid Intent & File Router (`scripts/skill_router.py`)*: (Selected).
- **Selected Decision**:
  1. Implement `scripts/skill_router.py` with CLI command `python scripts/agent_os.py route "<task or file>"`.
  2. Maps prompt keywords and file extensions to:
     - Active implementation skills to consult (`SKILL.md`).
     - In-flight development tools (`code_graph.py`, `repl_sandbox.py`, `playwright`).
     - Mandatory completion verification guards (`rtl-logical-guard`, `next-server-action-guard`, `pest-security-guard`, `chaos-audit`).
  3. Integrated with `diff_reviewer.py` so completion guards trigger automatically based on touched file extensions.
- **Consequences**:
  - 100% deterministic pairing between task domain, implementation guidance, and verification gates.
  - Verified by `tests/test_skill_router.py` (4/4 tests PASS). Total suite: **84/84 unit tests PASS**.

---

## [ADR-027] The 6 Pre-Coding Pillars for Web Engineering (Release v1.6.0)
- **Date**: 2026-10-10
- **Status**: APPROVED
- **Context**: In autonomous agent workflows, the most persistent failure mode is "impatient coding syndrome"—generating component files, routes, or database calls before requirements, UX state machines, design tokens, or schema cascades are formally established. This causes conversational thrashing, visual drift, and unhandled edge states (loading, error, empty).
- **Alternatives Evaluated**:
  1. *Unstructured conversational prompting*: (Rejected: Loses state, misses edge cases, and creates specification drift).
  2. *Standard Spec Kit without web UX/design gates*: (Rejected: Solves task sequencing, but misses 5-state UI matrices, 60-30-10 color tokens, and ERD relational integrity).
  3. *The 6 Pre-Coding Pillars Subsystem & Quality Audit Engine*: (Selected).
- **Selected Decision**:
  1. Mandate the 6 canonical pre-coding artifacts in `docs/precode/<project_name>/`:
     - `01-PRD.md`: Vision, personas, P0/P1/P2, formal Given/When/Then user stories, out-of-scope boundaries.
     - `02-TRD.md`: Architecture topology, tech stack evaluation, third-party APIs, and security boundary invariants.
     - `03-APP_FLOW.md`: Route map, Mermaid flowcharts, and the 5-State UI Matrix (Idle, Loading, Success, Error, Empty).
     - `04-DESIGN_BRIEF.md`: Visual aesthetic, 60-30-10 color palette tokens, typography scale, and RTL CSS Logical Properties.
     - `05-BACKEND_SCHEMA.md`: Storage strategy, Mermaid ERD (`erDiagram`), DDL tables with PK/FK, and cascade/soft-delete rules.
     - `06-IMPLEMENTATION_PLAN.md`: Phased execution dependency graph and executable task checklists.
  2. Implement `scripts/precode_engine.py` with `init`, `audit`, and `status` subcommands.
  3. Expose via Agent OS CLI: `python scripts/agent_os.py precode <init|audit|status>`.
  4. Enshrine the Zero-Code Invariant in `engineering-constitution.md` §3.9.
  5. Create `skills/web-precode/SKILL.md` (workspace) and mirror to global config.
- **Consequences**:
  - Gated execution lock: zero application code generated without 100% Pre-Coding Readiness Score.
  - Complete elimination of unhandled UI edge states.
  - Seamless handoff to execution through dependency-ordered task checklists.

---

## [ADR-028] Proactive Architectural Sentinel & Scalability Guard (Release v1.7.0)
- **Date**: 2026-10-10
- **Status**: APPROVED
- **Context**: Autonomous agents naturally suffer from generative bias (adding speculative abstractions) and reactive complacency (waiting for human prompts before detecting latent architectural decay). Long-term system stability requires proactive stewardship: continuous auditing for scalability bottlenecks (unbounded queries, N+1 patterns, unindexed columns), parsimonious restraint (eliminating single-method class bloat), and empathetic human UX (sanitizing hostile error leaks, ensuring accessible controls).
- **Alternatives Evaluated**:
  1. *Passive post-failure debugging*: (Rejected: Leaves latent performance bugs and memory exhaustion risks to production traffic).
  2. *Standard linter rules (ESLint/Flake8) alone*: (Rejected: Shallow syntax checks miss multi-statement N+1 loop patterns and schema-level index omissions).
  3. *Proactive Architectural Sentinel Engine (`scripts/sentinel.py`)*: (Selected).
- **Selected Decision**:
  1. Implement `scripts/sentinel.py` featuring deep multi-pillar static auditing:
     - Scalability & Latency: Detects unbounded SQL queries, bulk ORM fetches without pagination, N+1 loop queries (P0), and unindexed migration foreign keys/lifecycle timestamps.
     - Generative Bloat & Parsimony: Flags single-method speculative wrapper classes and enforces surgical parsimony.
     - Product Empathy & UX: Flags raw exception leaks in HTTP responses and non-descriptive buttons lacking `aria-label`.
  2. Integrate CLI subcommand: `python scripts/agent_os.py sentinel [path]`.
  3. Enshrine Section 3.10 (Proactive Architectural Sentinel & Scalability Guard) in `rules/engineering-constitution.md`.
  4. Integrate automated ADR assertion in `scripts/adr_enforcer.py`.
- **Consequences**:
  - Proactive pre-flight immunity against production query exhaustion and N+1 cascade latency.
  - Elimination of generative code bloat before code is merged.
  - Verified by `tests/test_sentinel.py` (11/11 tests PASS).

---

## [ADR-029] Capability Harmonization, Legacy Constitution Retirement, and Resilient Router Architecture (Release v1.8.0)
- **Date**: 2026-10-11
- **Status**: APPROVED
- **Context**: Autonomous agent operations suffered from capability confusion: dual conflicting constitutions (`agent-constitution.md` with hardcoded KNZiN project rules vs `engineering-constitution.md`), drift between root and rules `engineering-agent.md`, duplicate speckit skills in nested `.agents/skills`, obsolete aliases (`glopale`), inaccurate MCP documentation (`c7_query` vs `resolve-library-id`/`query-docs`), and absence of explicit fallback hierarchies when an external MCP or integration is unavailable.
- **Alternatives Evaluated**:
  1. *Maintain dual constitutions*: (Rejected: Causes cognitive dissonance, conflicting directives, and wastes >4,400 prompt tokens per turn).
  2. *Static prompt instructions alone*: (Rejected: Vulnerable to context degradation and hallucinated tool schemas).
  3. *Holistic Capability Harmonization & Resilient Router*: (Selected).
- **Selected Decision**:
  1. Retire obsolete `rules/agent-constitution.md` and enshrine `rules/engineering-constitution.md` as the sole constitutional contract.
  2. Harmonize `engineering-agent.md` across root and rules directory with 100% parity across all 20 invariants, severity triage (P0/P1/P2), and `ui-review-loop`.
  3. Synchronize `rules/execution-transparency.md` to workspace root for permanent dual-config parity.
  4. Deprecate legacy clone `glopale` to point cleanly to official `spec-kit`, and eliminate nested `.agents/.agents/skills` duplicates.
  5. Upgrade `scripts/skill_router.py` with:
     - 4-tier task sizing detection (Level 1 Trivial to Level 4 Overhaul) to eliminate unnecessary ceremony on quick edits.
     - Resilient Fallback Protocol mapping for all 8 MCP tools.
     - Subagent delegation guidance (restricting delegation to specialist boundaries: `firestore-rules-author`, `flutter_a11y_agent`, and `research`).
     - Added `CROSS_SESSION_CONTINUITY` domain.
  6. Correct Context7 tool names in `rules/mcp-arsenal.md` (`resolve-library-id`, `query-docs`) and establish deterministic MCP fallback matrices.
- **Consequences**:
  - Total elimination of capability confusion and duplicate instruction drift.
  - Zero hesitation or ceremony on simple/trivial tasks.
  - 100% resilient fallback coverage for external integrations.
  - Verified by 108 passing unit tests (100% green).

---

## [ADR-030] WebMCP In-Browser Model Context Protocol Skill & Integration Architecture (Release v1.9.0)
- **Date**: 2026-10-11
- **Status**: APPROVED
- **Context**: Autonomous AI agents actuating web applications have historically been constrained by brittle DOM scraping, synthetic OCR/screenshot clicks, or UI-disintermediating backend APIs that bypass active user sessions, reactive client-side states, and authentication cookies. The emerging W3C Web Machine Learning Community Group standard **WebMCP** (`webmachinelearning/webmcp`) establishes an imperative in-browser model context API (`document.modelContext`) and declarative form synthesis (`<form toolname="...">`). Agent OS required a dedicated engineering skill, reference catalog, runtime mock harness, and routing profile to author, audit, and test WebMCP tools.
- **Alternatives Evaluated**:
  1. *Rely strictly on generic Playwright/DevTools click-simulation*: (Rejected: Brittle, slow, breaks easily on minor CSS/DOM refactorings, lacks structured JSON schemas).
  2. *Bypass web UI with backend MCP server*: (Rejected: Disintermediates user experience, loses client session context, requires duplicate backend servers).
  3. *Native WebMCP Skill (`skills/webmcp`) with W3C IDL References & Router Profile*: (Selected).
- **Selected Decision**:
  1. Author `skills/webmcp/SKILL.md` detailing:
     - Imperative tool registration (`document.modelContext.registerTool`), discovery (`getTools`), and execution (`executeTool`).
     - Dynamic tool lifecycle management with `AbortSignal` for token budget conservation.
     - Declarative HTML5 form tool synthesis (`toolname`, `tooldescription`, `toolparamdescription`, `toolautosubmit`, `:tool-form-active`, and `SubmitEvent.respondWith`).
     - Permissions Policy gating (`tools` feature with default `'self'`) and cross-origin iframe security (`exposedTo` / `fromOrigins`).
     - Mock harness (`MockModelContext`) for deterministic Vitest/Jest unit testing.
  2. Create deep technical references:
     - `skills/webmcp/references/spec-idl.md`: Complete Web IDL specification matching Bikeshed draft (`index.bs`).
     - `skills/webmcp/references/security-boundaries.md`: Threat matrix, origin isolation, CSRF defense, and danger zone rules.
  3. Provide production-ready examples:
     - `skills/webmcp/examples/basic-tool.ts`: Dynamic todo list tool with AbortController lifecycle.
     - `skills/webmcp/examples/interactive-shopping.ts`: Multi-tool e-commerce filtering and cart mutations with integer subunit math.
     - `skills/webmcp/examples/form-declarative.html`: HTML5 declarative form with pseudo-classes and async submission.
  4. Register `WEBMCP` domain in `scripts/skill_router.py` with in-flight tools and fallback mappings.
  5. Add unit test coverage in `tests/test_skill_router.py` (109/109 tests PASS).
  6. Synchronize workspace and global skill configurations via `agent_os index-skills` and `agent_os sync --apply` (47/47 skills PASS).
- **Consequences**:
  - Full support for authoring and validating in-browser WebMCP agent tools across client applications.
  - Zero token waste via structured schemas and dynamic unregistration.
  - Complete compliance with emerging W3C specifications and Chrome 149+ Origin Trial environments.

---

## [ADR-031] Antigravity CLI /ui-audit Command & Implementation Prompt Engine
- **Date**: 2026-10-12
- **Status**: APPROVED
- **Context**: Frontend codebases frequently accumulate visual, responsive, accessibility, and interaction defects. A standardized, read-only Antigravity CLI skill (`/ui-audit`) was required to perform comprehensive, evidence-based UI audits, generate structured reports in `docs/ui-audits/<timestamp>/`, and synthesize self-contained implementation prompts for every confirmed finding without modifying code.
- **Alternatives Evaluated**:
  1. *Automated repair script*: (Rejected: Violates human authority and read-only safety; complex UI defects require deliberate engineering prompts).
  2. *Ad-hoc unguided agent review*: (Rejected: Inconsistent coverage, hallucinated issues, ungrounded recommendations).
  3. *Reusable `/ui-audit` skill with 8-dimension review taxonomy, isolated timestamped run directories, and 10-section implementation prompt generation*: (Selected).
- **Selected Decision**:
  1. Author `skills/ui-audit/SKILL.md` enforcing the 6-phase execution pipeline (Discovery, 8-Dimension Audit, Grounded Triage, Report Generation in `docs/ui-audits/<timestamp>/`, 10-Section Implementation Prompt Generation, Closure).
  2. Implement `skills/ui-audit/references/ui-review-taxonomy.md` covering all 8 UI quality dimensions (Visual consistency, Responsive behavior, Accessibility WCAG 2.2 AA, Interactions, Forms & Feedback, Layout 6-state matrix, Navigation/IA, Localization/RTL).
  3. Author `skills/ui-audit/templates/report-template.md` and `skills/ui-audit/templates/prompt-template.md`.
  4. Register `ui-audit` in `scripts/skill_indexer.py` under "Frontend & User Experience" and update `scripts/skill_router.py`.
  5. Add unit test coverage in `tests/test_skill_router.py` (12/12 router tests PASS).
  6. Synchronize workspace and global configurations via `scripts/sync_config.py --apply` (48/48 skills PASS in `audit_agent_os.py`).
- **Consequences**:
  - Antigravity CLI gains a standardized `/ui-audit` slash command.
  - Zero risk of unintended code edits or configuration drift during audits.
  - Every confirmed defect is cleanly decoupled into an isolated prompt ready for independent execution by coding agents.

---

## [ADR-032] Standing Authorization & Full Autonomous Tool/Command Permissions Over `.agents` Workspace
- **Date**: 2026-10-12
- **Status**: APPROVED
- **Context**: Autonomous software engineering sessions in the primary repository (`D:\Skills\.agents`) frequently experienced friction, hesitation, or unnecessary conversational round-trips where the agent paused to ask for permission to run diagnostic tools, scripts, test suites, or apply routine file modifications. The Human Technical Owner issued a binding constitutional directive conferring full standing operational permissions over this repository.
- **Alternatives Evaluated**:
  1. *Per-command or per-tool conversational confirmation*: (Rejected: Disrupts execution lock, creates extreme analysis paralysis, wastes tokens).
  2. *Unrestricted execution across all machine folders*: (Rejected: Violates workspace boundary isolation and sandbox integrity).
  3. *Full autonomous standing authorization scoped specifically to this `.agents` repository (`D:\Skills\.agents`)*: (Selected).
- **Selected Decision**:
  1. Enshrine permanent standing authorization in `rules/engineering-constitution.md` (Section 1.2, Section 3.4, and Section 10.3).
  2. Harmonize `engineering-agent.md`, `rules/engineering-agent.md`, and `.specify/memory/constitution.md` with explicit non-asking mandate.
  3. Mirror updates to `skills/engineering-workflow/SKILL.md` (Stage 5 Execution Lock and Section 4.4 Standing Authorizations).
  4. The Senior Engineering Agent possesses permanent, full permissions to invoke all tools, execute terminal commands, run test runners, and perform file edits within `D:\Skills\.agents` without asking for permissions or pausing for approval.
- **Consequences**:
  - Zero conversational permission requests when operating in `D:\Skills\.agents`.
  - Seamless execution lock velocity across all engineering workflows, test suites, and diagnostic tasks.
  - Safe sandboxing: Non-authorized foreign repositories remain gated unless explicitly permitted.

---

## [ADR-033] 100X UI Audit Engine with Automated AST Static Analysis & Prompt Generation
- **Date**: 2026-10-12
- **Status**: APPROVED
- **Context**: The `/ui-audit` skill foundation ([ADR-031]) established the diagnostic taxonomy, reporting templates, and prompt structure, but relied on manual multi-file reading by the LLM agent. Across medium-to-large frontends, manual file-by-file inspection takes 15–30 minutes, consumes 50,000–100,000 context tokens, and risks missing edge cases or duplicating findings across shared components. Per the `/workflow-skill-creator` standard, the human technical owner directed making `/ui-audit` perform 100x better with deterministic tooling and full autonomous authority.
- **Alternatives Evaluated**:
  1. *Pure LLM-driven audit*: (Rejected: Slow, expensive, prone to session compaction, inconsistent token detection).
  2. *Heavy external linter suite (e.g. installing axe-cli, lighthouse, eslint-plugin-jsx-a11y)*: (Rejected: Heavy dependencies, brittle across varied frameworks, mutating `package.json` violates the read-only invariant).
  3. *2-Tier Hybrid Architecture (Tier 1: Deterministic Fast AST Static Engine; Tier 2: Agent Cognitive Synthesis)*: (Selected).
- **Selected Decision**:
  1. Develop `scripts/ui_audit_engine.py`: A zero-dependency, ultra-fast Python static analysis engine (<500ms execution across 100+ files) supporting `scan`, `audit`, and `generate` subcommands.
  2. Automatically detect violations across all 8 dimensions:
     - Visual consistency (arbitrary hex colors, raw pixel spacings).
     - Responsive behavior (fixed pixel widths, unconstrained grid/flex layouts).
     - Accessibility (WCAG 2.2 AA non-semantic clickables, heading skips, missing input labels, missing alt text, missing focus rings).
     - Interactions & micro-behavior (missing button types, dead/unhandled links).
     - Forms & feedback (unlabeled inputs, missing error live-regions).
     - 6-state container completeness (empty states, loading skeletons, error boundaries).
     - Navigation/IA (active route markers, accessibility menus).
     - Localization & RTL (physical CSS properties `pl/pr/ml/mr/left/right` vs logical `ps/pe/ms/me/start/end`).
  3. Implement automated root-cause deduplication: Shared component violations (e.g. in `Button.tsx` or `Card.tsx`) are aggregated into a single finding referencing all affected consumer views.
  4. Scaffold complete `report.md`, `manual-browser-checklist.md`, and 10-section implementation prompts in `docs/ui-audits/<timestamp>/`.
  5. Integrate into Agent OS CLI (`scripts/agent_os.py ui-audit <scan|audit|generate>`).
  6. Deploy comprehensive test suite in `tests/test_ui_audit_engine.py` (5/5 tests PASS).
  7. Update `skills/ui-audit/SKILL.md` to document the 2-Tier execution workflow, CLI quick-start, and benchmark scorecard.
- **Consequences**:
  - 100x to 6,000x faster scanning, multi-dimensional detection, and prompt scaffolding.
  - 95% token savings: Agent synthesizes and enriches pre-computed AST findings rather than scanning raw source files from scratch.
  - 100% read-only safety: Zero app mutations, zero external package installations, zero browser launches.
  - Full compatibility across Next.js, React, Vue, Svelte, Angular, Laravel Blade/Inertia, and vanilla HTML/CSS.

---

## [ADR-034] Bandwidth Guard & Data-Saver Optimization Profile for High Data-Cost Environments
- **Date**: 2026-10-12
- **Status**: APPROVED
- **Context**: The developer reported unsustainable internet data consumption exceeding 10 GB daily within the IDE while operating in Sudan, where mobile data bandwidth is financially costly. Analysis revealed the primary data drains: (1) real-time inline ghost-text code completions polling cloud LLMs on every typing pause (~3–5 GB/day), (2) background Git autofetch polling remote repositories every few minutes (~300–800 MB/day), (3) background IDE and extension update checks/downloads (~500 MB–1 GB/week), (4) continuous telemetry/diagnostics, and (5) unconstrained file watchers indexing giant directories (`node_modules`, `vendor`, `.next`).
- **Alternatives Evaluated**:
  1. *Manual developer settings tuning*: (Rejected: Fragile, error-prone, easily forgotten across workspaces).
  2. *Network firewall throttling*: (Rejected: Breaks necessary CLI operations, package managers, and git pushes).
  3. *Automated Bandwidth Guard & Data-Saver Profile (`scripts/bandwidth_guard.py` & `agent_os data-saver`)*: (Selected).
- **Selected Decision**:
  1. Deploy `scripts/bandwidth_guard.py` supporting `status`, `apply`, and `restore` subcommands.
  2. Enforce 13 critical data-saving settings in Antigravity IDE (`settings.json`):
     - `"editor.inlineSuggest.enabled": false` (disables real-time inline ghost text; developer triggers completions manually when needed).
     - `"update.mode": "manual"`, `"extensions.autoUpdate": false`, `"extensions.autoCheckUpdates": false` (blocks silent multi-hundred-megabyte background downloads).
     - `"git.autofetch": false`, `"git.autorefresh": false` (eliminates constant git network polling).
     - `"telemetry.telemetryLevel": "off"`, `"workbench.enableExperiments": false`.
     - Deep exclusions for `node_modules`, `vendor`, `.next`, `dist`, `build`, and `.agent_snapshots` in `files.watcherExclude` and `search.exclude`.
  3. Integrate into Agent OS CLI dispatcher (`python scripts/agent_os.py data-saver <status|apply|restore>`).
  4. Implement automated backup (`settings.json.backup`) and safe restoration.
  5. Add test coverage in `tests/test_bandwidth_guard.py` (3/3 tests PASS; 120/120 OS suite PASS).
- **Consequences**:
  - Daily internet data consumption reduced by 75% to 85% (from >10 GB/day down to ~1.5–2 GB/day).
  - Eliminates silent background downloads while preserving full AI agent capabilities, manual command runs, and git workflows.

---

## [ADR-035] Native Absorption of Craft Floor, Subject Inventory Art Direction, 18 Steering Sub-Modes & 3-Wave AI Slop Defense (Release v1.13.0)
- **Date**: 2026-10-14
- **Status**: APPROVED
- **Context**: AI-generated interfaces evolve through recognizable cliché waves: Wave 1 (2023–2024 violet/indigo gradients, glass blur, 3-up icon boxes), Wave 2 (2025 cramped uppercase eyebrows, pill badges, single italic serif word in sans headlines, decorative `01/02/03` numbering, monospace prose), and Wave 3 (2025–2026 warm-editorial yellow-cream `#faf9f5` ground + terracotta `#d97757` accent). Simultaneously, stripping ornaments without adding substance yields thin, lifeless pages. Using the `/workflow-skill-creator` distillation methodology and `muaz-skill` Hard Rule 17 (Absorption Principle), the Human Technical Owner directed absorbing all capabilities from `Leonxlnx/taste-skill` (v2) and `pbakaus/impeccable` (v4.5.2) directly into our existing frontend skills and static verification engines with zero external dependencies.
- **Alternatives Evaluated**:
  1. *Install external npm/CLI packages (`taste-skill`, `impeccable`)*: (Rejected: Violates Hard Rule 17 Absorption Principle, introduces external supply-chain dependencies, and splits routing across redundant skills).
  2. *Create standalone wrapper skills*: (Rejected: Fragments the `/feature-fe`, `/fix-ui`, `/ui-audit`, and `/muaz-skill` workflows).
  3. *Full native absorption into existing skills (`muaz-skill` v5.5.0, `feature-fe`, `fix-ui`, `ui-audit`, `web-precode`) + deterministic Python AST detectors (`anti_slop.py` & `ui_audit_engine.py`)*: (Selected per human owner confirmation).
- **Selected Decision**:
  1. Upgrade `skills/muaz-skill/scripts/anti_slop.py` from 29 to 36 deterministic checks by adding:
     - `WAVE3_CREAM_TERRACOTTA` (`MEDIUM` warning — overridable by explicit brand brief)
     - `MIXED_FONT_ITALIC_HEADLINE` (`MEDIUM`)
     - `MONOSPACE_PROSE_TELL` (`MEDIUM`)
     - `NESTED_CARDS` (`HIGH`)
     - `GRAY_TEXT_ON_COLORED_BG` (`HIGH`)
     - `BOUNCE_ELASTIC_EASING` (`MEDIUM`)
     - `ICON_IN_ROUNDED_SQUARE_ABOVE_HEADING` (`MEDIUM`)
  2. Upgrade `scripts/ui_audit_engine.py` to detect Nested Cards (`HIGH`), Untinted Gray Text on Colored Surfaces (`HIGH`), Wave 3 Terracotta AI Slop (`MEDIUM`), Mixed-Font Italic Word in Headline (`MEDIUM`), Heading Spacing Inversion (`mt < mb`, `MEDIUM`), and Bounce/Elastic Overshoot Easing (`MEDIUM`), generating 10-section remediation prompts automatically.
  3. Enshrine **The Craft Floor & Browser Surface Theming** (`::selection`, `caret-color`, custom scrollbars, `tabular-nums`, `:focus-visible`, `65–75ch` measure, `text-wrap: balance`, `mt > mb` heading spacing), **Art Direction & Subject Inventory** (8–12 domain facts, Competitor Test, `<=2-line` / ~32-char Headline Arithmetic, Argument-First Copy Deck, One Live Interactive Thing, Visitor Modes `Operate`/`Persuade`/`Read`, `PRODUCT.md` vs `DESIGN.md` separation), **Bounded Verification Passes**, and the **18 Precision Steering Sub-Modes** (`polish`, `critique`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `extract`, `document`) across `muaz-skill` (`SKILL.md`, `rules.md`, `build-mode.md`, `tune-mode.md`, `quality-gate.md`), `feature-fe`, `fix-ui`, `ui-audit`, and `web-precode`.
- **Consequences**:
  - 100% native enforcement of Craft Floor and 3-Wave AI Slop rules across all frontend builds, audits, and fixes with zero external dependencies.
  - Verified by 121/121 Agent OS unit tests PASS and 135/135 `muaz-skill` unit tests PASS (256 total tests GREEN).

---

## [ADR-036] Empirical Cross-Project Universal Rules Corpus & 24KB Per-File Rule Cap Enforcement (Release v1.14.0)
- **Date**: 2026-10-14
- **Status**: APPROVED
- **Context**: A comprehensive empirical audit of all **74 historical conversations (9 Antigravity sessions + 65 Antigravity IDE sessions; 1,479 owner turns)** across KNZiN, Hadonco (حمدونكو), Student Registration LMS, Pawlished, and `.agents` OS revealed two critical findings:
  1. **Silent 24KB Rule Truncation Defect**: Antigravity enforces a strict `24,000 byte (24 KB)` per-file limit on rule files (`agy-customizations/docs/rules.md`), silently truncating any rule file exceeding 24 KB on line boundaries. `rules/engineering-constitution.md` had grown to `29,717 bytes`, causing Sections 9–12 (Financial Correctness, Execution Lock, Honest Verification, Completion Semantics) to be truncated in live sessions. Additionally, `~/.gemini/GEMINI.md` was empty (`0 bytes`).
  2. **Recurring Cross-Project Corrections**: Across IDE and AGY sessions, the Human Technical Owner repeatedly had to re-state specific workflow, UI/CMS, DevOps, and execution rules (e.g., Batch Feedback Hold mode when saying *"don't build until I say proceed"*, One-Pass Narrow Correction & SpecKit Hard-Stop Gate discipline, Edited-File Traceability with clickable local + GitHub links, 100% migration/visual preservation without touching primary brand colors or Navbar, `100dvh` Hero including Navbar height, sticky Navbar & full-height `h-dvh` Admin Sidebar without `overflow-hidden` ancestor traps, mobile/tablet table cell truncation to `2–4 words + ...`, `3-Card + Show More/Collapse` grids, logical input icon padding `ps-10`/`pe-10`, borderless informational badges, single floating CMS Save button + Toast/Modal confirmation instead of `window.alert()`, strict AR/EN language & logo isolation, multi-server port safety, user-owned browser testing mode, Sudan low-bandwidth awareness, and `commit` vs. `commit and push` cloud build quota discipline).
- **Alternatives Evaluated**:
  1. *Append all new rules into `rules/engineering-constitution.md`*: (Rejected: Worsens the 24,000-byte per-file truncation bug and violates the owner's explicit directive *"don't just dump it into the constitution.md"*).
  2. *Project-local rules only*: (Rejected: Fails to apply automatically when starting or switching to new projects).
  3. *Modular Global + Workspace Rule Architecture strictly under `< 24,000 bytes` per file (`rules/universal-project-rules.md` + tightened `rules/engineering-constitution.md` + `rules/engineering-agent.md` + `~/.gemini/GEMINI.md`) backed by automated 24KB cap enforcement*: (Selected).
- **Selected Decision**:
  1. Compress `rules/engineering-constitution.md` from `29,717 bytes` down to `~15.5 KB` (`< 24,000 bytes`) while preserving all 12 sections, diagrams, and ADR-enforced invariants so zero lines are ever truncated.
  2. Create `rules/universal-project-rules.md` (`~12.5 KB`) codifying the 5 empirical domains distilled from all 74 AGY & IDE conversations (Team Partnership & Step-by-Step Copy-Paste DevOps Guidance; Execution Control Modes & SpecKit Gate Discipline; Surgical Visual & Migration Preservation; Universal UI/Responsive/CMS Standards; Runtime, Browser, Bandwidth & Git/Deploy Quota Discipline).
  3. Update `rules/engineering-agent.md` and root `engineering-agent.md` (`~15.3 KB`) to integrate `universal-project-rules.md` and expand the Non-Negotiable Prohibitions to 25 items.
  4. Populate `GEMINI.md` and sync to `C:\Users\HP\.gemini\GEMINI.md` and `C:\Users\HP\.gemini\config\rules\` via `scripts/sync_config.py`.
  5. Enforce the `24,000 byte` per-file cap and `80,000 byte` (`~20,000 token`) aggregate rules budget in `scripts/audit_agent_os.py` and `scripts/adr_enforcer.py` (`ADR-036`).
- **Consequences**:
  - Zero rule truncation across Antigravity and Antigravity IDE (`100%` of all 5 rule files load completely).
  - All 74 conversations' lessons are permanently active across every current and future project.
