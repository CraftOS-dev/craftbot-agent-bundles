<!--
Sources: Playwright https://playwright.dev/
         SCIP Code of Ethics https://www.scip.org/page/Ethical-Intelligence
         USPTO PatentsView https://api.patentsview.org/
         GitHub REST https://docs.github.com/en/rest
Companion playbook: role.md → "Product teardown playbook"
-->

# Competitor product teardown (depth)

In-product walkthrough + IA + state-machine + activation-moment timing for a single competitor, paired with public engineering blog / GitHub / patent / job-post back-fill. Output: pptx teardown deck + parity-matrix delta + battlecard updates. Public-source only; trial signup with rep's real ID where ToS permits.

## When to use

- "Do a full product teardown of [competitor X]"
- "Why is [competitor] winning [job-to-be-done]?"
- New entrant in your category — establish baseline understanding
- Quarterly deep dive on a top-3 competitor
- Pre-launch competitive review (your launch vs theirs)

## When NOT to use

- Continuous monitoring → use `continuous-competitor-monitoring-klue-kompyte-crayon`
- Pricing-only teardown → use `competitor-pricing-tier-comparison`
- Feature-list-only compare → use `feature-parity-tracking`
- Trial signup blocked by domain gate → escalate; do not pretext

## Setup

```bash
# Playwright with browser binaries
uvx playwright install chromium firefox
# Or pipx if persistent install preferred
pipx install playwright && playwright install chromium

# ffmpeg for demo-video frame extraction
# (windows) winget install Gyan.FFmpeg
# (mac)     brew install ffmpeg

# GitHub token (free) for OSS competitor repos
export GITHUB_TOKEN="ghp_..."
```

MCPs already in `agent.yaml`: `playwright-mcp`, `github-api`, `uspto-mcp`, `firecrawl-mcp`, `gemini-ocr-mcp`, `mistral-ocr-mcp`, `youtube-mcp`.

## Common recipes

### Recipe 1: Playwright onboarding screen capture

```python
# Capture every onboarding screen with DOM + screenshot + timing
from playwright.sync_api import sync_playwright
import time, json, pathlib

OUT = pathlib.Path("teardowns/acme/onboarding")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir=str(OUT/"video"))
    page = context.new_page()
    page.goto("https://acme.example.com/signup")
    step = 0
    while True:
        step += 1
        page.screenshot(path=OUT/f"step-{step:02d}.png", full_page=True)
        (OUT/f"step-{step:02d}.html").write_text(page.content(), encoding="utf-8")
        # Advance — wait for user input or auto-click "next"
        time.sleep(2)
        if page.url == "https://acme.example.com/app/home":
            break
    context.close()
    browser.close()
```

### Recipe 2: IA + nav map extraction

```python
# After login, walk the top-level nav and map child pages
nav_links = page.eval_on_selector_all(
    "nav a", "els => els.map(e => ({text: e.innerText, href: e.href}))"
)
# Returns: [{text:"Dashboard",href:"/app/home"}, {text:"Reports",href:"/app/reports"}, ...]
```

Recursive 2 levels deep for a complete IA map.

### Recipe 3: State machine for primary jobs

```python
# Each primary job = state machine:
#   empty state → setup → first-action → result → repeat
# Capture each state with screenshot + timing.

states = []
for state_name in ["empty","setup","first_action","result","power_user"]:
    page.screenshot(path=OUT/f"job-create-{state_name}.png")
    states.append({"state": state_name, "url": page.url, "ts": time.time()})
```

### Recipe 4: Activation moment timing

```python
# Measure: signup → first-value (the "aha")
import time
t0 = time.time()
page.goto("https://acme.example.com/signup")
# ... walk through signup + first action
page.click("text=Create your first report")
page.wait_for_selector("text=Report ready", timeout=60_000)
print(f"Time-to-first-value: {time.time() - t0:.1f}s")
```

Compare vs your product's equivalent measurement. Sub-3-minute activation is best-in-class SaaS.

### Recipe 5: Engineering blog back-fill

```bash
# Scrape the engineering blog index + extract architecture-mentioning posts
curl -s https://acme.example.com/engineering | \
  pup 'article h2 a attr{href}' | \
  while read u; do echo $u; curl -s "https://acme.example.com$u" | \
    grep -Ei "kubernetes|kafka|postgres|rust|go|elixir|temporal|snowflake"; done
```

### Recipe 6: GitHub OSS repo signals

```python
import requests
H = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
org = "acme-org"
repos = requests.get(f"https://api.github.com/orgs/{org}/repos?per_page=100", headers=H).json()
# Counts of repos by language, top contributors, recent activity
from collections import Counter
langs = Counter(r["language"] for r in repos if r["language"])
print(langs.most_common())
```

### Recipe 7: USPTO patent direction signal

```bash
curl "https://api.patentsview.org/patents/query" \
  -d 'q={"_and":[{"assignee_organization":"Acme Corp"},{"_gte":{"patent_date":"2024-01-01"}}]}&f=["patent_number","patent_title","cpc_subgroup_id","patent_date"]&o={"per_page":100}'
```

