# Quality & Acceptance Checklist: Prompt Caching & Optimized Agent Intake

**Purpose**: Verifiable criteria to validate implementation correctness before merging
**Feature**: [spec.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/spec.md) | [plan.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/plan.md)
**Status**: ✅ All Checks Passed (100% Converged)

## 1. Intake Tier Architecture & Ordering

- [x] **Tier 0 Precedence**: Core Identity and Human-Agent Engineering Constitution are placed at the absolute start of prompt assembly.
- [x] **Tier 1 Capability Stability**: Tool schemas and indexed skills appear immediately following Tier 0 in deterministic sorted order.
- [x] **Tier 2 Architecture Grounding**: Active project ADRs and boundaries follow Tier 1 without per-turn state contamination.
- [x] **Tier 3 Monotonic History**: Conversation turns append monotonically without rewriting or reordering earlier turns.
- [x] **Tier 4 Tail Isolation**: Current user prompt, current time, and volatile telemetry are strictly positioned at the prompt tail.

## 2. Deterministic Serialization & Formatting

- [x] **Line-Ending Invariance**: All prompt blocks are normalized to `\n` (LF) regardless of Windows `\r\n` filesystem state.
- [x] **JSON Key Determinism**: All JSON structures in Tier 0–2 are serialized with sorted keys (`sort_keys=True`).
- [x] **Tool/Skill Sorting**: Tools and skills are sorted alphabetically by identifier before tokenization.

## 3. Cache Integrity & Leak Prevention

- [x] **Zero Early Clock Leak**: The system timestamp never appears in Tier 0, 1, 2, or 3.
- [x] **Zero Early Git Stats Leak**: Uncommitted file counts or dirty file arrays never appear in the static prefix.
- [x] **Prefix SHA-256 Stability**: Consecutive simulated turns with different user prompts yield identical SHA-256 hashes for the static prefix.

## 4. CLI Tooling & Diagnostics

- [x] **`agent_os.py cache-audit`**: Inspects workspace prompt components and outputs cache readiness score and prefix breakdown.
- [x] **`agent_os.py cache-sim`**: Simulates multi-turn conversation and measures prefix token reuse percentage and estimated latency savings.

## 5. Verification & Test Suite

- [x] **Automated Unit Tests**: `tests/test_prompt_caching.py` passes all test cases (hash invariance, ordering, tail isolation, LF normalization).
- [x] **Regression Suite**: Full Agent OS test suite (`agent_os.py test`) passes 100% green (48/48 tests PASS).
