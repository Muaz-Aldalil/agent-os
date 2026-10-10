# Technical Requirements Document (TRD): Pawfect Grooming Salon & Spa

## 1. System Architecture & Topology
- **Rendering Architecture**: High-Performance Semantic HTML5 + Tailwind CSS with an Event-Driven Vanilla JavaScript Client Controller.
- **Client State Architecture**: Reactive state store managing the multi-step booking wizard, package selection, date/slot availability, and client-side validation.
- **Data Persistence**: LocalStorage storage adapter (`pawfect_appointments_v1`) enabling appointment persistence, draft recovery, and instant confirmation reloads.
- **Deployment & Portability**: 100% standalone, zero server-side build lock-in. Deploys cleanly to GitHub Pages, Vercel, Netlify, or any static/cloud host.

---

## 2. Technology Stack Selection & Rationale

| Layer | Selected Technology | Version / Spec | Rationale & Trade-offs |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | HTML5 Semantic Standard & Tailwind CSS | HTML5 + Tailwind v3.4+ / v4 | Native browser accessibility (`<main>`, `<section>`, `<dialog>`, `<form>`), zero hydration delays, CSS logical properties. |
| **Styling & Design** | Tailwind CSS Utility Framework | Modern Tailwind | Utility-first, responsive grid/flexbox, custom warm color tokens, zero CSS runtime overhead. |
| **Icons & Media** | Lucide Icons (SVG) | Latest CDN / Inline | Lightweight, crisp vector iconography for pet care (scissors, bath, paw, calendar, shield, star). |
| **Typography** | Google Fonts (`Plus Jakarta Sans` & `Outfit`) | Modern Variable | Friendly, trustworthy, warm aesthetic tailored to pet wellness. |
| **Backend / Client Logic** | Event-Driven Vanilla JavaScript (ES2022+) | Native Standard | Zero runtime framework overhead; sub-50ms execution speed; optional API webhook hooks. |
| **Database & Persistence** | LocalStorage Adapter (`pawfect_appointments_v1`) | Browser Storage / JSON | Standalone client persistence with drop-in PostgreSQL/Supabase schema readiness. |
| **Security & Auth** | Guest Checkout + Input Sanitization | DOMPurify / Regex | Anti-XSS DOM sanitization, rate-limit submission locks, guest access via verification code. |

---

## 3. Third-Party Integrations & External Services
- **Google Maps Embed / Map Link**: Quick directions link to physical salon location.
- **Calendar Add-to-Calendar**: Dynamic `.ics` / Google Calendar link generation on booking confirmation.
- **Web Share API**: Native mobile share capability for booking confirmation cards.
- **Future Integration Hooks**: Pre-configured event listeners for Stripe Checkout and Twilio SMS webhooks.

---

## 4. Security Architecture & Boundary Invariants
- **Input Sanitization**: All user-submitted strings (`petName`, `ownerName`, `notes`) pass through strict DOM sanitization (`textContent` mapping and regex filtering) to prevent Cross-Site Scripting (XSS).
- **Double-Submission Prevention**: The "Confirm Booking" action sets an immediate button lock (`disabled` + spinner state) preventing race conditions or duplicate booking entries.
- **Privacy & PII Protection**: Client-side storage of phone and email is restricted strictly to local browser storage; no telemetry or data scraping.
- **Accessible Focus Trap**: When the booking modal is active, focus is trapped inside the dialog and background scrolling is disabled (`overflow-hidden`).

---

## 5. Performance Budgets & Core Web Vitals
- **First Contentful Paint (FCP)**: $\le 0.8\text{s}$
- **Largest Contentful Paint (LCP)**: $\le 1.5\text{s}$
- **Interaction to Next Paint (INP)**: $\le 50\text{ms}$
- **Cumulative Layout Shift (CLS)**: $0.00$ (Explicit aspect ratios on all dog photography).
- **Bundle Budget**: Total HTML + CSS + JS payload $< 50\text{kB}$ gzipped.
