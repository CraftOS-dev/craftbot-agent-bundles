---
name: transcreation-cultural-adaptation
description: Transcreation (creative adaptation) for marketing copy, taglines, CTAs. Brief format + persona + in-market reviewer + Lilt/Smartcat dispatch. Use when the user asks "transcreate", "adapt our slogan", "localize marketing copy", or wants brand voice in a new market.
---

# Transcreation & Cultural Adaptation

Transcreation > translation for headlines, taglines, CTAs, brand voice. A literal translation of "Think Different" or "Just Do It" reads flat or absurd in target markets. Transcreation gives the brief writer creative latitude — idioms encouraged, cultural references swapped, structure rewritten — but locked to brand voice.

Defer the final creative call to `marketing-agent` + in-market reviewer.

## When to use

- Marketing copy: hero text, taglines, CTAs, ad headlines, landing pages.
- Product naming for a new market.
- Email subject lines + preheaders (regional open-rate differences).
- Brand voice + tone for a new locale.
- A/B test variants for in-market reviewers.

Trigger phrases: "transcreate", "transcreation", "localize tagline", "marketing copy in [locale]", "brand voice in [market]", "adapt slogan", "cultural adaptation".

## Setup

```bash
# Smartcat marketplace (transcreation vendor + translator dispatch)
# Sign up: https://www.smartcat.com/ — get API key

# Lilt (adaptive MT + transcreation workflow)
# Enterprise contract required: https://lilt.com/

# Crowdin transcreation workflow (marketplace integrated)
npm i -g @crowdin/cli

# Phrase transcreation via Phrase TMS LSP connector
npm i -g @phrase/cli
```

Auth/env:
- `SMARTCAT_API_KEY` — from `https://www.smartcat.com/api`
- `LILT_API_KEY` — enterprise contract
- TMS tokens as per `tms-setup-crowdin-lokalise-phrase`

## The transcreation brief (template)

Every transcreation request must include:

1. **Source string + context** — the original copy + where it appears (homepage hero, email subject, ad headline).
2. **Brand voice** — adjectives (friendly, authoritative, playful, formal). Reference 5-10 brand-approved examples in target locale.
3. **Target persona** — buyer/user persona in target market (age, income, profession, pain point, motivation).
4. **Cultural don'ts** — taboos, sensitive imagery, off-limit references (politics, religion, humor styles, local-event collisions).
5. **Constraints** — character/word budget, must-have keywords (SEO), must-avoid trademarks.
6. **Reference assets** — 5+ brand-approved transcreated examples in target locale.
7. **Acceptance criteria** — what "good" looks like; A/B test plan if any.

## Common recipes

### Recipe 1: Transcreation brief format

```markdown
# Transcreation Brief: <campaign name>

## Source
**EN copy:** "Save time. Save money. Save everything."
**Context:** Hero tagline, homepage above-the-fold.
**Word count:** 8 words. **Character count:** 38.

## Target locales
- de-DE (priority)
- fr-FR
- ja-JP

## Brand voice
- Adjectives: confident, warm, slightly playful
- Avoid: corporate jargon, hype words ("revolutionary"), fake urgency
- Tone reference: see https://brand.example.com/voice/de

## Target persona (de-DE)
- Title: SaaS product manager, 28-45
- Pain: drowning in tabs, fragmented workflows
- Motivation: reclaim focus + sanity
- Cultural fit: Germans value directness + competence > playfulness

## Cultural don'ts
- No World Cup / Oktoberfest references (overdone)
- No English idioms transliterated ("save the day" → don't translate literally)
- Politically neutral; no East/West Germany allusions

## Constraints
- Max 12 words per locale
- Must contain product category keyword: "Produktivität" (DE), "productivité" (FR), "生産性" (JA)

## References (de-DE approved tone)
1. "Fokus. Effizienz. Endlich." (previous campaign)
2. "Weniger Lärm. Mehr Arbeit." (previous campaign)

## Acceptance
- 3 variants per locale from transcreator
- In-market reviewer ranks; preferred + 1 challenger ship for A/B test
```

### Recipe 2: Dispatch to Smartcat marketplace

