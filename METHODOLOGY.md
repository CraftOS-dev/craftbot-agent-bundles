# Agent Bundle Methodology

This file is the canonical reference for **how to build a high-quality CraftBot agent bundle**. Follow it whenever you add an agent to the v0 → v130 catalog.

If you're new to this folder: read this file first, then `PROGRESS.md` for current roster and status, then look at `agents/senior-python-engineer/` as a worked example of every step.

---

## The hard rules

These are non-negotiable. Skip any of them and the resulting agent will be generic, low-value, and indistinguishable from "I asked Claude to write a system prompt."

### 1. Never invent content. Always research.

**Every sentence in `soul.md` and `role.md` must trace back to a downloaded reference file** in `agents/<slug>/reference/`. If you can't cite the source, you can't write the sentence. The exception is short operational glue (a few sentences) that connects lifted sections — flag those clearly in `SOURCES.md`.

The "generic philosophy bullets" failure mode looks like: a 5-bullet list of pleasant-sounding rules that someone could have written without any research. If your soul.md has paragraphs that read like motivational copy, you skipped the research step.

### 2. Skills are the most important capability lever.

The agent's `enabled_skills` list is what gives it hands. A handful of decisions on this list does more to determine agent quality than thousands of words of `soul.md`. **Target double-digit counts**, not 1-5. Hunt aggressively.

Two sources to combine:

- **Bundled SOTA skills** — sourced from online catalogs (see "Where to look" below), copied into `agents/<slug>/skills/<name>/`, ship inside the `.craftbot` bundle.
- **CraftBot default skills** — already shipped on every recipient's install. Referenced by name in `agent.yaml`. Live in the repo's top-level `skills/` folder; their availability is recorded in `app/config/skills_config.json`.

### 3. SOUL.md is always-loaded context. Pay tokens deliberately.

SOUL.md is in the agent's context window on every turn. **Every sentence costs tokens forever.** Only content that drives turn-by-turn decisions belongs here.

Things that BELONG in soul.md:
- Identity / persona (who they are)
- Purpose (what they do)
- Entry procedures ("When invoked" variants per mode)
- Core operating rules (hard rules — "Always X", "Never Y", "Don't suggest Z for W")
- Mode-specific decision rules (per primary verb the agent handles)
- Decision tables (e.g., sync vs async)
- Flag-priority lists (what to surface first in review / what to fix first in a bug)
- Antipatterns to flag on sight (the quick scan)
- Order-of-operations rankings (when ranking matters — performance wins, etc.)
- Compact rules sections (error handling, resource, resilience, design, code style, project structure — short bullets, each tells the agent what to do)
- Communication style
- Output format
- Push-back / defer rules
- First-conversation PROACTIVE.md self-init footer

Things that DO NOT belong in soul.md (move to role.md):
- Capability lists (e.g., "uses TypeVar, ParamSpec, Protocol, TypedDict...") — these are facts the agent knows from training, costing tokens for no decision benefit
- Framework / tool inventories ("FastAPI, Django, Flask, SQLAlchemy, Pydantic...") — the agent already knows these
- Long exhaustive feature lists where the operative rule is already in soul.md
- Code examples (those live in role.md)
- Verbose narrative paragraphs that don't end in an actionable rule

**Test:** for every bullet in soul.md, ask "if the agent didn't see this bullet, would it make a worse decision next turn?" If no — move it to role.md.

### 4. role.md is grep-only deep reference.

`role.md` is appended to `AGENT.md`. AGENT.md is **not** loaded into the agent's default context. The agent greps it when stuck or when the SOUL.md summary isn't enough.

Use search-friendly headings: "Code review playbook", "Antipattern catalog", "Performance investigation playbook", "Refactoring procedures", "Capability reference". The agent will literally grep for these strings.

Things role.md SHOULD carry:
- Capability reference (the factual lists banished from soul.md)
- Antipattern catalog with concrete BAD/GOOD code pairs
- Step-by-step procedures (debugging, performance investigation, refactoring)
- Reference patterns (test patterns, validation patterns, resource management examples)
- Deep code examples per topic
- Anything the agent would benefit from looking up but shouldn't pay tokens for every turn

### 5. Citations live in SOURCES.md, not inline.

