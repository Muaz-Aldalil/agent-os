# UI Audit Report Template

This document provides the standard templates for generating `docs/ui-audits/<timestamp>/report.md` and `docs/ui-audits/<timestamp>/manual-browser-checklist.md`.

---

## 1. Structure of `report.md`

```markdown
# Frontend UI Quality Audit Report

- **Run ID**: `<YYYY-MM-DD-HHmmss>`
- **Audit Date**: `<YYYY-MM-DD>`
- **Frontend Stack**: `<Discovered Framework, Styling System, UI Library>`
- **Total Confirmed Findings**: `<Count>`
- **Severity Breakdown**: Critical: `<N>`, High: `<N>`, Medium: `<N>`, Low: `<N>`
- **Unverified Observations**: `<Count>`

---

## 1. Executive Summary

### Overview & Systemic Issues
<Provide a high-level summary of the frontend architecture health. Highlight systemic defects that span across multiple routes or shared components (e.g., missing focus rings across all forms, physical CSS spacing breaking RTL globally, or hardcoded container widths breaking mobile viewports).>

### Severity Breakdown
| Severity | Count | Primary Impact |
| :--- | :---: | :--- |
| **Critical** | `<N>` | Blocks core user flows, extreme accessibility barrier, severe layout collapse |
| **High** | `<N>` | Significant usability defect, WCAG AA violation, major responsive failure |
| **Medium** | `<N>` | Noticeable visual defect, inconsistent component variant, missing empty/error state |
| **Low** | `<N>` | Minor visual polish, token drift, subtle spacing inconsistency |

### Highest-Priority Issues (Address First)
1. **[UI-001] <Title>**: <1-sentence rationale why this must be resolved immediately.>
2. **[UI-002] <Title>**: <1-sentence rationale why this must be resolved immediately.>

---

## 2. Audit Scope & Coverage Matrix

### Discovered Frontend Architecture
- **Framework & Routing**: `<e.g. Next.js 15 App Router with [locale] dynamic routing>`
- **Styling & Design Tokens**: `<e.g. Tailwind CSS v4 with custom CSS variables in globals.css>`
- **UI Components**: `<e.g. Radix UI primitives with custom Tailwind wrappers>`
- **Internationalization & Directionality**: `<e.g. next-intl with ar/en locales, dir="rtl" on html>`
- **Testing & Diagnostics Available**: `<e.g. npm run lint (ESLint), npm test (Vitest)>`

### Inspected Touchpoints
- **Routes Inspected**:
  - `/<route-1>` (`<file-path>`)
  - `/<route-2>` (`<file-path>`)
- **Shared Layouts & Spines**:
  - `<layout-file-path>`
- **Shared Components Analyzed**:
  - `<component-path>` (consumed by `<routes>`)

### Uninspected Areas & Limitations
- **Area**: `<Path or Route>`
- **Reason Not Inspected**: `<e.g., dynamic server-only dashboard requiring authenticated session database seed>`

---

## 3. Detailed Confirmed Findings

### [UI-001] <Descriptive Title of the Defect>
- **Category**: `<Visual Consistency | Responsive Behavior | Accessibility | Interactions | Forms & Feedback | Layout & Content | Navigation & IA | Localization & RTL>`
- **Severity**: `<Critical | High | Medium | Low>`
- **Confidence**: `<High | Medium>`
- **Affected Routes**: `/<route-a>`, `/<route-b>`
- **Primary Source Locations**:
  - `[<file-path>](file:///<absolute-path>#L<start>-L<end>)` (Component: `<ComponentName>`)

#### Evidence from Implementation
```<language>
// <Excerpt showing exact offending code>
```

#### Current Behavior
<Explain what the code currently renders or does.>

#### Expected Behavior & Standard
<Explain what the code should do, citing the applicable design token, WCAG criterion, or responsive requirement.>

#### User Impact
<Why this matters to real users: screen reader failure, mobile horizontal scroll, confusion, lack of feedback.>

#### Root Cause Analysis
- **Root Cause Classification**: `<Confirmed Root Cause | Hypothesis>`
- **Diagnosis**: <Exact structural explanation of why the defect occurs.>

#### Recommended Correction
<Actionable architectural advice on how to resolve the root cause while preserving surrounding styles and invariants.>

#### Generated Implementation Prompt
- **Prompt File**: [`prompts/UI-001-<short-description>.md`](./prompts/UI-001-<short-description>.md)

---

## 4. Unverified Observations

> [!NOTE]
> The following items represent suspected issues identified during static analysis where conclusive determination requires a running browser, specific responsive runtime viewport, or live data state. They are NOT counted as confirmed violations.

### [OBS-001] <Observation Title>
- **Suspected Area**: `<File path / Route>`
- **Missing Evidence**: `<e.g., whether parent CSS grid forces overflow when text expands>`
- **Recommended Verification Procedure**: `<Exact browser or runtime check to confirm or dismiss>`

---

## 5. Recommended Implementation Order & Dependency Graph

1. **Phase 1: Critical & Foundational Blockers**
   - **UI-001**: Fixes `<component>`, unblocking `<routes>`.
2. **Phase 2: High-Impact Accessibility & Responsive Fixes**
   - **UI-002**: Resolves mobile navigation drawer focus trap.
3. **Phase 3: Visual Polish & Design Token Harmonization**
   - **UI-003**: Standardizes button variant tokens.

---
```

---

## 2. Structure of `manual-browser-checklist.md`

```markdown
# Manual Browser Verification Checklist

> [!IMPORTANT]
> **Audit Execution Disclosure**: The `/ui-audit` command is a static, code-grounded inspection engine. In accordance with tool constraints, **no browser was launched and no browser automation was executed** during the audit.
>
> The test matrix below specifies the exact manual browser verification checks that the human technical owner should perform to visually evaluate responsive layouts, dynamic animations, and interactive focus states.

| Test ID | Route / URL | Target Viewport / Device | User Interaction / Steps | Expected Visual & Behavioral Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-001** | `/<route>` | Mobile (375px × 667px) | Open route and scroll vertically | No horizontal overflow scrollbar; text wraps cleanly within cards | [ ] |
| **TC-002** | `/<route>` | Desktop (1280px × 800px) | Tab through header navigation via keyboard | Distinct focus ring appears on each link; no focus is lost | [ ] |
| **TC-003** | `/<route>` | Mobile / Desktop | Toggle locale to Arabic (`/ar/...`) | Layout mirrors correctly; icons flip if directional; no physical alignment clipping | [ ] |
| **TC-004** | `/<route>` | All Viewports | Submit empty contact form | Inline error messages appear beneath inputs with clear visual distinction | [ ] |
```
