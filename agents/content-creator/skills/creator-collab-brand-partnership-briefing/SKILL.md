# Creator Collab + Brand Partnership Briefing — Notion DB + FTC + Outreach

> Brief a brand partnership / creator collab end-to-end, FTC-compliant, with Notion pipeline and Gmail outreach.

## When to use

Trigger on: "brand partnership brief", "creator collab pitch", "sponsorship pitch deck", "outreach to <brand>", "FTC disclosure language", "co-marketing brief", "guest cross-promo deal". This skill owns: partnership brief templates, FTC disclosure language, deal structure, outreach via Gmail, pipeline tracking in Notion, contract checklist. For podcast-specific sponsorship integration (host-read scripts + DAI) see `podcast-sponsorship-integration`. For guest collab discovery + research see `podcast-guest-research-outreach`.

## Setup

```bash
# Notion MCP for partnership pipeline
npx -y @notionhq/mcp-server@latest

# Gmail MCP for outreach
npx -y @gongrzhe/server-gmail-autoauth-mcp@latest

# Optional: DocuSign / PandaDoc for contract execution (out of scope for this skill;
# the brief drives the contract; legal handles signature)
```

Auth env vars:
- `NOTION_PARTNERSHIPS_DB` — DB ID of the partnership pipeline table.
- `GMAIL_FROM` — outreach sender Gmail.

## Common recipes

### Recipe 1: Partnership brief template

```markdown
# Partnership Brief: <Brand Name> × <Creator Name>

## One-sentence pitch
<why this partnership creates more value together than apart — single sentence>

## Audience overlap
- Your audience: <demographic + size>
- Brand audience: <demographic + size>
- Overlap rationale: <why these two audiences share enough that a partnership compounds>

## Deliverables
- Asset 1: <e.g., 1 newsletter dedicated issue with brand integration>
- Asset 2: <e.g., 1 LinkedIn carousel co-branded>
- Asset 3: <e.g., 1 podcast episode with brand-supplied guest>
- Asset 4 (optional): <e.g., webinar / event / shared lead magnet>

## Timeline
- Brief sign-off: <date>
- Asset 1 draft: <date>
- Asset 1 publish: <date>
- ...
- Wrap report: <date>

## Compensation
- Flat fee: $<amount>
- Performance bonus: $<amount> at <metric threshold>
- Or revenue share: <%>
- Or in-kind: <product / service / cross-promo>

## Deliverable rights
- Brand can repurpose: <yes / no / with credit>
- Creator can repurpose: <yes / no / for X months>
- Exclusivity: <category / period / none>

## Approval workflow
- Creator drafts → brand reviews → creator finalizes → publish
- Brand has <X> revision rounds; subsequent rounds = additional fee
- Brand cannot demand voice changes that violate creator's editorial standards

## FTC compliance
- Disclosure: <"Paid partnership with <Brand>" pinned in copy + "#ad" or "#sponsored" hashtag>
- Placement: <opening 2 lines / first 30s / above-the-fold>
- Endorsement language: <"In partnership with <Brand>"> NOT misleading personal endorsement

## Success metrics
- Asset 1: <CTR target / impression target / conversion target>
- Asset 2: <...>
- Wrap report: <Notion dashboard view + per-asset performance>
```

### Recipe 2: FTC disclosure language (current as of June 2026)

```markdown
## FTC required disclosure rules

**When to disclose** — any time you've received compensation, free product, or other material consideration for content that endorses a brand.

**How to disclose** — clearly, conspicuously, and in close proximity to the endorsement.

**Where to disclose**:
- Top of newsletter / blog post (above the fold)
- First 30s of podcast / video
- First line of social caption (BEFORE the "more" cut-off)
- Pinned comment is NOT sufficient on its own

**Language that works**:
- "Paid partnership with <Brand>"
- "Sponsored by <Brand>"
- "<Brand> sent me <product> in exchange for an honest review"
- "Today's newsletter is sponsored by <Brand>. They didn't review or approve this writing."
- "I'm a paid affiliate of <Brand>. If you click through, I earn a commission."

**Language that DOES NOT comply**:
- "#partner" alone (too vague)
- Disclosure in a footer no one reads
- "Thanks <Brand> for the gear" without making it clear it was a gift
- "I love <Brand>" without disclosing the relationship

**Platform-specific tags**:
- Instagram: "Paid Partnership" tag (use Meta's built-in tool)
- TikTok: "Branded Content" toggle (TikTok's built-in tool)
- YouTube: "Includes paid promotion" checkbox in Studio
- X / LinkedIn: open prose "Paid partnership with <Brand>" in opening line
```

