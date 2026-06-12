<!--
Source: https://everything-pr.com/linkedin-thought-leadership-a-2026-playbook/
Forbes Contributor program: https://www.forbes.com/sites/forbescontent/
HBR contributor guidelines: https://hbr.org/guidelines-for-authors
-->
# Op-Ed + Contributed Article Placement — SKILL

Outlet-specific pitching for contributed pieces in Forbes Contributor, Fast Company Impact, Inc, HBR, and trade press. Pitch FIRST (don't write speculatively unless outlet asks). On acceptance: draft to outlet spec (word count + tone + structure). Pair with `media-list-muck-rack-cision` for editor lookup.

## When to use this skill

- **Forbes Contributor / Fast Co Impact / Inc / Entrepreneur / Newsweek** — major business outlets with contributor programs.
- **HBR / MIT Sloan Review / Stanford Social Innovation Review** — academic-leaning thought leadership.
- **Trade press op-eds** — TechCrunch op-ed, Modern Healthcare commentary, AdAge POV column.
- **Regional / industry-specific** — local Business Journal op-ed, sector trade journal commentary.
- **WSJ / NYT op-ed** — rare, high-stakes; multi-week placement cycle.

**Do NOT use this skill when:**
- The piece is being published on owned channels (LinkedIn newsletter, Substack, company blog) — use `executive-thought-leadership-linkedin-substack`.
- The pitch is for a news interview — use `journalist-outreach-cold-warm-embargoed`.
- The "op-ed" is a press release in disguise — push back; outlets reject those instantly.

## Setup

### Outlet contributor / editor research

Pull editor + contributor program details from Muck Rack via `media-list-muck-rack-cision`:

```bash
# Search for op-ed editors at target outlet
curl "$MUCKRACK_API_BASE/search?\
outlet=forbes,fastcompany,hbr,inc&\
title=editor,oped+editor,commentary+editor&\
limit=30" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY"
```

### Outlet-spec database in Notion

Per outlet:
- `outlet_name` (text)
- `program_type` (select: contributor, op-ed_solicited, op-ed_unsolicited)
- `submission_email` (email)
- `submission_url` (URL — if web form)
- `word_count_min` (number)
- `word_count_max` (number)
- `tone_notes` (rich text — "academic", "punchy", "first-person", etc.)
- `structure_template` (rich text — "hook → thesis → 3 arguments → close")
- `editorial_calendar_theme` (multi-text — current quarter's themes)
- `byline_requirements` (text — "C-suite only", "academic affiliations", etc.)
- `exclusivity` (select: required, preferred, not-required)
- `payment` (select: paid, unpaid, varies)
- `recent_oped_urls` (multi-text — last 5 published op-eds in this outlet)
- `lead_time_days` (number — typical pitch-to-publish lead time)

### Vale linter for outlet-spec rules

Outlet-specific style rules:
- HBR: ban first-person plural overuse, require data citations
- Forbes: ban brand promotion language, require declarative thesis in para 1
- Fast Co: ban academic jargon, require accessible voice

## Common recipes

### Recipe 1: Outlet research (read recent op-eds)

```bash
# Pull last 10 op-eds from target outlet via firecrawl
outlet_oped_url="https://www.forbes.com/sites/forbes-business-council"
firecrawl scrape --url "$outlet_oped_url?page=1" | jq -r '.links[]' | grep "/article/" | head -10 > recent_opeds.txt

for url in $(cat recent_opeds.txt); do
  body=$(firecrawl scrape --url "$url" | jq -r .markdown)
  # Claude analyzes structure
  analysis=$(claude --prompt "What's the headline pattern, opening hook style, evidence cadence, byline structure, and word count? URL: $url")
  echo "$url: $analysis" >> outlet_analysis.txt
done
```

### Recipe 2: Pitch draft (NOT the article itself)

```python
prompt = f"""
Draft a 250-word op-ed pitch to {outlet['name']} editor for {exec['name']}.

PROPOSED PIECE TITLE: "{title}"
THESIS (1 sentence): {thesis}
WHY NOW (timeliness hook): {why_now}
3 SUPPORTING ARGUMENTS:
1. {arg_1}
2. {arg_2}
3. {arg_3}

OUR CREDIBILITY:
- {exec['title']} at {company}
- {credentials_brief}
- {recent_relevant_coverage}

OUTLET FIT:
- Recent op-eds from {outlet['name']} have covered: {outlet['recent_themes']}
- Our piece would slot into: {topical_fit}

REQUIREMENTS:
- Subject: "Op-ed pitch: <thesis-summary>" under 60 chars
- First line cites a recent {outlet} piece by name
- Pitch is the PITCH, not the article — propose, don't write speculatively
- Indicate exclusivity preference: "Happy to offer first-look exclusive to {outlet}."
- Offer to write to spec (word count, tone, structure)
- Include 100-word author bio + LinkedIn + recent press URLs
- Total under 250 words

NO buzzwords. NO "I'm reaching out". NO "hope this finds you well."
"""
pitch = claude(prompt)
```

### Recipe 3: Editor identification + send

```bash
# Editor lookup (per outlet)
editor=$(notion query "outlet_editors WHERE outlet=$outlet AND section=oped" | jq -r .editor_email)

gmail-mcp send \
  --to "$editor" \
  --subject "Op-ed pitch: $thesis_summary" \
  --body "$pitch"

# Log to Notion outreach tracker
notion-mcp create_page --db oped_pitches --properties "{
  outlet: $outlet,
  editor: $editor,
  pitch_date: $(date -I),
  thesis: $thesis,
  status: pitched
}"
```

### Recipe 4: Draft to spec (on acceptance)

```python
# Acceptance triggers: editor says "yes" or "interested — send draft"
# Pull outlet spec from Notion

spec = notion.query(filter={"outlet_name": outlet})[0]

prompt = f"""
Draft the full op-ed to {outlet['name']} specifications.

THESIS: {accepted_thesis}
WORD COUNT TARGET: {spec['word_count_max']} (within ±50 of {spec['word_count_min']}-{spec['word_count_max']})
TONE: {spec['tone_notes']}
STRUCTURE: {spec['structure_template']}
EDITORIAL FIT: {spec['editorial_calendar_theme']}

CONTENT:
- HOOK (first 50 words): timely, specific moment in industry that frames the piece
- THESIS (next 100 words): clear position, no hedging, "I argue X"
- 3 ARGUMENTS (300-700 words each, depending on total target):
  - Each argument: position → 1 data point → 1 named example → counter-objection addressed
- CLOSE (last 100 words): forward-looking, prescriptive ("here's what should happen")

REQUIRED ELEMENTS:
- 3-5 data points with source citations
- 2-3 named companies / customers / examples (with permission)
- 1 acknowledgment of the strongest counter-argument
- Declarative voice — "I argue" not "one might suggest"

BANNED:
- {outlet['banned_phrases']}
- All buzzwords from the AI-slop catch list
- Em-dashes >1 per paragraph
- Passive voice chains

Author bio (100 words) goes at end.
"""
article = claude(prompt)
```

### Recipe 5: Vale lint pass (outlet-specific rules)

```bash
# Per-outlet Vale config
uvx vale --config=styles/Outlet/$outlet.yml --output=JSON article.md > vale_results.json

errors=$(jq '[.[][] | select(.Severity == "error")] | length' vale_results.json)
if [ "$errors" -gt 0 ]; then
  jq -r '.[][] | select(.Severity == "error") | "Line \(.Line): \(.Message)"' vale_results.json
  exit 1
fi
```

### Recipe 6: Submit to outlet (per submission mechanism)

```bash
# Email submission (most outlets)
case $outlet in
  "forbes")
    gmail-mcp send \
      --to "$editor_email" \
      --subject "Op-ed draft: $title" \
      --body "<intro paragraph>

Draft attached. Word count: $word_count. Bio + author photo included.

Exclusive to Forbes; willing to revise per editor input.

— $exec_name"
    # Attach via gmail-mcp attachment
    ;;
  "fastcompany")
    # Fast Co uses web submission form for Impact section
    mcp tool playwright-mcp.browser_navigate --url "https://www.fastcompany.com/submit"
    # Fill form (see playwright recipe)
    ;;
  "hbr")
    # HBR has formal submission portal
    mcp tool playwright-mcp.browser_navigate --url "https://hbr.org/guidelines-for-authors"
    ;;
esac
```

### Recipe 7: Track + measure published placements

```bash
# Editor confirms publish date
# Calendar reminder for go-live
google-calendar-mcp create_event \
  --title "PUBLISHED: $title on $outlet" \
  --date "$publish_date" \
  --description "Track first-week metrics + repurpose"

# Day-of-publish:
# 1. LinkedIn org post + CEO personal post
# 2. Twitter thread with key arguments
# 3. Internal Slack announce
# 4. Email to relevant customer references
# 5. Add to media kit + future pitch decks

# 30-day metrics
posthog-mcp query --filter "url contains $article_url" \
| jq '{unique_visitors, time_on_page, scroll_depth, conversion_signups}'
```

### Recipe 8: Re-pitch after rejection

```bash
# If outlet declines, log + iterate
notion-mcp update_row --id $pitch_id \
  --status "declined" \
  --decline_reason "$reason" \
  --re_pitch_after "90 days with different angle"

# After 90 days, fresh angle pitch (different thesis, same exec voice)
```

## Examples — quarterly contributed program

```yaml
exec: Jane Smith, CEO Acme
goal: 1 tier-1 contributed piece + 2-3 trade-press op-eds per quarter

q3_targets:
  tier_1:
    - Forbes Contributor (3-pitch attempts; 1 accept target)
    - HBR (1-pitch attempt; long-shot)
  tier_2:
    - Fast Company Impact
    - Entrepreneur
    - Inc
  trade:
    - TechCrunch op-ed (3-pitch attempts)
    - MarTech Today
    - Modern Healthcare (if vertical)

per_pitch_workflow:
  - outlet research: read last 10 op-eds in target section
  - thesis development: claude brainstorming skill
  - pitch draft (250 words)
  - human approval
  - send via gmail-mcp to editor
  - track in notion
  - follow-up at day 7 if no reply
  - close at day 14 no reply (re-pitch in 90 days)

on_acceptance:
  - draft to outlet spec
  - vale outlet-specific lint
  - exec read-aloud review
  - submit
  - publish-day amplification (linkedin + twitter)
  - 30-day metrics review
```

## Edge cases

### Outlet exclusivity expectations
HBR, Forbes Contributor: prefer/require exclusive. Trade press: usually flexible. Communicate upfront: "Happy to offer first-look exclusive to [outlet]; if you pass, I'll pitch to [tier-2]."

### Forbes Contributor reality
Forbes Contributor was historically wide-open; 2024-2026 tightening. New contributor approval is selective. If exec has byline already, easier to place pieces. If not, target Forbes Councils first (paid membership but higher acceptance).

### HBR is hard
HBR rejection rate is >95%. Pitching HBR is a multi-year game. Realistic: 1 HBR placement per 3-5 years for most execs. Don't sell client on "we'll get HBR" — it's directional.

### Pitch first, write speculatively never (mostly)
Wasting hours on a speculative article without editor commitment = wasted time. ONLY write speculatively for outlets that explicitly ask for the full draft upfront (rare; usually trade press).

Exception: if exec already wrote a strong draft for owned channels, repackage as a pitch with offer to revise.

### Draft to spec, not to thesis
Once accepted, the editor's spec becomes the brief. If editor says "we want 1,200 words on X angle," that's the brief. Don't drift back to your original thesis.

### Author bio + headshot mandatory
Outlets require:
- 60-100 word bio
- Hi-res headshot (1MB+ JPG)
- LinkedIn URL
- Optional: previous published byline links

Pre-pack these in `notion-mcp` author DB so they're ready to attach.

### Tier-1 op-ed = tier-1 voice
The exec needs to actually be capable of articulating the position. Ghost-writing is common but the exec must own the position in interviews afterward. If exec can't speak the argument fluently, don't place the piece.

### Customer mentions need permission
Customer names in the piece = same permission discipline as press releases. Pre-clear via `customer-reference-program-pr` skill.

### Pay-to-play "contributor" programs
Some outlets (less reputable) charge for contributor status. These are NOT real op-ed placements. Distinguish:
- **Real op-ed**: editorial review, editor input, prestige
- **Paid placement**: looks like an article, was actually paid sponsored content

Don't conflate these in client reporting.

### Counter-argument is mandatory
Strong op-eds acknowledge the strongest counter-argument and respond to it. Hedge-free op-eds with only one-sided argument get rejected by tier-1 editors. The "but some argue X — here's why I think Y is right" paragraph is required.

### Republication on owned channels
After publication on outlet, exec wants to republish to LinkedIn newsletter / Substack. Outlet rules vary:
- **HBR**: no republication for 90 days, then with "first published in HBR" attribution
- **Forbes**: republish freely with attribution back
- **WSJ/NYT**: no republication, ever

Check outlet contract; don't violate.

### Op-ed vs contributed article distinction
- **Op-ed**: thesis-driven, declarative position, advocates a stance (often 800-1500 words)
- **Contributed article**: educational, framework-driven, advice-style (1000-2500 words)

Forbes Contributor + HBR lean contributed article. Op-ed sections (NYT, WSJ, Washington Post) lean thesis.

### Failed pitch → repurpose to owned
If a pitch fails across 3 outlets, the piece still has value. Move to LinkedIn newsletter (`executive-thought-leadership-linkedin-substack` skill). Audience builds from owned channel.

### Embargo + simultaneous wire
For some high-stakes pieces, coordinate: op-ed publishes morning of, related press release fires same morning, customer reference quoted in both. Triangulate the coverage.

### After-action retro
Per quarter: which pitches landed? Which outlets responded? Which pieces drove most amplification? Update Notion editor scoring + topical preferences for next quarter.

## Sources

- **LinkedIn thought leadership 2026 playbook**: https://everything-pr.com/linkedin-thought-leadership-a-2026-playbook/
- **Forbes Contributor program**: https://www.forbes.com/sites/forbescontent/
- **HBR author guidelines**: https://hbr.org/guidelines-for-authors
- **MIT Sloan Management Review**: https://sloanreview.mit.edu/contribute/
- **Stanford Social Innovation Review**: https://ssir.org/articles/submit
- **Fast Company submissions**: https://www.fastcompany.com/contact
- **Muck Rack API for editor lookup**: https://muckrack.com/pr-software/api
- **Vale linter**: https://vale.sh/
