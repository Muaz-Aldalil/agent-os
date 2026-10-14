---
name: fix-ui
description: >-
  All-in-one UI Violation Scanner & Auto-Fixer for any frontend or CMS stack.
  Scans the project with /ui-audit, generates structured fix prompts automatically,
  fixes broken Sticky Navbars, Sticky Sidebars, overflowing Data Tables, messy Forms,
  RTL/LTR bugs (/rtl-logical-guard), and verifies everything via /ui-review-loop.
---

# `/fix-ui` — Scan UI Violations, Auto-Generate Fix Prompts & Fix Automatically

You are the **Senior UI Audit & Remediation Engineer**. Use this skill whenever a developer has visual bugs, UI violations, non-sticky navbar/sidebar panels, overflowing CMS tables, misaligned forms, broken mobile responsiveness, or broken Arabic/English RTL layouts.

---

## 1. Chained Skills Activated Automatically
- `/ui-audit` (`python scripts/agent_os.py ui-audit`)
- `/muaz-skill` (Tune & Audit Mode)
- `/rtl-logical-guard` (Bilingual LTR/RTL Logical CSS)
- `/ui-review-loop` (Visual & Structural Verification Loop)
- `/clean-code-guard`

---

## 2. Mandatory 4-Step Execution Pipeline

### 🔍 Step 1: Run `/ui-audit` + `anti_slop.py` & Generate Fix Prompts Automatically
1. Run the deterministic UI audit scanner and 36-check Anti-Slop gate on the target directory:
   ```powershell
   python scripts/agent_os.py ui-audit audit --dir <target_dir>
   python skills/muaz-skill/scripts/anti_slop.py <target_dir> --fail-on MEDIUM
   ```
2. Inspect the generated audit report and self-contained fix prompts in `docs/ui-audits/<timestamp>/`.
3. Also inspect the project's App Shell, Navbar, Sidebar, Tables, Forms, and global CSS (`::selection`, `caret-color`, `:focus-visible`) directly.

---

### 🛠️ Step 2: Apply Mandatory CMS, Craft Floor & Precision Steering Fixes
Automatically fix all detected violations across the **Top 5 CMS Frontend Pain Points** and **The Craft Floor**:
1. **Non-Sticky Top Navbar**:
   - Fix to `sticky top-0 z-40 h-16 bg-card/85 backdrop-blur border-b` so it stays pinned while scrolling.
2. **Non-Sticky / Broken Sidebar Panel**:
   - Fix desktop sidebar to `lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto` so it scrolls independently and never disappears when scrolling down long pages.
   - Add an off-canvas mobile drawer (`< 1024px`) with backdrop overlay so mobile/tablet screens aren't crushed.
3. **Wide Data Tables Breaking Page Width (`min-w-0` + `tabular-nums` Fix)**:
   - Add `flex-1 min-w-0` to the main content wrapper next to the sidebar.
   - Wrap every table in `w-full overflow-x-auto rounded-xl border`, add `tabular-nums` on numeric/currency/date columns, add sticky `<thead>`, and ensure `Idle`, `Loading`, `Empty`, and `Error` states exist.
4. **Messy or Broken Forms**:
   - Align inputs in a clean responsive grid (`grid-cols-1 md:grid-cols-2 gap-6`), ensure visible labels and inline error messages, and add a sticky bottom `Save / Cancel` bar (`sticky bottom-0 z-30`) on long forms.
5. **Craft Floor & 3-Wave AI Slop Remediation**:
   - **Un-nest Nested Cards**: Replace `<Card>` inside `<Card>` (`bg-card` inside `bg-card`) with flat tone steps (`bg-muted/40`), spacing, or subtle dividers.
   - **Fix Untinted Gray on Colored Surfaces**: Replace `text-gray-*`/`text-slate-*` on colored backgrounds with hue-tinted text or `text-primary-foreground/80`.
   - **Fix Heading Spacing & Typography**: Enforce more space above headings than below (`mt > mb`), `text-wrap: balance` on headings, `65–75ch` prose measure, and remove mixed-font single-italic-word headline gimmicks.
   - **Fix Motion & Browser Surfaces**: Replace `animate-bounce` / elastic overshoot with `cubic-bezier(0.16, 1, 0.3, 1)` ease-out, and theme `::selection`, `caret-color`, and `:focus-visible` in global CSS.
6. **18 Precision Steering Sub-Modes (`muaz-skill` Tune Mode)**:
   - Honor any targeted steering verb requested by the user: `polish`, `critique`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `extract`, `document` (see `skills/muaz-skill/references/tune-mode.md`).
7. **RTL/LTR & All-Media Responsiveness (`/rtl-logical-guard`)**:
   - Replace hardcoded `ml-*`/`mr-*`, `pl-*`/`pr-*`, `left-*`/`right-*`, `text-left`/`text-right` with CSS Logical Properties (`ms-*`/`me-*`, `ps-*`/`pe-*`, `start-*`/`end-*`, `text-start`/`text-end`).
   - Verify Mobile (`375px`), Tablet (`768px`), Laptop (`1024px`), and Desktop (`1280px+`) breakpoints.

---

### 🔄 Step 3: Bounded Verification Pass (Max 1 Re-Check Round)
Re-run `python scripts/agent_os.py ui-audit audit --dir <target_dir>` and `python skills/muaz-skill/scripts/anti_slop.py <target_dir> --fail-on HIGH` in a single batched pass to confirm all Critical/High visual, Craft Floor, layout, and RTL issues are resolved — then stop over-polishing.

---

### ✅ Step 4: Beginner "What Was Fixed & How to Check It" Card
Output a simple summary in plain English + Arabic showing:
- Which UI violations were found and fixed (e.g., Sticky Nav, Sidebar, Table overflow, RTL classes).
- Which screen sizes (`Mobile / Tablet / Desktop`) and directions (`LTR / RTL`) to check in the browser.
