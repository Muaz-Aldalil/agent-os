# Google Stitch × `/taste-design` × Impeccable — The Operator's Prompt Handbook

> **Purpose**: Ready-to-copy-paste slash-command prompts for designing, auditing, steering, syncing, and building production UIs using **Google Stitch (`StitchMCP` + 16 Official Stitch Skills)**, **`/taste-design` (3 Aesthetic Calibration Dials)**, and **Impeccable (18 Precision Steering Modes + 36-Check Anti-Slop Defense inside `/muaz-skill` & `/fix-ui`)**.

---

## 1. How the 3 Design Engines Work Together

When you run a UI prompt in `.agents`, three engines interlock so your UI never looks like generic AI output:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. /taste-design + /muaz-skill (Aesthetic Dials, Intake & DESIGN.md)         │
│    • Sets Density (1–10), Variance (1–10), Motion (1–10)                     │
│    • Bans Inter, pure #000000, AI purple/neon glows, and fake metrics        │
│    • Searches 91 styles, 169 palettes, 72 font pairings + Taste Memory       │
├──────────────────────────────────────────────────────────────────────────────┤
│ 2. Google Stitch (StitchMCP + 16 Official Stitch Skills)                     │
│    • Syncs DESIGN.md to Stitch (/manage-design-system, /design-md, /site-md) │
│    • Enhances prompts (/enhance-prompt) & generates screens (/generate-design)│
│    • Runs multi-page loops (/stitch-loop) & syncs code (/code-to-design)     │
│    • Converts screens to code (/react-components, /shadcn-ui, /remotion)     │
├──────────────────────────────────────────────────────────────────────────────┤
│ 3. Impeccable Steering + Anti-Slop Gate (/muaz-skill + /ui-audit + /fix-ui)  │
│    • 18 Precision Steering Modes (polish, critique, bolder, quieter,         │
│      distill, harden, onboard, animate, colorize, typeset, layout, delight,  │
│      overdrive, clarify, adapt, optimize, extract, document)                 │
│    • 36-Check Anti-Slop Gate (anti_slop.py) + Responsive/RTL Layout Armor    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### The 3 Taste Dials (`/taste-design` Cheat Sheet)

Include these 3 numbers in any prompt to lock the exact visual feel before Stitch or `/muaz-skill` generates a screen:

| Dial | Scale `1–3` | Scale `4–7` | Scale `8–10` |
| :--- | :--- | :--- | :--- |
| **`Density`** | **Art Gallery Airy** (generous whitespace, editorial landing pages) | **Daily App Balanced** (standard SaaS, docs, consumer web apps) | **Cockpit Dense** (CMS tables, financial terminals, admin ops, monospace numbers) |
| **`Variance`** | **Predictable Symmetric** (strict grids, enterprise admin, forms) | **Offset Asymmetric** (split-screen heroes, zig-zag bento grids) | **Artsy Chaotic** (creative studios, inline-image typography, bold editorial) |
| **`Motion`** | **Static Restrained** (instant state changes, zero distraction) | **Fluid CSS** (`cubic-bezier(0.16, 1, 0.3, 1)` ease-out, subtle micro-states) | **Cinematic Choreography** (spring physics, staggered reveals, View Transitions) |

#### Ready-to-Paste Dial Presets
- **Preset A — CMS / Admin Dashboard Cockpit**: `Taste Dials: [Density: 8, Variance: 3, Motion: 4]`
- **Preset B — High-Craft SaaS / Product Landing Page**: `Taste Dials: [Density: 4, Variance: 7, Motion: 6]`
- **Preset C — Interactive Developer / Learning Platform**: `Taste Dials: [Density: 6, Variance: 6, Motion: 6]`
- **Preset D — Calm Fintech / Healthcare / Booking Portal**: `Taste Dials: [Density: 4, Variance: 3, Motion: 3]`

---

## 2. Quick Command Directory (16 Stitch Skills + 18 Impeccable Modes)

### A. All 16 Installed Google Stitch Skills

