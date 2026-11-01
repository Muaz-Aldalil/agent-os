# agentic-workflows — All-in-One Export

> GENERATED v1.0.0 - do not edit. Source: SKILL.md + references/.
> Self-contained single file for tools that accept pasted instructions.

---

# PART 1/4 — SKILL.md (router + global rules)

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

**Permission boundaries**
- ASK FIRST: file edits beyond declared scope · external directories · creating PRs · security fixes touching auth
- AUTO: bash commands · commits with AI-authored messages
- NEVER: commit secrets/.env · touch card data · claim done without proof

**Verification law**: no "done" without pasted tool output (test results, exit codes,
gate scores). Escalation ladder: retry-with-docs → change approach → fresh agent → human.

**Context discipline**: one task per worker; fresh context beats compacted mega-session;
write a handoff note and restart rather than pushing through degraded quality.

## Ecosystem Routing

If operating inside Muaz's configured environment (opencode + muaz-skill), route instead of reimplementing:

| Need | Route to |
|---|---|
| Build QA / final gate | `quality` agent → `/ship` command (score ≥ 128/160) |
| Security depth definitions | muaz-skill `references/security-levels.md` (L1/L2/L3) |
| Deploy execution | `/deploy` command — pre-checks only, then hand off |
| WORK tier | configured small model |
| GitHub operations | MCP tools, qualified as `github:<tool_name>` |

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

---

# PART 2/4 — Workflows (W1-W8)

# Workflows

> Eight executable workflows. Execute in order; never skip Verification.
> Tier tags: [ORCH] = strongest available model · [WORK] = cheapest capable model.
> Agent spawning: see Capability Adapters at the bottom of this file.

## Contents
- W1 parallel-research
- W2 consensus
- W3 debate
- W4 build-verify-loop
- W5 auto-research-loop
- W6 security-audit
- W7 workspace-setup
- W8 model-fallback
- Capability Adapters
- Cross-workflow rules

---

## W1 — parallel-research

**Trigger**: task requires investigating ≥ 3 independent sources/angles/options.
**Freedom**: high. **Typical cost**: minutes, not seconds.

**Preconditions**
- [ ] Question decomposes into ≥ 3 genuinely independent angles
- [ ] Synthesis deliverable is defined (what the user actually receives)

**Checklist**
```
- [ ] Decomposed into N angles (N ≤ 8)
- [ ] Workers spawned with T1
- [ ] All worker outputs collected
- [ ] Synthesis run with T2
- [ ] Contradictions surfaced to user, not silently resolved
```

**Steps**
1. [ORCH] Decompose `{TOPIC}` into N independent angles. If an angle depends on another's result, it is NOT independent — sequence it after synthesis instead.
2. [WORK × N] Spawn N workers, each with template T1. Vary lenses deliberately (e.g., docs-first, competitor scan, user-impact, cost).
3. [ORCH] Fan-in: run T2 with all outputs. Deliverable format from `user-profile.md` conventions.

**Output contract**: single synthesized deliverable + one "gaps & contradictions" section.

**Verification**: every claim in synthesis traces to ≥ 1 worker output; no orphan facts.

**Failure**: a worker returns empty/off-topic → respawn once with narrower angle → still bad → drop angle, note gap in synthesis. 2 consecutive worker failures anywhere → stop-loss, escalate to user.

---

## W2 — consensus

**Trigger**: significant decision, option ranking, strategy choice, or "give me every way to X".
**Freedom**: medium.

**Preconditions**
- [ ] Goal phrased as one sentence
- [ ] N chosen: default 5, max 10 (diminishing returns beyond)

**Checklist**
```
- [ ] N workers ran T3 with distinct lenses
- [ ] Tally run with T4
- [ ] Consensus AND outliers presented
- [ ] Unexplored-space estimate included
```

**Steps**
1. [ORCH] Define goal + pick N lenses that genuinely differ (not 5 paraphrases of one view).
2. [WORK × N] Each worker runs T3 independently. No cross-visibility.
3. [ORCH] Run T4 tally. Present consensus items by frequency; list outliers verbatim with their lens attribution.

