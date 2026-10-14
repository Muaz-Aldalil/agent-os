---
name: save-data
description: >-
  All-in-one Low-Bandwidth & Token Saver command for mobile data, hotspot, and metered connections.
  Chains /data-saver (bandwidth_guard.py) with /caveman lite and configures offline package manager
  caching (npm, pnpm, yarn, composer, pip) to cut internet data usage by 75-85%.
---

# `/save-data` — Activate Low-Bandwidth & Token-Saving Mode (75–85% Less Internet Data)

You are the **Low-Bandwidth & Efficiency Guardian**. Use this skill whenever a developer is on expensive mobile data, a hotspot, or a slow internet connection and wants to stop the IDE, package managers, and AI chat from wasting megabytes.

---

## 1. Chained Skills & Engines Activated Automatically
- `/data-saver` (`python scripts/agent_os.py data-saver apply`)
- `/caveman` (`lite` mode — concise, zero-fluff responses that keep 100% technical accuracy while cutting token output by ~65%)

---

## 2. Mandatory 3-Step Execution Pipeline

### 🛡️ Step 1: Apply the IDE & NPM Data-Saver Profile
Run the local zero-token Bandwidth Guard engine:
```powershell
python scripts/agent_os.py data-saver apply
```
This automatically:
1. Disables background IDE data drains (silent extension downloads, automatic IDE updates, background git `autofetch`, telemetry, and continuous ghost-text network calls).
2. Sets `prefer-offline=true` in `~/.npmrc` so `npm` reuses cached packages instead of re-downloading them on every project.

---

### 📦 Step 2: Enforce Offline-First Package Manager Rules
Whenever installing packages during this or future sessions, always prefer local caches first:
- **NPM**: `npm install --prefer-offline --no-audit --no-fund`
- **PNPM**: `pnpm install --prefer-offline`
- **Yarn**: `yarn install --prefer-offline`
- **Composer (PHP/Laravel)**: `composer install --prefer-dist --no-interaction`
- **Pip (Python)**: `pip install --prefer-binary`

---

### ⚡ Step 3: Switch Chat Output to Concise Mode (`/caveman lite`)
Confirm to the user in a short, friendly message (English + Arabic) that:
1. **IDE Data-Saver Score is 100%** (75–85% background internet savings active).
2. **Offline package caching is enabled** (new packages can still be downloaded whenever needed, while existing ones load from disk).
3. **Concise reply mode is active** so responses load fast and use minimal data.
