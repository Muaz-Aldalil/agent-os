# 01 — Product Requirements Document (PRD): Agent OS Beginner Handbook & 11 Situation Combo Skills

## 1. Executive Summary & Value Proposition
Pre-junior and beginner developers struggle to navigate large AI agent ecosystems containing 49+ specialized skills, security guards, and 30+ CLI flags. Without a clear guide, beginners either type vague prompts ("build a users page")—causing the AI to act like a "fast intern" that guesses requirements, breaks CMS sticky sidebars/navbars, ignores RBAC permissions, and breaks Arabic/English RTL layouts—or they accidentally pick the wrong `/command` from IDE autocomplete.

The **Agent OS Beginner Handbook (`HANDBOOK.md`)** and **11 Situation Combo Skills** solve this by turning `.agents` into an approachable **Senior Tech Team in a Box**. It opens with an unforgettable "With vs. Without `.agents`" hook, teaches the **1-2-3 Traffic Light Rule**, provides a **30-Second Top 4 Magic Commands** quick-card, and delivers **11 Situation-Based Combo Commands & Copy-Paste Prompts** (bilingual English + Arabic) that automatically run `/grill-me` + `/muaz-skill` Smart Intake before coding and auto-verify UI/Security/Tests after coding.

---

## 2. Target Personas & User Journeys
- **Primary Persona**: Pre-junior developers, students, first-time builders, and CMS/full-stack developers working across diverse stacks (React, Next.js, Vue, Laravel, Blade/Livewire, WordPress/WooCommerce, Node, Python, MySQL, PostgreSQL, SQLite, MongoDB) often under limited internet bandwidth (Sudan / mobile hotspot).
- **Pain Points**:
  1. Mixing up the **AI Chat Box** and the **Terminal**.
  2. Not knowing which of the 49 skills to invoke for Frontend, Backend, or Database work.
  3. Recurring CMS layout bugs: non-sticky top navbar, non-sticky sidebar, wide data tables breaking page width (`min-w-0` missing), broken forms, and broken RTL/LTR layouts.
  4. Missing backend/DB essentials: missing RBAC permissions, unpaginated tables, missing server-side validation, unsafe file uploads, and missing foreign keys/soft deletes.
- **Core User Journey**:
  1. Opens `HANDBOOK.md` → immediately sees the **"Without `.agents` (Fast Intern) vs. With `.agents` (Senior Tech Team)"** hook.
  2. Runs the 1-step setup prompt in AI Chat (including `/save-data` for bandwidth protection).
  3. Picks their situation from the **Top 4 Magic Commands** or the **11 Situation Cards** (either typing the 1-word `/command` or pasting the Full Copy-Paste Prompt in English or Arabic).
  4. Answers the `/grill-me` + `/muaz-skill` Smart Intake questions (clicking `(Recommended)` when unsure).
  5. Receives verified code plus a plain-language **"How to Test It"** card.

---

## 3. Functional Requirements
- **P0 (Must Have)**:
  - `FR-001`: Bilingual (Simple English + Arabic) `HANDBOOK.md` at repository root with the "Fast Intern vs. Senior Tech Team" hook and "1-2-3 Traffic Light Rule".
  - `FR-002`: 11 installable Situation Combo Skills in `skills/` (`/start-project`, `/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, `/feature-wp`, `/fix-ui`, `/fix-backend`, `/check-all`, `/doc-project`, `/save-data`).
  - `FR-003`: Mandatory `/grill-me` + `/muaz-skill` Smart Intake (`references/intake-template.md`, Q1–Q28 Frontier Rounds + Phase 1E Confirmation Summary) before `/start-project` and before every feature skill (`/feature-fe`, `/feature-febe`, `/feature-full`, `/smart-feature`, `/feature-wp`).
  - `FR-004`: 100% stack-agnostic skill routing (auto-detects project stack or honors user's chosen Frontend, Backend, and Database stack).
  - `FR-005`: Mandatory CMS Frontend Armor (sticky top nav, sticky `h-dvh` sidebar with mobile drawer, `flex-1 min-w-0` main column, responsive overflow tables with sticky headers/pagination, multi-column forms with sticky save bar, all-media responsiveness, and RTL/LTR logical CSS).
  - `FR-006`: Mandatory CMS Backend & Database Armor (RBAC role/permission guards on UI + API, server-side pagination/search/filter/sort, field-level server validation, safe file/image uploads with cleanup, and DB foreign keys, indexes, and soft deletes).
  - `FR-007`: Automatic post-build self-check (`/ui-review-loop`, `/clean-code-guard`, `/test-guard`, security guards) and a plain-language **"How to Test It"** handoff card.
- **P1 (Should Have)**:
  - `FR-008`: Cross-links in `README.md`, `SKILLS_DIRECTORY.md`, and updated `SKILL_INDEX.json` synced to global `~/.gemini/config`.
- **P2 (Post-v1)**:
  - `FR-009`: Video/GIF walkthroughs embedded in documentation.

---

## 4. Formal User Stories with Acceptance Criteria

### User Story 1: The Hook & 30-Second Onboarding
- **User Story**: As a beginner developer, I want to immediately understand what `.agents` does and set it up in one step so that my AI acts like a Senior Tech Team instead of a fast intern.
- **Given** a beginner developer opens `HANDBOOK.md` for the first time
- **When** they read the introduction and setup section
- **Then** they see a clear English + Arabic comparison of how the AI performs **Without `.agents`** vs. **With `.agents`**, understand the difference between 💬 **AI Chat** and 💻 **Terminal**, and can copy-paste a single setup prompt to activate all skills and low-bandwidth mode.

### User Story 2: Starting Any New Project or Feature with `/grill-me` Intake
- **User Story**: As a developer using any tech stack, I want to trigger a single situation command that interviews me before coding so that requirements are never guessed.
- **Given** a developer wants to start a new project (`/start-project`) or build a feature (`/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, `/feature-wp`) in any tech stack
- **When** they paste either the 1-word `/command` or the Full Copy-Paste Prompt from `HANDBOOK.md`
- **Then** the agent auto-detects existing project files, runs `/grill-me` + `/muaz-skill` Smart Intake questions with `(Recommended)` defaults, waits for Confirmation Summary approval, and only then generates the architecture and code.

### User Story 3: CMS Frontend, Backend & Database Quality Guarantees
- **User Story**: As a CMS/full-stack builder, I want to have sticky navbars, sticky sidebars, responsive tables, forms, RBAC, and database constraints enforced automatically so that pages never break.
- **Given** a developer builds a CMS dashboard, table, form, API, or database feature using the combo commands
- **When** the agent generates the code and completes the post-build verification loop
- **Then** the UI enforces sticky nav, sticky sidebar, `flex-1 min-w-0` table containment, responsive forms, and RTL logical properties; the backend enforces RBAC, pagination/search, field validation, safe uploads, and DB foreign keys/soft deletes; and the agent outputs a plain-language **"How to Test It"** card.

---

## 5. Explicitly Out of Scope
- Locking developers into a single framework (e.g., forcing Next.js when the user wants Laravel Blade, Vue, or WordPress).
- Requiring beginners to memorize all 49 internal skill names or 30+ Python CLI flags.
- Removing or breaking any existing skills in `skills/`.