```bash
# Create transcreation project
curl -X POST 'https://smartcat.com/api/integration/v2/project' \
  -H "Authorization: Basic $SMARTCAT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "homepage-tagline-Q3",
    "description": "Transcreate homepage tagline into DE/FR/JA",
    "deadline": "2026-07-15",
    "sourceLanguage": "en",
    "targetLanguages": ["de", "fr", "ja"],
    "workflowStages": ["translation", "editing", "in-market-review"]
  }'

# Upload brief + reference file
curl -X POST 'https://smartcat.com/api/integration/v2/project/{projectId}/document' \
  -H "Authorization: Basic $SMARTCAT_API_KEY" \
  -F 'file=@brief.docx'
```

### Recipe 3: Lilt transcreation API

```bash
curl -X POST 'https://api.lilt.com/v2/translate' \
  -H "Authorization: Basic $(echo -n :$LILT_API_KEY | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "Save time. Save money. Save everything.",
    "memory_id": "<brand-voice-memory-id>",
    "source_lang": "en",
    "target_lang": "de",
    "style_guide_id": "<de-tone-style-guide-id>",
    "request_creative": true
  }'
```

Lilt returns multiple variants ranked; human reviewer (in-house) picks final.

### Recipe 4: A/B test variant rollout

```ts
// pages/_app.tsx — Optimizely / split.io / LaunchDarkly per-locale variant
import { useExperiment } from '@optimizely/react-sdk';

const heroVariant = useExperiment(`hero-tagline-${locale}`, {
  variants: ['variant-a', 'variant-b'],
});

const taglines = {
  de: {
    'variant-a': 'Fokus. Effizienz. Endlich.',
    'variant-b': 'Weniger Lärm. Mehr Arbeit.',
  },
  // ...
};
```

Measure: CTR on hero CTA, scroll depth, conversion rate. Promote winner after 14 days at p<0.05.

### Recipe 5: In-market reviewer panel

Recruit 3-5 in-market reviewers per locale:
- Native speakers, full-time residents.
- Match persona (PM 28-45 for our hero example).
- 1-hour async review per variant set.
- Output: ranked preference + rationale.

Distribute via Notion form, Google Forms, or via Smartcat's in-market review workflow.

### Recipe 6: Brand voice tone matrix

```markdown
| Tone dimension | EN baseline | DE | FR | JA | AR |
|---|---|---|---|---|---|
| Formality | informal | formal-neutral | informal-warm | formal | formal |
| Directness | direct | very direct | indirect-elegant | indirect-respectful | indirect-respectful |
| Humor | light | dry | witty | restrained | restrained |
| Address | "you" | "Sie" or "du" (pick per persona) | "vous" or "tu" | です/ます form | formal pronouns |
| Sentence length | short | medium | long | medium | medium |
```

### Recipe 7: Forbidden terms list per locale

```yaml
# forbidden-terms.yml
de-DE:
  - "Lösung"        # overused jargon
  - "innovativ"     # hype word
  - "revolutionär"  # hype word
fr-FR:
  - "incroyable"    # over-promised
  - "génial"        # too casual for brand
ja-JP:
  - "革命的"         # hype
  - "凄い"           # too casual
```

### Recipe 8: Crowdin transcreation workflow

```bash
# Tag a string as transcreation (not translation)
crowdin string update --id <STR_ID> --label "transcreation,marketing"

# Filter view in Crowdin for transcreation strings only
# UI: Source → Filter: Label = transcreation
```

### Recipe 9: Backtranslation gate

For high-stakes copy (legal disclaimer in marketing, slogans):
```
1. Transcreator writes DE variant
2. Independent translator back-translates DE → EN literally
3. Compare to source intent
4. Discrepancies highlighted for reviewer
```

Backtranslation is required for some regulated industries (pharma, finance).

### Recipe 10: Cost projection

```
Translation rate (EN→DE):   $0.10-0.18 / word
Transcreation rate:         $0.40-1.20 / source word OR $150-500 / hour
A/B test variants:          3× the per-locale cost (3 variants)
In-market review:           $300-800 per locale per round
```

Budget signal: transcreation costs 3-10× translation. Reserve for high-leverage copy only.

### Recipe 11: Style guide handoff

```markdown
# Brand Style Guide — DE

## Voice
[3-5 paragraphs in DE describing voice]

## Glossary
- product → Produkt (singular), Produkte (plural)
- dashboard → Übersicht (NOT Dashboard — too anglicism)
- AI → KI (in marketing); AI (in technical docs)

## Tone examples
[5-10 approved DE strings showing voice in action]

## Don't
- Don't use "wir" excessively
- Don't say "kostenlos" — say "ohne Kosten"
- Don't use ! in body copy (only in CTAs)
```