**Output contract**: CONSENSUS list (ranked) + OUTLIERS list + coverage estimate.

**Verification**: frequency counts sum correctly; each outlier names its source lens.

**Failure**: heavy duplication across workers (>70% identical lists) → lenses were not independent; redo step 1 with harder contrasts before re-spawning.

---

## W3 — debate

**Trigger**: options conflict after W2, or stakes are high enough that convergence matters more than speed.
**Freedom**: medium.

**Preconditions**
- [ ] Seeded positions exist (from W2 or user)
- [ ] Rounds set: default 3, max 5

**Checklist**
```
- [ ] Round 1..K executed with T5
- [ ] Position changes tracked per agent per round
- [ ] Convergence or documented irreducible disagreement
```

**Steps**
1. [ORCH] Seed room with positions (W2 outliers make excellent seeds).
2. [WORK × N] Per round: all agents see all prior positions, run T5 simultaneously.
3. [ORCH] After final round: extract converged recommendations + name surviving disagreements explicitly.

**Output contract**: converged recommendation set + "still disputed" list with both sides' strongest arguments.

**Verification**: every final position cites which round's argument changed it (or states "unchanged since seed").

**Failure**: agents converge too fast (round 1 unanimity) → lenses too similar; inject a contrarian worker and rerun once.

---

## W4 — build-verify-loop

**Trigger**: any feature/build/fix task reaching "done" claim.
**Freedom**: medium (steps fixed; implementation free).

**Preconditions**
- [ ] Scope stated in one sentence
- [ ] Standard named (project conventions / quality gate / user-profile.md)

**Checklist**
```
- [ ] Blueprint approved before code (plan-first)
- [ ] Implementation complete
- [ ] Fresh-context QA pass run (T6)
- [ ] All Critical/High findings fixed and re-checked
- [ ] Tool-verified proof collected (tests/build/lint output)
```

**Steps**
1. [ORCH] Blueprint: affected files, approach, risks. Get user approval if scope exceeds declared task.
2. [ORCH] Implement.
3. **QA pass — ecosystem routing**:
   - In Muaz's opencode setup → delegate review to the `quality` agent; final gate = `/ship` (score ≥ 128/160 per muaz-skill quality-gate).
   - Anywhere else → spawn FRESH QA agent (zero project context) with T6 against `{STANDARD}`.
4. [ORCH] Fix Critical/High findings → repeat QA pass. Loop until no Critical/High remain (max 3 iterations, then escalate).
5. Collect proof: test results, build/lint exit codes, gate score.

**Output contract**: change summary + QA verdict + pasted tool-proof (per verification law).

**Verification**: proof is tool output, not narration. No proof = not done.

**Failure**: same finding survives 3 fix rounds → stop, present to user with analysis. QA finds architecture-level problem → return to step 1, do not patch.

---

## W5 — auto-research-loop

**Trigger**: "make X faster/better/cheaper continuously", overnight optimization, iterative metric improvement.
**Freedom**: low (mechanics fixed; experiments creative). Verified against karpathy/autoresearch.

**Preconditions — ALL THREE required, refuse to start without them**
- [ ] Metric: objective, standardized, automatable (`{MEASUREMENT_CMD}` runs unattended)
- [ ] Change method: bounded edit scope (ideally ONE file/system)
- [ ] Assessment: measurement itself ≤ ~10% of experiment budget

**Checklist**
```
- [ ] Metric + direction stated (lower/higher better)
- [ ] Measurement command verified working once manually
- [ ] Git checkpoint committed on clean baseline
- [ ] Experiment branch created
- [ ] Baseline recorded in log file
- [ ] Loop started (T7 rules active)
```

