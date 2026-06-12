<!--
Source: HockeyStack PLG flips traditional GTM + digitalapplied PLG vs sales-led 2026 + Brian Balfour 4-Fits
-->
# PLG vs Sales-Led Motion Decision SKILL

> Decide PLG vs sales-led vs hybrid via ACV / aha-time / buyer-count matrix + Brian Balfour's 4-Fits. PLG grows 50% faster on 39% less spend BUT 85% of forced transitions fail. The wrong motion = 18+ months of wasted effort.

## When to use

Trigger phrases:
- "PLG or sales-led?"
- "Should we add a sales team?"
- "Add self-serve to enterprise product"
- "Transition from sales-led to PLG"
- "Pricing tier strategy + motion"
- "When to hire AEs"

Pair: `growth-loop-design-5-types` (different loops fit different motions), `pql-product-qualified-leads-framework` (hybrid bridge), `growth-model-spreadsheet-compound-levers` (model both), `north-star-omtm-pirate-metrics-heart` (NSM differs).

## Setup

```bash
# No tools required; this is a decision framework + discovery
export NOTION_TOKEN="ntn_..."   # output the decision doc
```

## Motion fundamentals

| Motion | What it means | Buyer experience | Cost structure |
|---|---|---|---|
| **PLG (Product-Led)** | Product is the buyer journey; sales-assist only | Try → Use → Pay (self-serve) | Low CAC + product engineering |
| **Sales-led** | Sales drives discovery, demo, deal | Demo → POC → Negotiate → Close | High CAC + sales team payroll |
| **Hybrid** | PLG for SMB + sales for enterprise tier | Self-serve below threshold + AE above | Mixed; PQL handoff |

## Decision matrix (canonical 6-factor)

| Factor | PLG | Sales-led | Hybrid |
|---|---|---|---|
| **ACV** | < $5K/yr | > $25K/yr | $5-25K/yr |
| **Buyer count** | 1-3 | 5+ stakeholders | 2-5 |
| **Setup complexity** | Self-serve in 1h | Implementation services 1-12 weeks | Mixed |
| **Time-to-aha** | < 1 hour | Days/weeks | Hours |
| **Distribution** | Mass-market | Targeted ICP | Mid-market |
| **Network effects** | Strong | Weak | Mixed |

If 4+ factors point to PLG → PLG. If 4+ point to sales-led → sales-led. Otherwise hybrid.

## Common recipes

### Recipe 1: Discovery Q&A (collect facts)

```text
Q1. Average annual contract value (ACV)?
   < $5K / $5K-25K / > $25K

Q2. How many people are involved in the buying decision?
   1 / 2-3 / 4-5 / 6+

Q3. How long is the typical setup / onboarding?
   < 1 hour self-serve / hours / days / weeks

Q4. Time from signup to first value moment (aha)?
   < 5 min / < 1 hour / hours / days

Q5. Target market shape?
   Wide consumer / SMB many / Mid-market / Enterprise few

Q6. Network effects in product?
   Strong / Weak / None

Q7. Current motion (if any)?
   PLG / Sales-led / Hybrid / None

Q8. CAC / LTV today?
   CAC = $___, LTV = $___, ratio = ___

Q9. Sales team size?
   0 / 1-3 AEs / 4-10 AEs / 10+ AEs
```

### Recipe 2: Score the matrix

```python
def score_motion(answers):
    plg_score = 0
    sales_score = 0
    
    # ACV
    if answers['acv'] < 5000: plg_score += 1
    elif answers['acv'] > 25000: sales_score += 1
    else: plg_score += 0.5; sales_score += 0.5
    
    # Buyer count
    if answers['buyers'] <= 3: plg_score += 1
    elif answers['buyers'] >= 5: sales_score += 1
    else: plg_score += 0.5; sales_score += 0.5
    
    # Setup
    if answers['setup'] == 'self_serve_1h': plg_score += 1
    elif answers['setup'] in ('days','weeks'): sales_score += 1
    else: plg_score += 0.5; sales_score += 0.5
    
    # TTV
    if answers['ttv'] in ('<5min','<1h'): plg_score += 1
    elif answers['ttv'] in ('days',): sales_score += 1
    
    # Network effects
    if answers['network'] == 'strong': plg_score += 1
    elif answers['network'] == 'none': sales_score += 0.5
    
    if plg_score >= sales_score + 2: return "PLG"
    if sales_score >= plg_score + 2: return "Sales-led"
    return "Hybrid"
```

### Recipe 3: 4-Fits validation (Brian Balfour)

