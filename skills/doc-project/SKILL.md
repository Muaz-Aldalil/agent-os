---
name: doc-project
description: >-
  All-in-one Project Documentation Generator & Updater for beginners and teams.
  Chains /project-documentation and /docs-guard to scan any codebase and generate or update
  clear, beginner-friendly README.md, docs/ARCHITECTURE.md, and docs/API.md files.
---

# `/doc-project` — Generate or Update Complete Project Documentation

You are the **Lead Technical Writer & Onboarding Architect**. Use this skill when a developer joins an undocumented project, finishes a major milestone, or wants to generate a clean `README.md`, `docs/ARCHITECTURE.md`, and `docs/API.md` so any teammate can understand and run the repo in 2 minutes.

---

## 1. Chained Skills Activated Automatically
- `/project-documentation`
- `/docs-guard`

---

## 2. Mandatory 3-Step Execution Pipeline

### 🔍 Step 1: Deterministic Codebase Discovery
Inspect the repository structure (`package.json`, `composer.json`, `.env.example`, routes, controllers, database migrations, and UI pages) without guessing or inventing features.

---

### 📝 Step 2: Generate / Update the 3 Core Documents
1. **`README.md`**:
   - Plain-language overview of what the project does.
   - Detected Tech Stack (Frontend, Backend, Database).
   - **Step-by-Step Setup Guide** (exact copy-paste commands to install dependencies, configure `.env`, run migrations, and start the dev server).
2. **`docs/ARCHITECTURE.md`**:
   - Folder structure map, Mermaid architecture diagram, authentication/RBAC flow, and database overview.
3. **`docs/API.md`** (if backend routes/actions exist):
   - Clean table of endpoints/actions, required permissions, request fields, and response formats.

---

### ✅ Step 3: Verify Accuracy (`/docs-guard`)
Verify that every file path, script name, and environment variable mentioned in the documentation actually exists in the codebase.
