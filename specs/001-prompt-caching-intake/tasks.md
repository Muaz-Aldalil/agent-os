# Tasks: Prompt Caching & Optimized Agent Intake

**Spec**: [spec.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/spec.md) | **Plan**: [plan.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/plan.md) | **Checklist**: [checklist.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/checklist.md)

## Phase 1: Setup & Foundational Engine

- [x] T001 Implement core prompt caching engine in `scripts/prompt_cache.py` with 5-tier stratification, LF newline normalization, and SHA-256 prefix hashing.
- [x] T002 Create comprehensive unit test suite in `tests/test_prompt_caching.py` validating prefix hash stability, deterministic ordering, and volatile tail isolation.

## Phase 2: User Story 1 - Deterministic Static-Prefix Intake (Priority: P1)

- [x] T003 [P] [US1] Enforce deterministic sorted JSON serialization with LF line endings in `scripts/skill_indexer.py`.
- [x] T004 [P] [US1] Enforce canonical key ordering and LF formatting for state persistence in `scripts/snapshot.py`.

## Phase 3: User Story 2 - Tail-Isolated Volatile Context & Ephemeral Metadata (Priority: P2)

- [x] T005 [US2] Build prompt assembly and cache efficiency simulation in `scripts/prompt_cache.py`.
- [x] T006 [US2] Codify Prompt Caching Principle III and Prefix Invariance rules into `rules/engineering-agent.md` and `rules/engineering-constitution.md`.

## Phase 4: User Story 3 - CLI Diagnostics & Tooling Integration (Priority: P3)

- [x] T007 [US3] Register `cache-audit` and `cache-sim` CLI commands in `scripts/agent_os.py`.
- [x] T008 [US3] Wire prompt cache validation into `scripts/preflight.py` and `scripts/audit_agent_os.py`.

## Phase 5: Verification & Governance Convergence

- [x] T009 Execute full Agent OS test suite via `python scripts/agent_os.py test` to guarantee 100% green verification.
- [x] T010 Record ADR-023 in `DECISIONS.md` and checkpoint operational milestones in `PROGRESS.md`.
