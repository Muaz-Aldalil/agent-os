# Technical Plan: Agent OS Beginner Handbook & 11 Situation Combo Skills (`001-beginner-handbook`)

## 1. Requirement-to-Architecture Mapping

| Requirement ID | Technical Decision & Target Files |
| :--- | :--- |
| `FR-001` | Author root `HANDBOOK.md` structured around: (1) The "Fast Intern vs. Senior Tech Team" Bilingual Hook & Side-by-Side Comparison Table, (2) Live Dogfooding Proof (`docs/precode/handbook/` + `specs/001-beginner-handbook/`), (3) The 1-2-3 Traffic Light Rule & 💬 AI Chat vs. 💻 Terminal Guide, (4) One-Time Setup, (5) Top 4 Magic Commands Card, (6) All 11 Situation Cards with Option A (`/command`) + Option B (Copy-Paste Prompt), (7) CMS Frontend/Backend/DB Armor Summary, and (8) Full Skill Appendix. |
| `FR-002` | Create 11 new skill directories under `skills/<name>/SKILL.md` with valid YAML frontmatter (`name`, `description`) and structured orchestration pipelines (Intake → Stack Detection → Chained Skills → CMS Armor → Auto Self-Check & "How to Test It" Card). |
| `FR-003` | Embed both the short `/command` invocation and the complete copy-paste prompt block in every Situation Card in `HANDBOOK.md`. |
| `FR-004` | Update `SKILLS_DIRECTORY.md` and `README.md`, run `python scripts/agent_os.py index-skills`, and synchronize to `C:\Users\HP\.gemini\config` via `python scripts/agent_os.py sync --apply`. |

---

## 2. Exact File Paths to Create or Modify

### New Files:
1. `docs/precode/handbook/01-PRD.md` .. `06-IMPLEMENTATION_PLAN.md` (Completed & 100% Audited)
2. `specs/001-beginner-handbook/spec.md`
3. `specs/001-beginner-handbook/plan.md`
4. `specs/001-beginner-handbook/checklist.md`
5. `specs/001-beginner-handbook/tasks.md`
6. `skills/start-project/SKILL.md`
7. `skills/smart-feature/SKILL.md`
8. `skills/feature-fe/SKILL.md`
9. `skills/feature-febe/SKILL.md`
10. `skills/feature-full/SKILL.md`
11. `skills/feature-wp/SKILL.md`
12. `skills/fix-ui/SKILL.md`
13. `skills/fix-backend/SKILL.md`
14. `skills/check-all/SKILL.md`
15. `skills/doc-project/SKILL.md`
16. `skills/save-data/SKILL.md`
17. `HANDBOOK.md`

### Modified Files:
1. `SKILLS_DIRECTORY.md` (Add Category 8: Beginner Situation Combos & link to `HANDBOOK.md`)
2. `README.md` (Add prominent top callout linking to `HANDBOOK.md`)
3. `SKILL_INDEX.json` (Auto-updated via `python scripts/agent_os.py index-skills`)
4. `tests/test_agent_os.py` (Verify total skill count and combo skills presence if needed)