| Group | Slash Command | What It Does |
| :--- | :--- | :--- |
| **Design & Canvas (`stitch-design`)** | `/generate-design` | Generates new screens, edits existing screens, or creates layout variants in `StitchMCP`. |
| | `/manage-design-system` | Creates, updates, lists, and applies `DESIGN.md` design systems in `StitchMCP`. |
| | `/extract-design-md` | Reverse-engineers a complete `DESIGN.md` from an existing repo, component tree, or URL. |
| | `/extract-static-html` | Extracts self-contained static HTML (inlined CSS/assets) from an app view for Stitch upload. |
| | `/code-to-design` | Converts local frontend code (React, Vue, Astro, HTML/Tailwind) into a live Stitch project. |
| | `/upload-to-stitch` | Uploads local HTML/design assets directly onto a Stitch project canvas without token truncation. |
| **Utilities & Loops (`stitch-utilities`)** | `/taste-design` | Generates a Stitch-ready `DESIGN.md` using the 3 Taste Dials (`Density`, `Variance`, `Motion`) and anti-slop rules. |
| | `/design-md` | Analyzes an existing Stitch project and synthesizes a semantic `DESIGN.md` file. |
| | `/site-md` | Synthesizes a `SITE.md` project constitution, sitemap, and screen roadmap for multi-page builds. |
| | `/enhance-prompt` | Upgrades a rough UI idea into a structured, keyword-rich Stitch generation prompt. |
| | `/stitch-loop` | Iteratively builds all screens in `SITE.md` using an autonomous baton-passing loop. |
| **Code Builders (`stitch-build`)** | `/react-components` | Converts Stitch screens into modular React + TypeScript components with AST validation. |
| | `/shadcn-ui` | Builds or maps Stitch screens into customized `shadcn/ui` components (tables, forms, dialogs). |
| | `/react-vite-dashboard` | Converts Stitch designs into a production React + Vite + TanStack Query dashboard. |
| | `/react-native` | Converts Stitch mobile screens into React Native (`StyleSheet`) components. |
| | `/remotion` | Generates a smooth Remotion product walkthrough video from your Stitch project screens. |

---

### B. All 18 Impeccable Precision Steering Modes (Inside `/muaz-skill` & `/fix-ui`)

You can pass any `Impeccable: [mode1, mode2]` directive into your Stitch or UI prompts:

| # | Impeccable Mode | What It Does (1-Line Transformation) |
| :--- | :--- | :--- |
| 1 | **`critique`** | Audits visual hierarchy, Competitor Test specificity, and 3-Wave AI slop tells; ranks issues before editing. |
| 2 | **`polish`** | Final Craft Floor pass: fixes micro-alignment, `mt > mb` heading rhythm, `tabular-nums`, `:focus-visible`, and `::selection`. |
| 3 | **`bolder`** | Amplifies a timid/generic UI: increases display contrast, commits to fields of color, sharpens asymmetry, and foregrounds the Subject Device. |
| 4 | **`quieter`** | Calms down an over-stimulated UI: strips competing accents, removes glowing pills/badges, and restores breathing room. |
| 5 | **`distill`** | Strips to essence: removes nested cards, redundant wrappers, and eyebrow clutter; replaces chrome with typographic clarity. |
| 6 | **`harden`** | Production armor: adds all 5 UI states (`Idle/Loading/Success/Error/Empty`), fixes table/text overflow (`min-w-0`, `truncate`), and locks RTL/LTR. |
| 7 | **`onboard`** | Designs zero-data empty states, first-run progressive disclosure, and teach-by-doing primary CTAs. |
| 8 | **`animate`** | Adds authored motion using exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) while banning `transition-all` and bounce/elastic overshoot. |
| 9 | **`colorize`** | Introduces hue-tinted color harmony (`60-30-10`) and tints secondary text on colored surfaces (`>= 4.5:1` contrast, zero raw gray on color). |
| 10 | **`typeset`** | Enforces expressive font pairings (bans `Inter`), fluid `clamp()`, `65–75ch` measure, `<= 2-line` hero headlines, `text-wrap: balance`, and `tabular-nums`. |
| 11 | **`layout`** | Fixes spatial rhythm, asymmetric compositions, sticky navbar (`top-0`), sticky full-height sidebar (`lg:h-dvh`), and `375px–1920px` reflow. |
| 12 | **`delight`** | Adds domain-specific personality and **One Live Interactive Thing** built directly from the product's subject matter. |
| 13 | **`overdrive`** | Pushes to high-ambition execution (View Transitions API, 60fps compositor choreography, interactive studio widgets) with `prefers-reduced-motion` safety. |
| 14 | **`clarify`** | Rewrites vague AI buzzwords ("seamless", "elevate", "unleash") into concrete Argument-First copy, clear form labels, and actionable error messages. |
| 15 | **`adapt`** | Adapts a desktop or single-direction screen across Mobile (`375px`), Tablet (`768px`), Desktop (`1280px+`), and Bilingual LTR/RTL (`ms-*`, `ps-*`, `start-*`). |
| 16 | **`optimize`** | Audits and fixes Core Web Vitals (`LCP < 2.5s`, `CLS < 0.1`, `INP < 200ms`), font loading, and layout thrashing. |
| 17 | **`extract`** | Extracts reusable design tokens (`CSS variables`, `Tailwind config`, `tokens.json`, `DESIGN.md`) and shared primitives from ad-hoc UI code. |
| 18 | **`document`** | Generates clear component usage specs, state matrices, and `.design-lock.md` documentation. |

