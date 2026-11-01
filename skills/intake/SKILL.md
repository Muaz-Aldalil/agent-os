---
name: intake
description: >-
  Dialog-First Smart Intake, Full-Stack Impact Translator & Do-Not-Remove Lock Gate.
  Activates on any new feature request, multi-part UI adjustment, or ambiguous instruction.
  Inspects the codebase in Read-Only mode first, checks for parallel Antigravity tab collisions,
  translates Frontend/UI requests into a 3-Layer Impact Map (UI + Backend API + Database Schema),
  lists existing UI/navigation elements that must NOT be removed, and opens the interactive
  ask_question Dialog Box with plain-product-language options and a final execution-mode selector.
compatibility: Platform-agnostic. Designed for Frontend-led Product Owners building full-stack applications.
---

# Dialog-First Smart Intake & Full-Stack Impact Translator (`SKILL.md`)

## 1. Purpose & Core Mandate
This skill eliminates premature coding, long text walls of questions, accidental deletion of existing UI/navigation elements, and missed Backend/Database impacts when the Owner describes features from a Frontend/UI perspective.

**Never write application code on Turn 1 when ambiguities, multi-part adjustments, or cross-layer impacts exist.** Instead, execute this 4-step Read-Only Intake cycle and collect all decisions via the interactive **`ask_question` Dialog Box**.

---

## 2. The 4-Step Turn-1 Intake Protocol (Read-Only)

### Step 1 — Read-Only Codebase, Parallel-Tab & Locked-Decision Inspection
1. **Parallel-Tab Collision Check**:
   - Run `git status --short` before inspecting or planning.
   - If modified or untracked files exist from another active Antigravity tab, list them explicitly and ensure your planned scope does not overwrite active work in another tab.
2. **Locked-Decision Pre-Check (Zero Repeat Questions)**:
   - Check `SESSION_SNAPSHOT.md` (`Locked Owner Decisions`) and `DECISIONS.md` first so you **never** re-ask a question the Owner already settled.
3. **Target Component & Route Spine Inspection**:
   - Inspect the actual target routes, components, API endpoints, and database models (`python D:\Skills\.agents\scripts\agent_os.py symbol <Name>` or `outline <file>`).
   - If any fact is missing or unverified, state **`"I don't know"`**—never guess.

### Step 2 — The 3-Layer Full-Stack Impact Map (`UI -> API -> DB`) & Canonical Domain Lexicon
Because the Owner focuses on Frontend/UI and relies on the Agent to own Backend and Database architecture, translate every UI request into a compact **3-Layer Impact Table** plus a **Canonical Domain Lexicon** row (preventing synonym drift between UI labels, API JSON keys, and DB columns):

| Layer | Impacted Files / Endpoints / Tables | What Changes |
| :--- | :--- | :--- |
| **1. Frontend / UI** | Exact components, routes, and responsive/theme states (`Light`/`Dark`, `Desktop`/`Mobile`, `AR`/`EN`) | Visual, interaction, and state changes requested by the Owner. |
| **2. Backend / API** | Controllers, Server Actions, Routes, Validation, Auth/RBAC scoping | New or updated API payloads, filters, permissions, or background jobs required to power the UI. |
| **3. Database / Schema** | Tables, columns, foreign keys, indexes, migrations | Any schema additions, relations, or data backfills needed so the UI persists real database truth. |
| **4. Domain Lexicon** | Canonical Entity & Status Names | Exact terms locked across UI, API, and DB (e.g., `Entry` vs `Ticket`, `Participant` vs `User`). |

### Step 3 — Explicit `"Do-Not-Remove / Keep-Intact"` Lock List & YAGNI/KISS Challenge
1. **`"Do-Not-Remove"` Lock List**:
   - Before proposing changes to any existing page, navbar, sidebar, card, or footer, inventory the existing sibling elements in that component and print a **"Do-Not-Remove Lock List"** (e.g., Admin Panel link, Profile actions, language/theme toggles, footer sections, mobile bottom-nav items) that will remain 100% untouched.
2. **Proactive YAGNI / KISS Challenge**:
   - If any part of the request adds unnecessary complexity, duplicates an existing component/table, or can be achieved 3x simpler by extending an existing pattern, state the simpler option in 1–2 lines before opening the dialog.

### Step 4 — Interactive Decision-Tree Dialog Box (`ask_question` Tool)
Immediately invoke the **`ask_question`** tool (interactive modal dialog) to resolve all missing context, edge cases, and business rules in one fast pass:
1. **Upstream-First Decision-Tree Order**: Ask upstream entity/ownership/source-of-truth questions first (which prune downstream branches) before asking UI column/badge questions.
2. **`(Recommended)` First**: Start every question with the strongest engineering/UX recommendation prefixed with `(Recommended)`.
3. **Plain Product Language for Backend/DB Rules**: Never ask backend/database questions using raw SQL or low-level jargon. Frame every Backend/DB question in plain product/business terms (e.g., *"Can one course belong to multiple filter tabs at the same time, or only one?"* instead of *"Should we use a many-to-many pivot table or a nullable FK?"*).
4. **Confirm the `"Do-Not-Remove"` Lock List**: Include a question or option verifying that all existing sibling links/sections not mentioned for removal must stay intact.
5. **Mandatory Final Question — Next Execution Mode**:
   Always include this final question in the `ask_question` modal:
   - **Question**: *"After this dialog, how should I proceed?"*
   - **Options**:
     - `(Recommended) Present the Bounded Plan + /critique Self-Review and wait for my "proceed" before writing code`
     - `Execute the code changes directly right after this dialog and run verification checks`
     - `Generate the full /web-precode (6 Pillars) + /spec-kit pipeline docs first and stop for review`
