# Architectural Layer & Domain Boundaries

Sources:
- Robert C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (2017) — Ch. 22, "The Clean Architecture" & The Dependency Rule.
- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003) — Ch. 14, "Maintaining Model Integrity" (Bounded Contexts & Anti-Corruption Layers).
- Martin Fowler, *Patterns of Enterprise Application Architecture* (2002) — Ch. 9, "Service Layer" & Ch. 10, "Repository".
- Alistair Cockburn, *Hexagonal Architecture (Ports and Adapters)* (2005).

## Contents

- Why LLMs systematically break architectural boundaries
- Rule 25: Unidirectional Layer Flow (No Layer Skipping)
- Rule 26: Domain & Application Shell Isolation (No Cross-Domain / Shell Leaks)
- Rule 27: No Abstraction Leaks Across Layer Contracts
- Stack-specific boundary maps (Next.js/TS, Laravel/PHP, Python/Node)
- Self-check for Architectural Boundaries

---

## Why LLMs systematically break architectural boundaries

When prompted to implement or fix a feature, language models optimize for **single-file locality**: they put validation, business policy, persistence queries, and response formatting directly inside whichever file is open in context (usually a Controller, Route handler, or UI Page). This produces three high-cost structural defects:

1. **Layer Skipping (Controller/UI -> Repository/Raw DB):** Transport handlers bypass the `Service` / `Action` layer and call `Repository` classes or raw ORM queries directly. Business rules become trapped inside HTTP controllers or React components and cannot be reused by CLI jobs, webhooks, or queues.
2. **Cross-Domain & Shell Bleed:** Modules reach across domain boundaries into another domain's internal repositories, or Public pages import `/admin/*` layout shells (and vice versa).
3. **Upward Abstraction Leaks:** Low-level persistence details (raw SQL exceptions, ORM query builders, vendor SDK response wrappers, or unmasked model columns) leak upward into controllers and client payloads.

---

## Rule 25 — Unidirectional Layer Flow (No Layer Skipping)

**Principle.** Source code dependencies and runtime calls must flow inward through well-defined layers:

```text
Presentation / Transport (UI Component, Page, Controller, Route, Webhook)
   │
   ▼
Application / Orchestration (Service, Action, UseCase, Server Action)
   │
   ▼
Domain & Data Access (Domain Entity, Repository, ORM / SQL Query)
```

### Smells to flag (Critical / Important)

- **Controller -> Repository / Raw DB Bypass:** An HTTP Controller (`*Controller.php`, `*.controller.ts`) or API route handler directly injects/calls a `*Repository`, runs raw SQL (`DB::raw`, `DB::select`, `prisma.$queryRaw`), or opens manual DB transactions (`DB::beginTransaction()`, `prisma.$transaction`) instead of delegating to a `Service` or `Action`.
- **Client UI -> Server/DB Leak (`CLIENT_SERVER_BOUNDARY_LEAK`):** A client-side UI file (`"use client"`, browser component) imports server-only persistence or infrastructure modules (`prisma`, `@/lib/db`, `repositories/*`, `fs`, `child_process`, or non-public environment secrets). **Severity: Critical.**
- **Business Policy in Presentation:** Calculating pricing, discounts, commissions, or role eligibility inside a Blade/JSX template or HTTP controller instead of an authoritative backend `Service` / `Action`.

### Bad (Layer Skipping in Controller)

```php
// app/Http/Controllers/OrderController.php
public function store(StoreOrderRequest $request, OrderRepository $orderRepo): JsonResponse
{
    // BAD: Controller bypasses Service/Action layer, opens DB transaction,
    // and talks directly to Repository + raw DB.
    return DB::transaction(function () use ($request, $orderRepo) {
        $order = $orderRepo->create($request->validated());
        DB::statement('UPDATE inventory SET reserved = reserved + 1 WHERE id = ?', [$request->item_id]);
        return response()->json($order);
    });
}
```

### Good (Controller -> Action/Service -> Repository)

```php
// app/Http/Controllers/OrderController.php
public function store(StoreOrderRequest $request, PlaceOrderAction $placeOrder): JsonResponse
{
    $orderDto = $placeOrder->execute($request->user(), $request->toDto());
    return OrderResource::make($orderDto)->response()->setStatusCode(201);
}
```

---

## Rule 26 — Domain & Application Shell Isolation (No Cross-Domain / Shell Leaks)

**Principle.** Each Bounded Context and Application Shell owns its internal components and persistence. Cross-boundary communication must go through public contracts or shared design tokens—never by reaching into another boundary's internals.

