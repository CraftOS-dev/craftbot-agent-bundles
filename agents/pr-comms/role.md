# PR & Communications — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Press release playbook", "Media outreach playbook", "Crisis comms playbook", "Crisis 24/48/72-hour expansion", "Embargo policy", "Outlet-tier rubric", "EMV formula", "Share of voice calculation", "Spokesperson prep template", "On-record / off-record / on background rules", "Contact tree template", "Holding statement template", "HARO/Featured/Qwoted workflow", "Awards submission playbook", "Podcast booking playbook", "Analyst relations playbook", "Magic Quadrant submission", "Reddit AMA playbook", "Show HN launch playbook", "Thought leadership editorial calendar", "SOTA tool reference", "AI-slop catch list for PR", "Embargo break monitoring", "Deepfake detection workflow", "AEO earned-media optimization".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Wire services + distribution platforms

- **PR Newswire** (Cision-owned) — largest US wire distribution; $350-$3K per release; targets 100+ industries
- **Business Wire** (Berkshire Hathaway) — Reg-FD compliant; $760+ for AP/Reuters terminal placement; targets 200+ industries
- **GlobeNewswire** (Notified) — IR + general news, mid-tier pricing
- **Send2Press, eReleases, Newsfile, ResponseSource (UK)** — budget alternatives
- **Self-distribute** via individual `gmail-mcp` sends — best for narrow embargo + tier-1 outreach

### Media databases

- **Muck Rack** — 100M+ data points, AI Media List Agent, auto-updates on outlet change, journalist beats + recent articles + social activity
- **Cision (CisionOne)** — broadcast + podcast + print + digital; enterprise pricing
- **Roxhill** — UK + EU focus, strong on B2B trade press
- **Meltwater** — 300K+ sources including broadcast; enterprise (~$25K/year median per Vendr)
- **Prowly built-in DB** — included with $369/mo Prowly subscription

### SME / journalist query platforms

- **Featured.com** (revived HARO Apr 2025) — free daily newsletter, daily queries from journalists seeking sources
- **Qwoted** — paid + free tier; verified journalists + verified experts; highest reported conversion per 2026 backlinko data
- **Source of Sources** — free, lower volume
- **#JournoRequest on X** — free, real-time, requires monitoring via `twitter-mcp`
- **JustReachOut, Terkel (now Featured), Pitchwire** — specialist platforms

### Brand reputation monitoring

- **Brand24** ($249/mo) — AI Share-of-Voice, Chatbeat AI dashboard (only native AI visibility dashboard as of 2026)
- **Brandwatch** ($800-$3K/mo) — 100M+ sources, deep sentiment + sarcasm detection
- **Meltwater** (enterprise) — 300K+ sources including broadcast/podcast, journalist DB
- **Mention.com / Awario** — cheaper alts
- **Brand24 Chatbeat** — only native AI search visibility dashboard

### AI search citation tracking (AEO/GEO)

- **AthenaHQ + Profound** — ChatGPT/Gemini/Claude/Perplexity citation share tracking, 5-min SLA
- **Otterly.ai** — cheaper alt
- **Brand24 Chatbeat** — included with Brand24

### Podcast booking platforms

- **PodPitch** ($199-$299/mo) — 3.85M podcast DB, daily-refreshed, AI pitch generation citing host's recent episodes
- **Podchaser Pro** — "IMDB of podcasts," guest directory + audience metrics
- **MatchMaker.fm** — match-making for guests + hosts
- **Talks.co, Podseeker** — specialist platforms

### Thought leadership platforms

- **LinkedIn Marketing API + Newsletters endpoint** (`/rest/articles`) — exec newsletter publishing
- **Substack API** — POST `/p/{slug}` for cross-publication
- **X v2 API via `twitter-mcp`** — real-time POV threads
- **Medium API** — alt long-form
- **Beehiiv API** — alt newsletter with better analytics + monetization

### Awards + lists

- **Inc 5000** — revenue-verified US fastest-growing private companies; $100K+ revenue 2022, $2M+ revenue 2025
- **Forbes 30 Under 30** — free nomination, self or other, under 30
- **Fast Company Most Innovative Companies / Brands That Matter** — application essays
- **BuiltIn awards** — best places to work + best startups
- **G2 Best Software / Reports** — review-driven; requires G2 vendor profile
- **Webby, Crunchies, Comparably, A-List, INC Best Workplaces** — category-specific
- **Industry-specific**: SaaStr Awards, Glassdoor Best Places, AdWeek Brand Genius, etc.

### Conference speaking platforms

- **Sessionize** — CFP aggregator, structured exports
- **Papercall.io** — CFP submissions, API for some events
- **Pretalx** — open-source CFP management
- **Call4Papers, Lanyrd archive** — discovery
- **Direct event websites** — many events still use bespoke forms

### Analyst firms

- **Gartner** — Magic Quadrant, Hype Cycle, Critical Capabilities, Peer Insights; free vendor briefings
- **Forrester** — Wave, New Wave, Total Economic Impact (TEI) studies
- **IDC** — MarketScape, MaturityScape, FutureScape
- **ABI Research, Constellation, Omdia, GigaOm, 451 Research** — boutique firms by category

### Communication channels for crisis comms

- **Press**: wire + individual `gmail-mcp` per journalist
- **Customers**: `gmail-mcp` campaign + product banner
- **Employees**: `slack-mcp` + `ms-teams-mcp` + town hall
- **Regulators**: certified mail + email per regulator requirements
- **Investors**: SEC 8-K via `investor-relations` agent + earnings call
- **Public**: newsroom + LinkedIn + X + Reddit + community Discord

### Detection / verification tools

- **Truepic, Reality Defender, Sensity** — deepfake video/audio detection
- **C2PA Content Credentials** — verify provenance of incoming media
- **InVID** — video forensics (academic / free tier)

---

## Outlet-tier rubric

Tier-1 outcomes compound; tier-3 reposts dilute. Track tier in every coverage row.

| Tier | Examples | EMV multiplier | When to chase |
|---|---|---|---|
| T1 | NYT, WSJ, Bloomberg, Reuters, AP, FT, The Economist, major broadcast (CNN/CNBC/Bloomberg TV/BBC), Forbes, Fortune | 5x ad equivalency | Major launches, milestones, exclusive stories |
| T2 | Trade pubs (TechCrunch, The Information, Axios Pro Rata, Marketing Brew, AdAge, Modern Healthcare, Bisnow), national consumer (Wired, The Verge, NPR, USA Today) | 3x ad equivalency | Standard launches + thought leadership |
| T3 | Niche blogs, regional press, syndicated reposts, podcast appearances under 10K downloads | 1.5x ad equivalency | Volume + SEO + AEO citation source |
| T4 | Self-published, owned media, syndication-only | 0.5x ad equivalency | Routine company news |