### Recipe 3: Notion partnerships DB schema

```yaml
Partnerships DB:
  properties:
    Brand: { type: title }
    Status: { type: select, options: [Researching, Pitched, Negotiating, Signed, In production, Live, Wrap, Closed-Won, Closed-Lost] }
    Deal Size: { type: number }
    Compensation Type: { type: select, options: [Flat, Performance, Revenue share, In-kind, Hybrid] }
    Deliverables: { type: multi_select }
    Brand Contact: { type: text }
    Brand Email: { type: email }
    Pitch Sent: { type: date }
    Brief Approved: { type: date }
    Contract Signed: { type: date }
    Go-Live Date: { type: date }
    Wrap Date: { type: date }
    KPI Target: { type: rich_text }
    KPI Actual: { type: rich_text }
    FTC Disclosure Verified: { type: checkbox }
    Repeat Partner: { type: checkbox }
    Notes: { type: rich_text }
```

Create rows via Notion MCP:

```bash
npx @notionhq/mcp create_page \
  --database_id "$NOTION_PARTNERSHIPS_DB" \
  --properties '{
    "Brand":{"title":[{"text":{"content":"<Brand>"}}]},
    "Status":{"select":{"name":"Pitched"}},
    "Deal Size":{"number":15000},
    "Compensation Type":{"select":{"name":"Flat"}},
    "Brand Contact":{"rich_text":[{"text":{"content":"Jane Smith, Marketing Lead"}}]},
    "Brand Email":{"email":"jane@brand.com"},
    "Pitch Sent":{"date":{"start":"2026-06-10"}}
  }'
```

### Recipe 4: Templated outreach email

```bash
BODY=$(cat <<'EOF'
Hi <FirstName>,

I run <PodcastName / NewsletterName / Channel>, a <one-line desc>
reaching <NumberOfReaders/Listeners> <PersonaDescription>.

I'm reaching out because <SpecificReasonRelatedToBrand>. Your
<RecentBrandActionOrProduct> hit on something my audience cares about:
<SpecificOverlap>.

I'd love to put together a partnership brief. Here's the rough shape:
- <Asset 1 — type + scope>
- <Asset 2 — type + scope>
- FTC-compliant disclosure on all assets
- Performance benchmarks set in advance

If this is a fit, I'll send a one-page brief with deliverables, timeline,
and compensation. If not a fit, a one-line "not now" is totally fine.

Past brand work + reach data: <portfolio_url>

— <YourName>
<podcast / newsletter URL>
EOF
)

npx @gongrzhe/server-gmail-autoauth-mcp send \
  --to "jane@brand.com" \
  --from "$GMAIL_FROM" \
  --subject "Partnership idea — <Brand> × <PodcastName>" \
  --body "$BODY"
```

### Recipe 5: Pre-brief audience-data sheet

Brand asks for audience data before signing. Have this ready:

```markdown
# Audience One-Sheet — <Creator Name>

## Reach
- Newsletter subs: <number> (active in last 30 days: <%>)
- Podcast monthly listens: <number>
- Total social followers: <breakdown by platform>

## Engagement
- Newsletter CTR: <%>
- Newsletter open rate: <%> (note: MPP-inflated; CTR is real signal)
- Podcast listen-through 25 min: <%>
- Avg social engagement rate: <%>

## Demographics
- Geography: <top 5 countries with %>
- Age: <distribution>
- Gender: <distribution>
- Role / industry: <top 5 with %>

## Past brand work
- <Brand 1>: <year, asset type, results>
- <Brand 2>: <year, asset type, results>

## Editorial guardrails
- We don't promote: <categories>
- We require: <FTC disclosure, brand voice approval, no veto on core writing>

## Standard rate card
- Newsletter dedicated issue: $<X>
- Newsletter classified: $<Y>
- Podcast host-read: $<Z> CPM
- LinkedIn carousel sponsored: $<W>
- Bundle discount: <%> for 3+ assets
```

