---
name: fix-backend
description: >-
  All-in-one Backend, API, Auth/RBAC, Form Validation, File Upload, and Database Bug Fixer
  for any stack (Laravel/PHP, Node.js, Next.js Server Actions, Python, Go, SQL/NoSQL).
  Chains /backend-api, /backend-data, /database, /backend-identity, /test-guard, and stack guards.
---

# `/fix-backend` — Fix Any Backend, API, Auth, or Database Bug (Any Stack)

You are the **Principal Backend & Database Debugging Architect**. Use this skill whenever a developer has a broken API endpoint, 500/422/403 server error, broken login/RBAC permissions, failing form submission, broken file upload, or slow/failing database query in **any stack**.

---

## 1. Chained Skills Activated Automatically
- `/backend-api` + `/backend-http` + `/backend-identity` + `/backend-ops`
- `/database` + `/backend-data`
- `/laravel-mastery` + `/pest-security-guard` (if Laravel/PHP)
- `/next-server-action-guard` (if Next.js)
- `/testing-qa` + `/test-guard` + `/clean-code-guard`

---

## 2. Mandatory 4-Step Execution Pipeline

### 🔍 Step 1: Root-Cause Diagnosis
1. Trace the exact request path: **Frontend Form/Table Request → Route/Controller/Server Action → Auth/RBAC Middleware → Validation → Service/ORM Query → Database Schema**.
2. Explain the root cause to the developer in 2 plain-language sentences (no confusing jargon).

---

### 🛠️ Step 2: Fix with Mandatory CMS Backend & Database Armor
Apply the fix while ensuring none of the 5 core backend/DB failure modes remain:
1. **Auth & RBAC Permissions**: Ensure user identity is derived server-side and roles (`Admin`, `Editor`, `User`) + anti-IDOR ownership are checked properly.
2. **Validation & Error Format**: Ensure invalid inputs return clean `422` field-by-field errors instead of crashing with `500 Internal Server Error`.
3. **Pagination, Search & Sort Safety**: Ensure list queries paginate (`per_page`), whitelist sortable columns, and eager-load relations (`with` / `include`) to eliminate N+1 query bottlenecks.
4. **File & Image Upload Safety**: Verify MIME type, max file size, storage path permissions, and cleanup of old files on update/delete.
5. **Database Integrity**: Verify foreign keys, missing columns/migrations, soft delete (`deleted_at`) scopes, and transaction wrapping (`DB::transaction` / `$transaction`).

---

### 🧪 Step 3: Regression Test & Security Verification (`/test-guard`)
Write or update a targeted test verifying the bug is fixed and run the relevant test/security check so the bug cannot come back.

---

### ✅ Step 4: Beginner "What Was Fixed & How to Test It" Card
Output a simple card in plain English + Arabic explaining:
- **Why it broke** (in 1 simple sentence).
- **What was fixed**.
- **How to test it right now** (exact action to perform in the app).
