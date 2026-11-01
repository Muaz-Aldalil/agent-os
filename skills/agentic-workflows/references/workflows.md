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
