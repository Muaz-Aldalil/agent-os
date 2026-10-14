# 04 — Design Brief & Visual Tokens: Agent OS Beginner Handbook & CMS Frontend Armor

## 1. Design Aesthetic & Mood
- **Handbook Aesthetic**: High-signal, zero-jargon, visual Recipe Book formatted with scannable comparison tables, traffic-light status badges (🔴 🟡 🟢), clear 💬 **Paste in AI Chat** vs. 💻 **Paste in Terminal** callouts, and bilingual English + Arabic explanations.
- **Generated CMS & App Aesthetic**: Powered by `/muaz-skill` (`ui-ux-pro-max` engine with 91 styles, 169 palettes, 72 font pairings), strictly forbidding generic AI-slop gradients and enforcing intentional hierarchy across light and dark modes.

---

## 2. The 60-30-10 Color Rule
Every UI built or fixed via `/feature-fe`, `/feature-febe`, `/feature-full`, `/start-project`, or `/fix-ui` must enforce the **60-30-10 Color Allocation**:
- **60% Dominant Background (`bg-background` / `#F8FAFC` light, `#0B0F19` dark)**: Primary app canvas and main scrollable content area.
- **30% Structural Surface (`bg-card`, `bg-muted` / `#FFFFFF` light, `#111827` dark)**: Sticky top navbar, sticky sidebar panel, data table containers, and form cards with subtle `border-border` (`#E2E8F0` / `#1E293B`) separation.
- **10% Accent CTA (`bg-primary` / e.g. `#2563EB`)**: Primary action buttons ("+ Create New", "Save Changes"), active sidebar indicator, and focus rings.
- **Semantic Tokens**:
  - **Success**: `#16A34A` (`text-emerald-600` / `bg-emerald-50`)
  - **Warning**: `#D97706` (`text-amber-600` / `bg-amber-50`)
  - **Error**: `#DC2626` (`text-red-600` / `bg-red-50`)

---

## 3. Typography Hierarchy
- **Display / Headings**: Geometric or editorial sans (`Inter` / `Plus Jakarta Sans` for LTR; `Cairo` / `Tajawal` / `IBM Plex Sans Arabic` for RTL Arabic), fluid scale from `1.25rem` (`20px`) section titles to `2.25rem` (`36px`) page headers, `font-semibold` (`600`), tight tracking (`-0.02em` in LTR, `0` in Arabic).
- **Body & Table Cells**: `0.875rem` (`14px`) to `1rem` (`16px`), line-height `1.5` (`leading-relaxed` for Arabic script legibility).
- **Monospace / IDs / Code**: `JetBrains Mono` / `Fira Code` (`0.8125rem` / `13px`) for order IDs, timestamps, and copy-paste prompt blocks.

---

## 4. Component Tokens & CMS Layout Shell Standards
- **Border Radii & Elevation**: `rounded-lg` (`8px`) for inputs/buttons, `rounded-xl` (`12px`) for CMS cards/tables, subtle `shadow-sm` elevation.
- **Tap Targets**: Minimum `44x44px` (`min-h-11 min-w-11`) on all mobile buttons, pagination controls, sidebar toggles, and table action icons.
- **Mandatory CMS App Shell Architecture**:
  1. **App Wrapper**: `min-h-dvh flex flex-col lg:flex-row bg-background`
  2. **Sticky Sidebar Panel**: ` lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto` on desktop; off-canvas drawer (`fixed inset-y-0 start-0 z-50`) with backdrop on `<1024px`.
  3. **Main Column Wrapper**: `flex-1 min-w-0 flex flex-col` (prevents wide tables from blowing out viewport width).
  4. **Sticky Top Navbar**: `sticky top-0 z-40 h-16 bg-card/80 backdrop-blur border-b` staying pinned during vertical scroll.
  5. **CMS Data Tables**: Outer `w-full overflow-x-auto rounded-xl border` + sticky `<thead>` + pinned action column + pagination footer.
  6. **CMS Forms**: Responsive grid (`grid-cols-1 md:grid-cols-2 gap-6`) + sticky bottom action bar (`sticky bottom-0 z-30 bg-card/95 backdrop-blur py-4 border-t`) for Save/Cancel.

---

## 5. RTL/LTR CSS Logical Properties
All components must pass `/rtl-logical-guard` with zero physical directional classes:
- Use `ms-*` / `me-*` instead of `ml-*` / `mr-*`.
- Use `ps-*` / `pe-*` instead of `pl-*` / `pr-*`.
- Use `start-*` / `end-*` instead of `left-*` / `right-*`.
- Use `text-start` / `text-end` instead of `text-left` / `text-right`.
- Use `border-s` / `border-e` and `rounded-s-*` / `rounded-e-*`.
