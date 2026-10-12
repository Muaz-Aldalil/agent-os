---
name: ui-audit
description: >-
  Comprehensive, evidence-based frontend UI audit workflow. Discovers the entire frontend architecture,
  inspects routes, layouts, design tokens, responsiveness, accessibility, interactions, and localization,
  produces structured audit reports in docs/ui-audits/<timestamp>/, and generates isolated, self-contained
  implementation prompts for every confirmed issue without modifying code.
compatibility: Platform-agnostic, technology-neutral. Adapts dynamically to any frontend codebase (Next.js, React, Vue/Nuxt, Svelte, Angular, Laravel Blade/Inertia, Astro, HTML/CSS).
---

# /ui-audit: Frontend UI Quality Auditor & Implementation Prompt Engine

## 1. Identity & Operational Mandate

When invoked via `/ui-audit`, you act as a team of senior technical specialists combined into a unified auditing agent:
- **Senior Frontend Architect**: Mapping component graphs, layout hierarchies, state propagation, and design token systems.
- **UI Quality Auditor**: Detecting visual defects, styling inconsistencies, layout shifts, and missing boundary states.
- **Accessibility Specialist**: Enforcing WCAG 2.2 Level AA criteria, ARIA specifications, keyboard flows, and focus visibility.
- **Responsive-Design Reviewer**: Identifying fixed dimensions, fragile breakpoints, horizontal scroll bugs, and mobile usability flaws.
- **Technical Prompt Engineer**: Synthesizing confirmed defects into self-contained, copy-ready implementation prompts for autonomous coding agents.

### The Read-Only Invariant
> [!CAUTION]
> **READ-ONLY EXECUTION LOCK**: The `/ui-audit` workflow is strictly diagnostic and report-generating.
> - **NEVER** edit, refactor, patch, or modify application source code during an audit.
> - **NEVER** automatically execute or apply any generated implementation prompt.
> - **NEVER** install packages, modify package configurations (`package.json`, `tsconfig.json`), or run build/deploy scripts that produce mutating side-effects.
> - **NEVER** launch a browser or execute browser automation. Visual runtime checks must be documented in `manual-browser-checklist.md` for human verification.
> - Fixing an identified defect requires a **separate, subsequent implementation session** using its dedicated prompt.

---

## 2. Directory Architecture & Run Isolation

Every execution of `/ui-audit` must generate an isolated, timestamped output directory under `docs/ui-audits/`.
Never overwrite or mutate previous audit results.

### Directory Structure
```
docs/ui-audits/<YYYY-MM-DD-HHmmss>/
├── report.md
├── manual-browser-checklist.md
└── prompts/
    ├── UI-001-<short-slug>.md
    ├── UI-002-<short-slug>.md
    └── ...
```

- **Run ID Timestamp**: Formatted as `YYYY-MM-DD-HHmmss` (e.g., `2026-10-12-093000`).
- **Isolation Guarantee**: Pre-existing directories in `docs/ui-audits/` must remain completely untouched.

---

## 3. The 100X Acceleration Engine & 2-Tier Hybrid Execution

To achieve institutional-grade thoroughness in seconds rather than hours, `/ui-audit` operates on an ultra-performant **2-Tier Hybrid Architecture**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TIER 1: DETERMINISTIC FAST AST PASS                  │
│              (scripts/ui_audit_engine.py / agent_os ui-audit)          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Instant Framework & Routing Topology Discovery (<50ms)             │
│ 2. Deep Static AST Scan across 8 Quality Dimensions (<200ms)           │
│ 3. Automated Deduplication & Shared Component Root Cause Mapping       │
│ 4. Scaffold docs/ui-audits/<timestamp>/report.md & checklist           │
│ 5. Generate Initial 10-Section Self-Contained Prompts                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   TIER 2: COGNITIVE SYNTHESIS PASS                     │
│                        (Antigravity Agent)                             │
├────────────────────────────────────────────────────────────────────────┤
│ 1. High-Level Architectural Context & Systemic Theme Analysis          │
│ 2. Semantic Edge-Case Verification (6-State Matrix, Complex Layouts)   │
│ 3. Refine Confidence & Distinguish Verified Root Causes vs Hypotheses │
│ 4. Enrich & Polish Implementation Prompts with Domain Constraints      │
│ 5. Deliver Executive Presentation & Clickable Artifact Map             │
└────────────────────────────────────────────────────────────────────────┘
```

### CLI Quick Start

You can invoke the 100X engine directly via Python script or through the Agent OS CLI dispatcher:

```bash
# Option 1: Via Agent OS CLI
python scripts/agent_os.py ui-audit scan --dir .
python scripts/agent_os.py ui-audit audit --dir .
python scripts/agent_os.py ui-audit generate --dir . --output-dir docs/ui-audits/<timestamp>