**Do not add `[from: X]` tags inside soul.md or role.md.** They cost tokens for no decision benefit (the agent doesn't change behavior based on citation).

Instead: a separate `SOURCES.md` file in the agent folder maps each section of soul.md and role.md back to its source file in `reference/`. This file ships in the bundle but is not loaded into context. It's for humans verifying provenance and for future updates.

### 6. PROACTIVE.md is not bundled.

The agent self-initializes proactive behavior in-conversation. Every agent's soul.md carries the same standard footer: "On first conversation, ask the user 2-3 questions about their routines, then propose a `PROACTIVE.md` setup that runs them on a schedule." The proactive layer ends up reflecting the user's actual workflow, not a generic template.

### 7. USE_CASES.md ships in every agent folder. Be honest about gaps.

Every agent **must** have a `USE_CASES.md` documenting what the agent is supposed to do, what it can actually EXECUTE today, what it currently CANNOT execute, when to use it, and when NOT to use it. This file ships in the bundle but is **not** loaded into the agent's context — it exists so users (and future contributors) can see at a glance what the agent is for and where the honest gaps are.

The "honest gaps" piece is non-negotiable. If a `video-creator` agent cannot actually render video, USE_CASES.md says so up top. If a `marketing-agent` can draft LinkedIn posts but cannot publish them, USE_CASES.md says so. The point is that nobody — user, contributor, or future-you — should be surprised by what the agent can and cannot do.

### 8. Map exhaustive use cases, research SOTA per use case, integrate the SOTA.

This is the hard rule that prevents the most common failure mode: under-capable agents that "sound right" but cannot actually execute the work in 2026 because nobody asked *"what is the SOTA way for an autonomous agent to perform this task today?"*

The mandatory three-phase loop:

**Phase A — List use cases exhaustively (aspirational, not conservative).** For the agent's role, write down *every* reasonable use case a senior practitioner of that role handles. A marketing agent doesn't have 5 use cases; it has 25+ (content strategy, content creation across 8+ formats, SEO technical audit, cannibalization audit, keyword research, topic clustering, on-page checklist, link building, AI search adaptation, social posting per platform × 6 platforms, social analytics, email lifecycle, email deliverability, post-MPP measurement, multi-language compliance, growth loops, brand voice, campaign management, lead generation, light analytics, paid ads per platform, etc.). If you stop at 5 you are about to ship a toy.

**Phase B — Research SOTA per use case.** For each use case, ask: *what is the SOTA way for an autonomous agent to perform this task today?* Search the web aggressively (2025-2026 sources, not 2022 blog posts). Catalog: (a) MCP servers in CraftBot's `mcp_config.json`, (b) third-party MCP servers (modelcontextprotocol/servers, mcp.so, smithery.ai, punkpeye/awesome-mcp-servers, glama.ai), (c) Python/npm libraries installable via `cli-anything` + `uvx`/`npx`, (d) REST APIs the agent can hit with `cli-anything` + `curl`, (e) CLI tools. SOTA changes monthly — your agent has knowledge up to its training cutoff, so a fresh web search per use case is non-negotiable.

**Phase C — Integrate.** The SOTA findings must show up in three places:
1. `agent.yaml` `mcp_servers:` — every CraftBot-catalog MCP matched in Phase B is included.
2. `agent.yaml` `enabled_skills:` — every bundled SOTA skill pack is included; `cli-anything` covers the "install via uvx/npx + curl any API" path.
3. `USE_CASES.md` "Execution status (SOTA — YYYY-MM)" table — every use case maps to a concrete `tool + path + confidence` row, with a fulfillment %.

**Floor:** 90%+ fulfillment. If less, you have not finished researching. The remaining <10% should be genuine impossibilities (e.g., GUI manipulation of proprietary desktop apps) or paywalled-on-recipient (e.g., Ahrefs API key) — not "I didn't bother to look."

If you settle for "this agent uses `filesystem` + `cli-anything`" without naming the specific 2026 SOTA tool for each use case, you have failed this rule.

---

## The ten-step workflow

### Step 1 — Plan the agent

Add or update the row in `PROGRESS.md`:
- `slug` (kebab-case, used in folder names)
- `display name`
- `tier` — `general` (covers a whole domain) or `specialized` (one slice of a domain)
- `category`
- One-liner of intent
- Initial `[ ]` status

A general/specialist pair within the same domain is encouraged: e.g., `marketing-agent` (general) + `video-creator` (specialized subset). Users compose.

### Step 2 — Research and download SOTA references

**Where to look** (in priority order):

1. **`github.com/wshobson/agents`** — folder-per-agent + folder-per-skill, ~192 agents across plugins. Look in `plugins/<domain>/agents/` and `plugins/<domain>/skills/`. Check `plugins/<domain>/commands/` too.
2. **`github.com/VoltAgent/awesome-claude-code-subagents`** — 154+ agents across 10 categories under `categories/<NN-name>/`.
3. **`github.com/msitarzewski/agency-agents`** — 232 agents, strong on agency / marketing / specialized roles.
4. **`github.com/vijaythecoder/awesome-claude-agents`** — 24 agents, framework specialists (Laravel/Rails/Vue/etc.).
5. **`github.com/JSONbored/claudepro-directory`** — directory site; may have skills + agents at `content/skills/` and `content/agents/`.
6. **`github.com/anthropics/skills`** — official Anthropic skills (currently mostly design/document/content — no engineering skills yet).
7. **`github.com/anthropics/claude-cookbooks`** — notebook-style recipes.
8. **Targeted GitHub searches** for `SKILL.md` + the domain (e.g., "SKILL.md technical writing").

**What to download** (full verbatim file content, never summaries):

- 4-8 **agent** definitions related to the role (different angles: e.g., for a backend role, fetch python-pro, backend-architect, code-reviewer, debugger, performance-engineer).
- 8-15 **skills** that match the agent's day-to-day work. Skills are the load-bearing capability.
- Any **commands / workflows** referenced in the plugins.

**Where to save:**

```
agents/<slug>/reference/
├── INVENTORY.md
├── agents/
│   ├── wshobson-<name>.md
│   ├── voltagent-<name>.md
│   └── ...
└── skills/
    ├── <skill-name>/SKILL.md
    └── ...
```

Each file starts with an HTML comment listing source URL + repo for traceability.

**A note on WebFetch:** for some files (especially long ones), WebFetch returns a summary instead of the verbatim content. When this happens, save the summary with a clear `NOTE:` block at the top stating that WebFetch summarized it and pointing to the source URL for full content. Try a re-fetch with an explicit "verbatim only" prompt before settling for the summary.

### Step 3 — Build INVENTORY.md and pause for approval

`reference/INVENTORY.md` lists every downloaded file with:
- File path
- Source URL
- Source repo (for license tracking)
- One-line description
- Status — `full` or `summary`

Plus a section "Sources Considered But Not Downloaded" explaining what you skipped and why.

**Stop here. Show the inventory to the user. Do not compose anything until they approve.** The inventory is the proof you actually researched; composition without that proof is back to "inventing."

### Step 4 — Map exhaustive use cases and research SOTA per use case

This step is the difference between a toy agent and a real one. **Do it before composing `agent.yaml`** — the SOTA findings directly drive which MCPs and skills you include.

**Phase A — List use cases exhaustively.** Write down every reasonable use case a senior practitioner of this role handles in 2026. Be aspirational. A senior role typically has 20-30+ use cases when you actually enumerate them:

- For *engineering*: write code, review code, debug, refactor, optimize perf, set up tooling, manage Git workflows, write ADRs, run security audits, set up CI, handle migrations, write integration tests, manage dependencies, profile production, instrument observability, …
- For *marketing*: content strategy, content creation (×8 formats), SEO technical audit, cannibalization audit, keyword research, topic clustering, on-page checklist, link building, AI search adaptation, social posting (×6+ platforms), social analytics, social listening, email lifecycle, email deliverability, post-MPP measurement, multi-language compliance, growth loops, brand voice, campaign management, lead generation, light analytics, paid ads (×5+ platforms), …
- For *research*: general topic investigation, market sizing, competitive intelligence, trend analysis, scientific literature, patents, datasets, targeted search, first-principles, cohort analysis, KPI design, data storytelling, deliverables (×6 formats), survey research, foreign-language source synthesis, OCR for scanned material, …
- For *video creator*: scripts, storyboards, shot lists, editing, color grading, audio engineering, motion graphics, subtitles, multi-platform export (×5+ formats), thumbnail design, YouTube optimization, TikTok viral mechanics, AI-assisted production, asset management, …
- For *technical writer*: READMEs, API docs, tutorials, reference docs, conceptual guides, ADRs, changelogs, doc-system architecture, Divio/Diátaxis classification, doc audits (prose / links / examples / a11y / analytics / search), co-authoring, diagram generation, translation, OCR for legacy docs, …

**If your list has fewer than ~15 use cases, you haven't tried hard enough.** Go wider.

**Phase B — Research SOTA per use case.** For each use case, ask the canonical question: *"What is the SOTA way for an autonomous agent to perform this task in 2026?"* This is not the same as "what tool exists?" — it's "what would a senior practitioner pick today, given an agent has `cli-anything` + `curl` + npm/uv install access?"

Search aggressively against fresh sources. Where to look:

1. **CraftBot's MCP catalog** — `app/config/mcp_config.json` (157+ servers). Cross-reference *every* SOTA tool against this catalog first — if it's already in the catalog as an MCP, add it to `agent.yaml`.
2. **Third-party MCP directories** — `github.com/modelcontextprotocol/servers`, `mcp.so`, `smithery.ai`, `glama.ai/mcp/servers`, `punkpeye/awesome-mcp-servers`, `pulsemcp.com`.
3. **Library / API ecosystems** — search for `<task> python library 2026`, `<task> npm package 2026`, `<task> API`, `<task> CLI`. Python: PyPI + uv-installable. JS: npm + npx-runnable. Both reachable via `cli-anything`.
4. **Official platform / SaaS docs** — most modern platforms publish REST APIs. Sora 2 / Veo 3.1 / Kling on Replicate; LinkedIn Marketing API; Meta Ads MCP; HubSpot mcp.hubspot.com; Klaviyo MCP; PostHog MCP; PageSpeed Insights API; SEC EDGAR XBRL; etc.
5. **Recent comparison posts** (2025-2026) — avoid 2022 listicles; the SOTA changes monthly. Look for posts titled "best X in 2026" or "X vs Y in 2026."

**For complex agents, parallelize via subagents.** Spawn one general-purpose agent per CraftBot agent (or per major use-case cluster) with the prompt: *"for each of these use cases, identify the SOTA tool/library/MCP/API and the exact execution mechanism."* Have them return a structured table. This is how the v0 agents reached 90-100% fulfillment.

**Where to save:**

```
agents/<slug>/reference/
├── INVENTORY.md
├── SOTA_USE_CASES.md       ← NEW — per-use-case SOTA mapping
├── agents/
└── skills/
```

`reference/SOTA_USE_CASES.md` structure:

```markdown
## <Use case>
- **SOTA approach:** <concrete method — name the tool/library/API>
- **Agent execution path:** <exact mechanism — "cli-anything + uvx <tool>" or "<mcp-name> MCP">
- **Source:** <URL>
- **Confidence:** ✓ Fully executable / ⚠ Executable with caveats / ✗ Genuinely impossible today
```

Plus a summary table at the bottom: use case | SOTA tool | mechanism | fulfillment.

**Phase C — Integrate (deferred to later steps).** The SOTA findings drive Step 5 (`agent.yaml` MCPs and skills) and Step 9 (USE_CASES.md execution table). Don't compose yet — finish Phase B for *all* use cases first so you have the full picture before writing.

**Verification gate at end of Step 4:** Open `SOTA_USE_CASES.md`. Count rows. If you have fewer than ~15, go back to Phase A. If your fulfillment column has more than two ✗ entries, go back to Phase B for those specific use cases — there is almost always a SOTA tool you missed.

### Step 5 — Compose `agent.yaml`

The metadata file. Fields:

```yaml
name: <Display Name>
slug: <kebab-slug>
category: <domain>
tier: general | specialized
description: >
  One paragraph of intent.
tags: [list, of, tags]

model:
  llm_provider: anthropic
  llm_model: claude-sonnet-4-5-20250929

enabled_skills:
  # ── Bundled (N) — SOTA skill packs shipped with this agent ───
  - <skill-from-agents/<slug>/skills/>
  - ...
  # ── CraftBot defaults (M) — already on recipient's install ───
  - <skill-from-top-level-skills/>
  - ...

mcp_servers:
  - filesystem
  - <other-mcps-relevant-to-role>

sources:
  - name: <Source name>
    url: <full URL>
    used_for: <what this informed in the agent>
```

**Skill resolution rule** (encoded in `build.py`): names in `enabled_skills` are looked up first in `agents/<slug>/skills/`, then in the repo's top-level `skills/`. This is why bundled skills go in the agent's local folder and defaults are referenced by name only.

**Priority #1 input: `reference/SOTA_USE_CASES.md` from Step 4.** Walk the SOTA table row by row. For every row where the SOTA mechanism is `<some-mcp-name>`, include it in `mcp_servers:`. For every row where the mechanism is `cli-anything + <library/CLI>`, make sure `cli-anything` is in `enabled_skills:` and the underlying tool is documented (Step 9). For every row where a bundled skill pack matches the SOTA, include that skill.

**Default skills audit checklist** — also scan these against the local `skills/` folder for matches:

For *every* agent, evaluate:
- `cli-anything` — does the agent run shell commands? (Almost always YES — it's the universal verb for SOTA tools)
- `file-format` — does the agent convert/touch files?
- `file-organizer` — does the agent manage workspace files?
- `using-git-worktrees` — does the agent work on isolated branches?

For *code/engineering* agents, also evaluate:
- `git-commit`, `github`, `github-api`, `debug-pro`, `systematic-debugging`, `test-driven-development`, `differential-review`, `requesting-code-review`, `receiving-code-review`, `mutation-testing`, `property-based-testing`, `codeql`

For *content* agents, also evaluate:
- `docx`, `pdf`, `pptx`, `doc-coauthoring`, `internal-comms`

For *research* agents, also evaluate:
- `brainstorming`, `concise-planning`, `playwright-mcp`, search-engine skills (brave, duckduckgo, baidu)

For *marketing/creative* agents, also evaluate:
- `docx`, `pptx`, `pdf`, `playwright-mcp`, `brainstorming`, content/template skills

**MCP audit checklist (SOTA-driven).** First and most important: the SOTA mapping from Step 4 dictates which MCPs are in scope. Then scan `app/config/mcp_config.json` for additional matches.

Baseline floor — always include:
- `filesystem` (mandatory for all)
- Role-cluster defaults: `github` + `postgresql-mcp` + `sentry-mcp` for engineering; `gmail-mcp` + `notion-mcp` for content/comms; `google-scholar-mcp` for research.

SOTA-driven additions — from the catalog as of mid-2026 (non-exhaustive, scan `mcp_config.json` for current list):
- *Video / creative:* `replicate-mcp` (Sora 2 / Veo 3.1 / Flux / Kling / Runway in one auth), `elevenlabs-mcp`, `ffmpeg-mcp-advanced`, `mcp-video-converter`, `mcp-media-processor`, `photoshop-mcp`, `imagegen-mcp`, `stability-ai-mcp`, `canva-mcp`, `minimax-mcp`, `mcp-tts`, `youtube-mcp`, `youtube-mcp-transcript`.
- *Marketing / social:* `twitter-mcp`, `insta-business-mcp`, `facebook-mcp-server`, `tiktok-mcp`, `reddit-mcp`, `facebook-ads-mcp`, `tiktok-ads-mcp`, `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp`, `deepl-mcp`, `brightdata-mcp`.
- *Research / analytics:* `sec-edgar-mcp`, `uspto-mcp`, `huggingface-mcp`, `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp`, `reddit-mcp`, `firecrawl-mcp`, `brightdata-mcp`, `gemini-ocr-mcp`, `mistral-ocr-mcp`.
- *Content / docs:* `drawio-mcp`, `figma-mcp`, `canva-mcp`, `gemini-ocr-mcp`, `mistral-ocr-mcp`, `deepl-mcp`.
- *Engineering:* `github`, `github-api`, `postgresql-mcp`, `sentry-mcp`, `huggingface-mcp` (ML-leaning), `kubernetes-mcp` (infra-leaning).

**Bloat rule:** include every MCP that matches an active SOTA row. *Do not* include MCPs that don't show up in any SOTA row "just because they sound relevant." Bloat is worse than absence — but under-inclusion (the v0 failure mode) is far worse than mild bloat.

### Step 6 — Compose `soul.md`

Structure (top to bottom):

1. **Title + persona intro** — 1-3 paragraphs. Who they are.
2. **Purpose** — short.
3. **When invoked** — entry procedure(s). Multiple variants if the agent has distinct modes.
4. **Core operating rules** — hard rules in bullet form. Each rule starts with a strong verb or "Don't" / "Never". These fire on every turn.
5. **Mode-specific decisions** — per primary mode the agent handles, what to do first.
6. **Domain-specific decision tables / priority lists** — code review priority, performance wins, antipattern flags, etc.
7. **Rules sections** — error handling rules, resource rules, design principles, code style, etc. Each section is 5-10 short bullets.
8. **Communication style** — how to phrase responses.
9. **Output format** — code blocks / diffs / prose conventions.
10. **When to push back / defer**.
11. **On first conversation with a new user** — PROACTIVE.md self-init.
12. **Closing rule** — one sentence.

Keep it lean. Target depends on the agent — senior-python-engineer landed at 279 lines after compaction. **Pressure-test every bullet.** If the agent could decide correctly without it, cut it.

### Step 6 — Compose `role.md`

Structure (top to bottom):

1. **Header note** — "This appends to AGENT.md. Not in default context. Grep when stuck."
2. **Capability reference** — the factual lists banished from soul.md (tools, frameworks, language features, exhaustive checklists). Tagged with subsection headings the agent will grep for.
3. **Domain-specific playbooks** — code review playbook, debugging procedure detail, performance investigation, refactoring procedures, etc. With step-by-step instructions and concrete examples.
4. **Antipattern catalog** — full BAD/GOOD code pairs (or domain-equivalent).
5. **Reference patterns** — Pydantic patterns, test patterns, resource management examples, etc.
6. **Deep examples** — anything where 10-50 lines of example code or markdown earn their place.

Use H2 / H3 headings with searchable phrases. The agent's grep query will look like `grep "Antipattern catalog" AGENT.md`, so make sure those strings exist literally.

### Step 8 — Write `SOURCES.md`

Two tables: section→source map for soul.md, section→source map for role.md. Plus a "Notes on authored-from-synthesis" section calling out any short paragraphs that aren't directly lifted (these should be rare, and always operational glue — not domain claims).

Footer: brief instructions for refreshing from upstream.

### Step 9 — Write `USE_CASES.md`

A user-facing description of what the agent does, what it can execute today via SOTA tools, and where any genuine gaps remain. Ships in the bundle but is **not** loaded into the agent's context.

Required sections (in order):

1. **Header block** — tier, category, one-line "Core job".
2. **Intro paragraph** — one or two sentences clarifying that this file is bundled but not in the agent's context.
3. **What this agent is supposed to do** — the categorized capability catalog from Step 4 Phase A (use cases). Be exhaustive — sub-bullets fine; this is the surface a user uses to decide "yes, this is the agent for my problem." Should match `reference/SOTA_USE_CASES.md` 1:1 on use case names.
4. **Execution status (SOTA — YYYY-MM)** — **mandatory** per-use-case execution table:

   ```
   | Use case | SOTA mechanism | Path |
   |---|---|---|
   | <use case from Step 4 Phase A> | <SOTA tool/library/API/MCP name> | <exact path — "<mcp-name>" OR "cli-anything + uvx <tool>"> |
   ```

   Every row from `SOTA_USE_CASES.md` appears here. This table is the proof the agent is real, not a toy.

5. **Remaining caveats (honest)** — only the rows where confidence is ⚠ or ✗ in the SOTA mapping. Each row: capability → status → notes (often "paid API key required" or "requires user's app approval"). If the agent has a genuinely director-only use case (rare in 2026 — most have SOTA mechanisms now), call it out here.
6. **Verdict line** — fulfillment % + one-sentence summary. Target ≥90%.
7. **When to use this agent** — 6-10 representative prompts the agent handles well.
8. **When NOT to use this agent** — explicit hand-offs to other agents in the catalog. Naming sibling agents is encouraged.

If the agent has any director-only fall-back (rare but possible — e.g., GUI manipulation of proprietary desktop software), surface that with a prominent disclaimer near the top *before* the supposed-to-do catalog. The user should not have to scroll to learn what's not executable.

### Step 10 — Update PROGRESS.md and verify

- Update the roster row: status `[~]` → `[?]` (needs review)
- Note final skill count, MCP count, and fulfillment % in the roster table
- Confirm `agents/<slug>/` final structure: `agent.yaml`, `soul.md`, `role.md`, `SOURCES.md`, `USE_CASES.md`, `skills/`, `reference/` (which contains `INVENTORY.md` and `SOTA_USE_CASES.md`)

Hand off to user for review before moving to the next agent.

---

## Verification gates before signing off

Before flipping the PROGRESS.md status to `[?]`, every yes must be honest:

1. **Use case enumeration.** Did I list ≥15 use cases in `reference/SOTA_USE_CASES.md`? If not, go back to Step 4 Phase A — I'm under-scoping the agent.
2. **SOTA research per use case.** Open `reference/SOTA_USE_CASES.md`. For every use case row, is there a named SOTA tool/library/API/MCP with a source URL? If any row says "TBD" or "uses cli-anything" without naming the specific tool, I have not finished researching.
3. **Fulfillment floor ≥90%.** Count the ✓ rows in `SOTA_USE_CASES.md`. If the ratio is below 90%, either (a) finish researching the missing ones (most likely) or (b) confirm the remaining are genuinely impossible (rare) or paywalled on the recipient (acceptable).
4. **SOTA → agent.yaml integration.** Every catalog-matched MCP from `SOTA_USE_CASES.md` is in `agent.yaml` `mcp_servers:`. Every bundled skill is in `enabled_skills:`. Spot-check by grepping a SOTA tool name in `agent.yaml`.
5. **SOTA → USE_CASES.md integration.** The "Execution status (SOTA — YYYY-MM)" table in `USE_CASES.md` has one row per use case, matching `SOTA_USE_CASES.md`. The verdict line states fulfillment %.
6. **Skill count.** Did I get to double digits? If not, did I genuinely audit both bundled SOTA + CraftBot defaults?
7. **MCP count.** Did I audit `mcp_config.json` for role-relevant servers, not just default to `filesystem`?
8. **Reference traceability.** Open `SOURCES.md`. For every section in soul.md and role.md, is there a non-synthesis source? Synthesis content should be rare (one or two short operational paragraphs) and always flagged.
9. **SOUL.md token discipline.** Read soul.md top to bottom. For every bullet, ask: "would the agent decide differently if this were missing?" If no for more than a handful of bullets, you have garbage to cut.
10. **role.md grep-ability.** Is every major section heading something the agent could plausibly grep for from soul.md? ("Antipattern catalog", "Code review playbook", "Performance investigation playbook" — these are good. "Notes" or "Examples" are bad.)
11. **No inline citations.** `grep -c '\[from:\|\[merged:' soul.md role.md` should both return `0`.
12. **`agent.yaml` skill grouping.** Comments clearly split Bundled (capability ships inside the .craftbot) vs CraftBot defaults (recipient already has).
13. **PROACTIVE.md self-init footer.** Same wording across all agents. Don't reinvent it per agent.
14. **`USE_CASES.md` exists and is honest.** All eight required sections present. If the agent has any director-only fall-back, the disclaimer is near the top, not buried. Caveats table is real, not padded.

---

## Common failure modes to avoid

- **Generic philosophy bullets.** "Be pragmatic. Write tests. Prioritize readability." These are platitudes any LLM would generate without research. Bin them.
- **Under-enumeration of use cases.** Listing 5 use cases for a marketing agent when the role has 25+. The fix is Step 4 Phase A — keep going until you've exhausted what a senior practitioner does, not what's easy to enumerate.
- **Skipping SOTA research per use case.** This is the v0-tier failure mode that produces "director-only" agents that cannot actually do the work. The agent's training data has a knowledge cutoff; SOTA changes monthly. *Every* use case requires a fresh web search asking "what is the SOTA way for an autonomous agent to do this in 2026?" If you settle for the use case's existence in the catalog without finding the SOTA execution path, you're shipping a toy.
- **Assessing fulfillment against what's already bundled.** Wrong framing. The agent SHOULD have the SOTA tools — it's the builder's job to put them there. If Remotion is the SOTA way to programmatically render video, the bundle should expose it (via `cli-anything + npx remotion` documented in role.md or via a Remotion MCP). "We don't have a Remotion MCP" is not a gap — it's a missing decision by the builder.
- **Single-digit skill count.** This means you didn't research the skill catalog. Both sources (bundled + defaults) should be audited.
- **Single-digit MCP count for high-surface roles.** Marketing/video/research agents in 2026 should typically have 15-25+ MCPs because the SOTA stack is platform-rich. Engineering agents can be leaner (5-8 MCPs + `cli-anything` covers most).
- **Fulfillment under 90%.** If the verdict line says "~70% executable" you have not finished Step 4 Phase B. There are SOTA tools for almost everything in 2026.
- **Inline citation tags polluting soul.md.** They cost tokens forever. Put them in `SOURCES.md`.
- **Capability lists in soul.md.** "Type system mastery: TypeVar, ParamSpec, Protocol, TypedDict..." — the agent already knows these. Move to role.md as Capability reference.
- **Composition before approval.** If you write `soul.md` before showing `INVENTORY.md` to the user, you've skipped the most important checkpoint.
- **WebFetch summaries treated as verbatim.** If WebFetch returned a summary, label it. Don't claim a file is "full" when it's been summarized.
- **Inventing the `PROACTIVE.md` footer.** Use the standard wording. The whole point is consistency across agents so users get the same UX.
- **Forgetting MCPs.** Default is to audit `mcp_config.json`, not skip it. `filesystem` alone is rarely enough.
- **Skipping `USE_CASES.md` or burying the honesty.** Every agent gets one. If the agent has any director-only use case, the disclaimer goes near the top — not at the bottom where nobody reads it.

---

## A note on tiers

Every agent is either `general` or `specialized`. This is load-bearing for how the catalog of 130 is organized.

- **General agents** (slug pattern: `<domain>-agent`) cover the whole domain end-to-end. Example: `marketing-agent` does positioning + copy + decks + video ideation + light analytics. Good fit for a solo user who wants one agent for the job.
- **Specialized agents** (slug pattern: `<specific-role>`) drill into a single niche inside a domain. Example: `video-creator` is one slice of marketing but goes much deeper on video craft. Good fit for users assembling a team of focused specialists.

The same domain typically gets one general agent plus several specialists. Users compose. The catalog should make the tier obvious — name + description must signal whether it's a generalist or a specialist and (if specialist) which domain it sits under.

---

## A note on PROACTIVE.md (decision #3 from PROGRESS.md)

No bundled `PROACTIVE.md`. Every agent's soul.md ends with:

> ## On first conversation with a new user
>
> After your first substantive exchange — not before — ask 2 to 3 short questions about routines that could be automated:
>
> - "[Two or three role-specific routine questions go here]"
>
> If they answer, propose a `PROACTIVE.md` setup that runs those routines on a schedule. If they don't, drop it and don't ask again. The proactive layer should reflect *their* workflow.

Only the routine questions change per role. The mechanic is the same across all agents.

---

## A note on what NOT to bundle

The `.craftbot` bundle format also supports shipping MCP server configs, Living UI projects, and additional MD files. For agents in this folder we deliberately ship:

- **Bundled skills** — yes
- **MD files** (`SOUL.md`, `AGENT.md` role section, `USE_CASES.md`, `SOURCES.md`) — yes (USE_CASES.md and SOURCES.md ship in bundle but are not loaded into the agent's context)
- **MCP server configs** — no, the recipient uses CraftBot's built-in catalog (157 servers, recipient enables them and fills in keys after import)
- **Living UI projects** — no, out of scope for v0
- **Skill folders for skills that already ship as CraftBot defaults** — no, would duplicate

This keeps `.craftbot` files small (typically <1 MB) and avoids version drift when CraftBot updates its defaults.

---

## Worked examples (v0 agents, post-SOTA upgrade)

All five v0 agents went through the full ten-step methodology and now sit at 95-100% SOTA fulfillment:

| Agent | Skills (bundled + defaults) | MCPs | Fulfillment | Notable SOTA wins |
|---|---|---|---|---|
| `senior-python-engineer` | 12 + 13 = 25 | 5 | ~100% | uv/uvx universal verb; memray/scalene/viztracer/py-spy replace cProfile/memory_profiler; pyrefly v1.0 (Meta); libcst for codemods; mutmut for mutation testing; ruff replaces 10+ tools |
| `technical-writer` | 4 + 13 = 17 | 9 | ~100% | Mintlify/Redocly/Scalar API docs; Log4brains ADRs; git-cliff changelogs; Lychee link checking; Vale prose linting; D2 diagrams; pytest-markdown-docs validation |
| `research-analyst` | 2 + 21 = 23 | 16 | ~95% | Paper Search MCP wraps 20+ academic sources; SEC EDGAR / USPTO direct MCPs; Perplexity Sonar Deep Research API; Exa neural search; FRED/World Bank/IMF authoritative data; lifelines for cohort survival analysis |
| `marketing-agent` | 20 defaults | 20 | ~98% | Buffer MCP for all 6+ social platforms; official Meta Ads MCP (29 tools); Google Ads MCP; HubSpot/Klaviyo/Resend MCPs; Ahrefs MCP; GA4/PostHog/GrowthBook MCPs; PageSpeed Insights; Vale brand voice; AthenaHQ/Profound AEO |
| `video-creator` | 15 defaults | 20 | ~95% | Replicate MCP (Sora 2 / Veo 3.1 / Flux 2 / Kling / Runway in one auth); ElevenLabs MCP; FFmpeg-MCP-Advanced; Photoshop MCP; Remotion (programmatic React/TSX → MP4); Whisper.cpp; Submagic; Hedra Character-3 |

When in doubt, read `agents/<slug>/reference/SOTA_USE_CASES.md` for that agent — it's the per-use-case SOTA mapping that drove the `agent.yaml` and `USE_CASES.md` content.

The biggest lesson from the v0 SOTA upgrade pass: **the original "honest" director-only assessment for `video-creator` was wrong**, not because the agent was misjudged but because Step 4 (SOTA research per use case) had been skipped. Every "gap" was closeable in 2026 with `replicate-mcp` + `elevenlabs-mcp` + `ffmpeg-mcp-advanced` + Remotion. The methodology now mandates this step so the failure can't recur.