---

## 3. Playbook 1 — Starting a Brand New Design System & Project From Scratch

Use these prompts when you want to establish a rock-solid `DESIGN.md` and `SITE.md`, sync them to `StitchMCP`, and generate your initial screens without any AI slop.

### 📋 Fill-in-the-Blanks Template
```text
/taste-design /design-md /site-md /manage-design-system /muaz-skill
Task: Create a complete Stitch Design System (DESIGN.md + SITE.md) and sync it to StitchMCP.
Project: [Project Name & 1-sentence purpose]
Visitor Mode: [Operate (Dashboard/CMS) | Persuade (Landing/Marketing) | Read (Docs/Editorial)]
Taste Dials: [Density: 1-10, Variance: 1-10, Motion: 1-10]
Impeccable Steering: [typeset, colorize, layout, clarify]
Direction & Locale: [English LTR | Arabic RTL | Bilingual EN/AR]
Core Screens to Plan in SITE.md: [Screen 1, Screen 2, Screen 3]
Constraints: Ban Inter font, ban pure #000000, ban purple/indigo neon gradients, and grill me on any missing product decisions before generating screens.
```

### ⚡ Ready Prompt 1A — Starting a SaaS / CMS Admin Dashboard From Scratch
```text
/taste-design /design-md /site-md /manage-design-system /muaz-skill
Task: Create a complete DESIGN.md and SITE.md from scratch and register the design system in StitchMCP.
Project: Multi-tenant Inventory & Order Management CMS Dashboard.
Visitor Mode: Operate (high-efficiency daily operator workspace).
Taste Dials: [Density: 8, Variance: 3, Motion: 4]
Impeccable Steering: [typeset, colorize, layout, harden, clarify]
Direction & Locale: Bilingual English (LTR) + Arabic (RTL).
Core Screens in SITE.md:
1. Main Analytics & Low-Stock Command Center
2. Orders Data Table (search, status filter, pagination, row drawer, 5 UI states)
3. Product Create/Edit Multi-Column Form (image upload preview + sticky bottom Save bar)
Constraints: Use Sans + Monospace pairing (Geist/Satoshi + JetBrains Mono, tabular-nums on all metrics/IDs/prices), sticky top navbar, sticky full-height sidebar (h-dvh), and zero nested cards. Grill me first if you need any business rules clarified.
```

### ⚡ Ready Prompt 1B — Starting a High-Craft Product Marketing Website From Scratch
```text
/taste-design /design-md /site-md /manage-design-system /muaz-skill
Task: Synthesize a non-generic DESIGN.md and SITE.md and sync to StitchMCP.
Project: Developer CLI & Cloud Deployment Platform Landing Site.
Visitor Mode: Persuade (conversion & technical proof).
Taste Dials: [Density: 4, Variance: 7, Motion: 6]
Impeccable Steering: [bolder, typeset, colorize, delight, clarify]
Core Screens in SITE.md:
1. Asymmetric Split Hero with One Live Interactive Terminal Widget
2. Architecture Proof & Benchmark Comparison Section (no 3-equal-card clichés)
3. Transparent Usage Calculator & Pricing Matrix
Constraints: Ban Inter, ban centered hero clichés, ban fake SLA numbers, and use Argument-First headlines (<= 2 lines).
```

---

## 4. Playbook 2 — Creating & Generating New Pages, Heroes, or Sections in Stitch

Use these prompts when you want to generate a brand new page, a specific section (Hero, Data Table, Form, Pricing), or an entire multi-page flow on your Stitch canvas.