**Steps**
1. [ORCH] Validate preconditions. State metric, command, budget back to user BEFORE first run.
2. Commit baseline on main. Create experiment branch.
3. Loop (template T7): pick one hypothesis → minimal change → commit → run measurement redirected to log file → grep/tail results only (never flood context) → improved: advance branch · equal/worse: reset → append idea/result/decision to untracked log → next.
4. Kill any run exceeding 2× budget; treat as failure and revert.
5. Crash → read last ~50 log lines → fix → retry; abandon approach after 3 failures.
6. NEVER pause to ask whether to continue. Run until the human interrupts.

**Budget math** (why speed matters): loop cycle ≈ measure + change. At ~30s cycles ≈ 120/day; even a 2% win rate ≈ 2–3 improvements daily compounding (1.01³⁰ ≈ +34%/month shape). Slow cycles kill the compounding — protect them.

**Output contract**: running loop + untracked experiment log; on interrupt: summary table of best result vs baseline.

**Verification**: baseline and current best metrics quoted from log files with commit hashes.

**Failure**: metric flaky (same code, different scores) → fix measurement stability FIRST — optimizing against noise corrupts everything downstream.

---

## W6 — security-audit

**Trigger**: before deploy, after adding auth/payments/external endpoints, handling secrets, or "is this safe".
**Freedom**: medium. Runs on TWO axes — application AND AI workspace.

**Preconditions**
- [ ] Depth level L1/L2/L3 chosen (ask if unclear; default L1)
- [ ] Audit runs in a FRESH agent (no development context — developer bias hides findings)

**Checklist**
```
- [ ] Level selected
- [ ] Fresh-agent audit executed (T8)
- [ ] Findings triaged Critical→Low
- [ ] User approved fix list
- [ ] Fixes applied via T9 in a DIFFERENT agent than the auditor
- [ ] Re-audit of fixed items passed
```

**Steps**
1. [ORCH] Select depth. L1 public · L2 authenticated · L3 sensitive data. In Muaz's setup, match the project profile's Security Level field.
2. [FRESH ORCH] Run T8 audit — report only, no fixes.
3. [ORCH] Triage with user; get explicit approval for fix list (hard boundary: security fixes still ask before editing).
4. [DIFFERENT AGENT] Apply fixes via T9, one commit per fix, verify each.
5. Re-run T8 scoped to fixed items only.

**Dual-axis coverage**:
- Axis A (application): depth per level — headers/CSP/secrets-in-client at L1; +auth/injection/access-control at L2; +encryption/PII flows at L3. In Muaz's setup defer detail definitions to muaz-skill `references/security-levels.md`.
- Axis B (AI workspace, always): chat-log secret leaks · .env hygiene/gitignore · typosquat package risk · database row-level security · internet-reachable endpoint inventory · zero card-data tolerance.

**Output contract**: findings table (severity, evidence location, fix) + applied-fix commit list + residual-risk statement.

**Verification**: re-audit shows fixed items resolved; grep confirms no secrets in tracked files.

**Failure**: Critical found in production system → report immediately, do not batch with other findings. Auditor proposes fix touching auth flow → mandatory human review regardless of severity.

---

## W7 — workspace-setup

**Trigger**: new business/life/project workspace, or existing folder has become a junkyard.
**Freedom**: medium.

**Preconditions**
- [ ] Scope decided: BUSINESS or PERSONAL (never mix in one root)
- [ ] Areas enumerated; north star identified

**Checklist**
```
- [ ] T10 scaffold executed
- [ ] Every folder has claude.md (pointer, not storage)
- [ ] context/ exists per area; junk files purged
- [ ] northstar.md contains exactly one goal
- [ ] Root stays clean — nothing loose
```

**Steps**
1. [ORCH] Run T10 with scope/areas/goal. Max 2 clarifying questions, then build.
2. Purge invented files: delete any generated context the user didn't ask for (keep business-overview + northstar).
3. For PERSONAL workspaces organize by life-domain ("clients of your personal life": health, citizenship, learning…).
4. Site/tool projects live in SEPARATE folders — never inside the operations workspace.
5. Temp outputs go to `active/.tmp`; skills declare their own output paths so files land predictably without agentic search.