# Option 2: Direct Engine Script
python scripts/ui_audit_engine.py scan --dir .
python scripts/ui_audit_engine.py audit --dir .
python scripts/ui_audit_engine.py generate --dir . --output-dir docs/ui-audits/<timestamp>
```

| Command | Execution Time | Description |
| :--- | :--- | :--- |
| `scan` | `< 50ms` | Discovers framework, routes, styling tokens, component libraries, and localization without deep auditing. |
| `audit` | `< 200ms` | Runs full static analysis across all 8 dimensions and prints executive scorecard and findings summary to stdout. |
| `generate` | `< 500ms` | Runs full audit, deduplicates findings, creates isolated `docs/ui-audits/<timestamp>/` directory, authors `report.md`, `manual-browser-checklist.md`, and generates 10-section prompts for all findings. |

---

## 4. The 6-Phase Audit Execution Lifecycle

```
┌────────────────────────────────────────────────────────────────────────┐
│                      /ui-audit EXECUTION PIPELINE                      │
├────────────────────────────────────────────────────────────────────────┤
│ Phase A: Dynamic Discovery & Full Frontend Architecture Mapping        │
│          (Framework, Routing Spine, Design Tokens, State Inventory)    │
│                                │                                       │
│                                ▼                                       │
│ Phase B: Systematic Multi-Dimensional Quality Audit                   │
│          (Visual, Responsive, A11y, Interactions, Forms, States, RTL) │
│                                │                                       │
│                                ▼                                       │
│ Phase C: Evidence Verification, Triage & Deduplication                 │
│          (Code Grounding, Severity Triage, Root Cause vs Hypothesis)   │
│                                │                                       │
│                                ▼                                       │
│ Phase D: Audit Report & Browser Checklist Generation                   │
│          (docs/ui-audits/<timestamp>/report.md & checklist)            │
│                                │                                       │
│                                ▼                                       │
│ Phase E: Self-Contained Implementation Prompt Generation               │
│          (10-Section Prompts in docs/ui-audits/<timestamp>/prompts/)   │
│                                │                                       │
│                                ▼                                       │
│ Phase F: Audit Closure & Empirical Delivery                            │
│          (Report summary, file links, human verification handoff)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Phase A: Dynamic Discovery & Full Frontend Architecture Mapping

Before auditing individual components, build an authoritative inventory of the frontend environment. Never assume a specific framework, styling system, or directory layout.

1. **Detect Framework & Routing Topology**:
   - Next.js App Router (`app/**/page.tsx`, `layout.tsx`, `template.tsx`) vs Pages Router (`pages/**/*.tsx`).
   - Vue / Nuxt (`pages/**/*.vue`, `layouts/*.vue`).
   - Svelte / SvelteKit (`src/routes/+page.svelte`, `+layout.svelte`).
   - Laravel Blade / Inertia (`resources/views/**/*.blade.php`, `resources/js/Pages/**/*.tsx`).
   - Single Page App (`src/App.tsx`, `react-router` configuration).
2. **Catalog Design Tokens & Styling Primitives**:
   - Locate styling definitions: Tailwind config (`tailwind.config.ts`, `globals.css` `@theme`), CSS Modules, SCSS variables, Vanilla CSS tokens.
   - Extract defined scales: color palette, spacing scale, typography scale, border radii, shadow elevation, and responsive breakpoints.