### 📋 Fill-in-the-Blanks Template
```text
/enhance-prompt /generate-design /taste-design /muaz-skill
Task: Enhance my prompt, generate the screen/section in StitchMCP using DESIGN.md, and prepare 2 layout variants.
Target Screen or Section: [Name of Page or Section, e.g. Hero Section / Billing Page / Users Table]
Visitor Mode: [Operate | Persuade | Read]
Taste Dials: [Density: 1-10, Variance: 1-10, Motion: 1-10]
Impeccable Steering: [bolder | layout | delight | harden | typeset]
Must-Have Elements: [List 3-5 concrete UI elements, columns, or interactive controls]
Layout Rules: [e.g. Asymmetric split hero / Sticky nav + sticky sidebar + min-w-0 table wrapper]
```

### ⚡ Ready Prompt 2A — Generate a Non-Generic Hero Section + 2 Variants in Stitch
```text
/enhance-prompt /generate-design /taste-design /muaz-skill
Task: Upgrade this prompt, generate a striking Hero section in StitchMCP, and generate 2 asymmetric layout variants.
Target Section: Hero Section (100dvh minus navbar height, zero vertical overflow).
Visitor Mode: Persuade.
Taste Dials: [Density: 4, Variance: 8, Motion: 6]
Impeccable Steering: [bolder, typeset, delight, clarify]
Must-Have Elements:
1. Left-aligned or split-screen headline (<= 2 lines, ~32 chars per line) with inline visual punctuation.
2. One single high-contrast primary CTA button (no secondary "Learn more" filler, no "Scroll to explore" arrows).
3. One Live Interactive Artifact on the right side (an interactive command/code preview switcher instead of a static stock image).
```

### ⚡ Ready Prompt 2B — Generate a Full CMS Page (Sticky Nav + Sticky Sidebar + Data Table + Form Modal)
```text
/enhance-prompt /generate-design /taste-design /muaz-skill
Task: Generate a production CMS Management screen in StitchMCP aligned with our DESIGN.md.
Target Screen: Customer Subscriptions & Invoices Management Page.
Visitor Mode: Operate.
Taste Dials: [Density: 8, Variance: 3, Motion: 4]
Impeccable Steering: [layout, harden, typeset, clarify]
Must-Have Elements:
1. Sticky top navbar (h-16) + sticky desktop sidebar (w-64, h-dvh, independent scroll) + mobile drawer trigger.
2. Top filter bar with logical icon padding (ps-10), status filter pills, and primary "New Subscription" CTA.
3. Responsive Data Table wrapped in overflow-x-auto with sticky header, tabular-nums on amounts/dates, truncated long text cells (2-4 words + ...), and 5 UI states (Idle, Loading skeleton, Empty, Error, Success).
```

### ⚡ Ready Prompt 2C — Autonomous Multi-Page Build Loop (`/stitch-loop`)
```text
/site-md /stitch-loop /generate-design /manage-design-system
Task: Run the Stitch autonomous baton-passing loop to generate every screen defined in SITE.md in sequence, applying our DESIGN.md design system to each screen and verifying visual consistency across all routes.
```

---

## 5. Playbook 3 — Polishing, Steering & Redesigning Existing UI or Sections (Impeccable + `/taste-design` + Stitch)

Use these prompts when you already have a page, section, or Stitch screen, and want to **polish it, make it bolder, calm it down, fix its typography/colors, or harden it**.

### 📋 Fill-in-the-Blanks Template
```text
/muaz-skill /taste-design /generate-design /fix-ui
Target: [File path, route, or Stitch Screen ID/Name]
Mode: [Refinement (keep identity, raise craft) | Redesign (replace visual surface, keep product truth)]
Impeccable Steering: [Pick 2-4 modes from the 18 Impeccable modes]
Taste Dials Adjustment: [Density: X, Variance: Y, Motion: Z]
What to Change: [Describe what feels off or generic right now]
What to Preserve: [e.g. Keep all existing routes, copy, data fields, and navbar/footer intact]
```

### ⚡ Ready Prompt 3A — "Make This Generic Section Bolder & Memorable" (`bolder` + `delight` + `overdrive`)
```text
/muaz-skill /taste-design /generate-design
Target: [Paste file path or Stitch screen name]
Mode: Redesign (keep all product copy and routes intact, replace generic visual layout).
Impeccable Steering: [critique, bolder, delight, overdrive, typeset]
Taste Dials Adjustment: [Density: 5, Variance: 8, Motion: 7]
Task: Critique why this page/section looks like generic AI output, then redesign it in Stitch and code:
1. Replace any 3-equal-card row with an asymmetric bento or 2-column zig-zag layout.
2. Replace generic stock/icon boxes with One Live Interactive Component built from the domain subject.
3. Increase display headline contrast (fluid clamp(), <= 2 lines) and commit to intentional surface color steps.
```