CPC subgroup frequency = R&D investment direction.

### Recipe 8: Demo-video frame extraction

```bash
# Their YouTube demo or conference talk → extract every 5s frame
yt-dlp "https://www.youtube.com/watch?v=XXX" -o "demo.mp4"
ffmpeg -i demo.mp4 -vf "fps=1/5" frames/frame-%04d.png
# Then OCR via gemini-ocr-mcp to capture UI text
```

### Recipe 9: Job-posting tech-stack reveal

```python
# /careers pages reveal back-end choices
import re
job_text = firecrawl_scrape("https://acme.example.com/careers/engineering")
techs = re.findall(r"\b(Kubernetes|Kafka|Postgres|Rust|Go|Elixir|Snowflake|Databricks|React|Vue|Svelte)\b",
                   job_text)
print(Counter(techs).most_common(10))
```

### Recipe 10: Empty-state / power-user split

For each primary job, capture:
- Brand-new account state (0 data, 0 collaborators)
- Active account state (after 30 days simulated use)

Document any progressive-disclosure or feature-gating you discover (e.g., "advanced filters appear after 5 saved searches").

### Recipe 11: Render teardown deck (pptx)

```python
from pptx import Presentation
prs = Presentation()
sections = ["Cover","IA map","State machine","Activation timing",
            "Feature inventory","Empty vs power user","Non-visible inferences",
            "Battlecard delta","Parity matrix delta","Sources"]
for s in sections:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = s
prs.save("teardowns/acme/teardown.pptx")
```

## Examples

### Example 1: Mid-cycle teardown of a fast-moving competitor

**Goal:** Understand how Acme's new "Auto-Insights" feature compares to ours.

**Steps:**
1. Trial signup with rep's real ID; confirm ToS allows internal CI use.
2. Playwright session (Recipe 1) capturing onboarding + first use of Auto-Insights.
3. Time-to-first-insight (Recipe 4); compare to our time-to-first-insight = 8 min vs theirs 2 min.
4. Engineering blog back-fill (Recipe 5) — find their "How we built Auto-Insights" post.
5. GitHub (Recipe 6) — search for `auto-insights` related OSS repos in `acme-org`.
6. Render pptx (Recipe 11); update feature parity matrix; flag battlecard pane 4.

**Result:** 15-slide teardown deck + parity-matrix row + battlecard delta surfaced in Slack.

### Example 2: Pre-launch competitive readiness

**Goal:** Before our new "Workflows" feature ships, understand how Acme positions theirs.

**Steps:**
1. Capture Acme's Workflows onboarding (Recipe 1) + IA path to find it (Recipe 2).
2. Note their activation-moment design choices — auto-import, templates, guided tour.
3. Mine G2 reviews mentioning their Workflows feature (top 3 complaints + top 3 praises).
4. Sync to messaging team for positioning differentiation language.

**Result:** Positioning brief + activation-design checklist for our launch.

## Edge cases / gotchas

- **Trial signup ToS** — many SaaS products restrict trial use to "evaluating for purchase." CI use may be a soft violation. Document the use, use rep's real ID, do not pretext.
- **Domain gate** — some products restrict trial signup to corporate email domains they recognize as prospects. If blocked, escalate to recipient; do not use throwaway email.
- **Re-signups** — multiple trial accounts under different emails to extend trial → ToS-violation in most SaaS. Don't.
- **Recording demos** — if requesting a live demo from sales, consent rules apply. SCIP forbids recording without consent. Take notes, not recordings.
- **Playwright + bot detection** — competitor may detect headless browser. Use `headless=False`, real user-agent, slow typing. If blocked, accept and proceed with public-only sources.
- **State machine gaps** — power-user state requires real account aging or sample data; document estimation vs measurement clearly.
- **Patent search latency** — USPTO PatentsView lags grant date by 2-4 weeks. For R&D direction, look at applications (separate query).
- **GitHub coverage** — public repos are sample, not full. Their main product is likely internal. Use OSS sample as a flavor signal only.
- **Pretexting line** — asking a current customer for screenshots ≠ pretexting; asking a sales rep "I'm a prospect" when you're not = pretexting and disallowed.
- **Activation timing variance** — run the measurement 3 times; report median. Avoid one-shot timing.

## Sources

- Playwright — https://playwright.dev/
- SCIP — Ethical Intelligence — https://www.scip.org/page/Ethical-Intelligence
- USPTO PatentsView — https://api.patentsview.org/
- GitHub REST API — https://docs.github.com/en/rest
- AutoBound — 15 CI tools compared 2026 — https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- role.md → "Product teardown playbook" (this bundle)

## Related skills

- `feature-parity-tracking` — teardown findings update the parity matrix
- `battlecard-authoring-maintenance` — teardown findings update battlecard panes
- `competitor-pricing-tier-comparison` — pricing of the teardown subject
- `competitor-tech-stack-builtwith-wappalyzer` — back-fill the tech stack inferences
- `ethical-public-source-methodology` — SCIP compliance for trial signups
