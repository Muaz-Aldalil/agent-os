#!/usr/bin/env python3
"""
scripts/precode_engine.py
The 6 Pre-Coding Pillars Engine for Agent OS.

Guarantees that no web project or complex feature begins implementation
without complete, validated specifications across the 6 mandatory documents:
1. Product Requirements Document (PRD)
2. Technical Requirements Document (TRD)
3. App Flow & State Machine (APP_FLOW)
4. Design Brief & Visual Tokens (DESIGN_BRIEF)
5. Backend Schema & Data Model (BACKEND_SCHEMA)
6. Implementation Plan & Execution Tasks (IMPLEMENTATION_PLAN)
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# UTF-8 terminal encoding configuration
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_DOCS = [
    "01-PRD.md",
    "02-TRD.md",
    "03-APP_FLOW.md",
    "04-DESIGN_BRIEF.md",
    "05-BACKEND_SCHEMA.md",
    "06-IMPLEMENTATION_PLAN.md",
]

ROOT_GOVERNANCE_DOCS = [
    "MASTER.md",
    "DESIGN.md",
    "SECURITY.md",
]

# 5 Mandatory UI States for App Flow
MANDATORY_UI_STATES = ["Idle", "Loading", "Success", "Error", "Empty"]

PRD_RAW_TEMPLATE = """# Product Requirements Document (PRD): __PROJECT_NAME__

## 1. Executive Summary & Vision
- **Project Name**: __PROJECT_NAME__
- **Status**: DRAFT <!-- DRAFT | IN_REVIEW | APPROVED -->
- **Target Audience**: <!-- Who uses this product? -->
- **Core Value Proposition**: <!-- Why does this exist? What painful problem does it solve? -->

---

## 2. Target Personas & User Journeys
### Primary Persona: <!-- Name / Role -->
- **Goal**: <!-- What are they trying to accomplish? -->
- **Pain Points**: <!-- What frustrates them today? -->
- **Key Journey**: <!-- Step-by-step path from first touch to core value -->

---

## 3. Functional Requirements (P0 / P1 / P2)

### P0 (Must Have for v1)
- [ ] **FR-001**: <!-- Core feature description -->
- [ ] **FR-002**: <!-- Core feature description -->
- [ ] **FR-003**: <!-- Core feature description -->

### P1 (Should Have)
- [ ] **FR-101**: <!-- Secondary feature description -->
- [ ] **FR-102**: <!-- Secondary feature description -->

### P2 (Post-v1 / Nice to Have)
- [ ] **FR-201**: <!-- Future extension -->

---

## 4. Formal User Stories & Acceptance Criteria

### User Story US-01: <!-- Title -->
**As a** <!-- persona -->  
**I want to** <!-- action -->  
**So that** <!-- outcome / benefit -->  

**Acceptance Criteria (Given / When / Then)**:
- **Given** <!-- pre-condition / initial state -->
- **When** <!-- user triggers action -->
- **Then** <!-- system outcome / expected behavior -->

---

## 5. Explicitly Out of Scope
The following capabilities are deliberately excluded from this release to prevent scope creep:
- <!-- Excluded item 1 -->
- <!-- Excluded item 2 -->

---

## 6. Non-Functional Requirements & Compliance
- **Performance**: Initial page load < 1.5s, Time-to-Interactive < 2.0s.
- **Accessibility**: WCAG 2.1 Level AA compliance, full keyboard navigability.
- **Localization**: LTR and RTL bi-directional support (if bilingual).
- **Security**: Strict authentication derivation, anti-IDOR checks, rate limiting.
"""

TRD_RAW_TEMPLATE = """# Technical Requirements Document (TRD): __PROJECT_NAME__

## 1. System Architecture & Topology
- **Rendering Architecture**: <!-- Next.js 15 App Router (Server/Client Components) | Laravel 11 Blade/Inertia | SPA -->
- **State Management**: <!-- Server-side state, React Query/SWR, or Zustand -->
- **API Convention**: <!-- Server Actions | RESTful JSON API | GraphQL -->
- **Execution Runtime**: <!-- Node.js LTS | Bun | PHP 8.3+ | Python 3.12+ -->

---

## 2. Technology Stack Selection & Rationale

| Layer | Selected Technology | Version | Rationale & Trade-offs |
| :--- | :--- | :--- | :--- |
| **Frontend** | <!-- Next.js / React / Vue --> | <!-- e.g. 15.x --> | <!-- Server components, fast streaming --> |
| **Styling** | <!-- Tailwind CSS v4 --> | <!-- v4.x --> | <!-- Logical properties, zero runtime overhead --> |
| **Backend / API** | <!-- Server Actions / Route Handlers / Laravel --> | <!-- ... --> | <!-- Type-safe contracts, low latency --> |
| **Database** | <!-- PostgreSQL / MySQL / SQLite --> | <!-- ... --> | <!-- ACID transactions, relational integrity --> |
| **ORM / Query** | <!-- Prisma / Drizzle / Eloquent --> | <!-- ... --> | <!-- Type safety, migration safety --> |
| **Authentication** | <!-- Auth.js / Supabase Auth / Laravel Breeze --> | <!-- ... --> | <!-- Session security, OAuth2, RBAC --> |

---

## 3. Third-Party Integrations & External Services
- **Auth Provider**: <!-- OAuth, Google, GitHub, Magic Links -->
- **Transactional Email**: <!-- Resend, Postmark, SendGrid -->
- **Object / File Storage**: <!-- Cloudflare R2, AWS S3, Supabase Storage -->
- **Payments / Billing**: <!-- Stripe Elements / Webhooks (Danger Zone 1) -->

---

## 4. Security Architecture & Boundary Invariants
- **Authentication Derivation**: Never trust client-provided `userId`; always derive from verified session server-side.
- **Authorization & Anti-IDOR**: Explicit ownership verification on every mutation and query.
- **Input Sanitization & Validation**: Runtime boundary validation via Zod / Form Requests.
- **Network Security**: Strict Content Security Policy (CSP), CORS isolation, CSRF token validation.

---

