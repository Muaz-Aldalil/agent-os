---
name: Agent OS Editorial Command Studio
colors:
  background: '#FAFAF7'
  surface: '#FFFFFF'
  surface-container-low: '#F3F4F0'
  surface-container: '#ECEEE7'
  surface-dark: '#0C0E12'
  surface-dark-elevated: '#141820'
  on-surface: '#111827'
  on-surface-variant: '#4B5563'
  outline: '#E4E6DF'
  primary: '#059669'
  on-primary: '#FFFFFF'
  primary-container: '#ECFDF5'
  on-primary-container: '#065F46'
  secondary: '#1E293B'
  tertiary: '#D97706'
  error: '#DC2626'
typography:
  headline-xl:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Sora
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: DM Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 26px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 20px
rounded:
  sm: 0.375rem
  DEFAULT: 0.5rem
  md: 0.625rem
  lg: 0.75rem
  xl: 1rem
spacing:
  gutter: 1.5rem
  margin-desktop: 2rem
  margin-mobile: 1rem
---

## 1. Visual Atmosphere & Taste Calibration (`/taste-design` + Impeccable)
- **Brand Identity**: **Agent OS — Engineering Handbook & Interactive Command Studio**. Original, authoritative developer documentation and interactive prompt studio. Strictly zero third-party tutorial branding (no "W3" or "W3Schools" badges, logos, or replica references).
- **Taste Dials**:
  - **Density (`5/10` — Daily App Balanced)**: Calm, focused 2-column workspace (Sticky Bidirectional Sidebar Navigation + Main Interactive Guide & Prompt Studio Canvas). Eliminates cluttered third-column gamification rails, story reels, and competing status widgets.
  - **Variance (`4/10` — Structured Editorial Studio)**: Clean, scannable documentation hierarchy paired with tactile, high-contrast terminal/prompt studio cards.
  - **Motion (`4/10` — Fluid CSS Micro-Interactions)**: Smooth `180ms cubic-bezier(0.16, 1, 0.3, 1)` transitions on sidebar navigation, language direction switching, and prompt copying.

## 2. Color Palette (60-30-10 Rule)
- **60% Foundation Canvas (`#FAFAF7` Warm Stone in Light / `#0C0E12` Deep Carbon in Dark)**: Soft off-white paper ground that reduces eye strain during technical reading.
- **30% Structural Surfaces (`#FFFFFF` Elevated Cards & Sidebar / `#F3F4F0` Subtle Code & Callout Containers / `#E4E6DF` 1px Hairline Borders)**: Clean tonal separation without nested card clutter.
- **10% Signal Accent (`#059669` Emerald Action / `#ECFDF5` Soft Mint Tint / `#065F46` Deep Emerald Text)**: Used strictly for active sidebar indicators, primary "Copy Ready Prompt" actions, and verified guard badges.
- **Dark Code Terminal Surface (`#111827` / `#141820`)**: High-contrast dark slate container reserved for the interactive slash-command prompt studio and copy-paste blocks.

## 3. Typographic Architecture (Bilingual LTR & Rich Arabic RTL)
- **English (`dir="ltr"`)**:
  - **Headlines**: `Sora` (SemiBold/Bold, tight `-0.02em` tracking, `text-wrap: balance`).
  - **Body Prose**: `DM Sans` (`15px–16px`, `1.7` line-height, `65ch` max reading width).
- **Arabic (`dir="rtl"`)**:
  - **Headlines & Detailed Explanations**: `Cairo` / `Tajawal` (`16px–17px` body size, generous `1.85` line-height) designed for deep, multi-paragraph Arabic architectural explanations ("لماذا نستخدم هذا الأمر؟ وكيف يعمل خطوة بخطوة؟").
- **Monospace & Numeric Discipline**:
  - `JetBrains Mono` with `tabular-nums` for all `/slash-commands`, CLI flags, skill counts (`76 Skills`), and code blocks. In RTL mode, all slash commands are isolated inside `<bdi dir="ltr">` chips so slashes never flip.

## 4. Layout & Redesigned Bidirectional Sidebar Navigation
- **Top Sticky Header (`64px` height)**:
  - Minimal, single-row sticky top bar (`sticky top-0 z-40`) containing: Brand Mark (`Agent OS` + version badge `v1.16 • 76 Skills`), 3 clean view tabs (`Interactive Guide`, `Prompt Builder Studio`, `76-Skill Dictionary`), Theme Toggle (`Light / Dark`), and prominent Language/Direction Switcher (`العربية RTL` / `English LTR`).
- **Redesigned Bidirectional Sidebar Navigation (`280px` width, `start-0` logical dock)**:
  - **Left-docked in English (`LTR`)** and **Right-docked in Arabic (`RTL`)**.
  - **Sidebar Header**: Instant filter input (`Filter commands or situations...` / `ابحث عن أمر أو حالة...`) with logical start icon padding.
  - **Track & Chapter Tree**: Organized into 4 clear tracks (`1. Core Workflow & 1-2-3 Rule`, `2. Starting & Building Features`, `3. Fixing UI, Backend & Stitch`, `4. Quality Guards & Data Saver`).
  - **Sidebar Item Design**: Each item displays a clean title on the start side and a compact monospace `/command` badge on the end side. The active item features a `3px` emerald start border (`border-s-4 border-emerald-600`), subtle `#ECFDF5` emerald tint background, and bold text.
- **Main Content Canvas (`flex-1 min-w-0`, max-width `960px` centered in workspace)**:
  1. **Situation Header Card**: Clear situation title, "When to use this" summary, and chained skills pills.
  2. **Deep Explanation Section (Rich Arabic & English)**: Clear step-by-step breakdown of what happens under the hood (Intake Interview -> Blueprint -> Build with Armor -> Auto-Verify), written in natural, comprehensive Arabic (`شرح تفصيلي وافٍ بالعربية`) and clear English.
  3. **Interactive Copy-Paste Prompt Studio**: Dark slate terminal card with stack selector pills (`Auto-Detect`, `Next.js/React`, `Laravel`, `Astro/HTML`, `WordPress`), editable feature input, and one-click `"Copy Ready Prompt"` button.
  4. **Before vs. After Comparison Strip**: Side-by-side comparison showing "Without Agent OS (Raw AI)" vs. "With Agent OS (Guarded & Verified)".
  5. **Previous / Next Chapter Footer Navigation**: Clean two-button pagination at the bottom of the lesson.

## 5. Anti-Patterns (Strictly Banned)
- Zero "W3", "W3Schools", or third-party clone branding anywhere.
- Zero noisy right-hand gamification/XP/story-reel sidebars.
- Zero nested cards (`bg-card` inside `bg-card`).
- Zero `Inter` font, zero pure `#000000`, and zero AI purple/neon gradients.
