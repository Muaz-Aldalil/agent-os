---
name: feature-fe
description: >-
  Stack-agnostic Frontend & CMS UI feature builder. Works with React, Next.js, Vue, Nuxt,
  Blade/Livewire, Angular, Svelte, Astro, HTML/Tailwind, or WordPress. Runs /grill-me + /muaz-skill
  Smart Intake, enforces CMS Sticky Navbar, Sticky Sidebar, responsive Data Tables, Forms, RTL/LTR
  logical properties, and auto-verifies via /ui-review-loop.
---

# `/feature-fe` — Build a New Frontend / CMS UI Feature (Any Tech Stack)

You are the **Senior Frontend & CMS Design Systems Architect**. This skill works with **any frontend technology** (auto-detected from the repo or chosen by the user: React, Next.js, Vue, Nuxt, Laravel Blade/Livewire/Filament, Angular, Svelte, Astro, HTML/Tailwind, or WordPress).

---

## 1. Chained Skills Activated Automatically
- **Always Active**: `/grill-me` + `/muaz-skill` + `/rtl-logical-guard` + `/ui-review-loop` + `/clean-code-guard` + `/test-guard`
- **Conditional by Stack**:
  - If Next.js / React: `/nextjs-fullstack`
  - If WordPress / WooCommerce: `/wp-guard` + `/woo-guard`

---

## 2. Mandatory 4-Phase Execution Pipeline

### 🔴 Phase 1: Stack Detection + Full `/grill-me` & `/muaz-skill` Smart Intake (NO CODE YET)
1. **Auto-Detect (`Phase 1A/1B`)**: Inspect project files (`package.json`, `composer.json`, `AGENTS.md`, existing layouts/components) to detect the frontend framework, styling system, and theme tokens. If the user specified a preferred stack in their prompt, honor the user's choice.
2. **Grill Interview (`Phase 1C/1D`)**: Use `ask_question` (with `(Recommended)` on the first choice) following `/muaz-skill` (`references/intake-template.md`) to clarify:
   - Page/component purpose, **Visitor Mode** (`Operate` for dense CMS/dashboards, `Persuade` for landing/marketing, `Read` for editorial/docs), layout shell (Sticky Top Nav, Sticky Sidebar, or Full-Width), and visual tone.
   - **Art Direction & Subject Inventory** (for public/marketing pages): 8–12 specific domain facts, the **Competitor Test** (*"On this page, [subject artifact] becomes [layout/interactive device]"*), and **One Live Interactive Thing**.
   - If building a **CMS Table**: exact columns, status badges, search/filter controls, row actions (`View`, `Edit`, `Delete`), and pagination.
   - If building a **CMS Form**: exact input fields, required/optional rules, file/image upload previews, and multi-column grouping.
   - Language & direction: English LTR, Arabic RTL, or Bilingual LTR+RTL.
3. **Confirmation Summary (`Phase 1E`)**: Present the confirmed intake summary + Design Blueprint and wait for `"yes"` before writing code.

---

### 🟡 Phase 2: Enforce Mandatory CMS, Craft Floor & Frontend Layout Armor
Every frontend feature or CMS screen MUST obey these non-negotiable structural and craft rules:
1. **Sticky Top Navbar**:
   - Use `sticky top-0 z-40 h-16 bg-card/85 backdrop-blur border-b` so the top navigation never scrolls out of sight.
2. **Sticky / Independent-Scroll Sidebar Panel**:
   - Desktop (`>= 1024px` / `lg:`): `lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto` so the sidebar stays fixed while the page scrolls.
   - Mobile & Tablet (`< 1024px`): Collapses into a smooth off-canvas drawer (`fixed inset-y-0 start-0 z-50`) with a dark backdrop overlay and a `44x44px` hamburger toggle button in the navbar.
3. **Main Content Column (`min-w-0` Rule)**:
   - Always apply `flex-1 min-w-0` to the main content wrapper next to the sidebar. Without `min-w-0`, wide tables or preformatted blocks will blow out the flex container and break the page width!
4. **CMS Data Tables (`tabular-nums` & 5 States)**:
   - Wrap tables in `w-full overflow-x-auto rounded-xl border` so wide tables scroll horizontally inside their container without breaking the screen.
   - Apply `tabular-nums` (`font-variant-numeric: tabular-nums`) to all numeric, currency, ID, timestamp, and metric columns so digits align vertically.
   - Include sticky table headers (`sticky top-0 bg-muted/90 backdrop-blur`), clear action buttons (`Edit` / `Delete`), pagination controls, search/filter bar, and all **5 UI States** (`Idle`, `Loading` skeleton rows, `Success`, `Error` retry banner, `Empty` state with CTA).
5. **CMS Forms**:
   - Use responsive multi-column grids (`grid-cols-1 md:grid-cols-2 gap-6`), clear `<label>` associations, inline field-by-field validation error text, loading spinner on submit, and a sticky bottom action bar (`sticky bottom-0 z-30 bg-card/95 backdrop-blur py-3 px-6 border-t flex justify-end gap-3`) for long forms.
6. **The Craft Floor & 3-Wave AI Slop Defense**:
   - **No Nested Cards**: NEVER nest a card inside a card (`<Card>` inside `<Card>` or `bg-card` inside `bg-card`). Use spacing (`space-y-4`), subtle dividers, or flat tone steps (`bg-muted/40`) for inner groups.
   - **Contrast on Colored Surfaces**: Never place raw untinted gray (`text-gray-*`/`text-slate-*`) on colored backgrounds; tint secondary text from the surface hue (`text-primary-foreground/80`).
   - **Typography & Heading Rhythm**: More space above headings than below (`mt > mb`), `text-wrap: balance` on headings, `<= 2 lines` (~32 chars) on hero headlines, and `65–75ch` (`max-w-[65ch]`) on body prose.
   - **Browser Surface Theming**: Theme `::selection`, `caret-color`, custom scrollbars, `:focus-visible` (`2px` ring + `2px` offset), and `text-underline-offset: 0.2em` from the palette.
   - **Motion**: Use exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`); ban `animate-bounce` and elastic overshoot easing.
7. **All-Media Responsiveness & Bilingual RTL/LTR (`/rtl-logical-guard`)**:
   - Must render cleanly at `375px` (Mobile), `768px` (Tablet), `1024px` (Laptop), `1280px` (Desktop), and `1920px` (Wide).
   - Zero physical directional CSS (`left-*`, `right-*`, `ml-*`, `mr-*`, `pl-*`, `pr-*`, `text-left`, `text-right`). Always use CSS Logical Properties (`start-*`, `end-*`, `ms-*`, `me-*`, `ps-*`, `pe-*`, `text-start`, `text-end`).

---

### 🟢 Phase 3: Code Generation & Bounded `/ui-review-loop` Verification
1. Write clean, modular, production-ready components following the project's framework conventions.
2. **Bounded Verification Passes**: Build completely, run 1 batched verification round (`python skills/muaz-skill/scripts/anti_slop.py <path> --fail-on MEDIUM` + `python scripts/agent_os.py ui-audit audit --dir <path>`), fix all violations in 1 batch, and confirm in at most 1 final round. Stop over-polishing once gates are green.

---

### ✅ Phase 4: Beginner "How to Test It" Card
Finish with a clear, plain-language **"How to Test It / كيف تختبر الواجهة"** card listing:
- Which route/page to open.
- How to test the sticky nav, sticky sidebar, mobile drawer, table scroll, and form states.
- Tip: *"If anything looks off on your screen, just type `/fix-ui`!"*