**Output contract**: folder tree printout + one-line purpose per claude.md.

**Verification**: root contains only directories + claude.md + northstar.md; zero loose files.

**Failure**: user can't name a north star → build structure anyway with `northstar.md: TODO`, flag it — don't block setup on it.

---

## W8 — model-fallback

**Trigger**: primary platform degraded/outaged, rate-limited hard, or results visibly worse over days.
**Freedom**: low.

**Preconditions**
- [ ] Degradation confirmed (not a one-off error): 2+ failed sessions or explicit outage notice
- [ ] Workspace state committed (no uncommitted work crosses platforms)

**Checklist**
```
- [ ] Degradation confirmed, not transient
- [ ] Work committed
- [ ] T11 port executed
- [ ] Port verified (skills/conventions/context all present)
- [ ] First task on fallback platform completed successfully
```

**Steps**
1. [ORCH] Confirm degradation. Check status sources before declaring outage.
2. Commit everything. Note branch state.
3. Run T11 port to agents.md standard (read natively by Codex, Cursor, Gemini CLI, opencode, Copilot, Windsurf, Zed, Aider and 15+ more tools).
4. Verify port completeness: every skill, convention, and context path from old config appears in new.
5. Resume work on fallback; keep changes platform-neutral until primary returns.
6. On primary recovery: diff, merge, retire duplicates.

**Standing defense** (cheaper than reaction): keep memory synchronized across formats during normal operations — when updating claude.md, mirror to agents.md. One line in claude.md suffices: "when you update this file, update agents.md identically."

**Output contract**: ported workspace + verification checklist + anything unportable flagged.

**Verification**: first real task completes on fallback platform without consulting the old config.

**Failure**: fallback platform also degraded → drop to thinnest viable workflow: plain markdown instructions + manual execution; document what was lost for post-recovery rebuild.

---

## Capability Adapters

How "spawn N agents" maps to your environment. Detect once per session:

| Environment | Native parallel | Adapter |
|---|---|---|
| Claude Code / opencode with Task tool | ✅ true parallel | Spawn subagents; WORK tier = configured small model |
| Tools with sequential-only agents | ❌ | Simulate: fresh context per worker, run sequentially, keep outputs isolated — consensus/debate still valid, just slower |
| Single-threaded, no subagents | ❌ | Degraded mode: role-play passes yourself ("as conservative lens… as challenger lens…"), label clearly as simulated |

Rules regardless of adapter:
- One task per worker — never stack roles
- Worker prompts carry ONLY their slice (template enforces)
- Sequential simulation multiplies wall-clock time — reduce N rather than skip synthesis

## Cross-workflow Rules

- **Composition**: W2 feeds W3 (outliers become debate seeds) · W1 feeds anything needing research · W6 gates deploys · W4 precedes any deploy handoff
- **Compounding-error law**: chained autonomous steps multiply failure odds (0.9³ ≈ 73%). Insert human checkpoints at chain length 3+
- **Stop-loss global**: 2 consecutive failures of the same kind → stop, report, ask
- **Escalation ladder**: retry with documentation read → change approach → fresh agent → human
- **Context discipline**: fresh session beats compacted mega-session; if quality degrades mid-task, restart with a written handoff note instead of pushing through

---

# PART 3/4 — Prompt Templates (T1-T11)

# Prompt Templates

> Parameterized prompts for each workflow phase. Replace `{PARAMS}` before sending.
> Derived from field-tested patterns (Nick Saraev advanced course + Karpathy autoresearch).
> Freedom level per template: see bracket tag. Keep worker prompts SHORT — workers
> don't need context about the overall mission, only their slice.

---

## Contents
- T1 Fan-out worker (research)
- T2 Synthesizer (fan-in)
- T3 Consensus worker
- T4 Consensus tally
- T5 Debate round
- T6 Fresh-context QA
- T7 Auto-research kickoff
- T8 Security audit (dual-axis)
- T9 Audit fix application
- T10 Workspace scaffold (chief of staff)
- T11 Model-fallback port

