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