### ⚡ Ready Prompt 3B — "Calm Down a Noisy, Cluttered, Over-Designed Page" (`quieter` + `distill`)
```text
/muaz-skill /taste-design /fix-ui
Target: [Paste file path or Stitch screen name]
Mode: Refinement.
Impeccable Steering: [quieter, distill, typeset, layout]
Taste Dials Adjustment: [Density: 4, Variance: 3, Motion: 3]
Task: Strip visual bloat and restore calm hierarchy:
1. Un-nest all nested cards (bg-card inside bg-card) and replace them with flat surface tone steps or spacing.
2. Remove decorative pill badges, uppercase eyebrow clutter, neon shadows, and competing accent colors (keep max 1 accent <= 10% of screen).
3. Let typography and whitespace carry the hierarchy.
```

### ⚡ Ready Prompt 3C — "Final Micro-Craft, Typography & Color Polish" (`polish` + `typeset` + `colorize` + `animate`)
```text
/muaz-skill /fix-ui
Target: [Paste file path or directory]
Mode: Refinement (100% preservation of layout, routes, and copy).
Impeccable Steering: [polish, typeset, colorize, animate]
Task: Execute a surgical Craft Floor pass:
1. Fix heading spacing rhythm so margin-top > margin-bottom, apply text-wrap: balance on headings, and cap body prose at 65-75ch.
2. Enforce tabular-nums on every number, price, percentage, timestamp, and table column.
3. Replace any raw gray text on colored backgrounds with hue-tinted foreground opacity (>= 4.5:1 contrast).
4. Theme ::selection, caret-color, custom scrollbars, and :focus-visible (2px ring + 2px offset), and replace any transition-all or bounce easing with cubic-bezier(0.16, 1, 0.3, 1).
```

### ⚡ Ready Prompt 3D — "Harden for Production, Mobile & RTL/LTR" (`harden` + `layout` + `adapt` + `onboard`)
```text
/fix-ui /rtl-logical-guard /ui-review-loop
Target: [Paste file path or directory]
Mode: Refinement.
Impeccable Steering: [harden, layout, adapt, onboard]
Task: Harden this UI for real production edge cases:
1. Add all 5 UI states (Idle, Loading skeleton, Success, Error with retry, Empty state with onboarding CTA).
2. Lock Sticky Navbar (top-0) without overflow-hidden ancestor traps (use overflow-x-clip), lock Sticky Sidebar (lg:h-dvh), and enforce flex-1 min-w-0 on the main content column.
3. Truncate long table cells (2-4 words + ...) with full details on expand/modal, and convert all physical directional classes (left/right/ml/mr/pl/pr) to CSS Logical Properties (start/end/ms/me/ps/pe).
4. Verify across 375px, 768px, 1024px, and 1280px+ in both LTR and RTL.
```

---

### 🎯 One-Liner Copy-Paste Prompts for Every Single Impeccable Mode (1–18)

When you want to fire **just one specific Impeccable lens** on a component, page, or Stitch screen, copy-paste any line below:

1. **Critique**: `/muaz-skill Impeccable: [critique] — Audit [target] for visual hierarchy, Competitor Test specificity, and 3-Wave AI slop; give me ranked findings before editing.`
2. **Polish**: `/fix-ui Impeccable: [polish] — Run a surgical Craft Floor pass on [target] (mt > mb heading spacing, tabular-nums, :focus-visible, ::selection, token alignment) without changing layout or copy.`
3. **Bolder**: `/muaz-skill /generate-design Impeccable: [bolder] — Amplify [target]: sharpen asymmetry, increase display scale contrast, and replace generic cards with a bold domain-specific layout.`
4. **Quieter**: `/muaz-skill /fix-ui Impeccable: [quieter] — Calm down [target]: remove glowing badges, extra accent colors, and visual noise while preserving all functionality.`
5. **Distill**: `/muaz-skill /fix-ui Impeccable: [distill] — Strip [target] to its essence: un-nest cards, remove redundant borders/eyebrows, and use whitespace and typography for hierarchy.`
6. **Harden**: `/fix-ui Impeccable: [harden] — Add all 5 UI states (Idle/Loading/Success/Error/Empty), fix long-text/table overflow (min-w-0, truncate), and harden keyboard/focus behavior on [target].`
7. **Onboard**: `/muaz-skill Impeccable: [onboard] — Redesign the empty state and first-run experience of [target] so new users learn by doing with one clear primary CTA.`
8. **Animate**: `/muaz-skill Impeccable: [animate] — Replace transition-all and bounce/elastic animations in [target] with 60fps transform/opacity choreography using cubic-bezier(0.16, 1, 0.3, 1) and prefers-reduced-motion safety.`
9. **Colorize**: `/muaz-skill /taste-design Impeccable: [colorize] — Calibrate [target] to the 60-30-10 color rule, fix raw gray text on colored surfaces, and ensure WCAG AA >= 4.5:1 contrast in Light and Dark modes.`
10. **Typeset**: `/muaz-skill Impeccable: [typeset] — Upgrade typography in [target]: replace generic fonts, apply fluid clamp() sizing, <= 2-line hero headlines, 65-75ch body measure, text-wrap: balance, and tabular-nums.`
11. **Layout**: `/fix-ui Impeccable: [layout] — Fix spatial rhythm and shell armor in [target]: sticky top-0 navbar (overflow-x-clip), sticky lg:h-dvh sidebar, flex-1 min-w-0 main column, and clean 375px-1920px reflow.`
12. **Delight**: `/muaz-skill /generate-design Impeccable: [delight] — Add One Live Interactive Thing to [target] built directly from the product's core subject matter.`
13. **Overdrive**: `/muaz-skill /generate-design Impeccable: [overdrive] — Push [target] to high-ambition interactive execution (View Transitions, interactive live studio, compositor micro-motion) with reduced-motion fallback.`
14. **Clarify**: `/muaz-skill Impeccable: [clarify] — Rewrite all AI buzzwords in [target] into concrete Argument-First claims (Claim + Proof), clear input labels, and helpful error recovery text.`
15. **Adapt**: `/fix-ui /rtl-logical-guard Impeccable: [adapt] — Adapt [target] for Mobile (375px), Tablet (768px), Desktop (1280px+), and strict Bilingual AR/EN RTL/LTR logical CSS.`
16. **Optimize**: `/muaz-skill Impeccable: [optimize] — Audit and optimize [target] for Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms), font loading, and rendering performance.`
17. **Extract**: `/extract-design-md /muaz-skill Impeccable: [extract] — Extract all colors, typography, spacing, and component patterns from [target] into DESIGN.md and CSS/Tailwind tokens.`
18. **Document**: `/design-md /muaz-skill Impeccable: [document] — Document the visual tokens, 5-state UI matrix, and component rules of [target] into DESIGN.md and .design-lock.md.`

---

## 6. Playbook 4 — Auditing Existing UI & Syncing Local Code ↔ Google Stitch

Use these prompts when you want to **audit an existing project for UI/slop violations**, **extract its design system into `DESIGN.md`**, or **upload your local codebase into Google Stitch** so we can redesign it on the Stitch canvas.

### 📋 Fill-in-the-Blanks Template
```text
/ui-audit /extract-design-md /code-to-design /muaz-skill
Target Directory or Page: [Path to repo, folder, or HTML/Astro/React file]
Action: [Audit only | Audit + Auto-Fix (/fix-ui) | Sync Local Code to Stitch Canvas + Redesign]
Impeccable Lens: [critique, extract, polish, harden]
```

### ⚡ Ready Prompt 4A — Full UI + Anti-Slop Audit (Generates Fix Prompts Automatically)
```text
/ui-audit /muaz-skill
Target: [Paste directory or file path]
Impeccable Steering: [critique]
Task:
1. Run the deterministic UI audit scanner (`python scripts/agent_os.py ui-audit audit --dir <target>`) and the 36-check Anti-Slop gate (`python skills/muaz-skill/scripts/anti_slop.py <target> --fail-on MEDIUM`).
2. Inspect the live DOM, responsive breakpoints (375px, 768px, 1024px, 1440px), RTL/LTR logical properties, and Craft Floor rules.
3. Output a ranked report of all violations and generate self-contained fix prompts in `docs/ui-audits/` without modifying code yet.
```

