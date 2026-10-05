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



