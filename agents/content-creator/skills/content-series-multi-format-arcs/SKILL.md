# Content Series + Multi-Format Arcs — Notion Editorial DB + Series Planning

> Plan, sequence, and ship 4-12-piece content series with parent tentpole + child derivative rows in Notion.

## When to use

Trigger on: "plan a content series", "build a 12-week arc", "design a themed week", "structure my next 8 episodes", "what should episode 3 cover", "how do I bridge weeks 4-6", "create a series page in Notion". This skill owns series-arc design + Notion editorial DB schema (parent tentpole + child derivative rows) + cadence sustainability checks. For per-piece publishing handoff use `long-form-newsletter-substack-beehiiv-ghost` or `podcast-scripting-show-notes`. For repurposing chain see `repurposing-pipeline-1-to-10`. For calendar maintenance see `content-calendar-notion-db`.

## Setup

```bash
# Notion MCP — primary tool
npx -y @notionhq/mcp-server@latest

# Verify Notion workspace access
curl -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  "https://api.notion.com/v1/users/me"
```

Auth env vars:
- `NOTION_API_KEY` — internal integration token from Notion → integrations → new.
- `NOTION_SERIES_DB` — DB ID of the Series table (parent of tentpoles).
- `NOTION_EDITORIAL_DB` — DB ID of the Editorial DB (tentpoles + derivatives).
- `NOTION_PARENT_PAGE_ID` — workspace page that contains both DBs.

## Common recipes

### Recipe 1: Series-arc design (the strategic doc)

```markdown
# Series: <Working Title>

## One-sentence thesis
<the single audience question this series answers>

## Audience question being answered
<the literal user query / pain point>

## Length
<4 | 6 | 8 | 12 | 16 | open-ended monthly>

## Cadence
<weekly | biweekly | monthly>

## Episode / issue arc
1. Tentpole 1 — <hook + thesis statement that frames the series>
2. Tentpole 2 — <first specific tactic / case study>
3. Tentpole 3 — <second specific tactic / case study>
...
N. Tentpole N — <synthesis or call-forward to next series>

## Cross-cutting elements
- Recurring guest / segment: <name>
- Recurring data column: <metric they revisit each tentpole>
- Series-wide CTA: <newsletter sign-up, course, community>

## Success metrics
- Subscribers / listeners gained: <target>
- Engagement per tentpole: <CTR / LTR target>
- Conversions to next tier: <number>
```

Examples from role.md:
- "How I built a $1M newsletter" — 12-week interview series with 12 operators
- "AI for non-engineers" — 8-week explainer series
- "Solo Founder's Playbook" — 10-week operational deep dive
- "What I Learned" — open-ended monthly retrospective

### Recipe 2: Create Series DB row

```bash
npx @notionhq/mcp create_page \
  --database_id "$NOTION_SERIES_DB" \
  --properties '{
    "Title": {"title":[{"text":{"content":"How I built a $1M newsletter"}}]},
    "Status": {"select":{"name":"In production"}},
    "Length": {"number": 12},
    "Cadence": {"select":{"name":"Weekly"}},
    "Start date": {"date":{"start":"2026-07-06"}},
    "End date": {"date":{"start":"2026-09-21"}},
    "Thesis": {"rich_text":[{"text":{"content":"<thesis>"}}]},
    "Audience question": {"rich_text":[{"text":{"content":"<question>"}}]}
  }'
```

### Recipe 3: Editorial DB parent (tentpole) row creation

```bash
# Per-tentpole row in editorial DB, linked to parent series
npx @notionhq/mcp create_page \
  --database_id "$NOTION_EDITORIAL_DB" \
  --properties '{
    "Title": {"title":[{"text":{"content":"Ep 1: Why I left my job to build a newsletter"}}]},
    "Series": {"relation":[{"id":"'"$SERIES_ROW_ID"'"}]},
    "Format": {"select":{"name":"Podcast"}},
    "Tentpole publish date": {"date":{"start":"2026-07-06"}},
    "Author": {"people":[{"id":"<user_id>"}]},
    "Editor": {"people":[{"id":"<user_id>"}]},
    "Status": {"select":{"name":"Drafting"}},
    "KPI target": {"rich_text":[{"text":{"content":"3k downloads / 5% reply rate"}}]},
    "Tags": {"multi_select":[{"name":"interview"},{"name":"creator-economy"}]}
  }'
```

### Recipe 4: Editorial DB child (derivative) rows

```bash
# For each derivative of the tentpole, create a child row
for FORMAT in "LinkedIn carousel" "X thread" "Reels clip 1" "Reels clip 2" "Audiogram" "Newsletter writeup" "Quote graphic 1" "Quote graphic 2" "Quote graphic 3" "Blog post" "YouTube video"; do
  npx @notionhq/mcp create_page \
    --database_id "$NOTION_EDITORIAL_DB" \
    --properties '{
      "Title":{"title":[{"text":{"content":"Ep 1 - '"$FORMAT"'"}}]},
      "Tentpole":{"relation":[{"id":"'"$TENTPOLE_ROW_ID"'"}]},
      "Format":{"select":{"name":"'"$FORMAT"'"}},
      "Status":{"select":{"name":"Drafting"}}
    }'
done
```