## 5. Performance Budgets & Core Web Vitals
- **Largest Contentful Paint (LCP)**: <= 2.5s
- **Interaction to Next Paint (INP)**: <= 200ms
- **Cumulative Layout Shift (CLS)**: <= 0.1
- **Bundle Budget**: Initial JS payload < 100kB gzip.
"""

APP_FLOW_RAW_TEMPLATE = """# App Flow & State Machine: __PROJECT_NAME__

## 1. Route Map & Navigation Hierarchy

| Route Path | Access Level | Description | Next Potential Routes |
| :--- | :--- | :--- | :--- |
| `/` | Public | Landing / Hero / Features | `/login`, `/register`, `/pricing` |
| `/login` | Public (Guest) | Authentication Form | `/dashboard`, `/forgot-password` |
| `/dashboard` | Protected (User) | Core Overview & Metrics | `/settings`, `/projects`, `/logout` |

---

## 2. Primary User Journey Flowcharts

```mermaid
flowchart TD
    Start([User arrives on Landing]) --> AuthCheck{Is Authenticated?}
    AuthCheck -- Yes --> Dashboard[/dashboard/]
    AuthCheck -- No --> LoginView[/login/]

    LoginView --> FormSubmit[Submit Credentials]
    FormSubmit --> ServerVal{Server Validation}
    ServerVal -- 200 OK --> SetSession[Set Secure HttpOnly Cookie]
    SetSession --> Dashboard
    ServerVal -- 401 / 422 --> ShowError[Render Inline Error Alert]
    ShowError --> LoginView
```

---

## 3. The 5-State UI Matrix
Every core interaction and dynamic view MUST define and handle all 5 states:

| View / Component | 1. Idle State | 2. Loading / Pending | 3. Success State | 4. Error State | 5. Empty State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Login / Auth Form** | Active input fields, enabled submit button | Submit button disabled with spinner, form locked | Redirect to dashboard, show success toast | Inline red field alerts + toast banner | N/A (Form input) |
| **Main Resource List** | Table/Cards populated with existing data | Shimmer/Skeleton loading cards matching layout | Crisp data grid with interactive row actions | Retry button with human-readable error | Illustrated empty state with 'Create New' CTA |

---

## 4. Session & Authentication State Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser
    participant Middleware
    participant ServerAction as Server Action / API
    participant DB as Database

    User->>Browser: Enters Protected Route (/dashboard)
    Browser->>Middleware: GET /dashboard with Cookie
    Middleware->>Middleware: Decrypt & Verify JWT/Session
    alt Session Valid
        Middleware->>ServerAction: Forward Request
        ServerAction->>DB: Fetch Scoped User Data
        DB-->>ServerAction: User Records
        ServerAction-->>Browser: Render Dashboard HTML
    else Session Missing or Expired
        Middleware-->>Browser: HTTP 307 Redirect to /login?redirect=/dashboard
    end
```

---

## 5. Edge & Error Handling Protocol
- **Optimistic Mutation Rollback**: When a user likes, toggles, or updates an entity, update UI immediately; on server rejection (500/timeout), revert state and display alert.
- **Session Expiry During In-Flight Form**: Preserve form input in `sessionStorage` before redirecting to `/login` to avoid user data loss.
- **Offline / Network Interruption**: Display persistent banner "Network disconnected - changes will sync when online".
"""

DESIGN_BRIEF_RAW_TEMPLATE = """# Design Brief & Visual Tokens: __PROJECT_NAME__

## 1. Brand Identity & Visual Aesthetic
- **Design Mood**: <!-- Minimalist Modern | Enterprise SaaS | Dark Cyberpunk | Playful Consumer -->
- **Design Inspiration / Benchmarks**: <!-- e.g. Linear, Stripe, Vercel, Apple -->
- **Density**: <!-- Compact (Data-heavy) | Comfortable (Standard SaaS) | Spacious (Marketing) -->

---

## 2. Color Palette & The 60-30-10 Rule

```
┌────────────────────────────────────────────────────────┐
│ 60% DOMINANT BACKGROUND                                │
│ Clean, calming surface providing breathing room        │
│                                                        │
│   ┌──────────────────────────────────────────────┐     │
│   │ 30% STRUCTURAL / CARDS / SIDEBARS            │     │
│   │ Defined surfaces, borders, elevated cards    │     │
│   │                                              │     │
│   │     ┌──────────────────────────────────┐     │     │
│   │     │ 10% ACCENT / CTA BUTTONS         │     │     │
│   │     │ High contrast focal interaction  │     │     │
│   │     └──────────────────────────────────┘     │     │
│   └──────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
```

| Token Role | Tailwind Class / CSS Variable | Hex / HSL Value | Usage Description |
| :--- | :--- | :--- | :--- |
| **Background (60%)** | `bg-background` / `--bg` | `#0f172a` (Dark) / `#f8fafc` (Light) | App shell, body canvas |
| **Surface / Card (30%)**| `bg-card`, `bg-muted` | `#1e293b` (Dark) / `#ffffff` (Light) | Sidebar, table cards, modal dialogs |
| **Accent / CTA (10%)** | `bg-primary`, `text-primary-foreground` | `#3b82f6` (Vibrant Blue) | Primary action buttons, active tabs |
| **Semantic Success** | `text-emerald-500`, `bg-emerald-500/10` | `#10b981` | Completed badges, success toasts |
| **Semantic Error** | `text-rose-500`, `bg-rose-500/10` | `#f43f5e` | Form errors, destructive actions |
| **Semantic Warning** | `text-amber-500`, `bg-amber-500/10` | `#f59e0b` | Caution banners, trial expiration |

---

## 3. Typography Hierarchy & Font Families
- **Display / Heading Font**: <!-- Inter, Plus Jakarta Sans, Geist, Cal Sans -->
- **Body Font**: <!-- Inter, Geist, System UI -->
- **Monospace Font**: <!-- JetBrains Mono, Fira Code, Geist Mono -->

