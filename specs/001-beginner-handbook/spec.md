# Feature Specification: Agent OS Beginner Handbook & 11 Situation Combo Skills (`001-beginner-handbook`)

## 1. Summary
Create a beginner-friendly, bilingual (Simple English + Arabic) **Agent OS Developer Handbook (`HANDBOOK.md`)** and **11 Situation-Based Combo Slash Commands** in `skills/` so pre-junior developers can use `.agents` effortlessly without memorizing 49 internal skills or 30+ CLI flags.

---

## 2. User Stories & Acceptance Criteria

### User Story 1 (`[US1]`): The Unseeable Hook & 30-Second Onboarding
- **As a** beginner or pre-junior developer opening `.agents` for the first time
- **I want to** see a crystal-clear comparison of how my AI behaves **Without `.agents` (Fast Intern)** vs. **With `.agents` (Senior Tech Team)** and set it up in one step
- **So that** I immediately understand its value, never confuse AI Chat with Terminal, and protect my internet bandwidth.
- **Acceptance Criteria**:
  - **Given** a developer opens `HANDBOOK.md`
  - **When** they read Section 1 and Section 2
  - **Then** they see the English + Arabic "Fast Intern vs. Senior Tech Team" hook, a concrete side-by-side table (Navbar/Sidebar, Tables/Forms, Security/RBAC, RTL/Arabic, Internet Data), the live proof that this Handbook was built with `/web-precode` + `/spec-kit`, the **1-2-3 Traffic Light Rule**, the 💬 **AI Chat** vs. 💻 **Terminal** badge legend, and the **Top 4 Magic Commands** quick-start table.

### User Story 2 (`[US2]`): 11 Stack-Agnostic Situation Combo Commands with `/grill-me` Intake
- **As a** developer building a project or feature in any tech stack (React, Next.js, Vue, Laravel, Blade, WordPress, Node, Python, MySQL, PostgreSQL, SQLite, MongoDB)
- **I want to** trigger one Situation Slash Command (or Copy-Paste Prompt) that interviews me first via `/grill-me` + `/muaz-skill` Smart Intake
- **So that** the agent never guesses my requirements and automatically loads the exact Frontend, Backend, Database, and Security skills for my stack.
- **Acceptance Criteria**:
  - **Given** a developer invokes `/start-project`, `/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, or `/feature-wp`
  - **When** the skill activates
  - **Then** it runs `Phase 1A Auto-Detect → 1B Detection Summary → 1C/1D Grill Questions (/grill-me + /muaz-skill intake-template.md) → 1E Confirmation Summary` and waits for user approval before writing code.

### User Story 3 (`[US3]`): Mandatory CMS Frontend, Backend & Database Armor + Self-Check Handoff
- **As a** CMS and full-stack builder
- **I want** sticky navbars, sticky sidebars, responsive overflow tables, forms, RBAC permissions, server-side pagination/validation, safe file uploads, and database foreign keys/soft deletes enforced automatically
- **So that** my pages never break on mobile/tablet/desktop or RTL/LTR, and every build ends with an automatic self-check and a plain-language **"How to Test It"** card.
- **Acceptance Criteria**:
  - **Given** a developer runs any feature or fix command (`/feature-fe`, `/feature-febe`, `/feature-full`, `/smart-feature`, `/fix-ui`, `/fix-backend`)
  - **When** the agent generates and verifies the implementation
  - **Then** it enforces the CMS Frontend Armor + CMS Backend/DB Armor, runs `/ui-review-loop` + `/clean-code-guard` + `/test-guard`, fixes any violations automatically, and outputs the **"How to Test It" Card** in plain English + Arabic.

---

## 3. Functional Requirements
- `FR-001`: Author `HANDBOOK.md` at repository root in Bilingual Simple English + Arabic.
- `FR-002`: Create 11 Situation Combo Skills under `skills/`:
  1. `start-project`
  2. `smart-feature`
  3. `feature-fe`
  4. `feature-febe`
  5. `feature-full`
  6. `feature-wp`
  7. `fix-ui`
  8. `fix-backend`
  9. `check-all`
  10. `doc-project`
  11. `save-data`
- `FR-003`: Each Situation Card in `HANDBOOK.md` must include both **Option A (1-Word Slash Command)** and **Option B (Full Copy-Paste Prompt)**.
- `FR-004`: Re-index `SKILL_INDEX.json`, update `SKILLS_DIRECTORY.md` and `README.md`, and sync all 60 skills (`49 + 11 = 60`) to `~/.gemini/config`.

---

## 4. Success Criteria
- `SC-001`: `python scripts/agent_os.py precode audit docs/precode/handbook` passes at **100%**.
- `SC-002`: All 11 Combo Skills pass YAML frontmatter and `agent_os.py audit` validation.
- `SC-003`: `python scripts/agent_os.py sync --apply` and `python scripts/agent_os.py test` pass 100%.
