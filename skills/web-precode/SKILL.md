---
name: web-precode
description: >-
  The 6 Pre-Coding Pillars Specification & Architecture Blueprint for web applications.
  Enforces authoring, structuring, and verifying all 6 essential documents (PRD, TRD,
  App Flow with 5-State UI Matrix, Design Brief with 60-30-10 tokens, Backend Schema with ERD,
  and Implementation Plan) before writing any code.
---

# The 6 Pre-Coding Pillars Specification Protocol

Official skill for the **Agent OS Pre-Coding Engine** (`python scripts/agent_os.py precode`).

This protocol guarantees that neither human nor AI writes a single line of application code without a complete, verified architectural blueprint. It eliminates the "impatient coding syndrome" and prevents architectural drift, missing edge states, and security vulnerabilities.

---

## 1. Constitutional Zero-Code Invariant

Under [engineering-constitution.md](file:///D:/Skills/.agents/rules/engineering-constitution.md) §3.9, writing application code without an audited pre-coding specification is an immediate **P0 Gate Failure**.

Before coding begins, the project or feature MUST possess 6 verified documents located at `docs/precode/<project_name>/`:

```
 docs/precode/<project_name>/
 ├── 01-PRD.md                 # Product Requirements (What & Why)
 ├── 02-TRD.md                 # Technical Requirements (Stack, Security, Budgets)
 ├── 03-APP_FLOW.md            # UX State Machine (Mermaid Flows & 5-State Matrix)
 ├── 04-DESIGN_BRIEF.md        # Visual System (60-30-10 Tokens & RTL Logical CSS)
 ├── 05-BACKEND_SCHEMA.md      # Data Persistence (ERD, DDL, Indexes & Cascades)
 └── 06-IMPLEMENTATION_PLAN.md # Execution Sequencing (Phased Task Battery)
```

---

## 2. The 6 Pillars Specification Standard

### Pillar 1: Product Requirements Document (`01-PRD.md`)
* **Focus**: What the product does, why it exists, and who it serves.
* **Mandatory Sections**:
  1. **Executive Summary & Value Proposition**: Core problem solved in 1–2 paragraphs.
  2. **Target Personas & User Journeys**: Primary user persona, pain points, and core journey.
  3. **Functional Requirements**: Prioritized as P0 (Must Have), P1 (Should Have), P2 (Post-v1).
  4. **Formal User Stories with Acceptance Criteria**: Written in strict `Given / When / Then` format.
  5. **Explicitly Out of Scope**: Non-negotiable list of excluded features to defeat feature creep.

### Pillar 2: Technical Requirements Document (`02-TRD.md`)
* **Focus**: Tools, frameworks, protocols, and architectural boundaries.
* **Mandatory Sections**:
  1. **System Topology & Rendering Strategy**: Server Components vs Client Components, SSR vs SPA.
  2. **Tech Stack Matrix**: Frontend, Backend, Database, Styling, State Management, Auth.
  3. **Third-Party APIs**: Payment processors (Stripe), email (Resend), object storage (S3/R2).
  4. **Security Boundary Invariants**: Server-side auth derivation, anti-IDOR checks, Zod validation, CSP/CORS headers.
  5. **Performance Budgets**: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1, initial JS bundle < 100kB gzip.

### Pillar 3: App Flow & State Machine (`03-APP_FLOW.md`)
* **Focus**: Screen navigation, event triggers, and system responses over time.
* **Mandatory Sections**:
  1. **Route Map**: Complete table of public, protected, and dynamic routes.
  2. **Mermaid Flowchart**: Visual state machine showing click triggers and decision nodes.
  3. **The 5-State UI Matrix**: Every core view MUST explicitly document:
     * **Idle**: Pristine resting state before user input.
     * **Loading / Pending**: Debounced submit lock, skeleton loaders, or progress indicator.
     * **Success**: Router redirect, cache revalidation, success toast.
     * **Error / Rejection**: 401/403 redirects, 422 inline input alerts, 500 retry buttons.
     * **Empty**: Zero-data illustrated view with a clear primary CTA.
  4. **Session & Auth Sequence**: Session expiration, token refresh, and protected route redirection.
  5. **Edge & Resilience Protocols**: Offline detection and optimistic mutation rollback handlers.

### Pillar 4: Design Brief & Visual Tokens (`04-DESIGN_BRIEF.md`)
* **Focus**: Aesthetic, art direction, typography, color hierarchy, Craft Floor, and spatial rhythm (separating durable product truth in `01-PRD.md` / `PRODUCT.md` from replaceable surface visual tokens in `04-DESIGN_BRIEF.md` / `DESIGN.md`).
* **Mandatory Sections**:
  1. **Visitor Mode & Art Direction**:
     * **Primary Visitor Mode**: `Operate` (dense utility/dashboard/CMS), `Persuade` (landing/conversion), or `Read` (editorial/docs).
     * **Subject Inventory (8–12 Facts) & Competitor Test**: *"On this page, [something that belongs to the subject] becomes [the layout/interactive device]."* Plus **One Live Interactive Thing** built from the subject's idea.
     * **Argument-First Copy Deck & Headline Arithmetic**: Section list written as Claim + Proof; hero headlines hold to `<= 2 lines` (~32 chars median).
  2. **The 60-30-10 Color Rule & Surface Contrast**:
     * **60% Dominant Background**: Tinted neutral canvas (`bg-background` — never pure `#000` or flat untinted gray; avoid default Wave 3 `#faf9f5` + `#d97757` terracotta unless explicitly in brand brief).
     * **30% Structural Surface**: Cards, sidebars, modals (`bg-card`, `bg-muted` — never nest cards inside cards).
     * **10% Accent CTA**: Focal interactive elements (`bg-primary`).
     * **Colored Surface Contrast**: Secondary text on colored backgrounds must be hue-tinted or foreground-opacity (`text-primary-foreground/80`), never raw gray.
  3. **Typography Craft Floor**: Font families (Display, Body, Mono) with fluid `clamp()` sizing scales, `65–75ch` body measure, `-0.04em` tracking floor, `text-wrap: balance` on headings, `mt > mb` heading spacing, and `tabular-nums` on all numeric/table data.
  4. **Component Tokens & Browser Surfaces**: Border radii (`rounded-lg`), offset shadows, minimum `44x44px` tap targets, exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`), and global browser surface tokens (`::selection`, `caret-color`, custom scrollbars, `:focus-visible`, `text-underline-offset`).
  5. **RTL/LTR CSS Logical Properties**: Strictly enforcing `ms-*`/`me-*`, `ps-*`/`pe-*`, `text-start`/`text-end`.

### Pillar 5: Backend Schema & Data Model (`05-BACKEND_SCHEMA.md`)
* **Focus**: Entity relationships, persistence, schema migrations, and relational integrity.
* **Mandatory Sections**:
  1. **Storage Engine & Driver**: PostgreSQL / MySQL / SQLite with Prisma / Drizzle / Eloquent.
  2. **Mermaid ERD (`erDiagram`)**: Complete relational graph showing cardinalities (1:1, 1:N, N:M).
  3. **DDL / Table Definitions**: Explicit columns, datatypes, constraints, and defaults.
  4. **Indexing Strategy**: Mandatory indexes on all foreign keys and compound lookup fields.
  5. **Data Integrity & Lifecycle Rules**: Cascade policies (`ON DELETE CASCADE` vs `RESTRICT`), soft deletes (`deleted_at`), and immutable audit timestamps.

### Pillar 6: Implementation Plan (`06-IMPLEMENTATION_PLAN.md`)
* **Focus**: Dependency ordering, critical path, and executable task batteries.
* **Mandatory Sections**:
  1. **Execution Dependency Graph**: Visual phase-by-phase execution path.
  2. **Phase 1**: Foundations, Database Schema & Initial Migrations.
  3. **Phase 2**: Core Domain Services, Auth Boundary & Input Validation.
  4. **Phase 3**: UI Shell, Layouts & Reusable Design System Primitives.
  5. **Phase 4**: Feature Integration, Forms & 5-State Workflows.
  6. **Phase 5**: Quality Verification, Negative Testing & Pre-Flight Clearance.

---

## 3. Interactive Execution Runbook

### Step 1: Initialize the 6 Document Templates
Run the unified CLI scaffolder:
```powershell
python scripts/agent_os.py precode init <project_name>
```

### Step 2: Interactive Product & Architecture Interview
Engage the Human Technical Owner to clarify:
1. What is the core problem and who is the primary persona?
2. If tech stack is unknown, recommend the optimal stack based on the project type:
   * **Content / SaaS with SEO**: Next.js 15 App Router + Tailwind v4 + PostgreSQL + Prisma.
   * **Enterprise / Robust Data Admin**: Laravel 11 + Pest + MySQL + Tailwind.
   * **Real-time / AI Application**: Next.js 15 frontend + Python FastAPI / Agent OS backend.
3. Review the primary user journey and map the 5 UI states.

### Step 3: Populate Documents Iteratively
Write detailed, production-grade specifications into each of the 6 files. Ensure all `<!-- ... -->` placeholder comments and `[TODO]` markers are replaced with concrete details.

### Step 4: Audit & Clearance Gate
Run the automated verification engine:
```powershell
python scripts/agent_os.py precode audit docs/precode/<project_name>
```
The audit checks all 8 invariants:
* [x] 1. All 6 canonical documents exist.
* [x] 2. Zero lingering placeholder markers (`[TODO]`, `[TBD]`, `[NEEDS INPUT]`).
* [x] 3. PRD contains formal User Stories with `Given / When / Then` criteria.
* [x] 4. TRD specifies stack decisions and security boundaries.
* [x] 5. App Flow contains Mermaid diagram AND all 5 UI states (`Idle`, `Loading`, `Success`, `Error`, `Empty`).
* [x] 6. Design Brief contains 60-30-10 palette, typography scale, and RTL logical properties.
* [x] 7. Backend Schema contains Mermaid ERD and relational keys.
* [x] 8. Implementation Plan contains at least 5 phased checklist tasks.

### Step 5: Unlock Execution Lock
Only when the Pre-Coding Readiness Score reaches **100% (CLEARANCE GRANTED)** is the Execution Lock unlocked, permitting code generation via Spec Kit or direct implementation.
