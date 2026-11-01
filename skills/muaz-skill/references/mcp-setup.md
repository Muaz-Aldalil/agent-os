# MCP Setup — Design Intelligence

How to configure MCPs for muaz-skill. MCPs are optional enhancements — the skill works without them, but design quality improves significantly with Mobbin.

---

## Where to Add MCPs

### Global (all projects — OpenCode v2 Schema)

Edit `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "timeout": {
      "startup": 30000,
      "catalog": 30000,
      "execution": 60000
    },
    "servers": {
      "mobbin": {
        "type": "remote",
        "url": "https://api.mobbin.com/mcp"
      }
    }
  }
}
```

### Project-level (single project — OpenCode v2 Schema)

Create `opencode.json` in project root (or run `opencode mcp add <name> --url <url>`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "mobbin": {
        "type": "remote",
        "url": "https://api.mobbin.com/mcp"
      }
    }
  }
}
```

---

## Available MCPs

### Mobbin (Highest Impact)

**What it does**: 600k+ real app screens from 1600+ shipped products. Search by pattern type (pricing, onboarding, dashboard, etc.) and get real examples with annotations.

**Setup**:
1. Add to `opencode.json` under `mcp.servers`:
```json
"mobbin": {
  "type": "remote",
  "url": "https://api.mobbin.com/mcp"
}
```
2. Restart OpenCode (or run `opencode reload`)
3. Authenticate via OAuth when prompted (`/mcps` inside OpenCode)
4. Verify: ask agent "search Mobbin for pricing page examples"

**Pricing**: Free tier (limited searches) / Pro ($19/mo) / Team ($49/mo)

**When to use**: Before Phase 3 — agent MUST search real screens before designing (Hard Rule 17)

**Agent workflow**:
```
1. Search Mobbin for "[pattern]" (e.g., "SaaS pricing page")
2. Get 3-5 real examples from shipped products
3. Analyze patterns: layout structure, component choices, whitespace strategy
4. Cite specific examples in blueprint DESIGN EVIDENCE field
5. Design from those patterns, not from training data
```

### Figma

**What it does**: Read/write Figma files directly. Extract colors, typography, layout, components from existing designs.

**Setup**:
1. Add to `opencode.json` under `mcp.servers`:
```json
"figma-dev-mode-mcp-server": {
  "type": "remote",
  "url": "https://mcp.figma.com/mcp"
}
```
2. Restart OpenCode (or run `opencode reload`)
3. Authenticate via OAuth when prompted
4. Verify: ask agent "extract design DNA from this Figma link: [url]"

**When to use**: Only when user provides a Figma file link. Not needed for designs created from scratch.

**Agent workflow**:
```
1. User provides Figma link
2. Extract design DNA: colors, typography, layout, components
3. Cross-reference with search engine results
4. Merge: Figma aesthetic + product-appropriate structure
```

### Higgsfield (Optional)

**What it does**: AI image/video generation with 30+ models (Flux, SDXL, etc.). Generate custom visuals for projects.

**Setup**:
1. Add to `opencode.json` under `mcp.servers`:
```json
"higgsfield": {
  "type": "remote",
  "url": "https://mcp.higgsfield.ai/mcp"
}
```
2. Restart OpenCode (or run `opencode reload`)
3. Authenticate via OAuth when prompted
4. Verify: ask agent "generate a hero image for a SaaS landing page"

**Pricing**: Paid credits per generation (varies by model)

**When to use**: When project needs custom hero images, illustrations, or product shots. Not required for most projects.

---

## Full Example Config (OpenCode v2)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "timeout": {
      "startup": 30000,
      "catalog": 30000,
      "execution": 60000
    },
    "servers": {
      "StitchMCP": {
        "type": "remote",
        "url": "https://stitch.googleapis.com/mcp",
        "headers": {
          "X-Goog-Api-Key": "<YOUR_STITCH_API_KEY>"
        },
        "oauth": false
      },
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "oauth": false
      },
      "mobbin": {
        "type": "remote",
        "url": "https://api.mobbin.com/mcp",
        "disabled": true
      },
      "figma-dev-mode-mcp-server": {
        "type": "remote",
        "url": "https://mcp.figma.com/mcp",
        "disabled": true
      },
      "higgsfield": {
        "type": "remote",
        "url": "https://mcp.higgsfield.ai/mcp",
        "disabled": true
      }
    }
  }
}
```

