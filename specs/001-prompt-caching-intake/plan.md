# Implementation Plan: Prompt Caching & Optimized Agent Intake

**Branch**: `001-prompt-caching-intake` | **Date**: 2026-10-08 | **Spec**: [spec.md](file:///d:/Skills/.agents/specs/001-prompt-caching-intake/spec.md)

**Input**: Feature specification from `specs/001-prompt-caching-intake/spec.md`

## Summary

This plan implements an end-to-end prompt caching and optimized intake architecture for the Antigravity Agent OS. It eliminates the multi-turn "latency tax" and repetitive token costs by partitioning prompt intake into strict stability tiers ("Static-First, Dynamic-Last"), guaranteeing 100% byte-for-byte prefix hash invariance for foundational instructions, normalizing LF line endings, enforcing deterministic key/alphabetical sorting across all tool and skill manifests, and introducing an automated cache efficiency auditor in `agent_os.py`.

## Technical Context

- **Language/Version**: Python 3.14+ (Windows PowerShell environment)
- **Primary Dependencies**: Built-in Python standard library (`hashlib`, `json`, `pathlib`, `re`, `unicodedata`) — zero external dependencies
- **Storage**: In-memory prompt construction + filesystem cached representations (`.agent_snapshot.json`, `SKILL_INDEX.json`)
- **Testing**: Python `unittest` via `agent_os.py test`
- **Target Platform**: Windows 11 / Antigravity Agent Runtime
- **Project Type**: Autonomous Agent OS & Developer Tooling Framework
- **Performance Goals**: Prefix hash assembly < 5ms; 100% byte stability on Tier 0–2 across consecutive turns
- **Constraints**: Zero floating-point math; no external pip dependencies; strict adherence to Human-Agent Engineering Constitution

## Constitution Check

| Principle | Check Status | Architectural Enforcement |
| :--- | :--- | :--- |
| **I. Authority Boundary** | **PASS** | Plan optimizes technical intake architecture without modifying business or product rules. |
| **II. Grounding Law** | **PASS** | All prompt components are inspected and verified from active files in the workspace. |
| **III. Prompt Caching** | **PASS** | Foundational instructions, tool definitions, and skill indexes are front-loaded in deterministic order; dynamic timestamps are isolated at the tail. |
| **IV. Execution Lock** | **PASS** | Follows dependency-ordered tasks without conversational interruption. |
| **V. Empirical Evidence** | **PASS** | Verifiable by automated tests checking exact SHA-256 prefix equality and token metrics. |
| **VI. Clean Continuity** | **PASS** | Integrates with `snapshot.py` and `PROGRESS.md` to ensure state snapshots form stable cache prefixes. |

## Project Structure & Target Files

```text
D:\Skills\.agents/
├── scripts/
│   ├── prompt_cache.py            # [NEW] Core intake stratification & deterministic serialization engine
│   ├── agent_os.py                # [MODIFY] Register 'cache-audit' and 'cache-sim' CLI commands
│   ├── skill_indexer.py           # [MODIFY] Ensure deterministic sorted JSON serialization
│   └── snapshot.py                # [MODIFY] Enforce deterministic key ordering and LF formatting
├── tests/
│   └── test_prompt_caching.py     # [NEW] Unit test suite verifying prefix stability, ordering, and leak isolation
├── specs/001-prompt-caching-intake/
│   ├── spec.md                    # Feature Specification
│   ├── plan.md                    # Implementation Plan (this document)
│   ├── checklist.md               # QA & Acceptance Checklist
│   └── tasks.md                   # Dependency-ordered execution checklist
```

## Architectural Design: The 5-Tier Intake Hierarchy

```
┌────────────────────────────────────────────────────────┐  ◄── TIER 0: IMMUTABLE BASE
│ System Identity & Core Constitution                   │      - engineering-constitution.md
│ (Zero turn-to-turn changes)                            │      - engineering-agent.md
├────────────────────────────────────────────────────────┤  ◄── TIER 1: CAPABILITY MANIFEST
│ Tool Schemas & Canonical Skill Index                   │      - Deterministic alphabetically sorted
│ (Changes only when tools/skills are added/removed)    │      - SKILL_INDEX.json / tool signatures
├────────────────────────────────────────────────────────┤  ◄── TIER 2: REPOSITORY GROUNDING
│ Repository Architecture & Decision Records             │      - DECISIONS.md summary
│ (Stable per workspace session)                         │      - Project structure boundaries
├────────────────────────────────────────────────────────┤  ◄── CACHE BREAKPOINT (Prefix Hash Boundary)
│ TIER 3: Conversation History Prefix                    │      - Prior turns (User + Assistant + Tool)
│ (Appended monotonically turn-by-turn)                  │      - Preserves previous turn KV cache
├────────────────────────────────────────────────────────┤  ◄── TIER 4: VOLATILE TAIL CONTEXT
│ Current Turn User Request & Dynamic Telemetry          │      - <USER_REQUEST>
│ (Volatile tokens strictly isolated at prompt end)      │      - Current clock timestamp & ephemeral state
└────────────────────────────────────────────────────────┘
```

## Deterministic Serialization Protocol

1. **Newline Normalization**: All incoming markdown, constitution blocks, and JSON strings are normalized to `\n` (stripping Windows `\r\n`), guaranteeing identical byte tokens regardless of git autocrlf settings.
2. **Alphabetical Sorting**:
   - Tool declarations sorted by `tool_name`.
   - Skill manifests sorted by `skill_id`.
   - JSON dumps use `sort_keys=True` and `separators=(',', ':')` for canonical formatting.
3. **Tail Isolation**:
   - Timestamps, session UUIDs, git diff stats, and execution durations are strictly prohibited from appearing before Tier 4.

## Complexity Tracking

Zero constitutional violations. Zero external libraries added. Standard library only.