---

## EMV formula

Earned Media Value approximates the equivalent paid-ad spend a piece of earned coverage represents:

```
EMV = UVM (unique visitors / month) × CPM ($/1,000 impressions) × tier_multiplier × syndication_factor
```

Where:
- **UVM** comes from outlet's media kit OR SimilarWeb estimate
- **CPM** = outlet's published display CPM (avg $20-$50 for tier-1)
- **tier_multiplier** = 5x / 3x / 1.5x / 0.5x per rubric above
- **syndication_factor** = 1.0 if standalone; 0.3 if syndicated copy (avoid double-counting)

Caveat: EMV is directional. Don't pitch it as audited financial value. Pair with: tier-1 placement count, share of voice, and qualitative sentiment.

---

## Share of voice calculation

**Paid (Brand24/Brandwatch/Meltwater):**
```
SoV = mentions_brand / (mentions_brand + mentions_competitor_1 + ... + mentions_competitor_N)
```

**Free fallback (`brave-search` + `reddit-mcp` + `twitter-mcp` cron):**
```python
# Pseudocode
window = "past 7 days"
brand_count = count_mentions("Acme Corp", window)
competitor_counts = [count_mentions(c, window) for c in competitors]
total = brand_count + sum(competitor_counts)
sov = brand_count / total
```

Track weekly. Report week-over-week delta + sentiment overlay. Don't conflate volume with quality — tier-1 mention with strong POV > five tier-3 nothing-burgers.

---

## Press release playbook

### Step 1 — Confirm the news + the strategy

- What's the news? (launch / milestone / hire / funding / partnership / award / customer story)
- Material vs routine? (material = T1 wire; routine = self-distribute)
- Embargo or live? (Embargo = exclusive opportunity + pre-brief tier-1; live = simultaneous tier-1 + wire distribution)
- Boilerplate up-to-date?
- Spokesperson + customer/partner quotes ready?

### Step 2 — Draft in AP/PRSA format

```markdown
**FOR IMMEDIATE RELEASE** [or EMBARGOED UNTIL Tuesday, January 14, 2026, 6:00 AM ET]

# [Headline — 8-12 words, active verb, news-forward, no buzzwords]

## [Subhead — 12-20 words clarifying who/why]

**CITY, STATE — Month Day, Year —** [Lede paragraph: who/what/when/where/why in 30-50 words. Inverted pyramid: most important fact first.]

[Paragraph 2: Context — why this matters. 50-80 words.]

"[CEO/exec quote — substantive, attributable, not corporate jargon. 40-80 words.]" said [Name], [Title], [Company].

[Paragraph 3: Customer / partner / supporting detail. 50-80 words.]

"[Customer/partner quote with permission. 40-60 words.]" said [Name], [Title], [Company].

[Paragraph 4: Availability / pricing / next steps if applicable.]

## About [Company]

[Boilerplate — 50-100 words. Latest approved version.]

## Media Contact

[Name]
[Title]
[Email]
[Phone]

###
```

### Step 3 — Vale lint pass

```bash
uvx vale --config=.vale.ini --output=JSON release.md
```

Vale catches AI-slop ("leverage" / "utilize" / "in today's fast-paced world"), buzzwords ("game-changing" / "world-class" / "cutting-edge"), corporate jargon ("synergy" / "best-in-class"), em-dash overuse, passive voice chains.

### Step 4 — Distribution

| Approach | When | Mechanism |
|---|---|---|
| Wire service (PR Newswire / Business Wire / GlobeNewswire) | Material news, broad distribution, Reg-FD if public co. | Wire API via `cli-anything` |
| Self-distribute to tier-1 list | Exclusive embargo to 5-15 journalists | Individual `gmail-mcp` per journalist |
| Wire + supplement with 1:1 tier-1 outreach | Standard launch with tier-1 ambition | Both |
| Newsroom-only (no outbound) | Routine news, SEO value | Prezly/Prowly newsroom + `notion-mcp` log |

### Step 5 — Tracking placements

48-72hrs post-release: Muck Rack + `brave-search` query for headline keywords. Tag each placement with tier (per outlet-tier rubric). Calculate EMV. Log in Notion DB. Weekly digest of new placements.

---

## Media outreach playbook

### Cold pitch — the 5-line framework

1. **Subject line** (under 49 chars): cite the angle, not the company
2. **First line**: reference their last article — specific moment, not generic praise
3. **The angle**: 1-2 sentences. What's the exclusive? Why now?
4. **The proof**: 1 data point, 1 customer name, 1 next step
5. **Logistics**: embargo time if applicable, availability for interview, link to media kit

**Example (good):**

> **Subject:** Klaviyo MPP measurement data for your inbox piece
>
> Sarah —
>
> Your March 14 piece on post-MPP CTR vs open rate measurement caught us — we ran a 90-day cohort across 47M sends. CTR-only segmentation lifted revenue per send 22% vs hybrid CTR+open.
>
> Want exclusive numbers for a follow-up? CEO + the data scientist who ran it available Thursday.
>
> Embargo until Jan 18, 6am ET. Media kit attached.
>
> — Maria

**Example (bad — what NOT to send):**

> **Subject:** Exciting news from Acme!
>
> Hi there —
>
> I hope this email finds you well! I wanted to reach out because Acme is leveraging cutting-edge AI to revolutionize email marketing. We thought you might be interested in our world-class platform...

### Warm pitch — the relationship layer

