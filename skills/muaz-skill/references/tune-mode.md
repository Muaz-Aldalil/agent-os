# Tune Mode — Improving Existing UI

Load this file when the request is to improve, fix, redesign, or optimize an existing UI.

---

## STEP 1 — AUDIT

```
Issues Found:
- [VISUAL]       [Description + why it's wrong]
- [UX]           [Description + user impact]
- [PERFORMANCE]  [Description + metric affected]
- [A11Y]         [Description + WCAG criterion]
- [SECURITY]     [Description + vulnerability type]
- [STATES]       [Missing loading/error/empty states]
```

## STEP 1.5 — DIAGNOSE (bug / perf reports only; skip for pure improvement work)

A reported bug gets a **Red** first (see `glossary.md`) — no fix without one. Source: mattpocock `diagnosing-bugs`, adapted to UI.

```
1. BUILD THE RED CHECK   — the tight pass/fail signal for THIS bug, in order of preference:
     visual_diff.py gate   -> pixel drift on the broken view (layout/visual bugs)
     Playwright script     -> DOM/console/network assertion on the exact symptom
     Component test        -> failing test at the component seam (interaction bugs)
     Lighthouse/curl loop  -> perf metric vs baseline (perf regressions)
   Must be: red-capable (catches this bug), deterministic, fast, agent-runnable.
   Cannot build one? Say so, list what you tried, ask for a capture (HAR,
   recording, screenshot). Do NOT hypothesise without a red check.
2. REPRODUCE + MINIMISE  — run it, watch it fail on the user's exact symptom,
   then cut inputs/steps one at a time until every remaining element is load-bearing.
3. HYPOTHESISE           — 3-5 ranked, falsifiable hypotheses BEFORE testing any
   ("If X is the cause, changing Y makes it green"). Show the ranked list to the user;
   proceed with your ranking if they're away.
4. INSTRUMENT            — one variable per probe; tag every debug log [DEBUG-x4f2]
   so cleanup is one grep. Perf branch: measure baseline first, bisect second.
5. FIX + REGRESS         — turn the minimised repro into a failing check, apply the
   fix, watch it green, re-run against the ORIGINAL un-minimised scenario.
6. CLEANUP               — grep [DEBUG-] tags removed; throwaway scripts deleted;
   winning hypothesis logged in .context/DECISIONS.md (D-00N).
```

## STEP 2 — PROPOSE

Rank changes by user impact:

```
- [HIGH]   [Change] — expected improvement
- [MEDIUM] [Change] — expected improvement
- [LOW]    [Change] — expected improvement
```

**Decision Brief:** per change (5-part: Advantages / Disadvantages / Alternatives / Appropriate when / Inappropriate when). Diminishing returns on flip-flop — if the brief says the change is inappropriate for this project's context, propose the alternative instead.

## STEP 3 — IMPLEMENT

Apply changes surgically. Don't rebuild what isn't broken.

- Edit existing components, don't rewrite
- Follow the stack rules in `references/build-mode.md` §4c
- Respect the existing design system; match what's there

### Refinement vs. Redesign Mode
- **Refinement (`polish`, `harden`, `clarify`, `typeset`, `adapt`, `optimize`)**: Preserve the incumbent identity, palette, copy, and scope while elevating execution to the **Craft Floor** (`references/rules.md` #38–44).
- **Redesign (`bolder`, `quieter`, `distill`, `overdrive`, `colorize`)**: Keep durable product truth (`PRODUCT.md` / functional contracts) intact, but replace the surface visual world (`DESIGN.md`) with a stronger, subject-grounded direction.

---

## STEP 3.5 — 18 PRECISION STEERING SUB-MODES

When the user (or `/fix-ui`) invokes a specific steering verb, apply its targeted transformation lens:

| Sub-Mode | Purpose & Exact Transformation |
|---|---|
| **`polish`** | Final Craft Floor pass: fix micro-alignment, `mt > mb` heading spacing, `tabular-nums`, `:focus-visible`, `::selection`, and token drift without changing layout or copy. |
| **`critique`** | Evaluate visual hierarchy, Competitor Test specificity, 3-Wave AI slop tells, and emotional resonance; output ranked findings before editing. |
| **`bolder`** | Amplify a timid or generic design: increase display scale contrast, commit to whole fields of color, sharpen asymmetry, and foreground the Subject Device. |
| **`quieter`** | Tone down an over-stimulated interface: strip competing accents, remove decorative badges/glows, soften surface steps, and restore calm breathing room. |
| **`distill`** | Strip to essence: remove nested cards, hairline dividers, eyebrow labels, and redundant wrappers; replace removed chrome with larger type and spatial clarity. |
| **`harden`** | Production resilience: add all 5 UI states (`Idle/Loading/Success/Error/Empty`), handle long-string overflow (`min-w-0`, `truncate`), i18n/RTL expansion, and keyboard traps. |
| **`onboard`** | Design zero-data empty states, first-run progressive disclosure, and clear primary CTAs that teach the user by doing. |
| **`animate`** | Add one authored motion moment per view using exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`), removing any `transition-all` or bounce/elastic overshoot. |
| **`colorize`** | Introduce strategic, hue-tinted color harmony to flat monochromatic UIs; tint secondary text on colored surfaces from the surface hue (`>= 4.5:1` contrast). |
| **`typeset`** | Fix font pairing, fluid `clamp()` scale, `65–75ch` body measure, `-0.04em` tracking floor, `text-wrap: balance`, `<= 2-line` headline arithmetic, and `tabular-nums`. |
| **`layout`** | Fix spatial rhythm, asymmetric compositions, sticky navbar/sidebar armor, `flex-1 min-w-0` main column protection, and responsive `375px–1920px` reflow. |
| **`delight`** | Add domain-specific moments of personality and the **One Live Interactive Thing** built directly from the subject's inventory. |
| **`overdrive`** | Push to technically ambitious execution (View Transitions API, 60fps compositor choreography, or custom canvas/shader surfaces) while respecting `prefers-reduced-motion`. |
| **`clarify`** | Rewrite vague AI buzzwords into concrete, Argument-First claims, clear form labels, and actionable recovery error messages. |
| **`adapt`** | Adapt the interface across mobile (`375px`), tablet (`768px`), desktop (`1280px+`), touch targets (`>= 44x44px`), and bidirectional LTR/RTL logical CSS. |
| **`optimize`** | Eliminate CLS, optimize LCP hero assets, enforce `font-display: swap`, remove scroll listeners, and trim JS/CSS bundle overhead. |
| **`extract`** | Extract ad-hoc hexes, spacing, and repeated markup into reusable design tokens (`tokens.json` / CSS variables) and shared primitives. |
| **`document`** | Codify durable product truth (`PRODUCT.md`) separately from the surface visual system (`DESIGN.md` / `design-system/MASTER.md`). |

---

## STEP 4 — BOUNDED VERIFICATION & DIFF SUMMARY

Enforce **Bounded Verification Passes**: build completely, inspect desktop + mobile in 1 batched round (`scripts/anti_slop.py` + `ui-audit`), apply fixes in 1 batch, and confirm in at most 1 final round. Stop over-polishing once gates are green.

```
Changed: [list of what changed + active Steering Sub-Mode]
Reason:  [why each change was made]
Result:  [expected measurable outcome + anti_slop.py / ui-audit proof]
```
