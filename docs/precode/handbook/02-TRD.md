# 02 — Technical Requirements Document (TRD): Agent OS Beginner Handbook & 11 Situation Combo Skills

## 1. System Topology & Rendering Strategy
- **Architecture Pattern**: Markdown-driven Skill Orchestration Layer (`skills/<combo-name>/SKILL.md`) paired with a Bilingual Developer Handbook (`HANDBOOK.md`) and deterministic Python CLI tooling (`scripts/agent_os.py`).
- **Execution Mode**: Hybrid AI Chat Slash Command invocation (`/start-project`, `/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, `/feature-wp`, `/fix-ui`, `/fix-backend`, `/check-all`, `/doc-project`, `/save-data`) + Zero-Token local Python engines (`precode_engine.py`, `ui_audit_engine.py`, `bandwidth_guard.py`, `skill_router.py`).
- **Rendering & Layout Target for Generated Web Apps**: Supports SSR, SPA, Server Components, Blade/Livewire, and Hybrid CMS shells across any user-selected stack.

---

## 2. Tech Stack Matrix
- **Frontend Stacks Supported (Auto-Detected or User-Chosen)**:
  - React, Next.js (App Router / Pages), Vue 3 / Nuxt, Blade / Livewire / Filament, Angular, SvelteKit, Astro, Vanilla HTML5 + Tailwind CSS, WordPress / WooCommerce themes & blocks.
- **Backend Stacks Supported (Auto-Detected or User-Chosen)**:
  - Laravel 11+ (PHP 8.3/8.4), Node.js (Express / NestJS / Fastify), Next.js Server Actions & Route Handlers, Python (FastAPI / Django), Go, WordPress REST API / AJAX hooks.
- **Database Engines Supported (Auto-Detected or User-Chosen)**:
  - PostgreSQL, MySQL / MariaDB, SQLite, MongoDB, Firebase / Firestore, Supabase, Redis, Google Cloud Bigtable / BigQuery.
- **Styling & RTL System**:
  - CSS Logical Properties (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start`, `text-end`) enforced via `rtl-logical-guard`.
- **State & Auth**:
  - Session/Cookie Auth, JWT, OAuth2/OIDC, Laravel Sanctum/Fortify, NextAuth/Auth.js, RBAC/ABAC role matrices via `backend-identity`.

---

## 3. Third-Party APIs & Local Engines
- **Internal Engines**:
  - `python scripts/agent_os.py precode` (6 Pre-Coding Pillars verification)
  - `python scripts/agent_os.py route "<task>"` (Smart skill routing)
  - `python scripts/agent_os.py ui-audit` (Automated UI violation scanner & fix prompt generator)
  - `python scripts/agent_os.py data-saver` (Low-bandwidth IDE & package manager guard)
  - `python scripts/agent_os.py sync --apply` (Global skill synchronization to `~/.gemini/config`)
- **External Integrations (Optional per User Project)**:
  - Stripe / PayPal payments, S3 / R2 / Local disk storage for CMS file uploads, SMTP / Resend email providers.

---

## 4. Security Boundary Invariants
1. **Server-Side Auth & RBAC Derivation**: Every protected route, controller, or Server Action must derive user identity and role permissions (`Admin`, `Editor`, `User`) server-side (`next-server-action-guard`, `pest-security-guard`, `backend-identity`).
2. **Anti-IDOR Ownership Verification**: Resource mutations (`UPDATE`, `DELETE`) must verify resource ownership or admin privilege before execution.
3. **Strict Boundary Validation**: All form payloads, query parameters (pagination, search, sort), and file uploads (MIME type, max size, safe filename) must be validated via Zod, Laravel FormRequest, Pydantic, or equivalent schema validators.
4. **WordPress / WooCommerce Hardening**: Nonce verification (`wp_verify_nonce`), capability checks (`current_user_can`), prepared SQL statements (`$wpdb->prepare`), and output escaping (`wp-guard`, `woo-guard`).

---

## 5. Performance Budgets
- **Core Web Vitals (for all generated Frontend/CMS UIs)**:
  - Largest Contentful Paint (`LCP`) <= 2.5s
  - Interaction to Next Paint (`INP`) <= 200ms
  - Cumulative Layout Shift (`CLS`) <= 0.1
- **Bundle & Network Budgets**:
  - Initial JS bundle < 100kB–200kB gzip
  - Bandwidth conservation: 75–85% reduction in background IDE traffic when `/save-data` (`bandwidth_guard.py`) is active.
  - Database queries: 0 N+1 query loops; mandatory pagination (`per_page` limit) on all CMS data table endpoints.