### Recipe 6: Performance contract structure

```markdown
## Performance bonus structure (when applicable)

Base fee + performance bonus:

| Metric | Target | Bonus |
|---|---|---|
| Newsletter CTR | 3% | $1,000 |
| Newsletter CTR | 5% | $3,000 |
| Podcast download | 5k | $2,000 |
| Podcast download | 10k | $5,000 |
| Use of UTM-tagged URL | required | base fee only if missing |

Cap total bonus at 50% of base fee. Brand pays performance retro after 30-day attribution window.
```

### Recipe 7: Follow-up cadence

```markdown
## 3-touch follow-up

- Touch 1 (day 0): initial pitch (Recipe 4)
- Touch 2 (day +7): "Hey, just floating this back up — happy to send the one-pager if helpful"
- Touch 3 (day +21): "Last note from me. If timing's bad now, want me to circle back in Q4?"

3 touches max. Move on if no reply.
```

### Recipe 8: Negotiation checklist

```markdown
- [ ] Both parties agree on exact deliverables (typed, not implied)
- [ ] Timeline locked with milestones
- [ ] Compensation structure clear (flat / performance / hybrid)
- [ ] Payment terms: 50% on signature, 50% on delivery (standard)
- [ ] Revision rounds defined (typically 2 included, more = additional fee)
- [ ] Exclusivity clause scope + duration (don't over-promise)
- [ ] Repurposing rights both directions
- [ ] FTC disclosure language pre-approved
- [ ] Editorial independence preserved (brand cannot demand voice changes)
- [ ] Kill fee if either party walks pre-publish
- [ ] Wrap report scope + delivery date
- [ ] Future-relationship clause (right of first refusal? no.)
```

### Recipe 9: Wrap report template

```markdown
# Wrap Report: <Brand> × <Creator Name>

## Deliverables shipped
| Asset | Date | URL | KPI target | KPI actual | Hit / miss |
|---|---|---|---|---|---|
| <Asset 1> | <date> | <url> | <target> | <actual> | <hit/miss> |
| ... |

## Total reach
- Combined impressions: <number>
- Engagement: <number + %>
- Click-throughs to brand: <number>
- Attributable conversions: <number>

## Qualitative
- Top-performing asset: <name + why>
- Audience feedback themes: <bullets>
- What we'd do differently: <one paragraph>

## Recommendations
- Recommend repeat partnership? <yes / no + reason>
- Scope for next time: <bigger / smaller / different format>
- Timeline for re-pitch: <Q4 / never / on-request>
```

### Recipe 10: Repeat-partnership flag

```python
# After wrap, mark "Repeat Partner" if all KPIs hit
def mark_repeat_partner(notion_row):
    actual_vs_target_hit_rate = ... # calculate
    if actual_vs_target_hit_rate >= 0.8:
        notion_update(notion_row, {"Repeat Partner": True})
        # Add to recurring outreach cadence
```

### Recipe 11: Multi-creator collab brief (no brand sponsor)

```markdown
# Collab Brief: <Creator A> × <Creator B>

(No brand sponsor; pure cross-promo deal)

## Goal
<grow each other's audience via cross-promotion>

## Deliverables
- <Creator A> guest on <Creator B>'s podcast
- <Creator B> writes guest issue for <Creator A>'s newsletter
- Co-tweet announcement
- Co-launch lead magnet to combined list

## Compensation
- None monetary. Even-value swap.

## Performance tracking
- Each creator reports new subs/listens attributable to the collab
- 30-day window post-launch

## FTC
- No paid sponsorship → no FTC disclosure required, but disclose the cross-promo relationship for transparency
```

### Recipe 12: Pitch deck PPTX (for big-budget brands)

Use the `pptx` skill (CraftBot default) to generate a sponsorship deck:

