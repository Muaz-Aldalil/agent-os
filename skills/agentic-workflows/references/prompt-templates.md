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
