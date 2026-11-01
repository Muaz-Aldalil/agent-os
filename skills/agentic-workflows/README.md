# agentic-workflows — README

Multi-agent workflow skill for AI coding agents. Built from the *Claude Code Advanced
Full Course* (Nick Saraev, 3h) + official Anthropic/agents.md spec compliance + deep
integration with Muaz's existing ecosystem (muaz-skill, agents, commands).

**Version:** 1.0.0 · **Created:** 2026-08-21 · **Owner:** Muaz Aldalil

---

## What It Does

Eight executable workflows an AI agent can run: parallel research, consensus,
debate, build-verify loops, autonomous optimization (Karpathy autoresearch pattern),
dual-axis security audits, workspace scaffolding, and model-outage fallback.
Fixed budgets, stop-loss rules, verification gates — no "done" without tool proof.

## File Map

| File | Role |
|---|---|
| `SKILL.md` | Canonical router + global rules. **Edit this one only.** |
| `references/workflows.md` | Full step-by-step procedures (W1–W8) |
| `references/prompt-templates.md` | T1–T11 parameterized prompts |
| `references/user-profile.md` | Personalization layer — edit freely |
| `exports/AGENTS.md` | GENERATED universal version — do not edit |
| `exports/all-in-one.md` | GENERATED single-file merge — do not edit |

## Install

| Tool | Steps |
|---|---|
| **opencode** | Copy folder → `~/.config/opencode/skills/agentic-workflows/` (path already registered in opencode.json). Restart session. |
| **Claude Code** | Copy folder → `~/.claude/skills/agentic-workflows/`. Restart session. |
| **Codex / Cursor / Gemini CLI / Copilot / Windsurf / Zed / Aider / 15+ more** | Copy `exports/AGENTS.md` → your repo root as `AGENTS.md`. Nested repos supported (closest file wins). |
| **Claude Code repo-level bridge** | Add `@AGENTS.md` as first line of the repo's `CLAUDE.md`, Claude-specific notes below it. |
| **Any tool with a paste box** | Use `exports/all-in-one.md` (~25 KB, self-contained). |

Verify install: new session → ask the agent to list available skills/instructions →
`agentic-workflows` appears.

## Update Flow

1. Edit `SKILL.md` and/or `references/*` (the sources)
2. Regenerate exports (concatenate; keep header notes)
3. Re-copy to all install locations
4. Bump version + changelog below

## Uninstall

Delete the folder from each install location. No other system changes were made
(no config edits required — opencode's skills path was already registered).

## Maintenance

- Re-validate after major model/platform changes (tier mapping, adapter behavior)
- Re-run collision check when adding skills with triggers: deploy, review, audit, test
- Review `user-profile.md` quarterly or on stack changes

## Changelog

### 1.0.0 — 2026-08-21
- Initial release: 8 workflows, 11 prompt templates, capability adapters,
  ecosystem routing (quality agent, /ship, /deploy, muaz-skill security levels),
  Windows-safe commands, spec-compliant frontmatter, exports for universal intake.