### Recipe 5: Sustainability check (the pre-launch sanity check)

```python
# Before committing to a 12-week weekly series, run a sustainability check
def can_we_actually_ship(series):
    tentpoles = series['length']  # 12
    cadence_weeks_per_tentpole = {"weekly": 1, "biweekly": 2, "monthly": 4}[series['cadence']]
    derivatives_per = series.get('derivatives_per_tentpole', 10)

    hours_per_tentpole = {
        "Newsletter": 8,
        "Podcast": 12,  # research + record + edit + show notes
        "Video": 16,
        "Blog": 6,
    }[series['format']]

    hours_per_derivative_avg = 1  # if pipeline is automated

    total_hours = tentpoles * (hours_per_tentpole + derivatives_per * hours_per_derivative_avg)
    total_weeks = tentpoles * cadence_weeks_per_tentpole
    weekly_hours_required = total_hours / total_weeks

    print(f"Series: {series['title']}")
    print(f"Required weekly hours: {weekly_hours_required:.1f}")
    if weekly_hours_required > 20:
        print("WARNING: not sustainable; cut tentpoles or stretch cadence")
    return weekly_hours_required <= 20
```

If the math says >20h/week, restructure. Daily ugly beats sporadic perfect.

### Recipe 6: Pre-write all N tentpole concept briefs at once

```bash
# Use Claude to draft N concept briefs in one pass
mkdir -p series/<series-slug>/briefs
for i in $(seq 1 12); do
  cat > series/<series-slug>/briefs/ep$(printf '%02d' $i).md <<EOF
# Episode $i: <working title>

## One-sentence thesis
<TBD>

## Pillar 1
<TBD>

## Pillar 2
<TBD>

## Pillar 3
<TBD>

## Hook
<TBD>

## CTA
<TBD>
EOF
done
```

Fill in via brainstorm (use `brainstorming` skill) + Claude long-context pass.

### Recipe 7: Series page (the public-facing landing)

```markdown
# How I Built a $1M Newsletter — Series Landing

A 12-week interview series with 12 newsletter operators who hit $1M in revenue.

## What you'll learn
- What changed at $10k, $100k, $1M MRR
- The hire that mattered most at each stage
- The pricing structure that converted

## Episodes
1. **<Operator 1>** — published 2026-07-06 — [Listen](url)
2. **<Operator 2>** — published 2026-07-13 — [Listen](url)
...
12. **<Operator 12>** — published 2026-09-21 — [Listen](url)

## Cross-series CTA
Sign up for the companion newsletter — every Tuesday, one written op-ed on the prior episode.
```

Publish via Ghost / Beehiiv / dedicated page on the podcast site.

### Recipe 8: Mid-series check-in (week N/2)

```python
# Halfway through, audit progress + adjust
def midseries_audit(series_id):
    tentpoles = notion_query(
        db_id=os.environ['NOTION_EDITORIAL_DB'],
        filter={'Series': {'relation': {'contains': series_id}}}
    )

    published = [t for t in tentpoles if t['Status'] == 'Published']
    drafting = [t for t in tentpoles if t['Status'] == 'Drafting']
    blocked = [t for t in tentpoles if t['Status'] == 'Blocked']

    # Calculate KPI hit rate so far
    kpi_hits = sum(1 for t in published if t.get('KPI actual', 0) >= t.get('KPI target', 0))

    return {
        'published_count': len(published),
        'drafting_count': len(drafting),
        'blocked_count': len(blocked),
        'kpi_hit_rate': kpi_hits / max(len(published), 1),
        'recommend_cut': blocked or kpi_hit_rate < 0.3,
    }
```

If <30% hitting KPI, cut remaining tentpoles or shift cadence. Don't death-march.

### Recipe 9: Series-to-evergreen funnel

```markdown
# After series ends, the funnel
- Series landing page (Recipe 7) — evergreen, indexed for SEO
- Each tentpole has its own page with full transcript / writeup
- Newsletter cross-promotion: "Catch up on the full series" — once per quarter
- Lead magnet: "All 12 case-study PDFs" gated behind email signup
- Sponsored re-promotion: pitch series-level sponsorship to relevant brand
```

### Recipe 10: Series post-mortem

```markdown
# Post-mortem: <series>

## Results vs target
| Tentpole | KPI target | KPI actual | Hit / miss |
|---|---|---|---|
| 1 | 3k downloads | 5.2k | hit |
| 2 | 3k | 2.1k | miss |
| ... |

## What worked
- <thing>
- <thing>

## What didn't
- <thing>

## What I'd cut from a v2
- <tentpole or format that didn't land>

## Backlog from this series for future series
- <topic that emerged but didn't fit this arc>
```