---

## Verification

After adding MCPs, restart OpenCode and verify:

1. **Mobbin**: "Search Mobbin for onboarding flow examples" — should return real screens
2. **Figma**: "Extract design DNA from [figma link]" — should return color/typography/layout data
3. **Higgsfield**: "Generate a hero image for a dark-themed SaaS" — should return image

If verification fails:
- Check MCP URL is correct
- Check OAuth authentication completed
- Check internet connection
- Restart OpenCode

---

## Windows Notes

- `anti-slop.sh` requires bash. On Windows, use git bash: `& "C:\Program Files\Git\bin\bash.exe" scripts/anti-slop.sh .`
- WSL also works if configured: `wsl -- bash scripts/anti-slop.sh .`

---

### Google Stitch MCP (`StitchMCP`) + Official Google Stitch Skills (`google-labs-code/stitch-skills`)

**What it does**: Already configured in Antigravity (`StitchMCP`) and paired with all **16 official Google Stitch skills** across 3 plugins (`stitch-design`, `stitch-build`, `stitch-utilities`):
- **Design & Canvas (`stitch-design`)**: `/generate-design`, `/manage-design-system`, `/extract-design-md`, `/extract-static-html`, `/code-to-design`, `/upload-to-stitch`
- **Design Utilities & Loops (`stitch-utilities`)**: `/design-md`, `/site-md`, `/taste-design`, `/enhance-prompt`, `/stitch-loop`
- **Production Code Conversion (`stitch-build`)**: `/react-components`, `/shadcn-ui`, `/react-vite-dashboard`, `/react-native`, `/remotion`

**When to use**:
- Phase 2–3: Use `/taste-design`, `/design-md`, `/site-md`, and `/manage-design-system` to synthesize `DESIGN.md` and sync design systems with `StitchMCP`.
- Phase 3–4: Use `/enhance-prompt`, `/generate-design`, and `/stitch-loop` to generate or iterate visual screens via `StitchMCP`, then convert them into modular code with `/react-components`, `/shadcn-ui`, or `/react-vite-dashboard`.
- Reverse-Engineering / Sync: Use `/extract-design-md` or `/code-to-design` to sync existing code and Stitch canvases.

---

## How MCPs Interact with the Skill

MCPs are **not dependencies** — the skill works without them. But when available:

| MCP / Skill Suite | Phase | What It Enables |
|---|---|---|
| **StitchMCP + 16 Google Stitch Skills** | Phase 2-4 | Generate screens (`/generate-design`), manage design systems (`/manage-design-system`, `/design-md`), run iterative loops (`/stitch-loop`), and convert to React/shadcn (`/react-components`, `/shadcn-ui`) |
| Mobbin | Phase 2-3 | Search real screens → cite in blueprint field 13 |
| Figma | Phase 2-3 | Extract design DNA → merge with search engine |
| Higgsfield | Phase 4-5 | Generate custom images → no stock photos |

The skill's CSV data (styles, colors, fonts, compositions) provides the foundation. MCPs add real-world evidence and canvas generation on top.

---

## Priority Order

1. **StitchMCP + Google Stitch Skills** — pre-installed and active for screen generation, `DESIGN.md` synthesis, and React/shadcn conversion
2. **Mobbin** — highest impact for real-world shipped screen references
3. **Figma** — only needed when user has Figma file
4. **Higgsfield** — optional, adds cost per generation
