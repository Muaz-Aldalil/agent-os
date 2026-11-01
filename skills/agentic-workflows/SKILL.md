---
name: agentic-workflows
description: >
  Orchestrates multi-agent workflows: parallel research fan-out, stochastic consensus,
  structured debate, build-verify QA loops, autonomous optimization research, dual-axis
  security audits, agent workspace scaffolding, and model-outage fallback. Use when a
  task needs parallelization, independent second opinions, continuous self-improvement
  loops, pre-deploy security review, workspace organization, or recovery from model
  degradation. Triggers on: parallelize, fan-out, subagents, consensus, debate,
  second opinions, research loop, auto-research, make it faster continuously,
  security audit, scaffold workspace, organize folders, model down, fallback.
---

# Agentic Workflows

Executable multi-agent procedures with fixed budgets, verification gates, and
platform-adaptive spawning. Every workflow ends in tool-verified proof — narration
is not evidence.

## When to Load

- Task needs ≥ 3 independent research angles or sources
- User asks for options, rankings, or "every way to X"
- High-stakes decision where convergence matters (debate)
- Any build/fix reaching a "done" claim (verification loop)
- Continuous improvement against a metric ("make this faster overnight")
- Before deploys or after touching auth/payments/secrets (security)
- New business/life/project workspace, or a junkyard folder
- Primary AI platform is down, degraded, or rate-limited

## Global Rules

**Model tiers** — never hardcode model names; map to whatever the platform offers:
- `ORCH` (orchestrator): strongest available model. Plans, synthesizes, decides.
- `WORK` (worker): cheapest capable model. Researches, drafts, executes slices.

**Budgets & stop-loss**
- Consensus N ≤ 10 (default 5) · debate rounds ≤ 5 (default 3) · fan-out workers ≤ 8
- Stop-loss: 2 consecutive same-kind failures → stop, report, ask
- Chained autonomous steps multiply error odds (0.9³ ≈ 73%) — human checkpoint at chain length 3+

**Permission boundaries (Harmonized with Agent OS Constitution)**
- ASK FIRST: spawning subagents or `/opencode-delegate` · file edits beyond declared scope · external directories · creating PRs · `git commit` or `git push` · security fixes touching auth
- AUTO: read-only codebase inspection · local diagnostic/test CLI commands (`agent_os.py`) within authorized workspace
- NEVER: auto-commit or auto-push without explicit Owner instruction · spawn unrequested subagents · commit secrets/.env · touch card data · claim done without tool-verified proof

**Verification law**: no "done" without pasted tool output (test results, exit codes,
gate scores). Escalation ladder: retry-with-docs → change approach → fresh agent → human.

**Context discipline**: one task per worker; fresh context beats compacted mega-session;
write a handoff note and restart rather than pushing through degraded quality.

## Ecosystem Routing

If operating inside Muaz's configured environment (Agent OS + opencode + muaz-skill), route instead of reimplementing:

| Need | Route to | Status |
|---|---|---|
| Build QA / final gate | `python D:\Skills\.agents\scripts\agent_os.py scan` + `sentinel` + `ui-audit` + `muaz-skill` `scripts/quality_gate.py` | available |
| Security depth definitions | `muaz-skill` `references/security-levels.md` (L1/L2/L3) + `security-audit` / `pentest` / `bug-hunter` | available |
| Deploy execution | `/devops-deploy` + W6 security-audit pre-checks, then hand off for manual Owner push | available |
| WORK tier | Subagent delegation ONLY when explicitly requested by the Owner (Prohibition #20) | gated by Owner approval |
| GitHub operations | `github` MCP server tools or local `git` CLI in shell (read-only unless Owner instructs `"commit"` / `"commit and push"`) | available |

Outside that environment: use generic equivalents from `references/workflows.md`.

## Workflow Router

| Trigger | Workflow | Freedom | Details |
|---|---|---|---|
| ≥ 3 independent angles to investigate | **W1 parallel-research** | high | fan-out workers → synthesize |
| Decision, ranking, "every way to X" | **W2 consensus** | medium | N independent lists → tally modes + outliers |
| Conflicting options, high stakes | **W3 debate** | medium | round-robin critique → convergence |
| Anything reaching "done" | **W4 build-verify-loop** | medium | implement → fresh QA → fix → proof |
| "Make X better continuously" | **W5 auto-research-loop** | low | metric+change+assess, branch advance/reset, never stop |
| Pre-deploy / secrets / auth touched | **W6 security-audit** | medium | app axis (L1-L3) + AI-workspace axis |
| New or messy workspace | **W7 workspace-setup** | medium | claude.md pointers + context/ folders, clean root |
| Platform down/degraded | **W8 model-fallback** | low | port to agents.md standard, verify, resume |

Composition: W2 seeds W3 · W1 feeds any research need · W4 precedes deploys · W6 gates them.

## Capability Adapters

Detect once per session:
1. Native subagents available → true parallel; WORK tier = small model
2. Sequential-only agents → fresh context per worker, run serially, outputs isolated
3. Single-threaded → simulated lenses in one context, clearly labeled

Full adapter rules: see `references/workflows.md` (bottom section).

## References

Load on demand — one level deep, read fully when needed:
- `references/workflows.md` — all 8 workflows: steps, checklists, output contracts, failure modes
- `references/prompt-templates.md` — T1–T11 parameterized prompts per phase
- `references/user-profile.md` — user's stack, conventions, communication contract

## Execution Order Per Workflow

1. Check trigger matches · 2. Verify preconditions (refuse if unmet) ·
3. Paste checklist into response · 4. Execute steps with tier tags ·
5. Honor output contract · 6. Run Verification · 7. Report with proof.
