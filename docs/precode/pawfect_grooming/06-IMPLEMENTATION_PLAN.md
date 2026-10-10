# Implementation Plan: Pawfect Grooming Salon & Spa

## 1. Execution Dependency Graph

```
 Phase 1: Foundation, Head & Design Tokens
         │
         ▼
 Phase 2: Landing Page Sections & Size-Pricing Switcher
         │
         ▼
 Phase 3: Multi-Step Interactive Booking Engine (Steps 1 - 4)
         │
         ▼
 Phase 4: 5-State UI Matrix, LocalStorage & Confirmation Screen
         │
         ▼
 Phase 5: Verification, Browser Check & Audit Clearance
```

---

## 2. Phase 1 — Foundation, Head & Design Tokens
- [ ] **Task 1.1**: Initialize `index.html` with HTML5 semantic doctype, responsive viewport metadata, and favicon.
- [ ] **Task 1.2**: Configure Google Fonts (`Plus Jakarta Sans` & `Outfit`) and Tailwind CSS with custom warm palette tokens (`#FAF8F5`, `#FAF8F5`, `#D97706`).
- [ ] **Task 1.3**: Configure CSS Logical Properties (`ms-*`, `pe-*`, `text-start`) and base responsive container styles.

---

## 3. Phase 2 — Landing Page Sections & Size-Pricing Switcher
- [ ] **Task 2.1**: Build Sticky Navigation Bar with salon logo, service links, phone click-to-call, and "Book Now" CTA.
- [ ] **Task 2.2**: Build Hero Section with high-conversion headline, social proof badge (4.9★ from 350+ dogs), and primary CTA button.
- [ ] **Task 2.3**: Build Dynamic Services Grid with interactive Dog Size Selector (Small, Medium, Large, Giant) dynamically recalculating package prices and duration in real time.
- [ ] **Task 2.4**: Build Before & After Grooming Showcase with coat-type filter tabs (All, Doodles, Double Coat, Short Coat).
- [ ] **Task 2.5**: Build Testimonial Section featuring verified pet owner reviews and dog portraits.
- [ ] **Task 2.6**: Build Interactive FAQ Accordion with accessible `aria-expanded` toggle states.
- [ ] **Task 2.7**: Build Footer with opening hours, hygiene guarantee, and map directions.

---

## 4. Phase 3 — Multi-Step Interactive Booking Engine
- [ ] **Task 3.1**: Build accessible Booking Modal Container (`<dialog>` or backdrop overlay) with backdrop blur, close button, and focus management.
- [ ] **Task 3.2**: Build Step Indicator Bar showing progress across Steps 1 to 4 with active/completed styling.
- [ ] **Task 3.3**: Implement Step 1: Pet Profile (Dog Name, Breed, Weight Category selector, Age).
- [ ] **Task 3.4**: Implement Step 2: Service Selection (Pre-selected package from landing page + checkbox spa add-ons like Blueberry Facial & Teeth Brushing).
- [ ] **Task 3.5**: Implement Step 3: Date & Slot Picker (Min-date restricted calendar input + dynamic morning/afternoon time pill buttons).
- [ ] **Task 3.6**: Implement Step 4: Owner Information (Full Name, Phone number, Email address, Special Handling / Temperament Notes).

---

## 5. Phase 4 — 5-State UI Matrix, LocalStorage & Confirmation Screen
- [ ] **Task 4.1**: Implement **Idle State**: Pristine forms, enabled buttons, clear price calculation summaries.
- [ ] **Task 4.2**: Implement **Loading State**: Simulated 600ms booking processing with animated paw spinner and locked button.
- [ ] **Task 4.3**: Implement **Success State (Step 5)**: High-fidelity Appointment Confirmation Card with generated appointment reference code (`PAW-XXXX`), dog summary, preparation instructions, and "Add to Calendar" button.
- [ ] **Task 4.4**: Implement **Error State**: Inline red alerts and boundary validation on empty required fields (Name, Phone, Email format).
- [ ] **Task 4.5**: Implement **Empty State**: Date selector handling days with zero available slots, displaying a friendly prompt to choose alternative dates.
- [ ] **Task 4.6**: Implement `BookingStore` in vanilla JS with LocalStorage persistence and draft recovery.

---

## 6. Phase 5 — Verification, Quality Gates & Pre-Flight Clearance
- [ ] **Task 5.1**: Run `python scripts/agent_os.py precode audit docs/precode/pawfect_grooming` to verify 100% Pre-Coding Readiness Score.
- [ ] **Task 5.2**: Test interactive booking flow end-to-end: select dog size, pick package, choose time slot, submit booking, verify confirmation.
- [ ] **Task 5.3**: Audit responsive behavior on mobile (375px), tablet (768px), and desktop (1280px).
- [ ] **Task 5.4**: Validate WCAG 2.1 AA contrast compliance and keyboard navigation.
