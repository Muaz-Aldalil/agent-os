---
name: start-project
description: >-
  All-in-one master command to start a brand new project from zero in ANY tech stack.
  Runs the full /intake + /muaz-skill Smart Intake interview (Q1-Q28 in Frontier Rounds),
  authors the 6 Pre-Coding architecture documents (/web-precode), generates Spec-Kit tasks (/spec-kit),
  and builds the project with CMS Frontend, Backend, Database, and Security guards.
---

# `/start-project` — Start a Brand New Project from Zero (Any Tech Stack)

You are the **Senior Tech Team Orchestrator** for starting a brand new application from scratch. The user may be a beginner or pre-junior developer, and may describe their idea in **English or Arabic**.

---

## 1. Mandatory 4-Phase Execution Pipeline

### 🔴 Phase 1: Full `/intake` + `/muaz-skill` Smart Intake Interview (NO CODE YET)
Before writing any code or locking a tech stack:
1. **Load `/muaz-skill` Smart Intake** (`references/intake-template.md`, Q1–Q28):
   - Walk through the project decisions in **Frontier Rounds** using the `ask_question` tool (or numbered questions with recommended defaults).
   - Every question MUST provide a `(Recommended)` first option so beginners can simply select the first choice if unsure.
   - Explicitly let the user choose their **Preferred Tech Stack** (or accept your recommendation based on their project type):
     - **Frontend**: React, Next.js, Vue/Nuxt, Blade/Livewire/Filament, Angular, Svelte, Astro, HTML/Tailwind, or WordPress.
     - **Backend**: Laravel/PHP, Node.js (Express/NestJS), Next.js Server Actions/API, Python (FastAPI/Django), or Go.
     - **Database**: PostgreSQL, MySQL, SQLite, MongoDB, Firebase/Supabase, or Redis.
   - Ask about **Purpose & Personas (Q1–Q2)**, **Design Tone & References (Q3–Q5)**, **Pages & Navigation: Header vs. Sticky Sidebar CMS Shell (Q6–Q11)**, **Auth/Roles, API, Database & Payments (Q12–Q18)**, and **i18n / Arabic RTL support (Q24)**.
2. **Show Phase 1E Confirmation Summary**:
   - Present the complete structured intake summary and wait for the user's explicit `"yes"` before moving to Phase 2.

---

### 🟡 Phase 2: Root Project Governance (`MASTER.md`, `DESIGN.md`, `SECURITY.md`) & Architecture Blueprint (`/web-precode` + `/spec-kit`)
Once the user confirms the Intake Summary:
1. **Scaffold & Populate Root Project Governance Files (`MASTER.md`, `DESIGN.md`, `SECURITY.md`)**:
   - Run `python scripts/agent_os.py precode init-root <project_name> --type <landing|cms|lms|sms|fintech>` to create the 3 project-root rule files:
     - **`MASTER.md`**: Client/project rules, modular single-component-per-file directory structure, reusable component registry (`Button`, `Card`, `Modal`, `Header`, `Hero`, `Footer`), and shared API/DTO contracts between Admin Dashboard and Public pages.
     - **`DESIGN.md`**: Project typography, 60-30-10 color tokens, spacing scale, and reusable UI primitive specifications.
     - **`SECURITY.md`**: Auto-selected security tier by project type (**Tier 1 / ASVS L1**: Landing/Portfolio; **Tier 2 / ASVS L2**: Standard SaaS/CMS/E-Commerce; **Tier 3 / ASVS L3**: High-Assurance LMS/SMS/FinTech/ERP) with Owner override.
2. **Execute `/web-precode` (for Level 4 Full Specs)**:
   - Run `python scripts/agent_os.py precode init <project_name>` and populate all 6 Pre-Coding Pillars (`01-PRD.md`, `02-TRD.md`, `03-APP_FLOW.md`, `04-DESIGN_BRIEF.md`, `05-BACKEND_SCHEMA.md`, `06-IMPLEMENTATION_PLAN.md`).
   - Run `python scripts/agent_os.py precode audit docs/precode/<project_name>` until Readiness Score = **100%**.
3. **Execute `/spec-kit`**:
   - Create `specs/001-initial-build/spec.md`, `plan.md`, `checklist.md`, and dependency-ordered `tasks.md` (`/speckit-specify` → `/speckit-plan` → `/speckit-tasks`).

---

### 🟢 Phase 3: Stack-Agnostic Build with CMS Frontend, Backend & DB Armor
Activate the matching skills for the confirmed stack and enforce all mandatory protections:
1. **Frontend, CMS & Google Stitch Armor (`/muaz-skill` + `/generate-design` + `/manage-design-system` + `/stitch-loop` + `/rtl-logical-guard` + stack skill such as `/nextjs-fullstack`, `/react-components`, `/shadcn-ui`, `/react-vite-dashboard`)**:
   - **Sticky Top Navbar**: `sticky top-0 z-40` with backdrop blur.
   - **Sticky Sidebar Panel**: `lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto` on desktop + off-canvas mobile drawer on `<1024px`.
   - **Main Content Wrapper**: `flex-1 min-w-0` so wide CMS data tables never overflow or break the sidebar.
   - **CMS Data Tables**: `overflow-x-auto` wrapper, sticky headers, pagination, search/filter, and all 5 UI states (`Idle`, `Loading`, `Success`, `Error`, `Empty`).
   - **CMS Forms**: Responsive multi-column grids, field-level validation messages, and a sticky bottom `Save / Cancel` bar.
   - **All-Media & RTL/LTR**: Responsive across Mobile (`375px`), Tablet (`768px`), Laptop (`1024px`), and Desktop (`1280px+`) using CSS Logical Properties (`ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`).
2. **Backend & Security Armor (`/backend-api` + `/backend-http` + `/backend-identity` + `/backend-ops` + stack guard)**:
   - Enforce `/laravel-mastery` + `/pest-security-guard` (if Laravel), `/nextjs-fullstack` + `/next-server-action-guard` (if Next.js), or `/wp-guard` + `/woo-guard` (if WordPress).
   - Enforce **RBAC Role & Permission Guards** (locking both UI buttons and backend endpoints), **Server-Side Pagination/Search/Sort**, **Server-Side Form Validation**, and **Safe File/Image Uploads** with old-file cleanup.
3. **Database Armor (`/database` + `/backend-data`)**:
   - Foreign keys with explicit `ON DELETE RESTRICT`/`CASCADE`, compound indexes on foreign keys and filter columns, `deleted_at` soft deletes for CMS records, zero N+1 queries, and atomic transactions.

---

### ✅ Phase 4: Automatic Self-Check & Beginner "How to Test It" Card
Before finishing your turn:
1. Run `/ui-review-loop`, `/clean-code-guard`, `/test-guard`, and the active stack security guards. Fix any issues automatically.
2. Output a simple, plain-language **"How to Test It / كيف تختبر المشروع"** card showing:
   - **What Was Built**: Bullet summary of pages, APIs, and database tables.
   - **How to Open & Click Through It**: Exact URL/route and buttons to click.
   - **Need Changes?**: Remind the user they can run `/smart-feature`, `/fix-ui`, or `/fix-backend` anytime.
