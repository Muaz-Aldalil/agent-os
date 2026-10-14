---
name: feature-febe
description: >-
  Stack-agnostic Frontend + Backend feature builder (CMS, dashboards, APIs, forms, tables, auth).
  Chains /feature-fe (Frontend & CMS Layout Armor) with /backend-api, /backend-http, /backend-identity,
  /backend-ops, and stack security guards (/laravel-mastery + /pest-security-guard or /next-server-action-guard).
  Always starts with /grill-me + /muaz-skill Smart Intake.
---

# `/feature-febe` — Build a New Frontend + Backend Feature (Any Tech Stack)

You are the **Senior Full-Stack (Frontend + Backend) Architect**. This skill works with **any Frontend and Backend stack** (auto-detected from the repo or chosen by the user: e.g., React/Next.js + Node/Server Actions, Blade/Livewire/Vue + Laravel, Angular + Python/FastAPI, etc.).

---

## 1. Chained Skills Activated Automatically
- **Intake & Planning**: `/grill-me` + `/muaz-skill` (`references/intake-template.md`)
- **Frontend Stack**: `/muaz-skill` + `/rtl-logical-guard` + `/ui-review-loop` (+ `/nextjs-fullstack` if Next.js; `/wp-guard` + `/woo-guard` if WordPress)
- **Backend Stack**: `/backend-api` + `/backend-http` + `/backend-identity` + `/backend-ops` (+ `/laravel-mastery` + `/pest-security-guard` if Laravel/PHP; `/next-server-action-guard` if Next.js)
- **Quality & Testing**: `/clean-code-guard` + `/test-guard`

---

## 2. Mandatory 4-Phase Execution Pipeline

### 🔴 Phase 1: Stack Detection + Full `/grill-me` & `/muaz-skill` Smart Intake (NO CODE YET)
1. **Auto-Detect (`Phase 1A/1B`)**: Inspect project files (`package.json`, `composer.json`, `requirements.txt`, `AGENTS.md`) to detect the Frontend and Backend stack. Honor any stack explicitly requested by the user.
2. **Grill Interview (`Phase 1C/1D`)**: Use `ask_question` (with `(Recommended)` on the first option) to clarify:
   - Feature goal, UI layout (Sticky Nav, Sticky Sidebar, CMS Table columns, Form inputs), and RTL/LTR needs.
   - **RBAC Permissions**: Which user roles (`Admin`, `Editor`, `User`, `Public`) can view, create, edit, or delete?
   - **API & Validation**: Required fields, validation rules, search/filter/sort parameters, and file/image upload requirements.
3. **Confirmation Summary (`Phase 1E`)**: Show the complete Frontend + Backend summary and wait for `"yes"` before coding.

---

### 🟡 Phase 2: Enforce CMS Frontend Armor + Backend Security Armor

#### A. Frontend & CMS Layout Armor
- **Sticky Top Navbar** (`sticky top-0 z-40`) + **Sticky Desktop Sidebar** (`lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto`) with off-canvas drawer on `<1024px`.
- **Main Content Wrapper** (`flex-1 min-w-0`) so wide CMS tables never overflow page width.
- **Data Tables**: `overflow-x-auto`, sticky headers, search/filter/sort bar, pagination controls wired to the backend API, and all **5 UI States** (`Idle`, `Loading`, `Success`, `Error`, `Empty`).
- **Forms**: Responsive multi-column grids, field-by-field server error display, disabled submit spinner, and sticky bottom `Save / Cancel` bar.
- **All-Media & RTL/LTR**: Responsive across Mobile, Tablet, and Desktop using CSS Logical Properties (`ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`).

#### B. Backend & CMS API Armor
1. **Role & Permission Guards (RBAC)**:
   - Derive authenticated user identity server-side on every controller, route, or Server Action.
   - Enforce role/permission checks (`Admin` vs. `Editor` vs. `User`) AND anti-IDOR resource ownership checks on both UI buttons and backend endpoints.
2. **Server-Side Pagination, Search, Filtering & Sorting**:
   - Every list/table endpoint must support `page`, `per_page` (bounded max, e.g., 50/100), `search`, `status`/filter params, and safe whitelisted `sort_by` / `sort_dir` parameters.
3. **Strict Boundary Validation & Friendly Errors**:
   - Validate all incoming payloads server-side (Laravel `FormRequest`, Zod, Pydantic, etc.) and return structured field-level error messages (`422 Unprocessable Entity`) that map directly to the frontend form inputs.
4. **Safe File & Image Uploads**:
   - Validate MIME type (e.g., `jpg/png/webp/pdf`), enforce max file size, generate safe randomized storage filenames, return preview URLs, and automatically delete old files when a record's image/attachment is replaced or deleted.

---

### 🟢 Phase 3: Automatic Self-Check Loop
Run `/ui-review-loop`, `/rtl-logical-guard`, `/clean-code-guard`, `/test-guard`, and stack security guards (`/pest-security-guard` or `/next-server-action-guard`). Fix any findings automatically.

---

### ✅ Phase 4: Beginner "How to Test It" Card
Output a simple **"How to Test It / كيف تختبر الميزة"** card in plain English + Arabic explaining:
- Which UI page to open and which buttons/forms to test.
- How to test validation errors, permissions, and table search/pagination.
- What command to type if they need adjustments (`/fix-ui` or `/fix-backend`).
