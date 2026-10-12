# UI Implementation Prompt Template

This template defines the mandatory 10-section structure for all generated implementation prompts created by `/ui-audit` under `docs/ui-audits/<timestamp>/prompts/UI-XXX-<short-description>.md`.

---

```markdown
# Implementation Prompt: [UI-XXX] <Descriptive Title>

## A. Role
You are acting as a senior **<Specialized Role, e.g. Frontend Accessibility Specialist | Responsive Layout Architect | Design Systems Engineer | UI Interaction Engineer>**.
You write clean, minimal, production-grade frontend code adhering strictly to the project's existing design tokens, component architecture, and engineering standards.

---

## B. Task & Objective
- **Issue Identifier**: `[UI-XXX]`
- **Title**: `<Brief Title>`
- **Severity**: `<Critical | High | Medium | Low>`
- **Intended Outcome**: `<Clear statement of what fixing this issue achieves>`
- **Definition of Success**: `<Precise, binary condition verifying resolution>`

---

## C. Context & Evidence
- **Problem Statement**: <Explain what the current code does and why it is deficient.>
- **Why It Matters to Users**: <Direct user-facing consequence, e.g., screen reader inability to activate controls, mobile viewport horizontal overflow, or lack of visual feedback.>
- **Expected Behavior & Standards**: <Applicable WCAG 2.2 AA criterion, design token system rule, or responsive layout standard.>
- **Root Cause Analysis**:
  - **Classification**: `<Confirmed Root Cause | Verified Implementation Gap | Hypothesized Runtime Behavior>`
  - **Analysis**: <Detailed explanation of the flaw in the markup, styling, or state machine.>

---

## D. Exact Location & Affected Scope
- **Primary Source Files**:
  - `path/to/component.tsx` (Component: `<ComponentName>`, Line(s): `<start-end>`)
- **Related / Sibling Files**:
  - `path/to/styles.css`
- **Affected Routes & Consumer Views**:
  - `/<route-1>`
  - `/<route-2>`
- **Architectural Relationship**:
  <Explain how this component fits into the route layouts, whether it is a shared UI atom, a composite molecule, or a page-level container.>

---

## E. Recommended Solution & Invariants
- **Proposed Correction**:
  <Step-by-step description of the architectural or styling fix.>
- **Reusability & Tokens**:
  - Reuse existing design tokens: `<e.g., bg-primary, text-muted-foreground, rounded-lg>`
  - Reuse existing components: `<e.g., Button variant="outline", DialogClose>`
- **Invariants (What Must NOT Change)**:
  - Do NOT alter unrelated styling, margin conventions, or layout wrappers outside the component.
  - Do NOT break existing desktop layout while fixing mobile breakpoints.
  - Preserve all existing props, exports, and contracts.

---

## F. Implementation Task Checklist
- [ ] **Step 1: Code Reality Verification** — Open and inspect the primary file and surrounding imports before touching any lines.
- [ ] **Step 2: Markup & Semantics** — Update HTML tags, ARIA attributes, and semantic roles.
- [ ] **Step 3: Styling & Responsive Layout** — Apply Tailwind utilities / CSS rules ensuring mobile-first responsive behavior and CSS logical properties.
- [ ] **Step 4: Interaction & State Handling** — Wire focus-visible indicators, disabled states, and keyboard event handlers.
- [ ] **Step 5: Shared Usage Harmonization** — Verify all consumers of the modified component render without regressions.

---

## G. Tools, Skills, and MCP Capabilities
> [!NOTE]
> Only verified tools and skills available in the active environment are recommended below.

- **Recommended Project Skills**:
  - `<e.g. rtl-logical-guard: Use to verify bidirectional CSS logical properties (ms/me/ps/pe)>`
  - `<e.g. muaz-skill: Use for design token alignment and UI palette guidance>`
  - `<e.g. clean-code-guard: Use after editing to audit code parsimony and avoid LLM code smells>`
- **Applicable MCP Servers & Tools**:
  - `<e.g. chrome-devtools-mcp (evaluate_script, get_css_styles): For post-implementation DOM inspection if connected>`
  - `<If no MCP is required: "No external MCP required. Standard local file editing and diagnostic commands suffice.">`

---

## H. Acceptance Criteria
- [ ] **AC-1 (Functional / Structural)**: `<Specific element rendered with proper tag/attributes>`
- [ ] **AC-2 (Responsive / Layout)**: `<No horizontal overflow at 375px viewport; clean wrapping>`
- [ ] **AC-3 (Accessibility)**: `<Reachable via keyboard Tab, visible focus indicator, WCAG 2.2 AA compliant>`
- [ ] **AC-4 (Preservation)**: `<All existing component props, test assertions, and sibling views remain untouched>`

---

## I. Verification Plan
- **Automated Diagnostics**:
  - Run existing project linting: `<e.g., npm run lint>`
  - Run existing component tests: `<e.g., npm test -- ComponentName.test.tsx>`
- **Manual Verification Steps for Human Evaluator**:
  1. Navigate to: `<Route URL>`
  2. Viewport: `<Mobile 375px | Tablet 768px | Desktop 1280px>`
  3. Action: `<Perform interaction, tab through controls, or resize window>`
  4. Expected Outcome: `<Verified behavior>`

---

## J. Implementation Boundaries
- **Strict Scope Limit**: Touch ONLY the files listed in Section D.
- **Zero Collateral Refactoring**: Do not reorganize imports, rename unrelated types, or clean up untouched code.
- **Verification Before Delivery**: Verify all acceptance criteria before concluding the implementation turn.
```