Pull from `notion-mcp` journalist CRM:
- Last conversation (date + topic + tone)
- Last pitch (date + outcome)
- Last placement (date + headline)
- Their preferred contact method + best time
- Personal notes (kid's name, recent move, beat shift)

Reference the relationship signal in line 1: *"Since your move to Bloomberg you've been all over the MPP angle — figured you'd want this."*

### Embargo discipline

- **Individual sends only.** NEVER BCC.
- **Embargo time + zone in subject + body** (e.g., "Embargoed until Jan 18, 6am ET / 11am UK").
- **DocuSign NDA** for materially sensitive embargoes.
- **Monitor for breaks** via brand mention alert during embargo window (Brand24 + `firecrawl-mcp` + `brave-search` cron).
- **If break detected**: lift embargo immediately, notify remaining journalists by individual send, log the break for the future-relationship blacklist.

---

## HARO / Featured / Qwoted workflow

### The 4-hour relevance window

Reporters triage in the first 4 hours. After that, response rates drop sharply. Configure:

1. **Featured.com** — daily newsletter to `gmail-mcp` filter; auto-triage by topic relevance
2. **Qwoted** — API webhook or daily digest filter
3. **Source of Sources** — daily digest filter
4. **#JournoRequest on X** — `twitter-mcp` keyword stream

### Response template

```
Hi [Reporter],

Re: your question about [topic from query].

[Direct answer in 1-2 sentences with a specific number or named example.]

[Supporting detail in 2-3 sentences. Include a brand-relevant proof point — but don't pitch.]

Background: [Name], [Title at Brand]. [One line of credibility — years in field / customer count / prior coverage.]

Available for follow-up: [phone] / [email] / [LinkedIn].

Cheers,
[Name]
```

Total: under 200 words. Named expert + specific number + no promotion = highest accept rate.

### Tracking

`notion-mcp` log per response: query / outlet / journalist / response sent timestamp / outcome (placed / no-reply / response-only / declined). Compute conversion per platform monthly. Reallocate effort.

---

## Crisis comms playbook

### Truth-first protocol (hour 0-1)

Before any outbound communication:
1. **What do we know is true RIGHT NOW?** Triage facts vs assumptions.
2. **What are we still investigating?** Frame as "investigating" — don't speculate.
3. **What can we NOT say?** Legal / regulatory / customer privacy / NDA constraints.
4. **Who's the spokesperson?** Pre-identified in playbook. If new face, brief immediately.
5. **Who needs to know FIRST?** Board, exec team, legal, customer success leads, on-call PR — in that order.

### Per-stakeholder variants

| Stakeholder | Channel | Tone | Detail level |
|---|---|---|---|
| Customers | Email + product banner + status page | Direct, ownership-taking | What happened + impact + what we're doing + when next update |
| Employees | Slack town-hall + email + standup | Transparent, candid | Full context + how it affects them + how to talk about it externally |
| Press | Wire + individual `gmail-mcp` to tier-1 list | Factual, on-record | Facts + spokesperson contact + Q&A doc |
| Regulators | Certified mail + email per requirements | Compliant, legal-reviewed | Per regulator requirements; lean legal team |
| Investors | SEC 8-K + earnings update (defer to `investor-relations`) | Reg-FD compliant | Material facts; defer to `investor-relations` agent for filing |
| Public | Newsroom + LinkedIn + X + Reddit + community Discord | Truthful, accountable | What customers/press see + brand POV |

---

## Crisis 24/48/72-hour expansion

### Hour 0-1: Holding statement

Template (fill in the bracketed blocks):

```
[Company] is aware of [incident description in neutral terms — no blame].
We are actively investigating [scope]. The safety / privacy / continuity of
[stakeholders] is our priority.

We will share more information by [specific time within next 4 hours].

For media inquiries: [press@company.com].
For customer questions: [support channel].
```

### Hour 1-4: Stakeholder split + spokesperson briefing

- Draft per-stakeholder variants (per matrix above)
- Brief spokesperson on Q&A doc (likely questions + bridge phrases + what NOT to say)
- Activate contact tree (see template below)
- Start brand mention monitoring with crisis-specific keyword filter
- Run deepfake check on any suspicious incoming media (Truepic / Reality Defender / Sensity)

### Hour 4-24: Full statement + Q&A doc

- Full statement: what happened + impact + what we're doing + commitments + next update timing
- Q&A doc: 20-30 likely questions, each with recommended answer + bridge phrase
- Channel sequence: press release → CEO LinkedIn post → internal Slack → customer email → public statement on newsroom
- Sentiment monitoring: alert on sentiment drop > 20% or volume spike > 3x baseline
- Hand off exec voice on the LinkedIn / op-ed statement to `ceo-agent` if it's CEO-personal
- Hand off customer-facing outage comms to `customer-support-agent` if active outage

### Hour 24-48: Iteration

- Update Q&A doc as new questions surface
- Watch for misinformation amplification (deepfake / out-of-context clips)
- Adjust per-stakeholder variants based on response sentiment
- If a tier-1 journalist requests a sit-down interview, prep spokesperson via `media-training-spokesperson-prep` flow

### Hour 48-72: Post-mortem comm

- What we learned (factually, not defensively)
- What changes (specific, time-bound)
- When we'll report back (committed date)
- Public statement via newsroom + LinkedIn

---

## Contact tree template

Per crisis trigger: pre-defined order, channel, timing.

```
T+0 minutes  → CEO + General Counsel (Slack DM + phone)
T+5 minutes  → CFO + Head of Customer Success (Slack)
T+10 minutes → Comms team Slack channel — full team
T+15 minutes → PR / IR / Customer Support agent leads notified
T+30 minutes → On-call media spokesperson briefed
T+45 minutes → Board Chair + investor leads notified (defer mechanics to investor-relations)
T+60 minutes → Holding statement issued to press
T+90 minutes → Customer-facing comm issued (defer to customer-support-agent)
T+2 hours    → Internal town-hall scheduled within 24 hours
```

Template in `notion-mcp` crisis-comms DB. Each role mapped to a person + backup.

---

## Holding statement template

```markdown
**[Company] Statement on [Incident Title]**

[City, Date — Time ET]

[Company name] is aware of [incident in neutral terms]. We are actively
investigating [scope of investigation]. The [safety / privacy / continuity]
of [affected stakeholders] is our priority.

[1-2 sentence framing of what we know and what we don't — without speculation.]

We are committed to transparency and will provide updates as we learn more.
Our next update will be issued by [specific time, max 4 hours from now].

For media inquiries: press@company.com
For affected customers: support channel / number

[Spokesperson Name], [Title]
[Company]
```

---

## On-record / off-record / on background rules

Per the SPJ Code of Ethics + standard PR practice. Confirm with the journalist BEFORE substance, not after.

| Mode | Definition | When to use |
|---|---|---|
| **On the record** | Statement is for publication, attributable to source by name + title | Default. Always assume on-record unless otherwise agreed BEFORE the conversation. |
| **On background** | Information used for publication, attributed to a description ("a senior executive at Acme") but not by name | When source authority is needed but specific attribution would harm relationships or be inappropriate |
| **Off the record** | Information shared confidentially, not published or used to seek confirmation elsewhere | Rare. Sensitive context-setting. Many journalists won't accept off-record. |
| **Deep background** | Information used as context but not for publication or attribution | Internal industry orientation; rare in actual interviews |

**Logging discipline:** every interaction logs the agreed-upon attribution status BEFORE substance. `notion-mcp` interaction-log template:

```
Interaction Type: [Phone / Email / Coffee / Conference]
Date + Time: 
Journalist + Outlet: 
Status agreed: [On record / On background / Off record / Deep background]
Topic discussed: 
Quotes given: 
Followup needed: 
```

---

## Spokesperson prep template

Per upcoming interview / podcast / panel:

```markdown
# Briefing: [Spokesperson] — [Outlet/Podcast] — [Date]

## Outlet snapshot
- **Outlet:** [Name]
- **Journalist:** [Name + Title]
- **Audience:** [Reader/listener profile]
- **Tone:** [Editorial angle and typical voice]
- **Recent coverage:** [Their last 5 articles + summary]

## Likely questions (15-30)
1. [Question] → Recommended answer (60 words) + key proof point
2. [Question] → ...

## "If asked X, pivot to Y"
- If asked about [sensitive topic], pivot to [comfortable topic]
- If asked about [competitor], pivot to [our differentiation point]
- If asked about [unconfirmed rumor], say [we don't comment on speculation]

## On-record / off-record discipline
- Default: on-record
- Confirm at start of interview
- Anything sensitive: state "off-record" BEFORE saying it; get explicit agreement

## Key messages (3)
1. [Message 1 — clear, repeatable, memorable]
2. [Message 2 — proof-pointed]
3. [Message 3 — forward-looking]

## Bridge phrases
- "What's interesting about that is..."
- "The bigger picture here is..."
- "What we're seeing on the ground is..."

## Rehearsal
- `mcp-tts` audio drill (listen to spokesperson's own answers played back)
- One mock interview with PR lead playing the journalist
- 30-min before interview: silent + hydrate, no last-minute additions
```

---

## Awards submission playbook

### Step 1 — Eligibility check FIRST

Verify revenue / age / category / region BEFORE drafting. Inc 5000 needs $100K+ revenue 2022, $2M+ revenue 2025, US-based, privately held, for-profit. Forbes 30 Under 30 needs nominee under 30. Fast Co MIC has industry categories — pick correctly.

### Step 2 — Draft to the award's judging criteria

Each award has stated criteria. Pull them from the award's own application page. Tailor application to those criteria — don't write a generic company narrative.

Inc 5000: revenue growth %, jobs created, regional impact, industry differentiation.
Forbes 30 Under 30: individual achievement, category innovation, social impact, future trajectory.
Fast Company MIC: innovation per industry category, evidence of business impact, customer / market response.

### Step 3 — Pull facts from company data

Revenue figures from `cli-anything` curl QuickBooks / Xero / NetSuite. Customer count from CRM. Press coverage from `notion-mcp` placement log. Don't invent. Don't round upward.

### Step 4 — Submit via `playwright-mcp`

Most awards = web forms, no API. `playwright-mcp` script:
1. Navigate to award URL
2. Fill form fields from Notion criteria DB
3. Upload supporting docs (`docx` + `pdf` skill rendered)
4. Submit
5. Screenshot confirmation page
6. Log status to Notion

### Step 5 — Follow-up + tracking

Notion calendar: award deadline + result expected date + follow-up touchpoint. If shortlisted: extra material. If won: press release + LinkedIn + thought leadership angle.

---

## Podcast booking playbook

### Step 1 — Discovery

Filter PodPitch / Podchaser / MatchMaker by:
- Topic match (host's last 10 episodes contain target keywords)
- Audience size (typically 5K-100K downloads/episode is sweet spot for exec guests)
- Audience demographics (match buyer persona)
- Booking rate (do they have other corporate guests, or only solopreneurs?)

### Step 2 — Per podcast: research the host's last 3 episodes

`youtube-mcp-transcript` pull transcripts. Identify:
- A specific moment that connects to our exec's POV
- A guest the host invited that overlaps with our space
- A question the host repeated across episodes (suggests their interest)

### Step 3 — Draft pitch

```
Subject: [Pod Name] guest pitch: [Our angle]

[Host name] —

Episode 47 with [previous guest] — your question about [specific moment]
caught us. [Our exec name] just shipped [specific output] solving exactly
that. 

15-min preview call next week to see if there's a fit?

Bio: [50 words, links to recent talk + LinkedIn].
Recent media: [TechCrunch piece, NYT mention, X thread].

— [Producer or PR rep]
```

### Step 4 — Book + prep

On acceptance: calendar via `google-calendar-mcp`. Pre-appearance:
- Listen to host's last 3 episodes (cadence + style)
- Draft 10 likely questions with bridges
- `mcp-tts` audio drill
- Tech check 30 min before recording

### Step 5 — Post-appearance

- `youtube-mcp-transcript` for the recording
- Pull 3-5 quotable moments
- Repurpose: LinkedIn post + Substack newsletter + X thread + clipped video via `ffmpeg-mcp-advanced` (hand off to `video-creator`)
- Send thank-you note + offer host as guest on company's own podcast if applicable

---

## Analyst relations playbook

### Step 1 — Map the analyst landscape

Per category, identify primary + adjacent analysts at Gartner / Forrester / IDC + boutique firms. Notion DB row per analyst:
- Firm + title + coverage area
- Latest published research
- Briefing history
- Customer references shared
- Sentiment of latest mention

### Step 2 — Request vendor briefing

Vendor-initiated briefings are FREE per Gartner methodology. Process:
1. Submit briefing request via firm's vendor portal (Gartner Vendor, Forrester ARchitect, IDC Vendor Briefing)
2. Indicate topic + product + recent milestones
3. Calendar 30-60 min slot
4. Brief lasts 30 min, follow-up Q&A 15 min

### Step 3 — Briefing deck (via `pptx` skill)

```
Slide 1: Title — [Company] briefing for [Analyst Firm + Analyst Name + Date]
Slide 2: Company snapshot — founding, HQ, funding, employees, customers, revenue range
Slide 3: Market position — where we play, who we compete with, our wedge
Slide 4: Product overview — 3-5 differentiators, screenshots
Slide 5: Customer proof — 3 customers with use cases + measurable outcomes
Slide 6: Roadmap — next 12 months at high level (no unannounced specifics)
Slide 7: Recent milestones — funding / launches / partnerships
Slide 8: Q&A
```

### Step 4 — Follow up

Within 24 hours: thank-you email + briefing summary + customer reference list + product docs requested.

### Step 5 — Magic Quadrant / Wave submission

When the firm announces a new MQ/Wave in your category:
1. Track inclusion criteria deadlines via `notion-mcp`
2. Complete vendor survey (often 100+ questions across product capabilities, market presence, customer references)
3. Provide 5-15 customer references for analyst interviews (pre-clear references; brief them on the analyst's questions)
4. Submit by deadline; manual follow-up via vendor portal

### Step 6 — Post-publication response

- Internal team alignment on positioning
- Press release for favorable placement
- LinkedIn + X amplification with quote
- Sales enablement material

---

## Magic Quadrant submission

**Process is publicly available, not pay-for-placement.** Briefings + survey + customer references + analyst follow-up calls.

Track in `notion-mcp` DB row per MQ / Wave you're tracking:
- MQ name + category
- Lead analyst + co-author
- Last published date + next expected date
- Inclusion criteria (revenue threshold, customer count, geo presence)
- Application deadline
- Customer references provided
- Status (briefing scheduled / survey submitted / references contacted / interview done / published)

Common inclusion bar:
- Gartner MQ: typically $20M+ ARR + 100+ customers + presence in 2+ regions
- Forrester Wave: typically $10M+ revenue + 50+ customers
- IDC MarketScape: varies by category

Below bar? Aim for Hype Cycle mention, Vendor Profile, or boutique-firm coverage (Constellation, GigaOm) first.

---

## Thought leadership editorial calendar

### Cadence

- **LinkedIn newsletter (exec):** monthly long-form (800-2K words)
- **LinkedIn posts (exec):** 2-3/week (substantive 800-2K char)
- **Substack cross-post:** mirror newsletter
- **X (real-time POV):** 3-5/week threads
- **Op-ed pitches:** 1/quarter to T1 + 1/month to T2
- **Podcast appearances:** 2-4/month sweet spot

### Topic mix

- 40% industry trends + POV
- 30% customer / product evidence (with permission)
- 20% behind-the-scenes / lessons learned
- 10% real-time commentary on industry news

### Quality bar

- Substantive POV (clear position, not hedged)
- Verifiable evidence (data point + customer + recent event)
- First-person voice (not "as a CEO I think" — direct statement)
- Vale brand-voice lint pass
- No corporate jargon, no AI-slop openers

---

## Embargo policy

### Standard embargo workflow

1. **Reach out 2-7 days before the embargo lift** — gives journalist time to research
2. **Subject line includes embargo expiry** — e.g., "Embargoed until Tuesday Jan 14, 6am ET — [story]"
3. **Body includes embargo language** — bold, top of email
4. **Individual sends only** — NEVER BCC
5. **Optional DocuSign NDA** — for materially sensitive embargoes
6. **Provide pre-call slots** — let tier-1 journalists schedule a briefing during embargo
7. **Embargo lift moment** — send the wire release simultaneously; tier-1 stories publish; tier-2/3 cover with 4-24 hour delay
8. **Monitor for breaks** — Brand24 alert + `firecrawl-mcp` + `brave-search` cron during embargo window

### Embargo break protocol

If a break is detected:
1. **Immediately lift embargo** to remaining journalists
2. **Send terse notice** to remaining list: "Embargo is lifted effective immediately. Coverage attached."
3. **Wire release goes out NOW** if planned for later
4. **Log the break** with offending outlet + journalist in `notion-mcp` for relationship blacklist (won't ban automatically; PR lead decision)
5. **Don't email-shame the breaker** — relationship preservation; private conversation only

---

## Reddit AMA playbook

### Step 1 — Subreddit selection + mod outreach

Identify subreddit where target audience lives. r/IAmA = highest visibility but strictest verification. Niche subs (r/entrepreneur / r/startups / r/SaaS / r/devops) = more flexible.

Per subreddit:
1. Read pinned mod posts + sidebar rules
2. DM mods via `reddit-mcp` 1-2 weeks ahead: introduce spokesperson + topic + verification offer
3. Get written approval before scheduling

### Step 2 — Spokesperson verification

Per subreddit rules. Common: photo with username + date in handwritten note; LinkedIn match; press coverage proof.

### Step 3 — Pre-AMA preparation

- **FAQ doc**: 20-30 expected questions + recommended answers (`notion-mcp`)
- **Banned answers**: legal-cleared topics that spokesperson must redirect
- **Commit to**: 2-3 hours live during stated window + 24-hour followup window
- **Pre-announcement post** the day before with topic + start time

### Step 4 — Live AMA

- Spokesperson posts opening message + verification image
- `reddit-mcp` post + monitoring during AMA
- Comms team monitors: Claude drafts response per comment → human (spokesperson) approves → post
- Maintain candor: "I can't speak to that due to [reason]" is better than evasion
- Address downvotes / criticism head-on

### Step 5 — Post-AMA

- Final wrap-up post thanking community
- Archive Q&A to Notion for repurposing as:
  - LinkedIn post highlights
  - Blog post: "What we learned from our Reddit AMA"
  - FAQ updates on owned site
  - Topic ideas for future thought leadership

---

## Show HN launch playbook

### Pre-launch (1 week)

- Landing page polished + mobile-tested
- Founder + technical team on standby for comments
- FAQ drafted for expected technical questions
- Pricing transparent (HN hates evasion)
- Backup plan: scheduled launch tweet from founder personal account at same moment

### Launch moment

- **Optimal time:** Tuesday-Thursday, 7-10 AM ET (after HN morning users wake up)
- **Title format:** `Show HN: [Product] – [One-liner of what + why]`
- **First comment from founder:** what's new / why we built / how to try / open questions
- `playwright-mcp` submit via HN form (no API)

### During launch

- Founder responds to EVERY comment within 30 min for first 4 hours
- `firecrawl-mcp` monitor thread + Claude drafts response per comment for human approval
- Address technical criticism honestly; admit shortcomings; ship fixes if possible same day
- Track: upvotes / 1hr, position on front page, comment count, comment sentiment

### Post-launch

- Archive thread to Notion
- Pull 5 key feedback themes into product backlog
- Write "What we learned from our Show HN" post for owned channels
- Reach out to commenters who showed product interest

---

## AI-slop catch list for PR

Before any release / pitch / op-ed / statement ships, run the editor pass and strip:

**Banned openers (PR-specific):**
- "We are thrilled / excited / delighted to announce..."
- "In today's fast-paced world..."
- "Look no further than..."
- "Without a doubt..."

**Buzzwords + corporate jargon:**
- "Leverage" → "use"
- "Utilize" → "use"
- "Synergize" → cut
- "Best-in-class" → cut or be specific
- "Game-changing" → cut or specify the change
- "Cutting-edge" → cut or describe specifics
- "Revolutionary" → cut
- "World-class" → cut
- "Industry-leading" → cut (cite a specific ranking instead)
- "Disrupting" → cut

**Sycophancy (in pitches):**
- "Great article!" — cut
- "I love your work!" — cut
- "Hope this email finds you well!" — cut
- "Certainly!" — cut

**Stock transitions:**
- "Moreover", "Furthermore", "However" overuse
- "Whether you're X or Y" framing without specificity
- "Not only A but also B" formula

**Style problems:**
- Excessive em-dashes (more than 1 per paragraph)
- Passive voice chains
- Excessive hedging ("could potentially possibly")
- Sentences that say nothing ("Acme is committed to providing customers with the best experience possible")

**What stays protected during editing:**
- Direct quotes from spokesperson / customer
- Specific numbers + dates + outlet names
- Original meaning and author's voice
- Technical terms required for accuracy

---

## Deepfake detection workflow

When suspicious media surfaces (potentially fabricated quote, doctored video, AI-cloned audio of exec):

1. **Don't amplify by responding immediately.** Confirm authenticity first.
2. **Truepic / Reality Defender / Sensity API check** — `cli-anything` curl with media URL
3. **C2PA Content Credentials check** — verify provenance metadata if present
4. **Reverse image search** for video frames (Google Lens / Yandex / TinEye)
5. **InVID forensics** for video splice detection (manual / academic)
6. **If confirmed fake**: legal coordination → takedown request to platform → public statement via newsroom (factual, not panicked) → log evidence
7. **If confirmed real**: this is a real crisis — execute crisis playbook
8. **If ambiguous**: hold position; don't amplify; continue verification

---

## Embargo break monitoring

During embargo window:
- **Brand24** alert on brand mention + story keyword
- **`firecrawl-mcp`** cron crawl of tier-1 outlets every 15 min
- **`brave-search`** query for headline keywords every 30 min
- **`twitter-mcp`** keyword stream for journalist Twitter accounts
- **Google Alerts** as triple-redundant safety net

If alert fires + content matches the embargoed story → embargo break protocol activates.

---

## AEO earned-media optimization

Every piece of earned coverage is a potential AI-search citation source. Optimize for extractability:

### Quote engineering

- **Named source + title + company** — AI models extract attributed claims
- **Specific number + date** — AI models prefer concrete over vague
- **Bold claim with caveat** — "X grew 40% in Q1" beats "X is growing fast"
- **Comparative framing** — "vs Y" pulls our brand into broader queries

### Outlet selection

AI search engines preferentially cite:
- Wikipedia entries
- Reddit threads (especially AMAs with substantive answers)
- News outlet primary-source articles
- Substack thought leadership with strong POV
- Podcast transcripts (especially well-known shows)

Prioritize pitch list toward outlets that show up in Profound / AthenaHQ citation responses for your category.

### Tracking

`notion-mcp` AEO citation tracker DB:
- Prompt (50-500 prompts in your category)
- Date
- AI engine (ChatGPT / Gemini / Claude / Perplexity / Brave)
- Citation? (yes / no)
- Outlet cited (if mention)
- Sentiment of citation (positive / neutral / negative)

Daily cron via Profound API → diff in citation share → weekly digest + alert on >20% drop.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Each entry links to a bundled `SKILL.md` (created in Round 2) or to a default skill / MCP already in scope.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Muck Rack media database + API

100M+ data points indexed; AI Media List Agent recommends journalist sets from a natural-language description; auto-alerts when a journalist on your list changes outlets. The default for US media list management. Cision / Roxhill / Meltwater are alts with different strengths (Cision = broadcast + print + podcast index; Roxhill = UK/EU; Meltwater = enterprise breadth).

- **Skill:** `skills/media-list-muck-rack-cision/SKILL.md` (Round 2)
- **Endpoint:** `https://api.muckrack.com/v1`
- **Auth:** API key → `MUCKRACK_API_KEY`
- **Key calls:** `search` (journalists by beat/outlet/keyword), `/journalists/{id}` (profile + recent articles), webhook subscribe (outlet-change alerts)
- **Source:** https://muckrack.com/pr-software/api

### PR Newswire + Business Wire + GlobeNewswire distribution

Three major US wire services. PR Newswire = broadest distribution (100+ industries). Business Wire = best targeting (200+ industries) + Reg-FD compliant. GlobeNewswire = mid-tier IR + general. All expose programmatic submission APIs included with subscription. Per-release distribution fees ($350-$3K) apply on top of subscription.

- **Skill:** `skills/press-release-writing-distribution/SKILL.md` (Round 2)
- **Endpoint:** wire-specific (PRN, BW, GNW each)
- **Auth:** subscription account + API key
- **Source:** https://signalgenesys.com/news-api-integration/

### Featured.com + Qwoted + Source of Sources (HARO replacements)

HARO (rebranded Connectively) shut down Dec 9, 2024 under Cision; Featured.com bought the brand from Cision in April 2025 and revived it as a free daily newsletter. Qwoted has the highest reported conversion rate among alternatives per 2026 backlinko data. Source of Sources = free, lower volume. #JournoRequest on X = free, real-time.

- **Skill:** `skills/haro-qwoted-featured-sme-quotes/SKILL.md` (Round 2)
- **Endpoint:** Featured.com daily email, Qwoted API, #JournoRequest via `twitter-mcp`
- **Auth:** free or paid tier per platform
- **Source:** https://www.qwoted.com/connectively-haro-is-going-away-heres-how-qwoted-can-help/ + https://backlinko.com/haro-alternatives

### Brand24 + Brandwatch + Meltwater monitoring

Brand24 ($249/mo) is the most cost-effective for SMB; Chatbeat AI dashboard is unique (only native AI visibility dashboard as of 2026). Brandwatch ($800-3K) covers 100M+ sources with deep sentiment + sarcasm. Meltwater (~$25K/yr median) covers 300K+ sources including broadcast + podcast + journalist DB.

- **Skill:** `skills/brand-reputation-monitoring-brandwatch-meltwater/SKILL.md` (Round 2)
- **Endpoint:** Brand24 API / Brandwatch API / Meltwater API
- **Auth:** per platform
- **Source:** https://brand24.com/blog/brand-monitoring-tools/

### AthenaHQ + Profound (AI search citation tracking)

5-min SLA on citation tracking across ChatGPT / Gemini / Claude / Perplexity. Profound has public API; AthenaHQ has dashboard. Brand24 Chatbeat = only native AI visibility dashboard. Otterly.ai = cheaper alt.

- **Endpoint:** `https://api.profound.com/v1/` + `https://api.athenahq.ai/v1/`
- **Auth:** API key per service
- **Source:** https://athenahq.ai/ + https://nicklafferty.com/blog/profound-vs-athena/

### PodPitch + Podchaser Pro + MatchMaker

PodPitch (3.85M podcast DB, daily refresh from Apple + Spotify, AI pitches citing host's recent episodes) is the default. Podchaser Pro = "IMDB of podcasts" with audience metrics. MatchMaker = guest-host match-making. PodPitch pricing $199-$299/mo per guest profile.

- **Skill:** `skills/podcast-tour-booking-for-execs/SKILL.md` (Round 2)
- **Endpoint:** PodPitch API + Podchaser API
- **Auth:** per platform
- **Source:** https://podpitch.com/

### LinkedIn Marketing API + Newsletters endpoint

LinkedIn's `/rest/articles` endpoint publishes newsletter articles. Requires Community Management product approval (5-15 day review). Pair with Substack API for cross-publication.

- **Skill:** `skills/executive-thought-leadership-linkedin-substack/SKILL.md` (Round 2)
- **Endpoint:** `https://api.linkedin.com/rest/articles`
- **Auth:** OAuth 3-legged → `LINKEDIN_ACCESS_TOKEN`
- **Source:** https://learn.microsoft.com/en-us/linkedin/marketing/

### Substack + Beehiiv API

Substack API allows POST `/p/{slug}` for cross-publication; Beehiiv is the API-first alt with better analytics + monetization but separate from LinkedIn ecosystem. 2026 best practice: LinkedIn for top-of-funnel reach; Substack/Beehiiv for owned email + monetization.

- **Source:** https://substack.com/api + https://www.beehiiv.com/

### Smartlead + Lemlist (cold outreach infra)

Used ONLY for cold journalist outreach when volume requires warmup infrastructure. Smartlead = inbox rotation + deliverability throttling. Lemlist = creative personalization (custom images / landing pages). 2026 journalists detect generic AI personalization in sentence 1 — these tools are infrastructure, not a quality substitute. Subject <49 chars + pitch <150 words + cite specific recent article remain non-negotiable.

- **Source:** https://www.smartlead.ai/blog/ai-cold-email-outreach-tools

### Inc 5000 / Forbes 30 Under 30 / Fast Company MIC + others

No public APIs for submission; `playwright-mcp` automates form fill from Notion criteria DB. Verify eligibility BEFORE drafting. Application tailored per award's stated criteria. Quarterly `firecrawl-mcp` scan of award index sites for new deadlines + category additions.

- **Skill:** `skills/award-list-submissions-inc-forbes-fast-co/SKILL.md` (Round 2)
- **Source:** https://www.inc.com/inc5000/apply + https://en.wikipedia.org/wiki/Forbes_30_Under_30

### Sessionize + Papercall.io + Pretalx (CFP discovery)

Aggregate open CFPs. Sessionize has structured exports. Papercall has API for some events. Pretalx is open-source. Most direct event CFPs use bespoke web forms → `playwright-mcp` submission.

- **Skill:** `skills/conference-speaking-submission/SKILL.md` (Round 2)
- **Source:** https://sessionize.com/ + https://www.papercall.io/

### Gartner / Forrester / IDC briefing + Magic Quadrant

Vendor briefings are FREE (per Gartner methodology). Magic Quadrant inclusion criteria publicly stated; no pay-for-placement. Process: identify analyst by coverage area → request briefing via vendor portal → 30-min briefing → MQ/Wave survey (often 100+ questions) → customer reference interviews → publication.

- **Skill:** `skills/analyst-relations-gartner-forrester-idc/SKILL.md` (Round 2)
- **Source:** https://spotlightar.com/blog/gartner-magic-quadrant-steps/

### Truepic + Reality Defender + Sensity (deepfake detection)

Used in crisis comms when suspicious media surfaces (potentially fabricated quote, doctored video, AI-cloned audio). API check via `cli-anything` curl. Pair with C2PA Content Credentials verification on incoming media.

- **Source:** https://www.thegutenberg.com/blog/crisis-comms-3-0-ai-crisis-communication-strategies-for-navigating-misinformation/

### Vale linter (brand voice + AI-slop lint)

Same Vale linter used by `marketing-agent`. Custom YAML rules in `styles/PR/APStyle.yml` + `styles/Brand/AISlop.yml` enforce AP style, banned buzzwords, AI-slop catch list, em-dash overuse, passive voice chains. Run before every release / pitch / op-ed publish.

- **Endpoint:** `uvx vale --config=.vale.ini --output=JSON content/release.md`
- **Source:** https://vale.sh/

### `playwright-mcp` (web form automation)

For platforms without APIs: awards submissions, CFP submissions, HN posts, Glassdoor responses, Trustpilot responses where no API access. Notion criteria DB → `playwright-mcp` script reads fields → submits → screenshots confirmation.

- **Endpoint:** `playwright-mcp` MCP server (in agent.yaml)

### `gmail-mcp` (journalist 1:1 outreach)

Default for journalist outreach + HARO/Featured responses + embargo distribution (per-journalist, NEVER BCC) + weekly client digest. Smartlead/Lemlist used ONLY when volume requires warmup infra.

- **MCP:** `gmail-mcp` (in agent.yaml)

### `notion-mcp` (media-list CRM, journalist log, criteria DB)

The default editorial calendar + media-list CRM + journalist relationship log + award criteria DB + customer reference DB + crisis playbook + AEO citation tracker + outlet-tier rubric + speaking calendar.

- **MCP:** `notion-mcp` (in agent.yaml)

### `firecrawl-mcp` + `brave-search` (free monitoring fallback)

When recipient doesn't have Brand24/Brandwatch/Meltwater budget: `brave-search` query `"brand" -site:brand.com` daily + `reddit-mcp` subreddit watch + `twitter-mcp` keyword stream + `firecrawl-mcp` outlet crawl. Stitch via Notion. Day-1 functional without paid keys.

- **MCPs:** `firecrawl-mcp`, `brave-search` (in agent.yaml)

### `reddit-mcp` + `discord-mcp-full` (community + dark social)

`reddit-mcp` for AMA scheduling + subreddit monitoring + mod outreach. `discord-mcp-full` for dark-social monitoring on permitted servers. Cron daily monitoring; Claude classifies; Notion log; weekly digest.

- **MCPs:** `reddit-mcp`, `discord-mcp-full` (in agent.yaml)

### `twitter-mcp` (real-time + monitoring)

#JournoRequest stream, real-time POV threads for thought leadership, brand mention monitoring, crisis comms thread distribution. Pair with brand mention alerts during embargo windows.

- **MCP:** `twitter-mcp` (in agent.yaml)

### `youtube-mcp-transcript` (podcast research + post-event)

Pull transcripts of host's last 3 podcast episodes for pitch research. Post-event: transcript pull for repurposing into LinkedIn / Substack / X thread / blog.

- **MCP:** `youtube-mcp-transcript` (in agent.yaml)

### `mcp-tts` + `elevenlabs-mcp` (spokesperson rehearsal audio)

Generate audio of spokesperson's recommended answers for them to listen to during prep. ElevenLabs for higher-quality voice when needed (executive demo reels, audio one-pagers).

- **MCPs:** `mcp-tts`, `elevenlabs-mcp` (in agent.yaml)

### `deepl-mcp` (multi-language press releases)

Source EN → translate per target language → distribute per-region wire (or self-distribute). Per-language press release template stored in Notion; router by region.

- **MCP:** `deepl-mcp` (in agent.yaml)

### `imagegen-mcp` + `canva-mcp` + `stability-ai-mcp` + `figma-mcp` (press kit design)

`canva-mcp` for branded press kit templates. `figma-mcp` for brand-system asset export. `imagegen-mcp` + `stability-ai-mcp` for AI image gen (press release imagery, social cards, AMA hero images).

- **MCPs:** `imagegen-mcp`, `canva-mcp`, `stability-ai-mcp`, `figma-mcp` (in agent.yaml)

### `sec-edgar-mcp` (competitor disclosures for predictive crisis)

Pull competitor 8-K disclosures + earnings calls for predictive crisis monitoring + M&A PR research + industry context for analyst briefings.

- **MCP:** `sec-edgar-mcp` (in agent.yaml)

### `posthog-mcp` (PR landing page + AEO referrer tracking)

Track press release landing page conversion + AEO referrer traffic (which AI search engines referred users post-citation).

- **MCP:** `posthog-mcp` (in agent.yaml)

### `huggingface-mcp` (local sentiment + topic clustering)

When paid sentiment APIs (Brand24/Brandwatch) aren't available: local sentiment classification + topic clustering on coverage corpus via HF transformer models.

- **MCP:** `huggingface-mcp` (in agent.yaml)

### `gemini-ocr-mcp` + `mistral-ocr-mcp` (scanned clippings)

OCR scanned print clippings or legacy media coverage. Convert to searchable text for Notion log + sentiment analysis.

- **MCPs:** `gemini-ocr-mcp`, `mistral-ocr-mcp` (in agent.yaml)

### `slack-mcp` + `ms-teams-mcp` + `zoom-mcp` (internal coordination)

Crisis comms internal alerts via Slack/Teams. Recorded analyst briefings + spokesperson prep sessions via Zoom (transcript for prep doc generation).

- **MCPs:** `slack-mcp`, `ms-teams-mcp`, `zoom-mcp` (in agent.yaml)

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Write a press release | `press-release-writing-distribution` | AP/PRSA format + Vale lint + wire or self-distribute |
| Distribute via wire | `press-release-writing-distribution` | PR Newswire / Business Wire / GlobeNewswire API |
| Build a media list | `media-list-muck-rack-cision` | Muck Rack default; free fallback via `brave-search` + Featured |
| Cold pitch journalist | `journalist-outreach-cold-warm-embargoed` | Subject <49 / pitch <150 / cite specific article |
| Embargoed launch | `embargoed-product-launches` | NEVER BCC; embargo break monitoring |
| HARO / Featured / Qwoted response | `haro-qwoted-featured-sme-quotes` | 4-hour relevance window |
| Prep spokesperson | `media-training-spokesperson-prep` | Outlet research + likely-question gen + `mcp-tts` drill |
| Crisis statement | `crisis-comms-24-48-72-hour-playbook` | Truth-first + per-stakeholder + contact tree |
| LinkedIn newsletter / Substack | `executive-thought-leadership-linkedin-substack` | LinkedIn API + Substack cross-post + Vale lint |
| Op-ed pitch + draft | `op-ed-contributed-article-placement` | Outlet-specific norms + draft-to-spec |
| Real-time X commentary | (Direct via `twitter-mcp` + Claude POV) | Industry-feed monitoring + thread structure |
| Award submission | `award-list-submissions-inc-forbes-fast-co` | Eligibility check + `playwright-mcp` form fill |
| Podcast booking | `podcast-tour-booking-for-execs` | PodPitch + episode-cited pitches |
| Conference talk | `conference-speaking-submission` | Sessionize / Papercall + abstract draft |
| Brand mention monitoring | `brand-reputation-monitoring-brandwatch-meltwater` | Paid stack + free `brave-search`/`reddit-mcp`/`twitter-mcp` fallback |
| Review responses (Trustpilot/G2) | `online-reputation-mgmt-review-responses` | Empathy + specific resolution |
| AEO / GEO citation tracking | (Direct via Profound/AthenaHQ + `notion-mcp`) | Track 50-500 prompts daily |
| Analyst briefing | `analyst-relations-gartner-forrester-idc` | FREE briefing + `pptx` deck |
| Magic Quadrant submission | `analyst-relations-gartner-forrester-idc` | Vendor survey + customer references |
| Reddit AMA | `reddit-hn-ama-show-and-tell` | Mod outreach + verification + 24-hr followup |
| Show HN launch | `reddit-hn-ama-show-and-tell` | `playwright-mcp` submit + comment monitoring |
| Dark social tracking | `dark-social-tracking` | Discord + private community |
| Share of voice + EMV | `pr-campaign-measurement-share-of-voice` | Outlet-tier rubric + EMV formula |
| Customer reference for press | `customer-reference-program-pr` | Notion DB + tag-match by journalist beat |

---

## Brief / output templates

### Crisis comm brief template

```markdown
# Crisis Brief: [Incident Title]

## Truth-first facts
- What happened (confirmed): 
- What we're investigating: 
- What we can't say (legal/privacy): 

## Stakeholders
| Stakeholder | Channel | Timing | Detail level | Owner |
|---|---|---|---|---|
| Customers | | | | |
| Employees | | | | |
| Press | | | | |
| Regulators | | | | |
| Investors | | | (defer to investor-relations) | |
| Public | | | | |

## Holding statement (T+0)
[Template from playbook]

## Spokesperson + Q&A
- Spokesperson: [Name + Title]
- Backup: [Name + Title]
- Q&A doc: [link]

## Contact tree
[Per crisis-comms playbook]

## Monitoring
- Brand24 / Brandwatch keywords: 
- Sentiment baseline: 
- Volume baseline: 
- Alert thresholds: 

## Hand-offs
- Exec voice: defer to `ceo-agent`
- Customer-facing outage comms: defer to `customer-support-agent`
- SEC 8-K / Reg-FD: defer to `investor-relations`

## Next update
- Time: 
- Channel: 
- Drafter: 
```

### Pitch tracking template

```
| Date | Journalist | Outlet | Beat | Story angle | Pitch type | Subject | Sent | Response | Outcome | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
```

### Coverage tracking template

```
| Date | Outlet | Tier | Headline | URL | UVM | Sentiment | Quote? | EMV | Notes |
|---|---|---|---|---|---|---|---|---|---|
```

---

## Closing rules

Build the relationship before you need it. Confirm attribution before substance. Truth first in crisis. Hand off when the ask isn't yours.