### ⚡ Ready Prompt 4B — Audit + Auto-Fix Everything in One Pass (`/fix-ui`)
```text
/fix-ui /rtl-logical-guard /ui-review-loop
Target: [Paste directory or file path]
Impeccable Steering: [critique, polish, layout, harden, adapt]
Task: Scan the project with `/ui-audit` and `anti_slop.py`, fix all Sticky Navbar, Sticky Sidebar, Table overflow (`min-w-0`), nested card, contrast, typography, and RTL/LTR logical CSS violations in one batch, and verify until both gates return 0 violations.
```

### ⚡ Ready Prompt 4C — Push Existing Codebase Up to Google Stitch Canvas (`/code-to-design`)
```text
/extract-design-md /extract-static-html /code-to-design /upload-to-stitch
Target: [Paste path to existing frontend app, e.g. learning-platform/ or handbook.html]
Task:
1. Extract the current design tokens and structure into `DESIGN.md` (`/extract-design-md`).
2. Extract clean self-contained static HTML (`/extract-static-html`) and upload our existing screens to a Google Stitch project (`/code-to-design` + `/upload-to-stitch`) so we can inspect and redesign them on the Stitch canvas.
```

---

## 7. Playbook 5 — Converting Stitch Canvas Screens into Production Code

Use these prompts after generating or editing screens in `StitchMCP` to convert them into clean, modular production code in your stack.

### 📋 Fill-in-the-Blanks Template
```text
/[react-components | shadcn-ui | react-vite-dashboard | react-native | remotion] /muaz-skill /rtl-logical-guard /ui-review-loop
Source Stitch Project / Screen: [Project ID or Screen Name in Stitch]
Target Tech Stack: [Next.js / React / Astro / Vue / Laravel Blade / HTML+Tailwind / React Native]
Impeccable Steering: [polish, harden, layout, adapt]
Task: Convert the Stitch screen into modular production components, wire all 5 UI states, enforce CMS layout armor and RTL/LTR logical properties, and verify with anti_slop.py and ui-audit.
```

### ⚡ Ready Prompt 5A — Convert Stitch Screens to React / Next.js + `shadcn/ui`
```text
/react-components /shadcn-ui /nextjs-fullstack /rtl-logical-guard /ui-review-loop
Source: Our active Stitch project screens and DESIGN.md.
Impeccable Steering: [polish, harden, layout, adapt]
Task: Convert the Stitch screens into modular React + TypeScript + shadcn/ui components. Enforce Server vs. Client component boundaries, sticky navbar/sidebar armor, `flex-1 min-w-0` table wrappers, `tabular-nums`, and CSS Logical Properties (`ms-*`, `ps-*`, `start-*`). Run `anti_slop.py` and `ui-audit` before finishing.
```

### ⚡ Ready Prompt 5B — Convert Stitch Screens to Astro / HTML + Tailwind (Or Any Custom Stack)
```text
/generate-design /muaz-skill /feature-fe /rtl-logical-guard /ui-review-loop
Source: Our active Stitch project screens and DESIGN.md.
Target Stack: [Astro + Tailwind CSS | Vue/Nuxt | Laravel Blade/Livewire | HTML + Tailwind]
Impeccable Steering: [polish, harden, typeset, colorize, adapt]
Task: Translate the approved Stitch canvas design and DESIGN.md tokens into clean, modular components in our target stack. Preserve 100% of existing routes and data contracts, enforce Light/Dark mode contrast (>= 4.5:1) and Bilingual EN/AR RTL support, and verify with `anti_slop.py` and `ui-audit`.
```

### ⚡ Ready Prompt 5C — Generate a Remotion Product Walkthrough Video From Stitch Screens
```text
/remotion
Source: Our active Stitch project screens.
Task: Build a smooth Remotion video walkthrough showcasing our Stitch screens with spring-physics transitions, zoom callouts on key interactive elements, and clean typographic captions.
```

---

## 8. Playbook 6 — Chaining Stitch + `/taste-design` + Impeccable Inside `.agents` Combo Commands

You can combine our **11 Beginner Situation Commands** with **Google Stitch**, **`/taste-design`**, and **Impeccable** in a single prompt:

