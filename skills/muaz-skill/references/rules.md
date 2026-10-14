# muaz-skill Design Rules

Priority order: User explicit request > These rules > Defaults

---

## Typography
1. Display text (h1, hero): weight 300-400, tracking -0.02em to -0.04em
2. Body text: weight 400, line-height 1.5-1.7
3. NEVER use weight 700+ on headings

## Color
4. NEVER use pure black (#000) or pure white (#FFF)
   Use #1A1A1A / #FAFAF8 instead
5. EXACTLY ONE action color per project — all accents derive from it
6. Background neutrals MUST be tinted (warm or cool), never flat gray

## Layout
7. Use asymmetric layouts (60/40, 2/3-1/3) — NEVER center everything
8. Section padding = 96px minimum (48px on mobile)
9. Use border, NOT box-shadow, for card/container elevation

## Effects
10. NEVER use gradient text (linear-gradient on text)
11. NEVER use glass morphism (backdrop-blur on containers)
12. NEVER use box-shadows on cards — use 1px border instead

## Anti-Hallucination
13. NEVER assume a library is installed — check package.json first
14. NEVER invent a function — grep for existing implementations
15. NEVER use `any` type in TypeScript — define or infer properly

## Accessibility
16. Use semantic HTML (<nav>, <main>, <section>, <article>)
17. Add alt text to all images
18. Ensure keyboard navigation works
19. Use aria-label on interactive elements without visible text

## Performance
20. Use CSS transitions over Framer Motion when possible
21. Don't import entire libraries — use named imports
22. Lazy load images below the fold

## Existing Code
23. Match the project's existing code style (naming, imports, structure)
24. Don't create new files if an existing file serves the purpose
25. Check neighboring files before writing new code

## Error Handling
26. Handle loading/success/error states on all async operations
27. Add form validation before submission
28. Don't swallow errors silently — log or surface them

## Workflow
29. Search 3-5 real design examples before building any section
30. Complete the pre-flight checklist before Phase 3
31. Write `.design-lock.md` after Phase 3 — re-read at session start, override only with user confirmation
32. Before claiming done, paste `anti-slop.sh` output + self-score — verbal claims without tool evidence are defects
33. Ask clarifying questions when requirements are ambiguous
34. Always detect before asking — never ask what you can read from the project
35. Pre-fill detected values — user confirms, not re-answers
36. Skip irrelevant questions — landing pages don't need auth/API/state questions
37. User answers always win over detection — detection is suggestion, not constraint

## Craft Floor & Browser Surface Theming
38. **Contrast on Colored Surfaces**: Body/placeholder text >= 4.5:1, large text >= 3:1. On colored surfaces, tint secondary text from that surface's hue or foreground opacity (`text-primary-foreground/80`) — NEVER place raw untinted gray (`text-gray-*`/`text-slate-*`/`text-neutral-*`) on a colored background.
39. **Depth & No Nested Cards**: Shadows must carry vertical offset + soft blur; zero-offset colored halo is banned decoration. NEVER nest cards inside cards (`<Card>` inside `<Card>` or `bg-card` inside `bg-card`) — use flat tone steps (`bg-muted/40`), spacing, or subtle dividers for inner groupings.
40. **Heading Spacing Law (`mt > mb`)**: Always place more vertical space above a heading than below it (`mt-8 mb-3` or `mt-10 mb-4`) so the heading visually anchors to the content it introduces.
41. **Typography Craft Floor**: Body measure MUST stay `65–75ch` (`max-w-[65ch]`); display size max `6rem`; tracking floor `-0.04em`; apply `text-wrap: balance` on headings and `font-variant-numeric: tabular-nums` (`tabular-nums`) on all tables, prices, counters, and metrics.
42. **Headline Arithmetic**: Hero and section headlines must hold to **<= 2 lines at every viewport width** (~5 words / ~32 characters median). Large statement paragraphs must stay <= 24px mobile / <= 36px desktop and <= 3–4 lines.
43. **Motion Craft Floor**: Author one deliberate motion moment per view using exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.22, 1, 0.36, 1)`). NEVER use bounce or elastic overshoot easing (`animate-bounce`, `cubic-bezier` overshoot > 1.15).
44. **Browser Surface Theming**: Every project's global CSS must theme browser-native surfaces from the design palette: `::selection` (accent background + high-contrast text), `caret-color`, custom scrollbars, `:focus-visible` rings (`2px` width, `2px` offset), and `text-underline-offset: 0.2em`.

## Art Direction & 3-Wave AI Slop Defense
45. **Subject Inventory & Competitor Test**: Inventory 8–12 specific facts unique to the subject before choosing layout or visuals. Formulate the core device: *"On this page, [something that belongs to the subject] becomes [the layout/interactive device]."* If substituting the nearest competitor still works, the idea is generic and must be rewritten.
46. **One Live Interactive Thing & Visitor Modes**: Classify every page by Visitor Mode (`Operate` for dense utility/dashboards, `Persuade` for conversion/landing, `Read` for editorial/docs). Every page gets 1 live interactive element built from the subject's idea (thumb-friendly on mobile, degrades without JS, never blocks reading).
47. **3-Wave Dated AI Slop Ban & Substance Rule**:
    - *Wave 1 (2023–2024)*: Violet/indigo gradients, gradient-clipped text, glass blur panels, glowing buttons, 3 identical icon-in-rounded-square cards, emojis as icons.
    - *Wave 2 (2025)*: Cramped uppercase tracked eyebrows above every heading, hero pill badges ("New/Beta/Introducing"), one-italic-serif-word inside a sans headline, decorative `01 / 02 / 03` numbering, monospace outside `<code>`/`<pre>`, thin hairline dividers (`<hr>`, `divide-y`) instead of tone steps.
    - *Wave 3 (2025–2026)*: Default warm-editorial yellow-cream ground (`#faf9f5`, `#f0eee6`) + terracotta/clay accent (`#d97757`, `#c15f3c`) — unless explicitly mandated by the client's brand brief (*"The brief wins"*).
    - *Why Removal Is Not Enough*: Stripping ornaments without adding substance produces a thin page. Replace cut chrome with larger type, whole fields of color, authentic subject imagery, and complete domain content.
48. **Bounded Verification Passes**: Build completely, inspect desktop + mobile in 1 batched round, apply fixes in 1 batch, and confirm in at most 1 final round — stop over-polishing.