| Level | Size (Desktop / Mobile) | Weight | Line Height | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Display H1** | `text-4xl md:text-5xl` | 700 / Bold | 1.15 | Hero landing titles |
| **Page H2** | `text-2xl md:text-3xl` | 600 / SemiBold | 1.25 | Main page headers |
| **Section H3** | `text-lg md:text-xl` | 600 / SemiBold | 1.35 | Card & modal titles |
| **Body Base** | `text-base` (16px) | 400 / Regular | 1.50 | Standard paragraph copy |
| **Caption / Small**| `text-xs` or `text-sm` | 500 / Medium | 1.40 | Form labels, table cells, metadata |

---

## 4. Spacing, Elevation & Component Tokens
- **Base Border Radius**: `rounded-lg` (8px) for buttons/inputs, `rounded-xl` (12px) for cards.
- **Card Shadow**: `shadow-sm` border-subtle in light mode; `border border-slate-800` in dark mode.
- **Focus Rings**: `focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2`.
- **Minimum Tap Target**: 44 x 44px for all touch/clickable surfaces.

---

## 5. Bi-directional (LTR / RTL) Layout Integrity
- **Mandatory Rule**: All spacing, alignment, and positioning MUST use **CSS Logical Properties** (ADR-003):
  * Use `ms-*` / `me-*` instead of `ml-*` / `mr-*`.
  * Use `ps-*` / `pe-*` instead of `pl-*` / `pr-*`.
  * Use `text-start` / `text-end` instead of `text-left` / `text-right`.
  * Use `start-0` / `end-0` instead of `left-0` / `right-0`.
"""

BACKEND_SCHEMA_RAW_TEMPLATE = """# Backend Schema & Data Model: __PROJECT_NAME__

## 1. Storage Architecture & Strategy
- **Database Engine**: <!-- PostgreSQL 16+ / MySQL 8+ / SQLite / Supabase -->
- **ORM / Driver**: <!-- Prisma / Drizzle ORM / Eloquent -->
- **Migration Strategy**: Version-controlled migrations, forward-only in production.
- **Isolation / Multitenancy**: <!-- Tenant ID column scoping / Row-Level Security (RLS) -->

