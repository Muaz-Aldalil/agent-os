---
name: data-saver
description: >-
  Audits, activates, and manages the low-bandwidth Data-Saver Profile for Antigravity IDE.
  Reduces daily internet data consumption by 75-85% by disabling background ghost-text completions,
  silent IDE and extension updates, continuous Git autofetch, and telemetry.
compatibility: Platform-agnostic, applies globally to Antigravity IDE settings across Windows, macOS, and Linux.
---

# /data-saver: Antigravity IDE Bandwidth & Data-Saver Controller

## 1. Overview & Purpose

The `/data-saver` skill optimizes Antigravity IDE for developers operating in bandwidth-constrained, high-cost internet environments (such as mobile data packages in Sudan). 

By default, modern AI IDEs can silently consume **10 GB+ daily** due to background processes (continuous inline code completion on every keystroke, Git autofetch polling every few minutes, silent IDE updates, and unconstrained file indexing).

This skill provides automated auditing, one-click enforcement of a **100% Data-Saver Profile**, and automated backup/restore mechanisms.

---

## 2. Global vs. Workspace Scope

> [!IMPORTANT]
> The Data-Saver Profile is **ACTIVE GLOBALLY**.
> It writes directly to your IDE's global configuration file:
> - **Windows**: `%APPDATA%\Antigravity IDE\User\settings.json`
> - **macOS**: `~/Library/Application Support/Antigravity IDE/User/settings.json`
> - **Linux**: `~/.config/Antigravity IDE/User/settings.json`
>
> Once applied, it protects **every workspace, every folder, and every project** you open in the IDE.

---

## 3. The 13 Data-Saving Safeguards

| Category | Setting | Action & Data Impact |
| :--- | :--- | :--- |
| **Inline Autocomplete** | `editor.inlineSuggest.enabled: false` | **Saves 3–5 GB daily**. Disables cloud predictions on every keystroke. Trigger manually with `Ctrl + Space`. |
| **Automatic Updates** | `update.mode: "manual"`<br>`extensions.autoUpdate: false`<br>`extensions.autoCheckUpdates: false` | **Saves 500MB–1.5GB**. Prevents multi-hundred-megabyte IDE updates from downloading silently in the background. |
| **Git Network Polling** | `git.autofetch: false`<br>`git.autorefresh: false` | **Saves 300–800 MB daily**. Stops Git from constantly polling GitHub for remote refs. Only connects when you run `git pull` or `git push`. |
| **Telemetry & Diagnostics** | `telemetry.telemetryLevel: "off"`<br>`workbench.enableExperiments: false`<br>`workbench.settings.enableNaturalLanguageSearch: false` | **Saves 100–300 MB daily**. Stops sending diagnostic logs and crash dumps. |
| **Background NPM/TS** | `npm.fetchOnlinePackageInfo: false`<br>`typescript.disableAutomaticTypeAcquisition: true` | Eliminates silent package registry lookups and automatic `@types` downloads. |
| **File Indexing & Watchers** | `files.watcherExclude`<br>`search.exclude` | Excludes `node_modules`, `vendor`, `.next`, `dist`, `build`, and `.agent_snapshots` from background scanning and indexing. |

---

## 4. Execution Commands

### Via Antigravity Chat
- **/data-saver**: Audits the active settings and reports current score.
- **/data-saver apply**: Enforces all 13 safeguards and creates a backup.
- **/data-saver restore**: Reverts settings to the previous backup.

### Via Terminal CLI
```bash
# Check current data-saving score
python scripts/agent_os.py data-saver status

# Apply all data-saving settings
python scripts/agent_os.py data-saver apply

# Restore original settings from backup
python scripts/agent_os.py data-saver restore
```

---

## 5. The 4 Golden Rules for Low-Data Coding

1. **New Chat per Task (`/new`)**:
   Always start a fresh chat thread when beginning a new task. Long conversations (30+ turns) re-send the entire chat history on every prompt, burning hundreds of kilobytes per turn.
2. **Manual Suggestions on Demand**:
   Use **`Ctrl + Space`** on any line when you want code completion suggestions, instead of keeping continuous streaming ghost text enabled.
3. **Use `/caveman` for Compressed Responses**:
   The `/caveman` skill instructs the agent to give concise, telegraphic answers, saving 50–70% of response tokens and download bandwidth.
4. **Prefer Local CLI Tools**:
   Local scripts (`scripts/ui_audit_engine.py`, `scripts/agent_os.py`, `npm test`) run in `< 200ms` on your CPU using **0 MB of internet data**.