Attach to every transcreation brief.

### Recipe 12: Per-locale tone calibration via reference

Build a "canonical examples" file per locale that transcreators must match:
```
canonical/de-DE-tone.md:
- 10 best-of brand copies in DE
- 5 examples of what's wrong in DE
- Top-3 don'ts
```

## Examples

### Example 1: Transcreate a homepage tagline into DE / FR / JA

**Goal:** Adapt "Save time. Save money. Save everything." for three markets.

**Steps:**
1. Write brief (Recipe 1) — include persona, brand voice, references.
2. Dispatch via Smartcat (Recipe 2) with workflow `translation → editing → in-market-review`.
3. Receive 3 variants per locale from transcreator.
4. In-market reviewer ranks (Recipe 5).
5. Top 2 per locale enter A/B test (Recipe 4).
6. Measure CTR over 14 days; promote winner.
7. Add winners to TM for future consistency.

**Result (illustrative):**
- DE: "Mehr Zeit. Mehr Geld. Mehr Fokus." (winner) vs "Zeit gespart. Geld gespart. Alles gespart." (challenger)
- FR: "Gagnez du temps. Gagnez de l'argent. Gagnez tout." vs "Le temps, c'est de l'argent. Tout en un."
- JA: "時間を、お金を、すべてを取り戻す。" vs "時間、コスト、すべてを節約。"

### Example 2: Email subject line localization

**Goal:** Adapt "You're missing out — 20% off ends tonight" subject line for 5 locales.

**Steps:**
1. Identify locale-specific subject-line norms:
   - JA: shorter (15-20 chars), softer urgency
   - DE: longer OK (40-60 chars), direct
   - AR: poetic OK, religious holidays avoided
   - PT-BR: emoji acceptable, exclamation marks fine
   - FR: subtle urgency preferred over hype
2. Transcreate with persona awareness (Recipe 1).
3. A/B test (Recipe 4) — measure open rate, not CTR.
4. Track preheader transcreation alongside subject.

**Result:** Localized subjects outperform translated subjects by 8-15% open rate (typical).

## Edge cases / gotchas

- **Transcreation rate is unbounded** — top-tier creative transcreators charge $1-2/source word + $500/hour for revision. Set budget caps upfront.
- **Legal copy is NOT transcreation territory** — Terms of Service, Privacy Policy, disclaimers need legal-aware translation, not creative adaptation.
- **A/B test stat sig at low traffic** — homepage variants need 10k+ visits per variant per locale for p<0.05. Small markets may take months.
- **Brand voice drift** — without canonical examples (Recipe 12), each transcreator interprets differently. Score against voice rubric every batch.
- **In-market reviewer bias** — single reviewer = single opinion. Need 3+ reviewers; track inter-reviewer agreement.
- **Cultural references age** — "Game of Thrones" reference is dated in 2026. Re-review every 12 months.
- **Trademark collisions** — winning variant may collide with existing trademark in target market. Run trademark search before final ship (USPTO / EUIPO / JPO).
- **Pronoun choice (Sie/du, tu/vous, です/だ)** — pick once + lock in style guide; switching mid-app is jarring.
- **Religious + political sensitivity** — Ramadan timing in MENA; Lunar New Year in CN/KR; election cycles in BR/IN. Brief must flag.
- **Compound nouns (DE)** — "Produktverwaltungssystem" looks scary but is natural; transcreator may shorten to "Produktverwaltung". Verify with reviewer.
- **CJK character density** — JA/ZH/KO pack more meaning per character; less length pressure than DE/RU; transcreate for impact, not for length match.
- **Backtranslation has bias** — back-translator may "interpret"; use literal-mode brief for accuracy.

## Sources

- Smartcat marketplace: https://www.smartcat.com/
- Smartcat API: https://developers.smartcat.com/
- Lilt adaptive MT + transcreation: https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work
- Adaptive MT vs PEMT: https://labs.lilt.com/free-the-translators-how-adaptive-mt-turns-post-editing-janitors-into-cultural-consultants
- Acclaro transcreation: https://www.acclaro.com/services/transcreation/
- CSA Research transcreation pricing: https://csa-research.com/
- Phrase TMS LSP routing: https://support.phrase.com/hc/en-us
- Crowdin transcreation labels: https://support.crowdin.com/labels/
- Brand voice frameworks (Slack): https://slack.design/articles/voice-and-tone/
