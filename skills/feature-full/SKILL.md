---
name: feature-full
description: >-
  Complete Full-Stack Feature Builder: Frontend + Backend + Database for ANY tech stack.
  Chains /feature-febe (CMS UI + Backend API/RBAC/Validation/Uploads) with /database and /backend-data
  (migrations, foreign keys, compound indexes, soft deletes, N+1 prevention, and transactions).
  Always starts with /grill-me + /muaz-skill Smart Intake.
---

# `/feature-full` — Build a Full Feature: Frontend + Backend + Database (Any Stack)

You are the **Principal Full-Stack & Database Architect**. Use this skill when building a complete end-to-end feature that spans **Database Schema/Migrations + Backend API/Business Logic + Frontend/CMS UI** in **any tech stack** (React/Next.js, Vue/Nuxt, Laravel/Blade/Livewire, Node, Python, Go, with MySQL, PostgreSQL, SQLite, MongoDB, Firebase, Supabase, or Bigtable).

---

## 1. Chained Skills Activated Automatically
- **Intake & Architecture**: `/grill-me` + `/muaz-skill` (`references/intake-template.md`)
- **Database Stack**: `/database` + `/backend-data` (adapted to MySQL, PostgreSQL, SQLite, Prisma, Drizzle, Eloquent, MongoDB, Firebase, etc.)
- **Backend Stack**: `/backend-api` + `/backend-http` + `/backend-identity` + `/backend-ops` (+ `/laravel-mastery` + `/pest-security-guard` if Laravel; `/next-server-action-guard` if Next.js)
- **Frontend & CMS Stack**: `/muaz-skill` + `/rtl-logical-guard` + `/ui-review-loop` (+ `/nextjs-fullstack` if Next.js; `/wp-guard` + `/woo-guard` if WordPress)
- **Quality & Testing**: `/clean-code-guard` + `/test-guard`

---

## 2. Mandatory 4-Phase Execution Pipeline

### 🔴 Phase 1: Stack Detection + Full `/grill-me` & `/muaz-skill` Smart Intake (NO CODE YET)
1. **Auto-Detect (`Phase 1A/1B`)**: Read project files (`package.json`, `composer.json`, `.env.example`, `prisma/schema.prisma`, `database/migrations/`) to detect the active Frontend, Backend, and Database stack. Honor any stack explicitly requested by the user.
2. **Grill Interview (`Phase 1C/1D`)**: Use `ask_question` (with `(Recommended)` on the first option) to clarify:
   - Feature goal, user personas, and CMS layout (Sticky Nav, Sticky Sidebar, Table columns, Form fields, RTL/LTR).
   - **Database Entities & Relations**: What tables/fields are needed? How do they relate (`1:N`, `N:M`) to existing tables (e.g., `users`, `categories`, `organizations`)? Should deletion be Soft Delete (`deleted_at`)?
   - **Backend Rules**: RBAC roles (`Admin`, `Editor`, `User`), validation rules, search/filter/pagination columns, and file/image uploads.
3. **Confirmation Summary (`Phase 1E`)**: Present the unified Database + Backend + Frontend blueprint and wait for `"yes"` before coding.

---

### 🟡 Phase 2: Build Bottom-Up with Full CMS Armor (DB → Backend → Frontend)

#### Step 1: Database & Data Integrity Armor (`/database` + `/backend-data`)
1. **Relations & Foreign Keys**: Define explicit foreign key constraints with intentional cascade policies (`ON DELETE RESTRICT` for core business records to prevent accidental data loss; `ON DELETE CASCADE` only for dependent pivot/child rows).
2. **Compound & Foreign Key Indexes**: Index every foreign key (`*_id`) and add compound indexes on columns used for CMS table filtering, searching, and sorting (`status`, `created_at`, `deleted_at`).
3. **Soft Deletes (`deleted_at`)**: Enable soft deletes on CMS business entities so admins can restore accidentally deleted items.
4. **Zero N+1 & Transactions**: Eager-load relationships (`with()` / `include:`) on list queries and wrap multi-table mutations in atomic database transactions (`DB::transaction` / `$transaction`).

#### Step 2: Backend API & Security Armor (`/backend-api` + `/backend-identity` + `/backend-http` + `/backend-ops`)
1. **RBAC Role & Permission Guards**: Enforce server-side authentication, role checks (`Admin`, `Editor`, `User`), and anti-IDOR ownership checks.
2. **Server-Side Pagination, Search, Filtering & Sorting**: Wire directly to the indexed DB columns so CMS tables handle 100,000+ rows smoothly.
3. **Field-Level Server Validation**: Validate all inputs and return clear field-by-field errors (`422`) to the frontend form.
4. **Safe File & Image Uploads**: Validate MIME type & file size, generate safe filenames, provide preview URLs, and clean up old files from disk/S3 on update or delete.

#### Step 3: Frontend & CMS UI Armor (`/muaz-skill` + `/rtl-logical-guard`)
1. **Sticky App Shell**: Sticky Top Navbar (`sticky top-0 z-40`), Sticky Desktop Sidebar (`lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto`) + mobile drawer, and `flex-1 min-w-0` main column.
2. **CMS Data Tables**: `overflow-x-auto` wrapper, sticky headers, search/filter/sort controls, pagination bar, role-gated action buttons, and all **5 UI States** (`Idle`, `Loading`, `Success`, `Error`, `Empty`).
3. **CMS Forms**: Multi-column responsive grids, inline validation error display, upload preview, and sticky `Save / Cancel` bar.
4. **All-Media & RTL/LTR**: Responsive across Mobile, Tablet, and Desktop using CSS Logical Properties (`ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`).

---

### 🟢 Phase 3: Automatic Self-Check & Migration Verification
1. Run safe schema/type checks, `/ui-review-loop`, `/rtl-logical-guard`, `/clean-code-guard`, `/test-guard`, and security guards. Fix any issues automatically.

---

### ✅ Phase 4: Beginner "How to Test It" Card
Output a plain-language **"How to Test It / كيف تختبر الميزة بالكامل"** card showing:
- Database tables/migrations created (and whether migrations were run or the 1 command to run them).
- Backend API endpoints & RBAC permissions added.
- Exact UI page & steps to test Creating, Viewing/Searching in the Table, Editing, and Deleting.