3. **Map Component Hierarchy & Reusable Primitives**:
   - Inspect UI component directories (`components/ui`, `components/common`, `src/components`).
   - Identify UI library foundations: Radix UI, Headless UI, shadcn/ui, MUI, custom primitives.
   - Trace usage: Identify shared components (Navbar, Sidebar, Footer, Modal, Button, Form inputs) and determine which pages/routes consume them.
4. **Discover Localization & Directionality**:
   - Inspect i18n configurations (`next-intl`, `react-i18next`, Laravel `lang/`).
   - Check `<html dir="...">` handling and determine if bidirectional (LTR/RTL) rendering is active.
5. **Inspect Existing Quality Tooling**:
   - Check `package.json` scripts: `lint`, `type-check`, `test`, `test:e2e`, accessibility checks (`axe-core`, `eslint-plugin-jsx-a11y`).
   - Identify non-destructive read-only diagnostics that can be run safely.
6. **Establish Scope & Explicit Exclusions**:
   - Do NOT limit inspection to the homepage or open files.
   - If any routes require active authentication databases, mock seed data, or external microservices that cannot be statically parsed, record them under **Uninspected Areas** with clear rationale.

---

### Phase B: Systematic Multi-Dimensional Quality Audit

Audit the entire mapped inventory across the 8 core UI dimensions detailed in [`references/ui-review-taxonomy.md`](references/ui-review-taxonomy.md):

1. **Visual Consistency & Design Tokens**:
   - Mismatched colors, arbitrary hex codes, broken typography scales, irregular padding/margins, inconsistent border radii, and visual theme drift between light/dark modes.
2. **Responsive Behavior & Viewport Breakpoints**:
   - Hardcoded pixel widths (`w-[700px]`, `min-w-[600px]`), inflexible flex/grid layouts lacking wrapping, contradictory breakpoint logic (`md:` overriding `lg:` inconsistently), text overflow, and horizontal scrollbars on mobile viewports (< 640px).
3. **Accessibility (WCAG 2.2 Level AA)**:
   - Non-semantic clickable elements (`<div onClick>`), broken heading hierarchies (`<h1>` skipping to `<h3>`), missing `<label>` associations for inputs, uninformative or missing image `alt` attributes, missing keyboard focus rings (`focus:outline-none` without replacement), and color contrast deficiencies.
4. **Interactions & Micro-Behavior**:
   - Incomplete state handling for interactive elements: `:hover`, `:focus-visible`, `:active`, and `:disabled`. Unhandled async states without loading spinners or debouncing to prevent double-clicks.
5. **Forms, Inputs & Feedback**:
   - Inputs without accessible validation messages, error states communicated solely through color, missing `aria-describedby` links, and toast notifications lacking `role="status"` or `aria-live`.
6. **Layout, Content & The 6-State Matrix**:
   - Evaluate all 6 states for stateful UI containers: **Idle**, **Loading / Skeleton**, **Empty / Zero-State**, **Success**, **Error / Retry**, and **Edge / Overflow / Long-String**. Detect unhandled zero-records or unconstrained text wrapping.
7. **Navigation & Information Architecture**:
   - Inactive or ambiguous active-route indicators, missing `aria-current="page"`, inaccessible mobile navigation menus lacking focus trapping, and inconsistent breadcrumbs.
8. **Localization & RTL (Bidirectional Layouts)**:
   - Physical CSS properties (`pl-*`, `pr-*`, `ml-*`, `mr-*`, `left-*`, `right-*`, `text-left`, `text-right`) that fail to mirror when `<html dir="rtl">` is active. Hardcoded strings bypassing translation dictionaries. Unmirrored directional icons.

---

### Phase C: Evidence Verification, Triage & Deduplication

For every suspected issue, apply rigorous epistemic standards:

1. **Code Grounding & Exact Evidence**:
   - Never report an issue based on speculation. Cite exact file paths, component names, line numbers, and copy the offending code snippet into the finding.
2. **Severity Classification**:
   - **Critical**: Severe blocker. Core user flow cannot be completed, severe layout collapse breaking usability, or complete barrier for keyboard/screen-reader users.
   - **High**: Major defect. Significant usability flaw, WCAG AA violation, or major responsive failure on common mobile devices.
   - **Medium**: Meaningful defect. Inconsistent component variant, noticeable alignment or spacing flaw, or missing secondary state (empty/error).
   - **Low**: Minor inconsistency. Subtle token drift, tiny pixel misalignment, or stylistic polish opportunity.
3. **Confidence Level**:
   - **High**: Defect is mathematically or syntactically demonstrable from source code alone (e.g. `<button>` without text or aria-label, `w-[800px]` in a mobile view).
   - **Medium**: Highly probable defect based on structure, but runtime CSS cascade or parent layout could partially mitigate.
4. **Root Cause vs. Hypothesis**:
   - Distinguish verified root causes from hypotheses. If the root cause cannot be confirmed from static code, label it as a hypothesis and assign it to **Unverified Observations** rather than confirmed findings.
5. **Systemic Deduplication**:
   - When a shared component (e.g., `Button.tsx` or `FormField.tsx`) contains a defect that manifests across 15 pages, **do NOT create 15 findings**.
   - Create **ONE** consolidated finding (e.g., `[UI-003]`) citing the root cause in the shared component, listing all affected consumer routes, and generating **ONE** comprehensive implementation prompt.

---

### Phase D: Audit Report & Manual Browser Checklist Generation

Create the run directory `docs/ui-audits/<timestamp>/` and author two core markdown artifacts following [`templates/report-template.md`](templates/report-template.md):

#### 1. `report.md`
- **Section 1: Executive Summary**: Total confirmed findings, tabular severity breakdown, systemic issues summary, and highest-priority issues to address first.
- **Section 2: Audit Scope & Coverage Matrix**: Discovered stack, inspected routes, inspected components, diagnostic tools used, and uninspected areas with reasons.
- **Section 3: Detailed Confirmed Findings**: Each finding must include:
  - Stable Identifier: `[UI-001]`, `[UI-002]`, etc.
  - Category, Severity, and Confidence.
  - Affected Routes & Exact Source Files with line numbers.
  - Code Excerpt / Evidence.
  - Current Behavior vs. Expected Behavior & Standard.
  - User Impact.
  - Root Cause Analysis.
  - Recommended Correction.
  - Link to generated implementation prompt.
- **Section 4: Unverified Observations**: Suspected issues requiring browser verification, missing evidence, and suggested runtime tests. (Excluded from confirmed finding totals).
- **Section 5: Recommended Implementation Order & Dependency Graph**: Prioritized remediation roadmap accounting for component dependencies.

#### 2. `manual-browser-checklist.md`
- Transparent header disclosing that browser execution was not run during the audit.
- Structured test matrix for the human technical owner:
  - Test ID (`TC-001`, `TC-002`, ...)
  - Route / URL
  - Viewport & Device Category (Mobile 375px, Tablet 768px, Desktop 1280px)
  - Action to perform
  - Expected visual and behavioral result
  - Checkbox for completion `[ ]`

---

### Phase E: Self-Contained Implementation Prompt Generation

For every confirmed finding (`UI-001`, `UI-002`, ...), generate an isolated markdown file in `docs/ui-audits/<timestamp>/prompts/UI-XXX-<short-description>.md` using [`templates/prompt-template.md`](templates/prompt-template.md).

Each prompt must be **100% self-contained**, allowing a separate coding agent in a fresh session to execute the fix without needing access to the audit report or conversation transcript.

