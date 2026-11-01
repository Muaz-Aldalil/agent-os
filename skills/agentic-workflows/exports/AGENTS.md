# AGENTS.md — Agentic Workflows (Universal Export)

> GENERATED from agentic-workflows v1.0.0 — do not edit.
> Source of truth: skill folder `SKILL.md` + `references/`.
> This file is self-contained so it works when copied alone to any repo root.

Multi-agent workflow procedures: parallel research, consensus, debate, build-verify
loops, autonomous optimization, security audits, workspace scaffolding, model fallback.
Load `agentic-workflows` skill when triggers below match; otherwise treat as standing guidance.

## Workflow Router

| Trigger | Workflow | Core mechanic |
|---|---|---|
| ≥ 3 independent angles to investigate | **parallel-research** | fan out N cheap workers on isolated angles → strongest model synthesizes; surface contradictions |
| Decision / ranking / "every way to X" | **consensus** | N independent lists through distinct lenses → tally frequency → keep modes AND outliers |
| Conflicting options, high stakes | **debate** | round-robin shared-room critique (default 3 rounds) → converged set + documented disagreements |
| Any task reaching "done" | **build-verify-loop** | implement → FRESH zero-context QA pass → fix Critical/High → loop ≤ 3 → paste tool proof |
| "Make X better continuously" | **auto-research-loop** | requires metric + bounded change scope + automated assessment; commit per experiment; improved = advance branch, worse = reset; log to file, never flood context; never pause to ask |
| Pre-deploy / auth/payments/secrets touched | **security-audit** | fresh-agent audit, report-only → user approves fixes → different agent applies → re-audit |
| New or messy workspace | **workspace-setup** | one folder per area; claude.md points (never stores); context/ holds real knowledge; root stays empty |
| Platform down / degraded / rate-limited | **model-fallback** | commit work → port config to agents.md standard → verify completeness → resume platform-neutral |

## Global Rules

**Model tiers** (map to whatever the platform offers — never hardcode names):
- ORCHESTRATOR: strongest available — plans, synthesizes, decides
- WORKER: cheapest capable — researches, drafts, executes slices

**Budgets**: consensus N ≤ 10 (default 5) · debate rounds ≤ 5 (default 3) · fan-out ≤ 8 ·
stop-loss after 2 consecutive same-kind failures → stop and ask.

**Compounding-error law**: chained autonomous steps multiply failure odds (0.9³ ≈ 73%).
Insert human checkpoints at chain length 3+.

**Verification law**: no "done" claim without pasted tool output (tests, exit codes,
scores). Escalation ladder: retry-with-docs → change approach → fresh agent → human.

**Permission boundaries**
- ASK FIRST: edits beyond declared scope · external directories · creating PRs · security fixes touching auth
- AUTO: bash commands · commits with AI-authored messages
- NEVER: commit secrets or .env · touch card data

**Context discipline**: one task per worker; worker prompts carry only their slice;
fresh session beats degraded mega-session — write a handoff note and restart instead.

**Agent spawning adapters**:
1. Native subagents → true parallel (worker tier = small/fast model)
2. Sequential-only agents → fresh context per worker, serial execution, isolated outputs
3. Single-threaded → simulated lenses in one context, clearly labeled as simulated

## Security Quick Reference (dual-axis)

- Application axis: secrets out of client bundles/URLs/localStorage · security headers · CSP baseline · depth L1 public / L2 authenticated / L3 sensitive
- AI-workspace axis (always): no secrets in chat history · .env gitignored and unread · flag unfamiliar packages (typosquat risk) · row-level security on external DBs · inventory internet-reachable endpoints · zero card data anywhere

## Standing Conventions

- Respond in the user's language (English/Arabic)
- Blueprint before code; suggest improvements, ask before doing
- Frequent small commits with AI-authored messages; ask before PRs
