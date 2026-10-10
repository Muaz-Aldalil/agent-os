# Design Brief & Visual Tokens: Pawfect Grooming Salon & Spa

## 1. Brand Identity & Visual Aesthetic
- **Design Mood**: Warm, Organic Luxury Pet Care ("Gentle, stress-free pampering for your furry companion").
- **Aesthetic Benchmark**: High-end pet hospitality combining the warmth of organic wellness brands with crisp modern digital clarity.
- **Visual Personality**: Compassionate, pristine, trustworthy, playful without being cartoonish.
- **Imagery Style**: Bright natural light, joyful dogs post-groom, calming clean salon equipment, macro shots of organic shampoos.

---

## 2. Color Palette & The 60-30-10 Rule

```
┌────────────────────────────────────────────────────────┐
│ 60% DOMINANT CANVAS                                    │
│ Warm Linen / Soft Oat (#FAF8F5)                        │
│ Calming organic surface that feels clean & hygienic    │
│                                                        │
│   ┌──────────────────────────────────────────────┐     │
│   │ 30% STRUCTURAL SURFACES & CARDS              │     │
│   │ Whipped Pure White (#FFFFFF) & Soft Biscuit  │     │
│   │ (#F3EFEA) with subtle borders (#E7E1D8)      │     │
│   │                                              │     │
│   │     ┌──────────────────────────────────┐     │     │
│   │     │ 10% ACCENT / CTA BUTTONS         │     │     │
│   │     │ Warm Honey Amber (#D97706 /      │     │     │
│   │     │ #B45309) & Deep Forest (#1B4332) │     │     │
│   │     └──────────────────────────────────┘     │     │
│   └──────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
```

| Token Role | Tailwind Class / CSS Variable | Hex Value | Usage Description |
| :--- | :--- | :--- | :--- |
| **Canvas Background (60%)** | `bg-[#FAF8F5]` / `--bg-canvas` | `#FAF8F5` | Whole-page body background, natural warm paper feel |
| **Surface / Card (30%)** | `bg-white`, `bg-[#F5F2EB]` | `#FFFFFF` | Service cards, booking modal container, review cards |
| **Primary Accent CTA (10%)** | `bg-amber-600`, `hover:bg-amber-700` | `#D97706` | "Book Appointment" primary buttons, active step indicators |
| **Secondary Accent** | `bg-emerald-800`, `text-emerald-900` | `#064E3B` | Trust badges, certified stamps, pricing highlights |
| **Text Primary** | `text-[#292524]` (Stone-800) | `#292524` | High-contrast readable headings and primary text |
| **Text Muted** | `text-[#78716C]` (Stone-500) | `#78716C` | Duration notes, breed details, helper subtext |
| **Semantic Success** | `text-emerald-600`, `bg-emerald-50` | `#059669` | Booking confirmed icon, active vaccination checks |
| **Semantic Error** | `text-rose-600`, `bg-rose-50` | `#E11D48` | Invalid phone number alert, missing dog name border |

---

## 3. Typography Hierarchy & Font Families
- **Display & Headings**: `Plus Jakarta Sans` or `Outfit` (Rounded, friendly, modern geometric sans).
- **Body & Microcopy**: `Inter` or `Plus Jakarta Sans` (Clear, high legibility on small mobile viewports).

| Level | Tailwind Classes | Size (Desktop / Mobile) | Weight | Line Height | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Display H1** | `text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight` | 44px - 60px | 800 | 1.10 | Hero headline ("Your Dog's Happy Place") |
| **Section H2** | `text-3xl sm:text-4xl font-bold tracking-tight` | 30px - 36px | 700 | 1.20 | Section headers (Services, Gallery, FAQ) |
| **Card Header H3** | `text-xl sm:text-2xl font-bold` | 20px - 24px | 700 | 1.30 | Package titles ("The Full Spa Groom") |
| **Body Base** | `text-base sm:text-lg text-stone-600` | 16px - 18px | 400 | 1.55 | Paragraphs and service descriptions |
| **Badge / Caption** | `text-xs sm:text-sm font-semibold uppercase tracking-wider` | 12px - 14px | 600 | 1.40 | "PUPPY FRIENDLY", step labels, ratings |

---

## 4. Spacing, Elevation & Component Tokens
- **Border Radius**:
  * Outer Cards: `rounded-3xl` (24px) for modern, friendly softness.
  * Inputs & Buttons: `rounded-xl` (12px) for comfortable clickability.
  * Badges & Size Switchers: `rounded-full` (pill shape).
- **Shadows**:
  * Subtle Card Elevation: `shadow-[0_4px_20px_-4px_rgba(41,37,36,0.06)]`.
  * Active Modal Dialog: `shadow-[0_25px_50px_-12px_rgba(41,37,36,0.25)]`.
- **Minimum Tap Target**: All clickable elements strictly maintain $\ge 44 \times 44\text{px}$ touch bounding boxes.

---

## 5. Bi-directional (LTR / RTL) Layout Integrity
To support potential bilingual localization (e.g. English / Arabic) without UI refactoring, all layout rules MUST adhere to **CSS Logical Properties** (ADR-003):
- Use `ms-2` / `me-3` instead of `ml-2` / `mr-3`.
- Use `ps-4` / `pe-4` instead of `pl-4` / `pr-4`.
- Use `text-start` and `text-end` instead of `text-left` and `text-right`.
- Use `start-0` / `end-0` for absolute positioned icons and badges.
- Flex and grid structures automatically invert when `<html dir="rtl">` is set.