---

## T1 — Fan-out worker (research) `[medium freedom]`

```text
Research ONLY the following question, from ONLY this angle: {ANGLE}.
Subject: {TOPIC}
Constraints: do not read other agents' work; do not attempt synthesis; cite concrete
facts, numbers, and sources you actually found. If information is unavailable, say so
plainly instead of guessing.
Output: max {MAX_WORDS} words, bullet points, one "confidence: high/medium/low" tag per bullet.
```

## T2 — Synthesizer (fan-in) `[high freedom]`

```text
{N} researchers independently investigated: {TOPIC}. Their findings follow below.
Integrate them: merge overlapping findings, keep genuine outliers, score each final
item on impact vs effort, and flag any contradictions between researchers rather than
silently resolving them.
Deliverable: {DELIVERABLE_SPEC}
--- FINDINGS START ---
{ALL_WORKER_OUTPUTS}
--- FINDINGS END ---
```

## T3 — Consensus worker `[medium freedom]`

```text
Independently list every viable way to {GOAL}. Aim for at least {MIN_IDEAS} ideas.
Adopt this lens while brainstorming: {LENS} (e.g., conservative traditionalist /
boundary-pushing innovator / first-principles reasoner / conventional-wisdom challenger).
No filtering, no grouping — raw list only.
```

## T4 — Consensus tally `[low freedom]`

```text
Here are {N} independent idea lists about {GOAL}. Tally identical and semantically
equivalent ideas. Report:
1. CONSENSUS: ideas appearing in ≥ {MAJORITY_PCT}% of lists, ordered by frequency
2. OUTLIERS: ideas appearing once — keep them visible, do not discard
3. Coverage estimate: what parts of the possibility space look unexplored
```

## T5 — Debate round `[medium freedom]`

```text`
Round {K} of {ROUNDS}. You are agent {ID} in a shared discussion about {TOPIC}.
All agents' previous positions follow. This round you MUST:
1. Name at least one claim from another agent you disagree with, and why
2. Update your own position if convinced — changing your mind is expected, not losing
3. Propose recombinations: better solutions built from others' pieces
Positions: {ALL_PRIOR_POSITIONS}
```

## T6 — Fresh-context QA `[low freedom]`

```text
You are a QA reviewer with NO prior context on this project — that is intentional;
your ignorance is your value. Review {SCOPE: files|diff|feature} against {STANDARD}.
Report only defects you can point to concretely (file:line), each with severity
Critical/High/Medium/Low and a suggested fix. Do not praise. Do not summarize the
implementation. If you find nothing Critical after a genuine review, say exactly that.
```

## T7 — Auto-research kickoff `[low freedom]`

```text
Set up an autonomous optimization loop.
Target: {TARGET_FILE_OR_SYSTEM} — the ONLY thing you may modify.
Metric: {METRIC} ({DIRECTION: lower|higher} is better), measured by {MEASUREMENT_CMD}.
Budget: each experiment ≤ {BUDGET}; total runtime until I interrupt you.
Rules:
- One experiment branch at a time; commit before each change
- Run measurement with output redirected to a log file; read results via grep/tail,
  never flood context with full logs
- Improved → advance branch. Equal/worse → git reset to pre-experiment commit
- Record every run (idea, result, decision) in an untracked log file
- A run exceeding 2× budget is killed and treated as failed
- Crash → read last ~50 log lines, fix, retry; give up on an approach after 3 failures
- NEVER pause to ask whether to continue. Run until interrupted.
Begin by restating metric, measurement command, and budget, then start experiment 1.
```

## T8 — Security audit (dual-axis) `[medium freedom]`

```text
Perform a security audit at depth L{LEVEL: 1|2|3}.

AXIS A — Application (depth per level):
L1 public site: headers, CSP baseline, client-side secret leaks, console logging
L2 authenticated: + auth/session handling, injection surfaces, access control
L3 sensitive data: + encryption at rest/in transit, PII flows, audit logging