## Examples

### Example 1: Plan a 12-week weekly podcast interview series

**Goal:** "How I built a $1M newsletter" — 12 operators, weekly cadence, podcast tentpole, 10 derivatives each.

**Steps:**
1. Recipe 1: write the strategic doc.
2. Recipe 5: sustainability check — 12 tentpoles × (12h podcast + 10×1h derivatives) / 12 weeks = 22 hrs/week. Over budget.
3. Cut derivatives to 8/tentpole or stretch to biweekly. Pick biweekly → 11 hrs/week. Sustainable.
4. Recipe 2: create Series DB row.
5. Recipe 3 + 6: create 12 tentpole rows + 12 concept briefs.
6. Recipe 4: queue 8 derivatives per tentpole = 96 child rows.
7. Recipe 7: build series landing page.
8. Begin production loop with `podcast-scripting-show-notes` → `podcast-editing-brief-descript-riverside` → `repurposing-pipeline-1-to-10`.
9. Recipe 8: week 6 mid-series check.
10. Recipe 10: post-mortem after week 24.

**Result:** Sustainable biweekly series with 96 tracked derivatives.

### Example 2: 8-week newsletter explainer series

**Goal:** "AI for non-engineers" — 8 newsletter issues, weekly cadence.

**Steps:**
1. Recipe 1: thesis = "AI is now non-technical; here's how to use it without engineering."
2. Sustainability: 8 × (8h newsletter + 5×1h derivatives) = 104h / 8 weeks = 13h/week. Sustainable.
3. Recipes 2-4: DB rows.
4. Run weekly Tuesday 6am send via `long-form-newsletter-substack-beehiiv-ghost`.
5. Per-issue Castmagic → X thread + LinkedIn carousel.
6. Week 4 check; full series ends week 8.
7. Recipe 9: package all 8 issues as a free PDF lead magnet for newsletter growth.

**Result:** 8-issue series + 40 derivative posts + post-series PDF lead magnet.

### Example 3: Open-ended monthly retrospective

**Goal:** "What I Learned" — month-end monologue podcast + newsletter recap.

**Steps:**
1. Recipe 1: open-ended monthly cadence, no fixed arc length.
2. Sustainability: 1 podcast + 1 newsletter + 6 derivatives = 16h/month. Sustainable indefinitely.
3. Recipe 2: Series row with `Length: open` and `Cadence: monthly`.
4. Last Friday of each month: produce + publish per `podcast-scripting-show-notes` + `long-form-newsletter-substack-beehiiv-ghost`.
5. Quarterly Recipe 8 audit to check engagement is holding.

**Result:** Long-running open-ended series compounding monthly.

## Edge cases / gotchas

- **Don't promise weekly cadence if your sustainability math says biweekly.** Promised weekly → missed week 3 = audience trust dies faster than slower-but-reliable cadence.
- **Series length sweet spot is 8-12 tentpoles.** Under 4 doesn't feel like a series; over 16 audience drops off mid-series.
- **Mid-series fatigue is real.** Schedule a "swing" episode mid-series (different format, different guest, lighter tone) to break monotony.
- **Don't relaunch a failed series under a new name.** Audit, post-mortem, restructure thesis, ship new series.
- **Recurring guest** (e.g., a panel returning every 4 weeks) anchors retention. But don't make it the ONLY hook.
- **Series CTA must be ladder-aligned**: lead magnet at series start, paid product at midpoint, community membership at series end.
- **Cross-link every tentpole to the series landing page** — SEO compounding requires the hub-and-spoke architecture.
- **Notion DB rows with broken `Series` relations** orphan derivative rows. Use Notion's `Roll-up` feature on the Series DB to count tentpoles.
- **Per-tentpole KPI must be set BEFORE publish** — retroactive KPIs are vanity metrics.
- **Series rights** — if guests appear, your release form must cover series + episode + clip + derivative usage. Standard podcast release covers episode-only; add series rider.
- **Don't overload child derivatives in Notion** if you're not actually going to ship them all. 8-10 derivatives per tentpole is the actionable cap; 30+ becomes a graveyard of "Drafting" status rows.

## Sources

- [Notion editorial calendar template](https://www.notion.com/templates/editorial-calendar)
- [Notion AI content calendar with Claude](https://espressio.ai/blog/claude-notion-content-calendar)
- [ThoughtLeaders — Podcast trends 2026](https://www.thoughtleaders.io/blog/podcast-trends-2026)
- [Castmagic Stormy AI repurposing 2026](https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic)
- [Blotato — Best AI content repurposing 2026](https://www.blotato.com/blog/ai-content-repurposing-tools)
