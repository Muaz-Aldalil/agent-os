# Quality & Acceptance Checklist: `001-beginner-handbook`

- [x] **CHK-01**: All 6 Pre-Coding Pillars in `docs/precode/handbook/` pass `python scripts/agent_os.py precode audit` at 100%.
- [x] **CHK-02**: `HANDBOOK.md` opens with the Bilingual (English + Arabic) **"Without `.agents` (Fast Intern) vs. With `.agents` (Senior Tech Team)"** hook and side-by-side impact table.
- [x] **CHK-03**: `HANDBOOK.md` includes the **Live Proof** section showing how `/web-precode` and `/spec-kit` were used to build the Handbook itself.
- [x] **CHK-04**: `HANDBOOK.md` clearly distinguishes 💬 **Paste in AI Chat** vs. 💻 **Paste in Terminal** and highlights the **1-2-3 Traffic Light Rule** + **Top 4 Magic Commands**.
- [x] **CHK-05**: Every new project and feature command (`/start-project`, `/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, `/feature-wp`) enforces the full `/grill-me` + `/muaz-skill` Smart Intake (`references/intake-template.md` Q1–Q28 + Confirmation Summary) before writing code.
- [x] **CHK-06**: Every command is 100% stack-agnostic (auto-detects project stack or honors user's chosen Frontend, Backend, and Database stack).
- [x] **CHK-07**: CMS Frontend Armor (sticky top nav, sticky `h-dvh` sidebar with mobile drawer, `flex-1 min-w-0` main wrapper, overflow tables with sticky headers/pagination, multi-column forms with sticky save bar, all-media responsiveness, and RTL/LTR logical CSS) is embedded in both the skills and the Handbook.
- [x] **CHK-08**: CMS Backend & DB Armor (RBAC permissions on UI + API, server-side pagination/search/filter/sort, field-level server validation, safe file uploads with cleanup, and DB foreign keys/indexes/soft deletes) is embedded in both the skills and the Handbook.
- [x] **CHK-09**: Every feature/fix command enforces the post-build self-check (`/ui-review-loop`, `/clean-code-guard`, `/test-guard`, security guards) and outputs a plain-language **"How to Test It" Card** in English + Arabic.
- [x] **CHK-10**: All 11 Combo Skills are indexed in `SKILL_INDEX.json`, documented in `SKILLS_DIRECTORY.md`, synced to `~/.gemini/config`, and pass `python scripts/agent_os.py audit` and `python scripts/agent_os.py test`.