### Smells to flag

- **Public vs. Admin Shell Bleed (`SHELL_BOUNDARY_LEAK`):**
  - A Public route/page (`app/[locale]/(public)/*`, storefront pages) importing `/admin/*` shell components (`AdminSidebar`, `AdminNavbar`, `@/components/admin/*`).
  - An `/admin/*` route/page importing or rendering the Public `Navbar` or Public `Footer`.
  - *Note:* Public and Admin shells share primitive design-system tokens and base UI atoms (`Button`, `Input`, `Modal`), but must maintain strictly separate layout shells and navigation trees.
- **Cross-Domain Repository Intrusion (`CROSS_DOMAIN_LEAK`):**
  - A service in Domain A (e.g., `BillingService` or `CatalogController`) directly importing and querying Domain B's internal repository (`Identity\UserRepository` or `Affiliate\CommissionRepository`) instead of calling Domain B's public `Service` or dispatching a domain event.

### Bad (Cross-Domain & Shell Leak)

```tsx
// src/app/[locale]/(public)/courses/page.tsx
import { AdminSidebar } from "@/components/admin/AdminSidebar"; // BAD: Admin shell leaked into Public page
import { userInternalRepo } from "@/domains/identity/repositories/user.repo"; // BAD: Internal repo leak
```

### Good (Clean Shell & Domain Boundary)

```tsx
// src/app/[locale]/(public)/courses/page.tsx
import { PublicShell } from "@/components/layout/PublicShell";
import { getPublishedCourses } from "@/domains/catalog/services/catalog.service";
```

---

## Rule 27 — No Abstraction Leaks Across Layer Contracts

**Principle.** A layer must not expose its internal implementation mechanism—database driver types, ORM query builders, raw SQL errors, or third-party SDK transport wrappers—in its public parameters, return values, or thrown exceptions.

### Smells to flag

- **ORM Builder / Cursor Leak:** A `Repository` or `Service` returning an unexecuted ORM query builder (`Eloquent\Builder`, `PrismaPromise`, SQLAlchemy `Query`) to a Controller so the Controller chains `.where(...)` or `.paginate(...)` on it.
- **Third-Party SDK Transport Leak:** A domain service returning `Stripe\ApiResponse`, `AxiosResponse`, or `GuzzleHttp\Psr7\Response` instead of a domain-typed result (`PaymentReceiptDto`).
- **Database Exception / Internal Column Leak:** Allowing `PDOException`, `PrismaClientKnownRequestError`, or raw model rows containing `password`, `remember_token`, or internal audit flags to cross the HTTP/Server Action boundary without mapping to a domain error and response DTO/Resource.

---

## Stack-Specific Boundary Maps

| Stack | Presentation / Transport | Orchestration / Business Policy | Persistence / Infrastructure |
| :--- | :--- | :--- | :--- |
| **Next.js App Router** | `app/**/page.tsx`, Client Components (`"use client"`), `route.ts` | Server Actions (`actions.ts`), `src/services/*`, `src/domains/*/services/*` | `src/repositories/*`, `src/lib/db.ts`, Prisma / Drizzle |
| **Laravel 11+** | `app/Http/Controllers/*`, `app/Http/Requests/*`, `app/Http/Resources/*`, Blade/Livewire | `app/Actions/*`, `app/Services/*`, `app/Domains/*/Actions/*` | `app/Repositories/*`, `app/Models/*`, Migrations |
| **Python (FastAPI / Django)** | `routers/*`, `views.py`, `serializers.py` | `services/*`, `use_cases/*` | `repositories/*`, `models.py`, SQLAlchemy / Django ORM |

---

## Self-Check for Architectural Boundaries

Before shipping or approving code:

1. **No Layer Skipping:** Did any Controller, Route handler, or UI Page directly call a `Repository`, raw SQL (`DB::raw`, `$queryRaw`), or multi-step transaction instead of delegating to a `Service` / `Action`?
2. **Client/Server Purity:** Did any `"use client"` component import a database client, repository, server-only helper, or secret env var?
3. **Shell Separation:** Did any Public page import `/admin/*` navigation/shell components, or did any `/admin/*` page render the Public Navbar/Footer?
4. **Cross-Domain Encapsulation:** Did any module import another domain's internal `Repository` instead of its public `Service`?
5. **Clean Return Contracts:** Do services and repositories return domain DTOs/models rather than leaking ORM query builders, third-party HTTP wrappers, or raw DB exceptions?