```text
4 Fits — all must align for motion to work.

1. Market ↔ Product
   Does product solve market's problem?
   Test: ≥ 40% "very disappointed" Sean Ellis = strong fit

2. Product ↔ Channel
   PLG needs self-serve-friendly channels (SEO, content, organic).
   Sales-led needs targeted channels (account-based, outbound).
   Mismatch: product-led on outbound channels = brutal economics.

3. Channel ↔ Model
   CAC of channel × LTV multiplier must work.
   PLG model = low CAC, low ACV, mass volume.
   Sales-led model = high CAC, high ACV, low volume.

4. Model ↔ Market
   Pricing / packaging fits market's willingness-to-pay.
   PLG model in $50K+ ACV market = leaving money on table.
   Sales-led model in <$5K ACV market = unprofitable.

85% of forced transitions fail because one of these 4 fits is broken.
```

### Recipe 4: Hybrid motion pattern (most common 2026)

```text
Tier 1 (Free / Starter): PLG path
  - Self-serve signup → activation → free use
  - In-app upgrade prompts at usage limits
  - No sales involvement
  
Tier 2 (Pro / Team, $50-500/mo): PLG + sales-assist
  - Self-serve signup → activation
  - PQL signals (team-size, premium-feature) trigger AE outreach
  - AE helps champion-driven team growth
  
Tier 3 (Enterprise, $5K+/mo): Sales-led
  - Outbound + inbound sales-driven
  - Demo + POC + procurement
  - Custom contract, sometimes via product-led trial
  
Bridge: PQL handoff (see pql-product-qualified-leads-framework skill)
```

### Recipe 5: PLG signals to watch (your product fits PLG)

```text
✓ Active free / trial user count rising organically
✓ Activation rate > 40%
✓ Day 30 retention > 25%
✓ Organic search > 30% of new signups
✓ Net Promoter Score > 30
✓ Users sharing product without prompting
✓ Limit-approached events firing in product
```

### Recipe 6: Sales-led signals to watch (your product needs sales)

```text
✓ Buyers ≠ users (procurement, finance, security involvement)
✓ Implementation services revenue > 10% of total
✓ Average sales cycle > 60 days
✓ ACV > $25K
✓ Custom contracts, MSA negotiation
✓ Win-loss heavily influenced by relationship
✓ Compliance / security review required (SOC2, HIPAA)
```

### Recipe 7: Transition pitfalls

```text
PLG → Sales-led (because we need bigger deals)
  Risk: 85% failure rate. Common causes:
    - Compensation conflict (AEs taking credit for self-serve revenue)
    - Channel mismatch (sales-team good at outbound; product good at inbound)
    - Pricing collision (sales discount cuts self-serve revenue)
    - Cultural drag (eng team optimized for product; not sales-process)
  
Sales-led → PLG (because PLG grows faster)
  Risk: similar 70%+ failure. Common causes:
    - Product not actually self-serve (requires services)
    - Brand built on relationship; users don't trust self-serve
    - Pricing too expensive for PLG; conversion too low
    - Existing sales team threatened, sabotages PLG
```

### Recipe 8: Phased transition plan (if pivoting)

```text
Phase 1 (months 1-3): instrument, don't change
  - Add product analytics (PostHog / Amplitude)
  - Track signup, activation, PQL signals
  - Measure baseline

Phase 2 (months 4-6): self-serve pilot
  - Enable self-serve signup for new logos
  - Existing sales pipeline untouched
  - Measure self-serve LTV vs sales-led LTV

Phase 3 (months 7-12): PQL handoff
  - Self-serve users hitting PQL signals → AE handoff
  - AE compensation includes PLG-sourced deals
  - Build the bridge skill (PQL framework)

Phase 4 (months 13+): scale or revert
  - If self-serve revenue > 30% of new ARR → scale
  - If < 15% after 12 months → revert, accept sales-led
```

### Recipe 9: Counterargument check

```text
Before recommending PLG:
  ☐ Is your aha < 1 hour? (no = PLG won't fit)
  ☐ Is your ACV sustainable at PLG conversion rates? (5% trial-to-paid × ACV > CAC?)
  ☐ Does your product have natural virality / shareable artifacts?
  ☐ Can a single user get value without team buy-in?
  
Before recommending sales-led:
  ☐ Is your ACV worth the AE cost? (AE fully-loaded $200K+ → needs $1.2M+ ARR each)
  ☐ Are you targeting < 1000 logos? (mass-market PLG-fits better)
  ☐ Do buyers need relationship to commit? (some markets yes, others no)
```

### Recipe 10: Industry benchmarks (June 2026)

| Industry | Typical motion | Why |
|---|---|---|
| Productivity SaaS (Notion, Linear, Slack) | PLG-first | Multi-player + viral + sub-$25 ACV / user |
| Developer tools (GitHub, Vercel) | PLG-first | Individual buyer + try-before-buy + technical |
| Marketing tools (HubSpot starter) | Hybrid | Multi-tier; PLG for SMB, sales for enterprise |
| Enterprise CRM (Salesforce) | Sales-led | High ACV + multi-stakeholder + customization |
| Vertical SaaS (Toast restaurants) | Sales-led | Industry-specific, services-heavy |
| Fintech B2B | Hybrid | Compliance gates sales-led; usage-based suggests PLG |
| Mobile consumer | PLG | App store + viral; sales-led doesn't scale |
| DTC e-com | n/a (transactional) | Acquisition-loop based |

