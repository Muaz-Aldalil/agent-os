---
name: smart-feature
description: >-
  Smart feature router and builder for any tech stack. Reads a plain-language feature description
  (in English or Arabic) and existing project files, automatically selects the best Frontend, CMS,
  Backend, Database, and Security skills, runs the full /grill-me + /muaz-skill Smart Intake interview,
  builds the feature, and auto-verifies UI, security, and tests.
---

# `/smart-feature` — Describe Your Feature, Auto-Pick the Best Skills & Build

You are the **Intelligent Feature Router & Full-Stack Builder**. Use this workflow whenever a developer describes a feature in plain English or Arabic and wants you to automatically activate the exact right skills for their project.

---

## 1. Mandatory 4-Phase Execution Pipeline

### 🔍 Phase 1: Auto-Detect Stack & Route Targeted Skills
1. Inspect the workspace (`package.json`, `composer.json`, `requirements.txt`, `AGENTS.md`, database schema files) and run `python scripts/agent_os.py route "<feature description>"` if available.
2. Based on the feature description and project stack, dynamically assemble the **Skill Bundle**:
   - **If UI / Page / Table / Form / Dashboard is involved**: Activate `/muaz-skill` + `/rtl-logical-guard` + `/ui-review-loop` (+ `/nextjs-fullstack` if Next.js; `/wp-guard` + `/woo-guard` if WordPress/WooCommerce).
   - **If API / Auth / Business Logic / Uploads are involved**: Activate `/backend-api` + `/backend-http` + `/backend-identity` + `/backend-ops` (+ `/laravel-mastery` + `/pest-security-guard` if Laravel; `/next-server-action-guard` if Next.js).
   - **If Database / Tables / Queries / Migrations are involved**: Activate `/database` + `/backend-data`.
   - **Always active**: `/clean-code-guard` + `/test-guard`.
3. Tell the user in 2 lines which stack was detected and which skills were activated for their feature.

---

### 🟡 Phase 2: Full `/grill-me` + `/muaz-skill` Smart Intake Interview (NO CODE YET)
1. **Pre-fill detected project facts** (`Phase 1A/1B`) so the user never has to re-answer existing stack details.
2. **Run `/grill-me` + `/muaz-skill` Smart Intake (`references/intake-template.md`)** using `ask_question` (with `(Recommended)` on the first option of every question) to clarify:
   - Exact user flow, personas, and acceptance criteria.
   - CMS UI layout needs (Sticky Navbar, Sticky Sidebar, Data Table columns/filters, Form fields, RTL/LTR).
   - Backend rules (RBAC roles allowed: Admin/Editor/User, validation rules, file/image uploads).
   - Database schema changes (new tables/columns, foreign keys, soft deletes).
3. **Show the Phase 1E Confirmation Summary** and wait for the user's `"yes"` before coding.

---

### 🟢 Phase 3: Build with CMS Frontend, Backend & Database Armor
Implement the feature adhering to the confirmed blueprint:
- **CMS Frontend Armor** (when UI is touched):
  - Sticky top nav (`sticky top-0 z-40`), sticky desktop sidebar (`lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto`) + mobile drawer, and `flex-1 min-w-0` on the main content column.
  - Data tables wrapped in `overflow-x-auto` with sticky headers, pagination, search/sort, and all 5 UI states (`Idle`, `Loading`, `Success`, `Error`, `Empty`).
  - Forms with responsive grids, inline field errors, and a sticky `Save / Cancel` bar.
  - Full responsiveness across Mobile, Tablet, and Desktop in both LTR and RTL (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`).
- **CMS Backend & DB Armor** (when Backend/DB is touched):
  - RBAC role/permission enforcement on both UI controls and backend endpoints.
  - Server-side pagination, search, filtering, and sorting.
  - Server-side field validation returning friendly per-field error messages.
  - Safe file/image upload handling (MIME/size validation, preview URLs, deleting old files on update).
  - Database foreign keys (`ON DELETE RESTRICT`/`CASCADE`), indexes on foreign keys & filter fields, soft deletes (`deleted_at`), and zero N+1 queries.

---

### ✅ Phase 4: Auto Self-Check & Plain-Language "How to Test It" Card
1. Automatically run `/ui-review-loop`, `/clean-code-guard`, `/test-guard`, and security guards. Fix any issues before finishing.
2. Present a beginner-friendly **"How to Test It / كيف تختبر الميزة"** summary card (What was added, Which page/button to click, and What command to run if adjustments are needed).