---

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    ORGANIZATION ||--o{ USER : "employs"
    USER ||--o{ POST : "authors"
    USER ||--o{ SESSION : "owns"

    ORGANIZATION {
        uuid id PK
        string name
        string slug UK
        datetime created_at
    }

    USER {
        uuid id PK
        uuid organization_id FK
        string email UK
        string password_hash
        string role
        datetime created_at
        datetime updated_at
    }

    SESSION {
        string id PK
        uuid user_id FK
        datetime expires_at
        datetime created_at
    }

    POST {
        uuid id PK
        uuid user_id FK
        string title
        text content
        string status
        datetime created_at
        datetime updated_at
    }
```

---

## 3. Schema DDL / Table Definitions

### Table: `users`
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_org_id ON users(organization_id);
CREATE INDEX idx_users_email ON users(email);
```

---

## 4. Indexing Strategy & Query Optimization
- **Index Invariant**: Every foreign key column MUST have a corresponding index.
- **Query Hotpaths**: Unique indexes on lookup fields (`email`, `slug`).
- **Composite Indexes**: Composite index on `(organization_id, status)` for fast dashboard filtering.

---

## 5. Data Integrity & Lifecycle Rules
- **Foreign Key Cascades**: Parent organization deletion cascades to child users/posts (`ON DELETE CASCADE`).
- **Soft Deletes**: Inactive accounts flag `deleted_at TIMESTAMP NULL` to preserve historical billing audit logs.
- **Immutable Timestamps**: `created_at` immutable; `updated_at` automated via trigger or ORM hooks.
"""

PLAN_RAW_TEMPLATE = """# Implementation Plan: __PROJECT_NAME__

## 1. Execution Dependency Graph

```
 Phase 1: Foundations & Schema
         │
         ▼
 Phase 2: Domain Services & Auth Boundary
         │
         ▼
 Phase 3: UI Shell & Design System
         │
         ▼
 Phase 4: Feature Integration & 5-State Flows
         │
         ▼
 Phase 5: Verification, Chaos Testing & Quality Gates
```

---

## 2. Phase 1 — Foundations & Data Layer
- [ ] **Task 1.1**: Initialize database schema and run initial migrations (`05-BACKEND_SCHEMA.md`).
- [ ] **Task 1.2**: Configure environment variables, database connections, and ORM client.
- [ ] **Task 1.3**: Seed base development data (test user, admin role, sample entities).

---

## 3. Phase 2 — Core Domain & Auth Boundary
- [ ] **Task 2.1**: Implement authentication session verification and middleware route guards.
- [ ] **Task 2.2**: Implement input validation schemas (Zod / Form Requests) for all endpoints.
- [ ] **Task 2.3**: Build core data services with anti-IDOR authorization checks.

---

## 4. Phase 3 — UI Shell & Design System
- [ ] **Task 3.1**: Configure Tailwind CSS tokens, 60-30-10 color palette, and font scales (`04-DESIGN_BRIEF.md`).
- [ ] **Task 3.2**: Enforce CSS Logical Properties for RTL/LTR bi-directional compatibility.
- [ ] **Task 3.3**: Build reusable atomic UI primitives (Buttons, Inputs, Modals, Cards).

---

## 5. Phase 4 — Feature Workflows & 5-State Pages
- [ ] **Task 4.1**: Build User Journey 1 according to `03-APP_FLOW.md`.
  - [ ] Implement Idle, Loading, Success, Error, and Empty states.
- [ ] **Task 4.2**: Build User Journey 2 with optimistic UI updates and rollback handlers.
- [ ] **Task 4.3**: Implement client-side and server-side validation error displays.

---

## 6. Phase 5 — Quality Gates & Pre-Flight Clearance
- [ ] **Task 5.1**: Run unit test battery (`python scripts/agent_os.py test`).
- [ ] **Task 5.2**: Run adversarial chaos negative assertion audit (`python scripts/agent_os.py chaos-audit`).
- [ ] **Task 5.3**: Run static guard analysis (`python scripts/agent_os.py scan`).
- [ ] **Task 5.4**: Run pre-flight clearance (`python scripts/agent_os.py preflight`).
"""


def get_templates(project_name: str) -> Dict[str, str]:
    """Generates the 6 standardized pre-code document templates."""
    return {
        "01-PRD.md": PRD_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
        "02-TRD.md": TRD_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
        "03-APP_FLOW.md": APP_FLOW_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
        "04-DESIGN_BRIEF.md": DESIGN_BRIEF_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
        "05-BACKEND_SCHEMA.md": BACKEND_SCHEMA_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
        "06-IMPLEMENTATION_PLAN.md": PLAN_RAW_TEMPLATE.replace("__PROJECT_NAME__", project_name),
    }


def init_precode(target_dir: Path, project_name: str, force: bool = False) -> Dict[str, Any]:
    """Initializes the 6-document pre-coding package in the target directory."""
    target_dir.mkdir(parents=True, exist_ok=True)
    templates = get_templates(project_name)
    created_files = []
    skipped_files = []

    for filename, content in templates.items():
        file_path = target_dir / filename
        if file_path.exists() and not force:
            skipped_files.append(str(file_path))
        else:
            file_path.write_text(content, encoding="utf-8")
            created_files.append(str(file_path))

    return {
        "project_name": project_name,
        "target_dir": str(target_dir),
        "created_files": created_files,
        "skipped_files": skipped_files,
        "success": True,
    }


def detect_security_tier(project_name: str, project_type: str = "") -> int:
    """
    Auto-selects the OWASP ASVS security tier based on project type or name:
    - Tier 1 (ASVS L1): Public Landing Page, Portfolio, Static Marketing Site
    - Tier 2 (ASVS L2): Standard Web App, SaaS, CMS, E-Commerce, Dashboard
    - Tier 3 (ASVS L3): High-Assurance LMS, SMS (School Management), FinTech, ERP, Healthcare
    """
    combined = f"{project_name} {project_type}".lower()
    tier3_keywords = ("lms", "sms", "school", "learning", "fintech", "payment", "bank", "wallet", "erp", "health", "medical", "gov")
    tier1_keywords = ("landing", "portfolio", "brochure", "static", "promo", "waitlist")
    if any(k in combined for k in tier3_keywords):
        return 3
    if any(k in combined for k in tier1_keywords):
        return 1
    return 2


def get_root_governance_templates(project_name: str, tier: int = 2, project_type: str = "web") -> Dict[str, str]:
    """Returns project-root MASTER.md, DESIGN.md, and tiered SECURITY.md templates."""
    tier_labels = {
        1: "Tier 1 (OWASP ASVS Level 1 — Public Landing Page / Portfolio Baseline)",
        2: "Tier 2 (OWASP ASVS Level 2 — Standard SaaS / CMS / Full-Stack Production)",
        3: "Tier 3 (OWASP ASVS Level 3 — High-Assurance LMS / SMS / FinTech / ERP)",
    }
    tier_label = tier_labels.get(tier, tier_labels[2])

    master_md = f"""# Project Master Rules & Modular Architecture (`MASTER.md`): {project_name}

## 1. Project Identity & Scope Hierarchy
- **Project Name**: {project_name}
- **Project Type**: {project_type.upper()}
- **Active Security Posture**: {tier_label} (see [`SECURITY.md`](./SECURITY.md))
- **Design System Contract**: See [`DESIGN.md`](./DESIGN.md)
- **Rule Precedence**: Global Agent OS Rules (`GEMINI.md`) govern engineering discipline; this `MASTER.md`, `DESIGN.md`, and `SECURITY.md` govern **project-specific client, architecture, and reusability rules**.

---

## 2. The 6-Pillar Code Quality Law (Every Line of Code)
Every edit in this repository—even a 1-line change—must honor this exact priority order:
1. **Readability**: Clear over clever. Code must be understood in **30 seconds by a Junior Developer**.
2. **Reusability (Practical 2+ Rule)**: If a UI element (`Button`, `Card`, `Modal`, `Badge`, `DataTable`), page section (`Header`, `HeroSection`, `Footer`), or backend service/query is used **2+ times**, extract it into a standalone reusable file. Never over-abstract raw CSS tokens (such as fonts) into wrapper components.
3. **Maintainability**: Strict separation between UI rendering, business services, and database persistence.
4. **Scalability**: Bounded queries (pagination/limits), indexed foreign keys, and zero N+1 loops.
5. **Security**: Enforced per [`SECURITY.md`](./SECURITY.md) ({tier_label}).
6. **Performance**: Fast initial load (LCP <= 2.5s), minimal client JS, and zero layout shift.

---

## 3. Single-Component-Per-File Modularity & 2–3 Line Header Contract
1. **Zero Monolith Files**: Never bundle `Header`, `HeroSection`, `Features`, `Footer`, or reusable cards inside `App.jsx`, `page.tsx`, or a single backend file. Every component lives in its own file.
2. **Mandatory 2–3 Line Component Header**: Every reusable Frontend component, Backend service/controller, or DB model begins with:
   ```tsx
   /**
    * Purpose: [Concise 1-line summary of what this component/module does]
    * Reused In: [e.g., Public Landing Page, Admin Dashboard, Course Catalog]
    * Key Props/Inputs: [Primary props or parameters required to use it]
    */
   ```

---

## 4. Shared Admin Dashboard <-> Public Landing Page Contracts
- **Layout Isolation**: Public pages (`(public)/*`) and Admin Dashboard (`/admin/*`) use strictly separate layout shells (`PublicNavbar`/`PublicFooter` vs. `AdminSidebar`/`AdminNavbar`).
- **Shared Primitives & Data Contracts**: Both surfaces reuse `components/ui/` primitives (`Button`, `Card`, `Badge`, `Modal`) and shared TypeScript/DTO data contracts so a junior developer building the Landing Page can seamlessly consume Admin-managed data.
"""

    design_md = f"""# Project Design System & Reusable UI Token Contract (`DESIGN.md`): {project_name}

## 1. Visual Direction & 60-30-10 Color Architecture
- **60% Dominant Canvas (`bg-background`)**: Clean, high-contrast surface (`#f8fafc` Light / `#090d16` Dark).
- **30% Structural Surface (`bg-card`, `bg-muted`)**: Elevated containers, sticky navbar, sticky sidebar, and modals (`#ffffff` Light / `#111827` Dark). Never nest `<Card>` inside `<Card>`.
- **10% Primary Accent (`bg-primary`)**: Interactive focal CTAs, active nav indicators, and primary buttons (`#2563eb`).
- **Semantic Status Tokens**: Success (`#10b981`), Warning (`#f59e0b`), Danger (`#ef4444`).

---

## 2. Typography Scale (CSS Tokens — Never Component Wrappers)
- **Display / Headings**: Bold geometric sans/display (`clamp(1.75rem, 3vw, 3rem)`, `tracking-tight`, `text-wrap: balance`, `mt > mb`).
- **Body Copy**: Clean readable sans (`1rem` / `16px`, `leading-relaxed`, `65–75ch` max measure).
- **Numeric & Table Data**: Enforce `tabular-nums` (`font-variant-numeric: tabular-nums`) on all prices, counts, dates, and IDs.
- *Practical Reusability Note*: Fonts and colors are shared via CSS variables / Tailwind tokens—never wrap plain text fonts in pointless custom wrapper components.

---

## 3. Reusable UI Primitive Catalog (2+ Reuse Threshold)
Every component used **2+ times** across sections lives in `src/components/ui/` (one component per file with a 2–3 line top description):
1. **`Button`**: Variants (`primary`, `secondary`, `outline`, `ghost`, `danger`), sizes (`sm`, `md`, `lg`), loading spinner lock (`min-h-[44px]`).
2. **`Card`**: Elevated surface container with consistent border radius (`rounded-xl`), padding (`p-6`), and optional header/footer slots.
3. **`Badge`**: Borderless informational tag or semantic status pill (`Active`, `Pending`, `Completed`, `Error`).
4. **`Modal` & `Toast`**: Accessible dialog and toast feedback (native `window.alert()` / `window.confirm()` are strictly forbidden).
5. **`DataTable`**: Responsive `overflow-x-auto` wrapper, sticky header, `2–4 words + ...` cell truncation, and all 5 UI states (`Idle`, `Loading`, `Success`, `Error`, `Empty`).

---

## 4. Layout & Bilingual (RTL / LTR) Logical CSS Rules
- **Hero Viewport**: `min-h-[calc(100dvh-var(--navbar-height))]` with zero vertical overflow.
- **Sticky Shells**: Public Navbar (`sticky top-0 z-50 overflow-x-clip`); Admin Sidebar (`lg:sticky lg:top-0 lg:h-dvh`).
- **CSS Logical Properties Only**: Enforce `ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start`, `text-end`.
"""

    if tier == 1:
        tier_controls = """## 2. Tier 1 (OWASP ASVS L1 — Public / Landing Page) Mandatory Controls
1. **Zero Hardcoded Secrets**: Never commit API keys, SMTP credentials, or tokens in client/server code; use `.env`.
2. **Contact / Lead Form Protection**: Validate and sanitize all form inputs server-side (email, phone digits, message length) and enforce rate limiting / anti-spam protection.
3. **XSS & Third-Party Script Hygiene**: Escape all dynamic output; enforce Content-Security-Policy (CSP), HTTPS/HSTS, and `rel="noopener noreferrer"` on external links.
4. **Dependency Integrity**: Verify every npm/composer/pip package exists in the official registry before installation."""
    elif tier == 3:
        tier_controls = """## 2. Tier 3 (OWASP ASVS L3 — High-Assurance LMS / SMS / FinTech / ERP) Mandatory Controls
1. **Strict Server-Side Identity & Multi-Role Isolation (Anti-IDOR)**:
   - Derive `user_id`, `tenant_id`/`school_id`, and `role` (`Student`, `Instructor`, `Parent`, `Admin`) strictly from the server session—never from client request payloads.
   - Scope every database read, update, and delete to the authenticated tenant and role boundary.
2. **Financial, Grade & Ledger Integrity (Zero-Float + ACID Locking)**:
   - Never use `float`/`double` for tuition, fees, balances, or grades; use integer subunits (cents/piastres) or `DECIMAL(12,2)`.
   - Wrap all multi-table mutations, balance updates, and seat/enrollment allocations in ACID transactions with pessimistic row locking (`SELECT ... FOR UPDATE` / `lockForUpdate()`) and idempotency keys.
3. **Protected Content, Exams & Safe File Uploads**:
   - Validate file MIME types and magic bytes, enforce strict size caps, store uploads outside the public web root with randomized names, and serve private LMS/SMS documents via signed/authorized URLs.
4. **Immutable Audit Trail & Error Boundaries**:
   - Log all role changes, grade/payment mutations, and deletions to an immutable audit log. Never leak stack traces or raw SQL errors to the client."""
    else:
        tier_controls = """## 2. Tier 2 (OWASP ASVS L2 — Standard SaaS / CMS / E-Commerce) Mandatory Controls
1. **Server-Side Auth & Anti-IDOR Scoping**:
   - Derive `user_id` and `role` (`Admin`, `Editor`, `User`) strictly from the authenticated server session—never from client payloads.
   - Enforce RBAC guards on both UI controls and backend endpoints/Server Actions.
2. **Boundary Validation & Parameterized Queries**:
   - Validate all incoming payloads via strict schemas (Zod, FormRequest, Pydantic) and use parameterized ORM/SQL queries exclusively.
3. **Safe Media Uploads & Session Security**:
   - Enforce MIME/size validation, randomized storage filenames, old-file cleanup on update/delete, and `HttpOnly` + `SameSite` session cookies.
4. **Zero Raw Error Leakage**:
   - Return structured user-friendly validation errors (`422`) and generic `500` messages while logging internal details server-side."""

    security_md = f"""# Project Security Governance (`SECURITY.md`): {project_name}

## 1. Active Security Profile
- **Project**: {project_name}
- **Security Tier**: **{tier_label}**
- **Enforcement**: Automatically checked by `clean-code-guard`, `next-server-action-guard` / `pest-security-guard`, and `python scripts/agent_os.py sentinel`.

---

{tier_controls}

---

## 3. AI Coding Agent Security Invariants
- Read this `SECURITY.md` before writing or modifying any route, controller, Server Action, form, or database query.
- Never bypass authentication, disable CSRF/validation guards, or return mock `"status": "ok"` fixtures in production paths.
"""

    return {
        "MASTER.md": master_md,
        "DESIGN.md": design_md,
        "SECURITY.md": security_md,
    }


def init_root_governance(
    target_dir: Path,
    project_name: str,
    tier: Optional[int] = None,
    project_type: str = "web",
    force: bool = False,
) -> Dict[str, Any]:
    """Scaffolds MASTER.md, DESIGN.md, and tiered SECURITY.md at the project root."""
    target_dir.mkdir(parents=True, exist_ok=True)
    resolved_tier = tier if tier in (1, 2, 3) else detect_security_tier(project_name, project_type)
    templates = get_root_governance_templates(project_name, tier=resolved_tier, project_type=project_type)
    created_files: List[str] = []
    skipped_files: List[str] = []

    for filename, content in templates.items():
        file_path = target_dir / filename
        if file_path.exists() and not force:
            skipped_files.append(str(file_path))
        else:
            file_path.write_text(content, encoding="utf-8")
            created_files.append(str(file_path))

    return {
        "project_name": project_name,
        "security_tier": resolved_tier,
        "target_dir": str(target_dir),
        "created_files": created_files,
        "skipped_files": skipped_files,
        "success": True,
    }


def audit_root_governance(target_dir: Path) -> Dict[str, Any]:
    """Audits project root for MASTER.md, DESIGN.md, and tiered SECURITY.md."""
    checks: List[Dict[str, Any]] = []
    findings: List[str] = []
    found_docs: Dict[str, str] = {}
    missing: List[str] = []

    for doc in ROOT_GOVERNANCE_DOCS:
        p = target_dir / doc
        if not p.is_file():
            missing.append(doc)
        else:
            found_docs[doc] = p.read_text(encoding="utf-8", errors="ignore")

    all_exist = len(missing) == 0
    checks.append({
        "name": "1. Root Governance Files Present (MASTER.md, DESIGN.md, SECURITY.md)",
        "passed": all_exist,
        "message": "All 3 root governance files present" if all_exist else f"Missing: {', '.join(missing)}",
    })
    if not all_exist:
        findings.append(f"Missing root project governance files: {', '.join(missing)}")

    master_txt = found_docs.get("MASTER.md", "")
    master_ok = bool(re.search(r"Readability", master_txt, re.IGNORECASE)) and bool(
        re.search(r"Reusability|Single-Component-Per-File", master_txt, re.IGNORECASE)
    )
    checks.append({
        "name": "2. MASTER.md Reusability & Junior-Readability Rules",
        "passed": master_ok,
        "message": "Verified 6-Pillar Priority & 1-Component-Per-File rules" if master_ok else "MASTER.md missing Readability/Reusability rules",
    })
    if not master_ok:
        findings.append("MASTER.md must define the 6-Pillar Priority (Readability, Reusability) and Single-Component-Per-File modularity.")

    design_txt = found_docs.get("DESIGN.md", "")
    design_ok = bool(re.search(r"Typography|Color|60-30-10", design_txt, re.IGNORECASE)) and bool(
        re.search(r"Button|Card|Reusable", design_txt, re.IGNORECASE)
    )
    checks.append({
        "name": "3. DESIGN.md Tokens & Reusable UI Primitives Catalog",
        "passed": design_ok,
        "message": "Verified color/typography tokens and reusable Button/Card primitives" if design_ok else "DESIGN.md missing tokens or reusable primitives",
    })
    if not design_ok:
        findings.append("DESIGN.md must specify typography/color tokens and reusable UI primitives (Button, Card).")

    sec_txt = found_docs.get("SECURITY.md", "")
    sec_ok = bool(re.search(r"Tier\s*[123]|ASVS", sec_txt, re.IGNORECASE))
    checks.append({
        "name": "4. SECURITY.md Tiered Security Profile (Tier 1 / 2 / 3)",
        "passed": sec_ok,
        "message": "Verified explicit Security Tier in SECURITY.md" if sec_ok else "SECURITY.md missing Security Tier (Tier 1/2/3)",
    })
    if not sec_ok:
        findings.append("SECURITY.md must declare its active Security Tier (Tier 1 Landing, Tier 2 SaaS/CMS, or Tier 3 LMS/SMS/FinTech).")

    passed_checks = sum(1 for c in checks if c["passed"])
    total_checks = len(checks)
    score = round((passed_checks / total_checks) * 100, 1)
    return {
        "passed": score == 100.0,
        "score": score,
        "passed_checks": passed_checks,
        "total_checks": total_checks,
        "checks": checks,
        "findings": findings,
        "target_dir": str(target_dir),
    }


def audit_precode(target_dir: Path) -> Dict[str, Any]:
    """
    Deeply audits a pre-code directory against the 8 quality invariants:
    1. All 6 files exist
    2. Zero lingering placeholder markers ([TODO], [TBD], [NEEDS INPUT])
    3. PRD contains User Stories and Acceptance Criteria (Given/When/Then)
    4. TRD contains Stack Decisions & Security Boundaries
    5. App Flow contains Mermaid diagram AND the 5 UI States
    6. Design Brief contains 60-30-10 Color Tokens and RTL/LTR specifications
    7. Backend Schema contains Mermaid ERD or SQL DDL with keys
    8. Implementation Plan contains phased checklist tasks
    """
    if not target_dir.exists() or not target_dir.is_dir():
        return {
            "passed": False,
            "score": 0.0,
            "checks": [{"name": "Directory Existence", "passed": False, "message": f"Directory not found: {target_dir}"}],
            "findings": [f"Target precode directory '{target_dir}' does not exist."]
        }

    checks: List[Dict[str, Any]] = []
    findings: List[str] = []

    # Check 1: File Existence (6/6)
    missing_files = []
    found_docs: Dict[str, str] = {}
    for doc in CANONICAL_DOCS:
        p = target_dir / doc
        if not p.is_file():
            missing_files.append(doc)
        else:
            try:
                found_docs[doc] = p.read_text(encoding="utf-8")
            except Exception as e:
                missing_files.append(f"{doc} (read error: {e})")

    file_exist_pass = len(missing_files) == 0
    checks.append({
        "name": "1. All 6 Canonical Documents Present",
        "passed": file_exist_pass,
        "message": "All 6 documents found" if file_exist_pass else f"Missing: {', '.join(missing_files)}"
    })
    if not file_exist_pass:
        findings.append(f"Missing canonical documents: {', '.join(missing_files)}")

    # Check 2: Absence of Placeholder Markers
    placeholder_pattern = re.compile(r"\[TODO\]|\[TBD\]|\[NEEDS INPUT\]|<!--.*?-->", re.DOTALL)
    unfilled_markers = {}
    for doc, content in found_docs.items():
        matches = placeholder_pattern.findall(content)
        suspicious = [m for m in matches if any(k in m.upper() for k in ["TODO", "TBD", "NEEDS INPUT", "WHO USES", "WHY DOES", "REPLACE"])]
        if suspicious:
            unfilled_markers[doc] = len(suspicious)

    placeholders_pass = len(unfilled_markers) == 0
    checks.append({
        "name": "2. Zero Lingering Placeholder Markers",
        "passed": placeholders_pass,
        "message": "No unfilled TODO/TBD markers" if placeholders_pass else f"Unfilled markers in: {', '.join(f'{k} ({v})' for k, v in unfilled_markers.items())}"
    })
    if not placeholders_pass:
        findings.append(f"Documents contain unfinalized placeholders: {list(unfilled_markers.keys())}")

    # Check 3: PRD Completeness
    prd_content = found_docs.get("01-PRD.md", "")
    has_user_stories = bool(re.search(r"User Story|As a|I want to", prd_content, re.IGNORECASE))
    has_acceptance_criteria = bool(re.search(r"Given.*?When.*?Then", prd_content, re.DOTALL | re.IGNORECASE))
    has_out_of_scope = bool(re.search(r"Out of Scope", prd_content, re.IGNORECASE))
    prd_pass = has_user_stories and has_acceptance_criteria and has_out_of_scope
    checks.append({
        "name": "3. PRD Quality & Given/When/Then Acceptance Criteria",
        "passed": prd_pass,
        "message": "Verified User Stories, G/W/T criteria, and Out-of-Scope boundaries" if prd_pass else "PRD missing User Stories, Given/When/Then criteria, or Out-of-Scope section"
    })
    if not prd_pass:
        findings.append("01-PRD.md lacks formal User Stories with Given/When/Then acceptance criteria or Out-of-Scope boundaries.")

    # Check 4: TRD Stack & Security Invariants
    trd_content = found_docs.get("02-TRD.md", "")
    has_stack = bool(re.search(r"Frontend|Backend|Database", trd_content, re.IGNORECASE))
    has_security = bool(re.search(r"Security|Authentication|IDOR|Sanitization", trd_content, re.IGNORECASE))
    trd_pass = has_stack and has_security
    checks.append({
        "name": "4. TRD Tech Stack & Security Boundary Invariants",
        "passed": trd_pass,
        "message": "Verified Stack Selection and Security Boundary rules" if trd_pass else "TRD missing stack details or security invariants"
    })
    if not trd_pass:
        findings.append("02-TRD.md lacks explicit technology stack specifications or security boundary invariants.")

    # Check 5: App Flow State Machine & 5 UI States
    flow_content = found_docs.get("03-APP_FLOW.md", "")
    has_mermaid_flow = "```mermaid" in flow_content and ("flowchart" in flow_content or "graph" in flow_content or "sequenceDiagram" in flow_content)
    missing_states = [s for s in MANDATORY_UI_STATES if not re.search(r"\b" + s + r"\b", flow_content, re.IGNORECASE)]
    states_pass = len(missing_states) == 0
    flow_pass = has_mermaid_flow and states_pass
    checks.append({
        "name": "5. App Flow Diagram & 5 Mandatory UI States",
        "passed": flow_pass,
        "message": "Verified Mermaid sequence/flowchart and all 5 UI states (Idle, Loading, Success, Error, Empty)" if flow_pass else f"Missing Mermaid diagram or UI states: {missing_states}"
    })
    if not flow_pass:
        findings.append(f"03-APP_FLOW.md requires a Mermaid interaction flowchart and all 5 UI states. Missing: {missing_states}")

    # Check 6: Design Brief Tokens & RTL/LTR Logical Properties
    design_content = found_docs.get("04-DESIGN_BRIEF.md", "")
    has_palette = bool(re.search(r"60-30-10|Palette|Color", design_content, re.IGNORECASE))
    has_typography = bool(re.search(r"Typography|Font", design_content, re.IGNORECASE))
    has_rtl_logical = bool(re.search(r"RTL|Logical Properties|ms-|ps-|text-start", design_content, re.IGNORECASE))
    design_pass = has_palette and has_typography and has_rtl_logical
    checks.append({
        "name": "6. Design Tokens, 60-30-10 Rule & RTL CSS Logical Properties",
        "passed": design_pass,
        "message": "Verified color hierarchy, typography scale, and RTL logical properties" if design_pass else "Design Brief missing 60-30-10 palette, typography scale, or RTL logical guidelines"
    })
    if not design_pass:
        findings.append("04-DESIGN_BRIEF.md missing 60-30-10 palette tokens, typography hierarchy, or CSS Logical Properties (RTL/LTR).")

    # Check 7: Backend Schema ERD & DDL
    schema_content = found_docs.get("05-BACKEND_SCHEMA.md", "")
    has_erd = ("erDiagram" in schema_content) or ("CREATE TABLE" in schema_content.upper()) or ("model " in schema_content)
    has_keys = bool(re.search(r"PRIMARY KEY|PK|REFERENCES|FK|@id|@relation", schema_content, re.IGNORECASE))
    schema_pass = has_erd and has_keys
    checks.append({
        "name": "7. Backend Schema ERD & Relational Integrity (PK/FK)",
        "passed": schema_pass,
        "message": "Verified ERD / DDL definitions with Primary and Foreign Keys" if schema_pass else "Schema missing ERD, DDL, or PK/FK definitions"
    })
    if not schema_pass:
        findings.append("05-BACKEND_SCHEMA.md missing Mermaid erDiagram or DDL table definitions with primary/foreign keys.")

    # Check 8: Implementation Plan Checklists
    plan_content = found_docs.get("06-IMPLEMENTATION_PLAN.md", "")
    task_checkboxes = re.findall(r"-\s*\[[ xX]\]", plan_content)
    plan_pass = len(task_checkboxes) >= 5
    checks.append({
        "name": "8. Implementation Plan Dependency-Ordered Task Battery",
        "passed": plan_pass,
        "message": f"Verified {len(task_checkboxes)} executable checklist tasks across phases" if plan_pass else f"Insufficient checklist tasks ({len(task_checkboxes)} found, minimum 5 required)"
    })
    if not plan_pass:
        findings.append(f"06-IMPLEMENTATION_PLAN.md lacks sufficient phased checklist tasks (only {len(task_checkboxes)} found).")

    passed_checks = sum(1 for c in checks if c["passed"])
    total_checks = len(checks)
    score = round((passed_checks / total_checks) * 100, 1)

    return {
        "passed": score == 100.0,
        "score": score,
        "passed_checks": passed_checks,
        "total_checks": total_checks,
        "checks": checks,
        "findings": findings,
        "target_dir": str(target_dir)
    }


def print_audit_report(result: Dict[str, Any]):
    """Pretty prints the pre-coding audit report."""
    print("=" * 68)
    print("      AGENT OS - 6 PRE-CODING PILLARS QUALITY AUDIT        ")
    print("=" * 68)
    print(f"Target Directory: {result.get('target_dir', 'Unknown')}")
    print("-" * 68)
    
    for check in result["checks"]:
        icon = "[PASS]" if check["passed"] else "[FAIL]"
        print(f"{icon:<7} {check['name']}")
        print(f"        -> {check['message']}")

    print("-" * 68)
    score = result.get("score", 0.0)
    print(f"PRE-CODING READINESS SCORE: {score}% ({result.get('passed_checks', 0)}/{result.get('total_checks', 0)} checks)")
    
    if result["passed"]:
        print("[CLEARANCE GRANTED] All 6 Pre-Coding Pillars 100% verified.")
        print(">> Execution Lock unlocked: Safe to proceed with code implementation.")
    else:
        print("[CLEARANCE DENIED] Resolve the following findings before coding:")
        for idx, f in enumerate(result.get("findings", []), 1):
            print(f"  {idx}. {f}")
    print("=" * 68)


def main():
    parser = argparse.ArgumentParser(description="Agent OS 6 Pre-Coding Pillars Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="Precode commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize the 6 pre-coding document templates")
    init_parser.add_argument("project_name", help="Name of the project or feature")
    init_parser.add_argument("--dir", dest="target_dir", default=None, help="Target directory (default: docs/precode/<project_name>)")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Audit the 6 pre-coding documents for completeness")
    audit_parser.add_argument("target_dir", nargs="?", default=None, help="Directory containing the 6 documents")

    # status command
    status_parser = subparsers.add_parser("status", help="Display status of the 6 pre-coding documents")
    status_parser.add_argument("target_dir", nargs="?", default=None, help="Directory containing the 6 documents")

    # init-root command (MASTER.md, DESIGN.md, SECURITY.md)
    init_root_parser = subparsers.add_parser("init-root", help="Initialize root MASTER.md, DESIGN.md, and tiered SECURITY.md")
    init_root_parser.add_argument("project_name", help="Name of the project")
    init_root_parser.add_argument("--type", dest="project_type", default="web", help="Project type (landing, cms, saas, lms, sms, fintech)")
    init_root_parser.add_argument("--tier", dest="tier", type=int, choices=[1, 2, 3], default=None, help="Security tier override (1, 2, or 3)")
    init_root_parser.add_argument("--dir", dest="target_dir", default=None, help="Target project root directory (default: current directory)")
    init_root_parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    # audit-root command
    audit_root_parser = subparsers.add_parser("audit-root", help="Audit root MASTER.md, DESIGN.md, and SECURITY.md")
    audit_root_parser.add_argument("target_dir", nargs="?", default=None, help="Project root directory")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    if args.subcommand == "init-root":
        target_path = Path(args.target_dir) if args.target_dir else Path.cwd()
        res = init_root_governance(
            target_path,
            args.project_name,
            tier=args.tier,
            project_type=args.project_type,
            force=args.force,
        )
        print(f"[SUCCESS] Initialized Root Governance (Tier {res['security_tier']}) for '{args.project_name}' at: {target_path}")
        for f in res["created_files"]:
            print(f"  + {Path(f).name}")
        sys.exit(0)

    elif args.subcommand == "audit-root":
        target_path = Path(args.target_dir) if args.target_dir else Path.cwd()
        res = audit_root_governance(target_path)
        print_audit_report(res)
        sys.exit(0 if res["passed"] else 1)

    elif args.subcommand == "init":
        if args.target_dir:
            target_path = Path(args.target_dir)
        else:
            safe_name = re.sub(r"[^\w\-]", "_", args.project_name.lower())
            target_path = WORKSPACE_ROOT / "docs" / "precode" / safe_name
        
        res = init_precode(target_path, args.project_name, force=args.force)
        print(f"[SUCCESS] Initialized 6 Pre-Coding Pillars for '{args.project_name}' at: {target_path}")
        print(f"Created {len(res['created_files'])} file(s):")
        for f in res["created_files"]:
            print(f"  + {Path(f).name}")
        if res["skipped_files"]:
            print(f"Skipped {len(res['skipped_files'])} existing file(s) (use --force to overwrite).")

    elif args.subcommand in ["audit", "status"]:
        if args.target_dir:
            target_path = Path(args.target_dir)
        else:
            default_base = WORKSPACE_ROOT / "docs" / "precode"
            if default_base.exists():
                subdirs = [d for d in default_base.iterdir() if d.is_dir()]
                if subdirs:
                    target_path = subdirs[0]
                else:
                    target_path = default_base
            else:
                target_path = Path.cwd()

        res = audit_precode(target_path)
        print_audit_report(res)
        sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