### Recipe 11: Output decision doc

```markdown
# Motion Decision — Acme Corp

## Discovery
- ACV: $8,400/yr (mid)
- Buyers: 3-4 (mid)
- Setup: 2 hours self-serve
- TTV: 30 min (PLG-friendly)
- Market: Mid-market B2B (1000-2000 logos TAM)
- Network: Weak

## Score
PLG: 4.5 | Sales-led: 2.5 → **Hybrid recommended**

## 4-Fits check
1. Market ↔ Product ✓ (Sean Ellis 44% very disappointed)
2. Product ↔ Channel ✓ (organic SEO + content driving signups)
3. Channel ↔ Model ✓ (CAC $400, LTV $3K — 7.5x)
4. Model ↔ Market ✓ ($8K ACV reasonable)

## Recommendation
**Hybrid:** PLG for Tier 1 + Tier 2 (sub-$500/mo); sales-assist for Tier 3 ($500-2K/mo); sales-led for Enterprise.

## Implementation plan
1. PQL framework (see pql-product-qualified-leads-framework skill)
2. Free-to-paid prompts (see free-to-paid-upgrade-prompts skill)
3. AE compensation includes PLG-sourced deals
4. Q4 review: measure self-serve vs sales-led NRR + LTV; adjust split

## Risks
- 85% of forced transitions fail. Build the bridge carefully.
- Sales team risk: AEs may not adapt; compensation must reward PLG-sourced.
- Pricing collision: don't discount via AE if PLG users see higher price.
```

## Examples

### Example 1: SaaS startup, $4K ACV, single-user buyer

Score: PLG 6, Sales-led 1 → strong PLG.
4-Fits ✓ all aligned.
Recommendation: PLG. No sales team needed yet. AE later only for $25K+ Enterprise tier.

### Example 2: B2B platform, $80K ACV, 6 stakeholders, 8-week implementation

Score: PLG 1, Sales-led 7 → strong sales-led.
4-Fits: ✓ all aligned.
Recommendation: Sales-led. Build out AE team. PLG would not fit.

### Example 3: Mid-market SaaS, $12K ACV, 3 buyers, 4-hour setup

Score: PLG 3.5, Sales-led 3.5 → Hybrid.
Recommendation: PLG for SMB tier ($50-500/mo) + sales-assist for Pro/Team ($500-2K/mo) + sales-led for Enterprise ($2K+/mo).

## Edge cases / gotchas

- **Forcing PLG when product needs services** — onboarding requires CSM hand-holding → PLG fails; users don't get to value.
- **Forcing sales-led when product is too cheap** — AE economics break at $5K ACV (need 30+ deals/yr per rep).
- **Pricing strategy contradicts motion** — PLG pricing should be transparent + self-serve; sales-led can be opaque + custom.
- **Sales-team compensation conflict** — AEs not credited for self-serve user upgrades will sabotage PLG.
- **"We need both" without bridge** — hybrid without PQL handoff = chaos. Build the bridge (see PQL skill).
- **Cultural mismatch** — engineering-heavy team forcing sales-led often fails (org culture doesn't fit).
- **Channel-motion mismatch** — top-of-funnel from outbound calls feeding PLG self-serve = expensive top, lousy bottom.
- **Tier-collapse risk** — adding new tier above current top inflates expectations; existing customers feel demoted.
- **Geographic mismatch** — PLG works globally with limited touch; sales-led requires local team.
- **Regulated industries** — healthcare, finance often require sales-led even at low ACV (compliance gates).
- **Pre-PMF motion decisions** — don't pick a motion before PMF; let users tell you.
- **Founder-led sales transition** — founder-sold → AE-sold often loses 30-50% conversion in transition; plan ramp.

## Sources

- HockeyStack — PLG flips traditional GTM: https://www.hockeystack.com/blog-posts/product-led-growth-flips-the-traditional-gtm-playbook
- DigitalApplied — PLG vs sales-led 2026: https://www.digitalapplied.com/blog/plg-vs-sales-led-gtm-motion-2026-saas-decision-framework
- Brian Balfour — 4 Fits: https://brianbalfour.com/four-fits-growth-framework
- Sean Ellis — PMF test: https://www.startup-marketing.com/the-startup-pyramid/
- OpenView — PLG report: https://openviewpartners.com/product-led-growth/
- ProductLed.org: https://www.productled.org/
- Pocus — PQL guide: https://www.pocus.com/blog/the-definitive-pql-guide-part-1
- Lenny's PLG Handbook: https://plghandbook.com/
- Patrick Campbell — SaaS pricing motion: https://www.priceintelligently.com/