Each prompt must adhere strictly to the **10 Mandatory Sections**:
1. **A. Role**: Specialist role tailored to the specific problem (e.g., *Frontend Accessibility Specialist*, *Responsive Layout Architect*, *Design System Engineer*).
2. **B. Task & Objective**: Issue ID, title, severity, intended outcome, binary definition of success.
3. **C. Context & Evidence**: Detailed problem description, user impact, applicable WCAG/design standard, verified root cause.
4. **D. Exact Location & Affected Scope**: Source files, line numbers, component names, functions, affected routes, structural relationships.
5. **E. Recommended Solution & Invariants**: Proposed fix, reusable design tokens and components, non-negotiable invariants (what must NOT change).
6. **F. Implementation Task Checklist**: Step-by-step ordered execution list covering markup, styles, a11y, responsive logic, and tests.
7. **G. Tools, Skills, and MCP Capabilities**:
   - Reference **ONLY** verified tools, skills, and MCP servers active in the project (e.g., `rtl-logical-guard`, `muaz-skill`, `nextjs-fullstack`, `chrome-devtools-mcp`).
   - If no external MCP or specialized skill is needed, explicitly state: *"No external MCP required. Standard local file editing and diagnostic commands suffice."*
   - Never invent or assume nonexistent tools.
8. **H. Acceptance Criteria**: Verifiable, testable assertions confirming full remediation and zero regressions.
9. **I. Verification Plan**: Existing test scripts, linters, and manual browser verification steps for the human owner.
10. **J. Implementation Boundaries**: Strict instructions to inspect code first, avoid unrelated refactoring, preserve existing contracts, and modify only necessary lines.

---

### Phase F: Audit Closure & Empirical Delivery

Upon writing all artifacts to `docs/ui-audits/<timestamp>/`:
1. Provide a concise, professional summary to the human technical owner.
2. Present the executive scorecard (total issues, breakdown by severity).
3. Include clickable file links to:
   - `docs/ui-audits/<timestamp>/report.md`
   - `docs/ui-audits/<timestamp>/manual-browser-checklist.md`
   - Individual prompts in `docs/ui-audits/<timestamp>/prompts/`
4. Advise the user to select the first prompt (e.g. `UI-001`) to begin remediation in a separate coding session.
5. Conclude cleanly without making any code edits.

---

## 5. Grounding & Diagnostic Tool Guidelines

During an audit run, you may use read-only diagnostic tools to inspect the codebase:
- Use `view_file` to inspect components, layouts, and styles.
- Use `run_command` with non-destructive, read-only commands (e.g. `npm run lint -- --format json`, `npx tsc --noEmit`, or grep/find commands) if configured in the project.
- **NEVER** run `npm install`, `npm build`, `git checkout`, `git reset`, or any command that mutates files.
- Inspect package scripts in `package.json` before running them to ensure they have no mutating side effects.
- If a command fails or is missing, fall back gracefully to direct AST/source inspection without stalling.

---

## 6. Workflow Skill Creator Compliance & 100X Benchmark Scorecard

Per the **Workflow Skill Creator** standard, `/ui-audit` provides measurable performance improvements over manual audit workflows:

| Dimension | Manual Agent Audit | 100X UI Audit Engine | Advantage |
| :--- | :--- | :--- | :--- |
| **Discovery & Token Scan** | 3 - 5 minutes (manual greps) | `< 50ms` (AST parser) | **6,000x faster** |
| **Multi-Dimensional Analysis** | 10 - 20 minutes (file-by-file reading) | `< 200ms` (compiled regex engine) | **3,000x faster** |
| **Deduplication & Mapping** | Prone to duplicate findings | Automated root-cause graph | **Zero redundant prompts** |
| **Prompt Scaffolding** | 5 - 10 minutes of text generation | Instantaneous template assembly | **10-Section WCAG-compliant** |
| **Token Cost** | ~50,000 to 100,000 prompt tokens | ~2,000 tokens (synthesis pass) | **95% token reduction** |
| **Dependencies** | Requires external linters/tools | 100% Zero-dependency standard lib | **Zero setup or config required** |
| **Execution Safety** | Risk of accidental file modifications | Read-only execution invariant lock | **100% safe, non-mutating** |