### ⚡ 6A — Start a Brand New Full-Stack Project with Stitch (`/start-project`)
```text
/start-project /taste-design /generate-design
Project Idea: [Describe your app idea in plain English or Arabic]
Preferred Stack: [e.g. Next.js + PostgreSQL | Laravel + MySQL | Auto-Recommend]
Taste Dials: [Density: 6, Variance: 6, Motion: 5]
Impeccable Steering: [bolder, typeset, colorize, layout, harden]
Task: Run the Smart Intake interview first, author the 6 Pre-Coding Pillars + DESIGN.md + SITE.md, prototype the core screens in StitchMCP, and build the full-stack app after I confirm the blueprint.
```

### ⚡ 6B — Build a New Frontend Feature with Stitch (`/feature-fe`)
```text
/feature-fe /taste-design /generate-design
Feature: [Describe the page, section, table, or form you want to build]
Taste Dials: [Density: 7, Variance: 4, Motion: 5]
Impeccable Steering: [layout, typeset, harden, delight]
Task: Grill me on any missing details first, generate the visual screen in StitchMCP aligned with DESIGN.md, then build the responsive LTR/RTL frontend code and verify with `/ui-review-loop`.
```

### ⚡ 6C — Build a Full-Stack Feature (Frontend + Backend + DB) with Stitch (`/feature-full`)
```text
/feature-full /taste-design /generate-design
Feature: [Describe the end-to-end feature]
Taste Dials: [Density: 8, Variance: 3, Motion: 4]
Impeccable Steering: [layout, harden, typeset, clarify]
Task: Grill me first, design the UI screen in StitchMCP, build the database migration + indexed foreign keys + RBAC backend API + responsive CMS UI, and run all quality guards.
```

---

## 9. Bonus — The Ready Prompt for Stage 2 (Redesigning Our `.agents` Handbook from Scratch with Google Stitch)

When you are ready to kick off **Stage 2** (hooking our deployed `.agents` Learning Platform / Handbook up to Google Stitch and redesigning it from scratch), you can copy-paste or tweak this exact prompt:

```text
/taste-design /design-md /site-md /manage-design-system /generate-design /muaz-skill
Task: Stage 2 Challenge — Hook our .agents Learning Platform (`learning-platform/` & `handbook.html`) up to Google Stitch and redesign its visual experience from scratch while preserving 100% of our 76 skills, 15 curriculum chapters, 4 interactive modes (Feed Hub, W3Schools Reader, Try-it-Yourself Studio, 76-Skill Dictionary), Bilingual EN/AR RTL parity, and `handbook-sync` pipeline.
Taste Dials: [Density: 6, Variance: 7, Motion: 6]
Impeccable Steering: [critique, bolder, typeset, colorize, layout, delight, overdrive, harden]
Step-by-Step Execution:
1. Grill me first on the visual direction, layout structure, and what we want to elevate on the Stitch canvas before touching any code.
2. Create a brand new `DESIGN.md` and `SITE.md` via `/taste-design` and sync them to `StitchMCP` (`/manage-design-system`).
3. Generate the redesigned screens on Google Stitch (`/generate-design`) so we can review the new look first.
4. Once approved, implement the redesign in `learning-platform/`, compile to `handbook.html` via `python scripts/agent_os.py handbook-sync --build`, and verify 0 violations in `anti_slop.py` and `ui-audit` (without touching `HANDBOOK.pdf`).
```

---

## 10. Automatic Anti-Slop & Craft Floor Checklist (Enforced on Every Prompt)

Whenever you run any prompt in this handbook, `/taste-design` + `/muaz-skill` (`anti_slop.py`) + `/ui-audit` automatically enforce:
- **Zero Banned Fonts**: No `Inter`, `Roboto`, `Arial`, or generic serifs (`Times New Roman`, `Georgia`).
- **Zero Banned Colors**: No pure `#000000`, no AI purple/indigo neon glows, no unrequested Wave-3 `#faf9f5` + `#d97757` terracotta defaults, and no raw gray text on colored backgrounds.
- **Zero Structural Slop**: No nested cards (`bg-card` inside `bg-card`), no 3-equal-card icon-box rows, no fake round metrics (`99.99% UPTIME`), and no `"Scroll to explore"` filler.
- **100% CMS & RTL Armor**: Sticky `top-0` navbar (`overflow-x-clip`), sticky `lg:h-dvh` sidebar, `flex-1 min-w-0` main column, `tabular-nums` on all numbers, `2–4 words + ...` table truncation, and strict CSS Logical Properties (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`).
