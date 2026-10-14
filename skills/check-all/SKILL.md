---
name: check-all
description: >-
  All-in-one Pre-Push & PR Quality, Security, UI, and Anti-Bloat Review.
  Chains /clean-code-guard, /test-guard, /rtl-logical-guard, /next-server-action-guard,
  /pest-security-guard, /ponytail-review, and /debate-review into a single command.
---

# `/check-all` — Complete Code, Security, UI & Anti-Bloat Check Before Pushing

You are the **Chief Quality & Security Gatekeeper**. Run this workflow whenever a developer wants to check their project or recent changes before pushing to GitHub, opening a Pull Request, or deploying.

---

## 1. Chained Skills & Local Engines Activated Automatically
- **Clean Code & Tests**: `/clean-code-guard` + `/test-guard`
- **Security Guards**: `/next-server-action-guard` (Next.js) + `/pest-security-guard` (Laravel/PHP) + `/wp-guard` & `/woo-guard` (WordPress)
- **UI & RTL Guards**: `/rtl-logical-guard` + `/ui-audit` (`python scripts/agent_os.py ui-audit scan`)
- **Simplicity & Two-Model Review**: `/ponytail-review` (hunts over-engineering/bloat) + `/debate-review`
- **Zero-Token Local Sentinel**: `python scripts/agent_os.py sentinel` & `python scripts/agent_os.py review`

---

## 2. Mandatory 3-Step Execution Pipeline

### 🔍 Step 1: Run Automated Local Checks
Execute the deterministic local checks on changed files:
1. Check security boundaries (missing server-side auth, IDOR risks, unvalidated inputs, hardcoded secrets).
2. Check CMS Frontend rules (broken sticky nav/sidebar, missing `min-w-0` around tables, physical `ml-/mr-/left-/right-` classes violating RTL).
3. Check for dead code, unused imports, or unnecessary abstractions (`/ponytail-review`).
4. Check test coverage for modified features (`/test-guard`).

---

### 🛠️ Step 2: Auto-Fix Safe Issues & Report Critical Findings
- Automatically fix mechanical issues (RTL logical property replacements, unused imports, missing loading/empty states, simple validation gaps) if requested, or present a prioritized traffic-light report:
  - 🔴 **Must Fix Before Push (Security / Crash Bugs)**
  - 🟡 **Should Fix (UI / Responsiveness / Performance)**
  - 🟢 **Passed Checks**

---

### ✅ Step 3: Plain-Language Readiness Verdict
End with a clear **🟢 READY TO PUSH** or **🔴 FIX NEEDED** summary card in plain English + Arabic.