```bash
# Outline pitch deck:
# Slide 1: Title / brand match
# Slide 2: Audience demographic + reach
# Slide 3: Past brand work + case studies
# Slide 4: Engagement benchmarks
# Slide 5: Deliverables menu
# Slide 6: Sample executions (visual mockups)
# Slide 7: Investment + ROI projection
# Slide 8: Timeline + next steps
```

## Examples

### Example 1: Outreach → signed deal in 4 weeks

**Goal:** Land a $15k newsletter + podcast brand partnership over 4 weeks.

**Steps:**
1. Identify 10 candidate brands whose audience overlaps yours.
2. Recipe 4: send 10 templated pitches over 5 days.
3. Recipe 7: 2-3 replies; follow up the rest at day +7.
4. Get 1-2 to "let's see the brief".
5. Recipe 1: send tailored brief.
6. Recipe 8: negotiate per checklist.
7. Sign contract; mark Notion row Status=Signed.
8. Recipe 9: 60 days post-delivery, send wrap report.

**Result:** $15k deal closed, FTC-compliant, wrap-reported.

### Example 2: Multi-creator co-marketing collab

**Goal:** Grow newsletter via cross-promo with another creator (no brand sponsor).

**Steps:**
1. Recipe 11: brief the swap (guest pod + guest newsletter + co-launch lead magnet).
2. Both creators agree on dates + scope.
3. Execute collab; both publish synchronously.
4. 30 days later: each creator reports new sub/listen attribution.
5. Mark repeat-collab if attribution >100 net new subs.

**Result:** ~500-2k net new subs via single high-quality swap.

### Example 3: Performance-bonus newsletter sponsorship

**Goal:** Brand wants performance-tied compensation; structure deal accordingly.

**Steps:**
1. Recipe 6: performance bonus structure.
2. Recipe 1 brief with base $5k + performance tiers.
3. Sign.
4. Ship sponsored issue with UTM-tagged links.
5. 30 days post: pull CTR + attributed conversions.
6. Recipe 9: wrap with performance compensation owed.
7. Invoice for base + earned bonus.

**Result:** Aligned incentives; trust built for repeat partnership.

## Edge cases / gotchas

- **FTC enforcement intensified 2025-2026.** Non-compliance = fines + brand-side liability. Don't skip disclosure even on "small" affiliate deals.
- **#ad / #sponsored is the minimum** — vague "#partner" or "#collab" doesn't satisfy FTC.
- **Hidden affiliate links require disclosure** — every embedded affiliate URL needs proximate disclosure.
- **Disclosure must be in the language of the audience** — auto-translated disclosures in non-English contexts get scrutinized.
- **Performance bonuses tied to vanity metrics (opens, impressions) are gameable.** Tie to CTR / clicks / conversions / unique attributable visitors.
- **Brand can review but cannot veto editorial voice.** Specify this in the brief; without it, brand will push for voice changes that tank engagement.
- **Don't promise exclusivity longer than 3 months** for category-exclusive deals; it kills your roster pipeline.
- **Kill-fee protects you** if brand walks pre-publish after you've done the work. 25-50% of total fee standard.
- **Repurposing rights both directions** — without explicit grant, brand cannot reuse your content; you cannot reuse theirs. Spell out in brief.
- **Don't accept product-only deals** unless you'd buy it yourself; in-kind has hidden costs (time, opportunity cost).
- **Repeat-partner cadence**: 1-2 deals/year per brand max. More = audience-trust erosion.
- **Always issue invoice + W-9 (US) / similar tax docs** — paid partnerships are reportable income.
- **Don't pitch 10 brands in the same vertical** — they talk; you'll get burned. Sequential is fine.
- **Pre-approved disclosure language** in the brief avoids day-of-publish friction.
- **Multi-creator collabs DON'T require FTC disclosure** when no money changes hands, but transparency about the cross-promo arrangement is best practice.

## Sources

- [FTC endorsement guides 2025](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)
- [FTC influencer disclosure 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [ThoughtLeaders — Podcast trends 2026](https://www.thoughtleaders.io/blog/podcast-trends-2026)
- [Podchaser API for collab discovery](https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api)
- [Notion partnership pipeline template](https://www.notion.com/templates/sales-pipeline)
- [Standard freelance contract terms](https://www.aiga.org/standard-agreement-for-design-services)
