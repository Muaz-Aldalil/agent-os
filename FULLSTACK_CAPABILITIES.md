# Full-Stack Engineering Capabilities & Architecture Guide

## 1. Executive Mandate
This Autonomous Senior Engineering Agent operates as a **Full-Stack Senior Staff Software Engineer & Principal Systems Architect**. It is designed to navigate, design, implement, and verify both frontend client applications and backend distributed services without contract drift or architectural silos.

---

## 2. High-Level Stack Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FULL-STACK CAPABILITY MAP                       │
├───────────────────────────────────┬────────────────────────────────────┤
│ FRONTEND SUBSYSTEM                │ BACKEND SUBSYSTEM                  │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Next.js 15+ App Router & React  │ • Laravel 11+ & Modern PHP 8.3/8.4 │
│ • RSC vs RCC Leaf-Node Boundaries │ • Strict Types & Form Requests     │
│ • Bidirectional Arabic/English    │ • Anti-N+1 Eager Loading & Indexes │
│ • CSS Logical Properties (RTL)    │ • Pest 3 Architectural Security    │
│ • 6-State Completeness Matrix     │ • Zero-Float Integer Currency Math │
│ • Temporal UI & DOM Verification  │ • Anti-IDOR Tenant Authorization   │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 3. Frontend Engineering Architecture

The frontend lifecycle is governed by strict type systems, design standards, and bidirectional layout rules:

### 3.1 Next.js 15 & React 19 ([nextjs-fullstack](file:///d:/Skills/.agents/skills/nextjs-fullstack/SKILL.md))
- **Component Boundaries**: Enforces Server Components (RSC) for data fetching and pushes Client Components (`'use client'`) to the interactive leaf nodes of the component tree.
- **Server Actions & Security ([next-server-action-guard](file:///d:/Skills/.agents/skills/next-server-action-guard/SKILL.md))**: Derives user sessions strictly on the server; validates mutation payloads with Zod schemas; prevents resource exposure via Anti-IDOR checks.
- **Suspense & Streaming**: Uses native React Suspense boundaries with skeleton fallbacks for non-blocking rendering.

### 3.2 Bidirectional (RTL/LTR) Layout Integrity ([rtl-logical-guard](file:///d:/Skills/.agents/skills/rtl-logical-guard/SKILL.md))
- **CSS Logical Properties**: Prohibits physical CSS properties (`left`, `right`, `ml-*`, `mr-*`, `pl-*`, `pr-*`).
- **Logical Utility Mapping**: Enforces bidirectional logical utilities (`ms-*`, `me-*`, `ps-*`, `pe-*`, `text-start`, `text-end`) to ensure Arabic and English interfaces mirror seamlessly by toggling `<html dir="rtl">` or `<html dir="ltr">`.

### 3.3 The 6-State Completeness Matrix ([SKILL.md](file:///d:/Skills/.agents/skills/engineering-workflow/SKILL.md))
Every frontend component and mutation hook is designed against all 6 operational states:
1. **Idle**: Pristine initial state with default payloads and valid buttons.
2. **Loading / Debouncing**: In-flight spinners, disabled triggers, and double-click prevention.
3. **Empty / Zero-State**: Graceful UI when collections or searches yield 0 results.
4. **Success / Mutated**: Optimistic update or authoritative cache invalidation.
5. **Error / Rollback**: Localized error banner, error boundary fallback, clean mutation rollback.
6. **Edge / Boundary / RTL**: Bidirectional logical spacing, overflow truncation, and integer currency formatting.

### 3.4 Temporal Verification ([ui-review-loop](file:///d:/Skills/.agents/skills/ui-review-loop/SKILL.md))
- Evaluates interactive web UI as a temporal state machine (debounced inputs, async fetches, CSS transitions) using DOM MutationObserver timelines and browser recordings rather than static screenshot guessing.

---

## 4. Backend Engineering Architecture

The backend lifecycle is governed by strict type contracts, relational database design, and high-stakes financial invariants:

### 4.1 Laravel 11+ Mastery ([laravel-mastery](file:///d:/Skills/.agents/skills/laravel-mastery/SKILL.md) & [backend-api](file:///d:/Skills/.agents/skills/backend-api/SKILL.md))
- **Strict Types**: Enforces `declare(strict_types=1);` across all PHP files.
- **Form Request Boundaries**: Enforces incoming payload validation in dedicated Form Requests before controller execution.
- **Eloquent Optimization**: Prevents N+1 database bottlenecks through proactive eager loading (`with()`) and selective column queries.

### 4.2 Architectural Security ([pest-security-guard](file:///d:/Skills/.agents/skills/pest-security-guard/SKILL.md))
- **Pest 3 Architecture Presets**: Validates `arch()->preset()->security()` and `arch()->preset()->php()`.
- **Forbidden Execution**: Strictly bans hazardous PHP functions (`eval`, `exec`, `system`, `passthru`, `shell_exec`).

### 4.3 High-Stakes Invariants & The Danger Zone Playbook ([SKILL.md](file:///d:/Skills/.agents/skills/engineering-workflow/SKILL.md))
- **Zero-Float Money Rule**: Currency calculations strictly use integer subunits (cents, piastres) or arbitrary-precision libraries (`bcmath`). Floating-point money arithmetic is prohibited.
- **ACID Ledger Symmetry**: Multi-row balance updates execute inside database transactions with pessimistic locking (`SELECT ... FOR UPDATE`).
- **Idempotency Keys**: All state-mutating endpoints (`POST`, `PUT`, `PATCH`) require unique idempotency keys to prevent duplicate billing on network retries.
- **Anti-IDOR Authorization**: Queries are always scoped to the authenticated user's tenant or session (`where('tenant_id', auth()->user()->tenant_id)`). Client-supplied IDs are never trusted blindly.
- **5-Phase Expand-and-Contract**: Zero-downtime database evolution (Expand → Dual-Write → Backfill → Cutover → Contract).

---

## 5. Full-Stack Contract Cohesion

The primary failure mode in modern full-stack systems is contract drift between frontend TypeScript interfaces and backend API resources. This agent eliminates drift via:

1. **The Framework Spine Traversal (Top-Down, 2 Hops Max)**:
   - *Frontend*: `frontend/src/app/[locale]/<route>/page.tsx` → imports child components and API mutation hooks (`useCheckout.ts`).
   - *Backend*: `backend/routes/api.php` → maps the route directly to the Controller (`OrderController.php`) and API Resource (`OrderResource.php`).
2. **Deterministic Payload Alignment**:
   - Matches model UUIDs (`string`), sanitized fields, and error response structures across client and server boundaries before generating code.
3. **AST Symbol Resolution**:
   - Queries `scripts/agent_os.py symbol <Name>` to verify signatures across languages (TypeScript, PHP, Python) without token bloat.

---

## 6. Governing Documents & References

- **Engineering Workflow Runbook**: [SKILL.md](file:///d:/Skills/.agents/skills/engineering-workflow/SKILL.md)
- **Agent Profile & Invariants**: [engineering-agent.md](file:///d:/Skills/.agents/rules/engineering-agent.md)
- **Engineering Constitution**: [engineering-constitution.md](file:///d:/Skills/.agents/rules/engineering-constitution.md)
- **Architectural Decision Records**: [DECISIONS.md](file:///d:/Skills/.agents/DECISIONS.md)
