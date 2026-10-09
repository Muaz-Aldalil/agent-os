# Feature Specification: Prompt Caching & Optimized Agent Intake

**Feature Branch**: `001-prompt-caching-intake`

**Created**: 2026-10-08

**Status**: Draft

**Input**: User description: "using /spec-kit let's improve the prompt caching"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deterministic Static-Prefix Intake for Multi-Turn Sessions (Priority: P1)

As a developer pair-programming with the agent on multi-turn tasks, I want the agent's foundation instructions, tool schemas, and governance rules to remain 100% byte-for-byte identical across consecutive turns, so that the underlying LLM provider reuses precomputed Key-Value (KV) cache states, drastically cutting latency and token consumption.

**Why this priority**: Without static prefix stability, every turn recalculates thousands of unchanging system and schema tokens, inducing unnecessary latency tax and cost compounding.

**Independent Test**: Can be verified by simulating consecutive conversation turns with identical toolchain definitions and observing zero prefix token divergence in prompt assembly.

**Acceptance Scenarios**:
1. **Given** an active conversation session, **When** the agent transitions from Turn $N$ to Turn $N+1$, **Then** all foundational instructions (Identity, Constitution, Invariants) precede any dynamic context and remain character-for-character invariant.
2. **Given** tool and skill definitions, **When** they are loaded into the prompt intake, **Then** they are serialized in a deterministic, sorted order rather than arbitrary filesystem or hashmap order.

---

### User Story 2 - Tail-Isolated Volatile Context & Ephemeral Metadata (Priority: P2)

As an engineering owner, I want per-turn timestamps, fluctuating file stats, and transient execution telemetry to be placed strictly at the prompt tail (or after conversation history), so that early prefix cache states are never invalidated by runtime clock changes.

**Why this priority**: Injecting dynamic variables (like current time or git dirty counts) high up in prompt headers invalidates the downstream cache, causing 0% cache hit rates.

**Independent Test**: Can be verified by altering the system clock or workspace dirty file list and confirming that the foundational prefix hash remains identical.

**Acceptance Scenarios**:
1. **Given** a turn with dynamic metadata (e.g. current clock timestamp, active working tree status), **When** assembled into the prompt, **Then** these dynamic attributes are positioned in the final payload tier after the static prefix.
2. **Given** a workspace state change (e.g. dirty files modified), **When** prompt intake occurs, **Then** the foundational system prompt prefix is unaffected.

---

### User Story 3 - Compact Skill & Symbol Discovery without Context Pollution (Priority: P3)

As an agent operating within a large ecosystem (45+ skills and multi-module codebase), I want skill discovery and AST symbol lookups to ingest only targeted, compact signatures into active prompt memory rather than dumping full documentation files, so that context windows stay clean and cacheable.

**Why this priority**: Ingesting massive documentation or unneeded skill files bloats prompt memory, triggers premature session compaction, and degrades attention quality.

**Independent Test**: Can be verified by running skill search and code symbol outline queries and measuring token consumption against full-file ingestion.

**Acceptance Scenarios**:
1. **Given** an agent needing capability discovery, **When** querying available skills, **Then** it uses compact, indexed metadata summaries (< 15 lines) rather than dumping full multi-page instruction files.
2. **Given** the need to inspect code structure, **When** examining a module, **Then** the agent utilizes AST outlines instead of reading entire files into conversational context.

---

### Edge Cases

- **What happens when a new skill or tool is added mid-session?** The system must invalidate the Tier 1 capability tier cleanly while keeping Tier 0 (Core Constitution & Identity) intact.
- **What happens on session turn compaction (exceeding context limit)?** The system must generate a deterministic cognitive snapshot checkpoint that forms a fresh, stable baseline cache prefix.
- **How does the system handle platform-specific line endings (CRLF on Windows vs LF)?** All prompt serialization must normalize line endings to standard LF to prevent whitespace-induced cache invalidation.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST partition agent intake into ordered, hierarchical stability tiers: Tier 0 (Core Identity & Invariants), Tier 1 (Tool & Skill Schemas), Tier 2 (Project Architecture & ADRs), Tier 3 (Turn History), Tier 4 (Current User Prompt & Volatile Metadata).
- **FR-002**: The system MUST enforce deterministic serialization: all JSON keys, skill lists, and tool definitions in Tier 0–2 must be alphabetically sorted and serialized with normalized LF line endings.
- **FR-003**: The system MUST isolate all volatile variables (timestamps, request IDs, uncommitted file counts) to Tier 4 at the prompt tail.
- **FR-004**: The system MUST provide an intake preflight and verification command within `agent_os.py` to audit prompt prefix invariance and calculate cache efficiency metrics.
- **FR-005**: The system MUST ensure cognitive snapshots (`SESSION_SNAPSHOT.md` and `.agent_snapshot.json`) are generated with deterministic key ordering and fixed formatting to serve as stable resumption prefixes.
- **FR-006**: The system MUST restrict file inspection fanout, enforcing the AST outline / symbol resolution mechanism to prevent premature context compaction.

### Key Entities

- **Intake Tier**: A discrete layer of prompt context categorized by change frequency (Immutable, Semi-Static, Monotonic, Volatile).
- **Prefix Boundary**: The exact token checkpoint separating static, cache-eligible prompt content from dynamic turn context.
- **Serialization Formatter**: A deterministic normalization pipe ensuring consistent whitespace, key ordering, and character encoding.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% byte-for-byte prefix hash stability across consecutive turns when tool definitions and core rules are unchanged.
- **SC-002**: Prompt prefix assembly latency under 5 milliseconds for standard agent turns.
- **SC-003**: Zero volatile metadata (timestamps, session IDs, git file tallies) located in the leading 80% of prompt context.
- **SC-004**: Automated intake audit tool achieves 100% verification score across all static prompt assets.

---

## Assumptions

- The underlying LLM inference provider (Gemini, Claude, or OpenAI) implements standard left-to-right prefix KV-caching.
- The agent environment runs on Windows PowerShell with Python 3.14+ runtime available.
- Core tool capabilities and skills are loaded from local version-controlled directories (`.agents/skills`, `.gemini/config/skills`).
- No external internet dependency is required to evaluate or construct the cached prompt prefix.
