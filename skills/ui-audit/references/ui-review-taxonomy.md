# Frontend UI Review Taxonomy & Audit Reference

This document serves as the technical reference taxonomy for the `/ui-audit` workflow. It details the inspection checklists, common anti-patterns, and evaluation criteria across all 8 audit dimensions.

---

## 1. Visual Consistency & Design Tokens

### Inspection Checklist
- [ ] **Color Tokens**: Check for hardcoded hex, rgb, or hsl values bypassing the design system or Tailwind palette (e.g., `#3b82f6` instead of `bg-primary` or `var(--primary)`).
- [ ] **Typography Scale**: Verify font sizes, line heights, font weights, and letter spacing correspond to defined scales (`text-sm`, `text-base`, `leading-relaxed`, etc.).
- [ ] **Spacing Scale**: Check padding, margins, and gaps for ad-hoc pixel values (e.g., `p-[13px]`, `gap-[7px]`) violating the 4px/8px design grid.
- [ ] **Border Radii & Borders**: Look for mismatched border radii (mixing `rounded-sm`, `rounded-xl`, `rounded-full` arbitrarily) and border color drift (`border-gray-200` vs `border-slate-300`).
- [ ] **Shadows & Elevation**: Check for custom `box-shadow` styles overriding standard elevation tokens (`shadow-sm`, `shadow-md`, `shadow-lg`).
- [ ] **Component Variant Alignment**: Verify that common components (buttons, badges, alerts) use consistent variants across pages rather than custom one-off class combinations.
- [ ] **Dark Mode / Theme Parity**: Check that foreground and background colors use semantic tokens that adapt properly across light and dark modes (e.g., avoiding hardcoded `bg-white` without `dark:bg-zinc-900`).

---

## 2. Responsive Behavior & Viewport Breakpoints

