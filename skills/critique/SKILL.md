---
name: critique
description: >-
  Adversarial Draft Self-Review & Gap Auditor ("Treat Your Previous Response as a Draft That May Be Wrong").
  Activates via /critique or automatically before presenting any Level 3-4 engineering plan, specification, or architectural proposal.
  Audits drafts against codebase truth, hidden Backend/Database blast radius, accidental UI/navigation deletions,
  missing 6-state matrix coverage, over-engineering, and parallel-tab file collisions.
compatibility: Platform-agnostic. Operates on plans, specs, Pre-Code docs, and implementation diffs.
---

# Adversarial Draft Self-Review & Gap Auditor (`SKILL.md`)

## 1. Purpose & Core Mandate
Act as an **Independent Senior Principal Reviewer & Adversarial Critic**.

**Treat the current plan, specification, or draft response as a draft that may be wrong.** Do not assume it is correct, complete, or well-designed simply because you produced it. Before endorsing or executing it, subject it to a rigorous 7-Point Adversarial Audit backed by real repository evidence.

---

## 2. The 7-Point Adversarial Audit Checklist

Verify every item below against the real codebase (never from memory):

1. **Epistemic Truth & `"I Don't Know"` Check**:
   - Which file paths, route names, API payloads, or database columns in this draft were assumed rather than inspected?
   - If any symbol or schema column was not verified via `read_file` or `agent_os.py symbol/outline`, inspect it now or flag it as `"I don't know — requires verification"`.
2. **Frontend-to-Backend/DB Completeness**:
   - Did the draft treat a full-stack requirement as a superficial UI-only tweak?
   - Trace the full authority chain: `UI Component -> API Endpoint / Server Action -> Validation & Auth/RBAC Scoping -> Database Column/Migration & Index`.
   - Are admin dashboard controls wired to real database persistence that the public UI actually reads?
3. **`"Do-Not-Remove"` Regression Audit**:
   - Does the draft risk deleting or hiding existing navigation links (e.g., Admin Panel link, Profile sign-out, PWA install link, mobile bottom-bar items, footer blocks) or breaking `Light`/`Dark` theme contrast?
4. **The 6-State Completeness Matrix**:
   - Does the plan explicitly handle: **1) Idle, 2) Loading/In-Flight, 3) Empty/Zero-State, 4) Success/Toast, 5) Error/Validation, and 6) RTL/LTR & Mobile/Desktop Responsive Boundaries**?
5. **Simplicity & Anti-Bloat Check (Karpathy Law 2)**:
   - Does the draft introduce unnecessary abstractions, extra dependencies, or complex patterns where a simpler brownfield extension (`Reuse -> Extend -> Introduce New`) works?
6. **Security & Financial/Data Integrity**:
   - Are `user_id`/`role` derived strictly server-side (Anti-IDOR)? Are financial values using integer subunits or `DECIMAL` (Zero-Float)? Are multi-table writes wrapped in ACID transactions?
7. **Parallel-Tab Collision Check**:
   - Did `git status --short` reveal dirty files currently being edited by another Antigravity tab? Does this plan avoid colliding with those files?
8. **Contradiction & Locked-Decision Audit**:
   - Does any part of this draft contradict settled decisions in `SESSION_SNAPSHOT.md` (`Locked Owner Decisions`), ratified ADRs in `DECISIONS.md`, or conflict with another requirement in the same prompt?

---

## 3. Required Output Format

Present the review concisely using this structure:

1. **Verdict & Flaws Found**: Direct bullet list of what was wrong, missing, risky, or unverified in the draft (lead with the conclusion).
2. **3-Layer Corrections Applied (`UI | Backend API | DB Schema`)**: Exact adjustments made to close every gap.
3. **Locked Preservation Guarantee**: Explicit confirmation of existing UI/nav elements and parallel-tab files that are protected from modification.
4. **Decision / Next Step**: If any business rule remains ambiguous, open the **`ask_question` Dialog Box** immediately; otherwise present the corrected, execution-ready plan and wait for `"proceed"`.
