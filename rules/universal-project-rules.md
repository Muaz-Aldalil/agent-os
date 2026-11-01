# Universal Cross-Project Engineering & UI Constitution (`universal-project-rules.md`)

Distilled from 74+ real project conversations across React, Next.js, Laravel/PHP, Node.js, WordPress/WooCommerce, and Agent OS. Every rule below is active across all repositories.

---

## 1. Execution Control, Gate Discipline & Traceability

1. **Batch Feedback Hold Mode**:
   - When the Owner says *"I will give you a lot of things to fix, don't build/proceed until I tell you to proceed"*, remain strictly in **Read-Only Hold Mode**: verify file paths and accumulate requirements without editing or running builds until told `"proceed"` or `"start"`.
2. **External Reviewer Verification**:
   - When the Owner shares feedback from an external reviewer agent, verify every claim against actual repository code; fix genuine defects and push back with line-level evidence when the external reviewer hallucinated or misread the architecture.
3. **Upstream-First Grilling & Hard-Stop SpecKit Gates**:
   - Resolve upstream product/actor/source-of-truth decisions before downstream UI column details.
   - **Never auto-chain SpecKit phases**: `/grill-me` → `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement` → `/speckit-converge` each require explicit Owner invocation.
4. **Edited-File Traceability & Mathematical Reconciliation**:
   - Report every `CREATED`, `MODIFIED`, `RENAMED`, or `DELETED` file with clickable `[basename](file:///path)`, repo-relative path, change type, and 1-line purpose.
   - Reconcile file counts (`CREATE + MODIFY + DELETE = TOTAL`), test pass counts, and untracked files (`git ls-files --others --exclude-standard`). Never use marketing language (*"100% complete"*, *"enterprise-grade"*, *"unbypassable"*, *"zero risk"*).

---

## 2. Surgical Visual, Content & Migration Preservation

1. **Full Migration Preservation**:
   - When organizing or migrating legacy code, preserve all existing routes, pages, copy, data, fonts, and brand colors.
2. **Zero Unrequested Redesign**:
   - Never alter primary brand colors, typography, or the **Navbar/Footer** when making targeted section edits.
3. **Public vs. Admin Shell Separation & Role-Aware Routing**:
   - Public pages and `/admin/*` share design tokens but must have strictly separate layout shells (never render the public navbar inside `/admin/*`, and never render the admin sidebar on public pages).
   - Admin users must see Admin Dashboard navigation and route to `/admin`; regular users must route to their user dashboard/profile and never see admin links.
4. **Single-Component-Per-File Modularity, 2–3 Line Header & Admin ↔ Public Reusability**:
   - Never dump multiple page sections (`Header`, `Hero`, `Features`, `Footer`) or reusable primitives (`Button`, `Card`, `Modal`) into `App.jsx`, `page.tsx`, or a single backend file. Each section and reusable component (used 2+ times) lives in its own file.
   - Top of every component/service file must include a concise **2–3 line comment block** stating: (1) What it does, (2) Where it is reused, and (3) Key props/inputs so a junior developer can reuse it across Admin and Landing pages in seconds.

---

## 3. Universal Layout, Responsive UI & CMS Ergonomics

1. **Hero Viewport Formula (`100dvh`)**:
   - Hero sections must subtract Navbar height: `min-h-[calc(100dvh-var(--navbar-height))]` with zero vertical overflow across Mobile, Tablet, and Desktop.
2. **Sticky Navigation & Sidebar**:
   - Public Navbar: `sticky top-0 z-50` with `overflow-x-clip` on page wrappers (never `overflow-hidden` on ancestors that break sticky positioning).
   - Admin Shell: Sticky top bar + full-height (`h-dvh sticky top-0`) sidebar with independent main content scroll (`overflow-y-auto`).
3. **Responsive Data Tables**:
   - Every Admin and User table must be responsive across mobile, tablet, and desktop.
   - Truncate long text cells to the **first 2–4 words + `...`** (`truncate max-w-[18ch]`), exposing full content in a detail modal or expandable row.
4. **Card Grids (3-Per-Row + Show More Toggle)**:
   - Use **3 cards per row on desktop (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)**. When a section has >3 cards, provide a **"Show More / Collapse All"** toggle.
5. **Input Icons & Logical Padding**:
   - Position input/search icons using logical properties (`start-3` / `end-3`, `ps-10` / `pe-10`, `pointer-events-none`) so icons never overlap placeholder or typed text in RTL or LTR.
6. **Minimalist Badges**:
   - Keep ordinary informational tags borderless and background-free; reserve colored pills/dots strictly for semantic statuses (`Winner`, `Active`, `Pending`, `Error`).
7. **CMS Ergonomics, Form Validation & Zero Native Alerts**:
   - Build structured CRUD tables, forms, and modals—never raw JSON textareas for end-users.
   - Include a **single Floating Save Button** in long CMS editors.
   - Enforce client + server validation for phone numbers (valid digits/length), emails, and required fields, and ensure Reset/Clear buttons cleanly reset form state.
   - Use **Toast notifications and Modal confirmations** for all feedback and destructive actions—**NEVER** use native `window.alert()`, `window.confirm()`, or `window.prompt()`.

---

## 4. Bilingual (AR/EN) Isolation & RTL/LTR Logical Parity

1. **Strict Locale Isolation & Navbar-Only Direction Switching**:
   - Zero English text leakage on Arabic pages (`/ar`) and zero Arabic text leakage on English pages (`/en`), including placeholders, validation errors, badges, and empty states.
   - Match the brand logo/wordmark to the active locale.
   - Only the language switcher changes `dir="rtl"` / `dir="ltr"`—ordinary nav links must never flip page direction and must scroll cleanly to the target section or top of the page.
2. **CSS Logical Properties Only**:
   - Enforce `ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start`, `text-end`, `border-s-*`, `border-e-*`.
   - Flip directional arrows/chevrons in RTL (`rtl:rotate-180` or `rtl:-scale-x-100`).
3. **Developer Attribution (Only When Requested)**:
   - **DigAge Solutions / ديجتال أيج** (`https://digagesolutions.com/`, `"Dig"` in `#00bcd4` + `"Age"` in `#e91e63`).

---

## 5. Runtime, Database, Bandwidth (Sudan) & Git Discipline

1. **Multi-Server Port Safety & Real DB Connectivity**:
   - Never run blanket `taskkill /F /IM node.exe` or kill dev servers on other ports; inspect only the target port (`Get-NetTCPConnection -LocalPort <port>`).
   - Verify real `Frontend -> Backend -> MySQL/MariaDB/PostgreSQL` connectivity and ensure the dev server is not accidentally pointed at `*_test`.
2. **Browser Testing Gate**:
   - When instructed *"don't open/test in the browser"*, never launch Playwright or Chrome DevTools MCP; verify via CLI tests and provide a **Manual Browser Acceptance Checklist**.
3. **Sudan Low-Bandwidth Awareness**:
   - Respect `/data-saver` (`bandwidth_guard.py`), prefer local/offline caches (`--prefer-offline`), and warn before large downloads.
4. **Git & Cloud Deployment Quota Protection (Netlify / Render)**:
   - Never run `git commit` or `git push` without explicit instruction (`"commit"` = local commit only; `"commit and push"` = commit + push).
   - Pushing to `main` triggers cloud builds on Netlify/Render that consume monthly free-tier build minutes; batch verified commits into a single push when requested.