### Inspection Checklist
- [ ] **Fixed Widths**: Detect fixed widths (`w-[600px]`, `min-w-[800px]`, `width: 500px`) that cause horizontal scrolling or layout clipping on mobile viewports (< 640px).
- [ ] **Inflexible Flex/Grid Layouts**: Look for flex containers without `flex-wrap` where items exceed viewport width, or grid templates with fixed columns (`grid-cols-4` without responsive modifiers like `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`).
- [ ] **Breakpoint Consistency**: Ensure breakpoint modifiers follow a consistent mobile-first progression (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`) without contradictory reverse overrides.
- [ ] **Text Truncation & Wrapping**: Check long headings, user names, or descriptions for missing `truncate`, `line-clamp-*`, or `break-words` causing container bursting.
- [ ] **Modal & Drawer Sizing**: Verify dialogs and drawers adjust max-width and margins appropriately on mobile viewports (e.g., full screen or bottom sheet on mobile, centered modal on desktop).
- [ ] **Table Responsiveness**: Check data tables for horizontal overflow handling (`overflow-x-auto`, card transformation on mobile, or stacked layouts).
- [ ] **Touch Target Sizing**: Ensure interactive targets on touch devices meet the minimum 44×44px or 48×48px dimension guideline.

---

## 3. Accessibility (WCAG 2.2 Level AA)

### Inspection Checklist
- [ ] **Semantic Markup**: Verify proper HTML element usage (`<button>`, `<a>`, `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`, `<dialog>`) instead of clickable `<div>` or `<span>` without ARIA.
- [ ] **Heading Hierarchy**: Ensure logical heading order (`<h1>` through `<h6>`) with exactly one `<h1>` per page and no skipped levels (e.g., `<h1>` directly to `<h3>`).
- [ ] **Form Labels & Associations**: Check that every `<input>`, `<textarea>`, and `<select>` has an explicit `<label for="...">` or `aria-label` / `aria-labelledby`.
- [ ] **Alternative Text**: Verify all meaningful `<img>` elements have informative `alt` text; decorative images must have `alt=""` or `aria-hidden="true"`.
- [ ] **Keyboard Navigability**: Verify all interactive elements are reachable via `Tab` key and activatable via `Enter` or `Space`.
- [ ] **Focus Visible Indicators**: Detect `outline-none` or `focus:outline-none` without replacement `focus-visible:ring-2` focus rings.
- [ ] **Color Contrast**: Check text vs background contrast meets WCAG AA minimums (4.5:1 for normal text, 3:1 for large text/icons).
- [ ] **ARIA Roles & Attributes**: Check for redundant, invalid, or misused ARIA (e.g., `role="button"` without `tabIndex={0}` and keyboard handlers; missing `aria-expanded` on accordion/dropdown triggers).
- [ ] **Reduced Motion Support**: Verify heavy animations or parallax effects respect `@media (prefers-reduced-motion: reduce)` or `motion-reduce:*` utilities.

---

## 4. Interactions & Micro-Behavior

### Inspection Checklist
- [ ] **Interactive State Completeness**: Check that interactive elements support `:hover`, `:focus-visible`, `:active`, and `:disabled` states with perceptible visual transitions.
- [ ] **Disabled State Treatment**: Verify disabled buttons have `disabled` attribute or `aria-disabled="true"`, reduced opacity, `cursor-not-allowed`, and prevented click handlers.
- [ ] **Non-Semantic Clickables**: Identify `<div onClick={...}>` or `<span onClick={...}>` lacking keyboard listeners (`onKeyDown`), `role="button"`, and `tabIndex`.
- [ ] **Link Destinations**: Check for empty links (`href="#"`, `href=""`), missing routing wrappers (`next/link` vs native `<a>`), or external links without `rel="noopener noreferrer"`.
- [ ] **Loading & Debounce Feedback**: Verify buttons performing async operations provide immediate loading indicators (spinner, text swap) and disable repeat clicks.
- [ ] **Micro-Feedback**: Confirm that copy-to-clipboard, toggle switches, and bookmarks provide immediate visual confirmation of state changes.

---

## 5. Forms, Inputs & Feedback

### Inspection Checklist
- [ ] **Input Constraints & Types**: Check that inputs use appropriate `type` attributes (`email`, `tel`, `number`, `url`, `password`) with appropriate `autoComplete` attributes.
- [ ] **Validation Feedback**: Ensure validation errors are rendered in close proximity to the affected input, linked via `aria-describedby` or `aria-errormessage`.
- [ ] **Accessible Error States**: Ensure error states do not rely solely on color (e.g., include an icon or descriptive error text).
- [ ] **Input Focus Traps**: Ensure dropdowns, datepickers, and comboboxes do not trap keyboard focus unexpectedly or dismiss on tab.
- [ ] **Toast / Notification Accessibility**: Verify toasts have `role="status"` or `role="alert"` and `aria-live="polite"` so screen readers announce them.

---

## 6. Layout, Content & The 6-State Matrix

### Inspection Checklist
- [ ] **Idle State**: Clean default rendering without flickering or unstyled layout shifts (CLS).
- [ ] **Loading State**: Content skeletons or loading spinners that preserve layout geometry and prevent content jumps.
- [ ] **Empty State**: Dedicated, informative empty states for lists, search results, filters, or collections with clear calls-to-action (CTA).
- [ ] **Success State**: Clear confirmation messages or views upon successful mutations (order placed, settings saved).
- [ ] **Error State**: Informative, user-friendly error views with retry mechanisms rather than generic or cryptic error dumps.
- [ ] **Edge & Overflow States**: Boundary conditions such as zero items, 10,000 items, extremely long text strings without spaces, missing avatar images.
- [ ] **Z-Index Hierarchy**: Check for uncontrolled `z-[9999]` stacking fights between navigation bars, modals, tooltips, and floating widgets.

---

## 7. Navigation & Information Architecture

### Inspection Checklist
- [ ] **Active Link Highlighting**: Verify current page is clearly indicated in navigation bars, sidebars, and breadcrumbs with `aria-current="page"` and distinct styling.
- [ ] **Skip Links**: Check for a "Skip to main content" link accessible via keyboard at the top of the DOM.
- [ ] **Breadcrumb Trails**: Verify breadcrumb lists use `<nav aria-label="Breadcrumb">` and `<ol>` semantic markup.
- [ ] **Mobile Menu Behavior**: Check that mobile hamburger drawers trap focus when open, close on `Escape`, prevent background body scroll, and restore focus on close.
- [ ] **Route Consistency**: Check that page layouts (header, footer, sidebar) do not jump or reload ungracefully between sibling routes.

---

## 8. Localization & RTL (Bidirectional Layouts)

### Inspection Checklist
- [ ] **CSS Logical Properties**: Detect physical CSS utilities (`ml-*`, `mr-*`, `pl-*`, `pr-*`, `left-*`, `right-*`, `text-left`, `text-right`) that break layout mirroring when `<html dir="rtl">` is set.
- [ ] **Bidirectional Replacements**: Verify use of logical utilities (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start`, `text-end`).
- [ ] **Icon Mirroring**: Identify directional icons (arrows, chevrons, back buttons) that must be mirrored in RTL (`rtl:rotate-180`), while non-directional icons (clocks, checkmarks, search) remain unmirrored.
- [ ] **Hardcoded Strings**: Detect user-visible text hardcoded in JSX/HTML instead of utilizing translation hooks (e.g., `useTranslations()`, `t('key')`, `i18n.t()`).
- [ ] **Text Overflow in Translated Languages**: Ensure button and badge containers do not clip when text expands in languages with longer average word lengths (e.g., German, Arabic).