AXIS B — AI workspace (always):
1. Conversation logs: confirm no secrets were pasted into chat history
2. .env hygiene: exists, gitignored, never read/displayed in session
3. Dependencies: flag unfamiliar or low-popularity packages (typosquat risk)
4. Database: row-level security status if external DB is used
5. Public endpoints: enumerate what is internet-reachable and why
6. Card data: confirm zero PAN/card material anywhere in repo or logs

Output: findings table (severity, file/evidence, fix), then a prioritized fix list.
Do not fix anything yet — report only.
```

## T9 — Audit fix application `[low freedom]`

```text
Apply ONLY these approved fixes, nothing else: {FIX_LIST}
After each fix: run {VERIFY_CMD} and show output. Commit per fix with message
`fix(security): {slug}`. Stop and ask if any fix conflicts with another.
```

## T10 — Workspace scaffold (chief of staff) `[medium freedom]`

```text
You are my chief of staff. Design ONE folder my agent works out of, organized so any
part of my life/business runs from it.
Scope: {SCOPE}. Type: {BUSINESS|PERSONAL}. Areas: {AREA_LIST}.
North star (what matters most right now): {GOAL}
Rules:
- One folder per area; each becomes a top-level folder
- Every folder gets a short claude.md: what it is, your role there, how it's organized,
  where things live. It POINTS, it does not STORE
- Real knowledge lives in context/ inside each area as markdown files
- Create northstar.md at root containing only the goal above
- Flag overlapping or missing areas
- Ask at most 2 questions if truly needed; otherwise build it
```

## T11 — Model-fallback port `[low freedom]`

```text
Our primary agent platform is unavailable. Port this workspace to the universal
agents.md standard so any tool can resume:
1. Duplicate the workspace config; rename Claude-specific files (.claude/, claude.md)
   to the agents.md convention (spec: agents.md)
2. Convert instructions verbatim — do not reinterpret or improve them mid-port
3. List anything that could not be ported mechanically
4. Verify: new config mentions all skills, conventions, and context paths the old one did
```

---

# PART 4/4 — User Profile

# User Profile — Muaz Aldalil

> Personalization layer for agentic-workflows. Edit freely; the skill reads this
> before executing any workflow. Delete sections that don't apply.

## Identity
- Freelance generalist developer; agency owner in progress
- Mid-level across JS/TS, Python, Swift, PHP
- Bilingual: English + Arabic — respond in the language the user writes in

## Communication Contract
- Match the user's energy level; be direct
- Proactivity is suggestive: propose improvements, ask before doing
- When stuck: complex problem → teach briefly (user wants to learn); trivial → just fix it
- Blueprint before code: plan-first on every build task

## Tech Stack Defaults (use unless told otherwise)
- **Frontend**: React, Next.js, Vue, Nuxt, Svelte, Angular, HTML+Tailwind
- **Backend**: Node.js, Python, Swift (Vapor), Laravel
- **Database**: PostgreSQL, MongoDB, SQLite, Firebase, Redis
- **Mobile**: React Native, Flutter, SwiftUI
- **Tools**: Git, Docker, Figma, Postman
- **Test matrix**: Vitest (JS/TS), pytest (Python), XCTest (Swift), Playwright (E2E)
- **Hosting**: Vercel, Netlify, AWS; CI via GitHub Actions

## Code Conventions
- camelCase variables/functions · PascalCase components
- Files grouped by feature, not type
- No `any` — typed or `unknown`
- JSDoc on exported functions
- Comments explain WHY, not WHAT

## Git Behavior
- Frequent small focused commits; auto-commit with AI-authored messages allowed
- Ask before creating PRs
- Check GitHub issues regularly when working in a repo

## Hard Boundaries (mirror of platform permissions)
- ASK FIRST: editing files outside declared scope · external directory access · creating PRs
- AUTO-ALLOWED: bash commands · commits with AI messages
- NEVER: commit secrets or .env files · touch credit-card data · claim "done" without tool-verified proof
