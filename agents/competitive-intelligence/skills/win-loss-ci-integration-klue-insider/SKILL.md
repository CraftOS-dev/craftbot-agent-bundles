<!--
Sources: Klue × Salesforce https://klue.com/blog/win-loss-battlecards-salesforce
         Klue Salesforce playbook https://klue.com/salesforce
         Klue CI tools 2026 https://klue.com/topics/competitive-intelligence-tools-b2b-software
         OpenAI Whisper https://platform.openai.com/docs/guides/speech-to-text
Companion playbook: role.md → "Win-loss CI playbook"
-->

# Win/loss CI integration (Klue Insider class)

Win/loss interviews → AI-coded transcripts → Salesforce stage notes → battlecard-attached "Why we won/lost" data card. Klue Win/Loss is the SOTA stack; self-build path uses Whisper + LLM thematic coding + Salesforce custom object. Loops insights back to battlecards within 1 week of interview.

## When to use

- "Track win/loss data for competitive deals"
- "Why are we losing to Acme?"
- "Build a win/loss program for Q3 competitive deals"
- After 5+ competitive closed-won/lost in a quarter
- Battlecard pane 3 (latest deal intel) feels stale

## When NOT to use

- Quantitative win-rate trend only → use `ci-program-metrics-adoption-rate`
- One-off post-mortem on a single deal → use `hot-deals-ci-deal-level`
- Pure CI delivery without research → use `ci-delivery-slack-crm-klue-insider`

## Setup

### Paid path (Klue Win/Loss)

```bash
export KLUE_API_KEY="..."
export KLUE_API_BASE="https://api.klue.com/v1"
# Klue Win/Loss is a higher-tier add-on; ~$30-50k/yr enterprise.
```

### Self-build path

```bash
# OpenAI Whisper API for transcription
export OPENAI_API_KEY="sk-..."
# Salesforce REST API
export SF_INSTANCE_URL="https://yourco.my.salesforce.com"
export SF_ACCESS_TOKEN="..."
# ffmpeg for audio extraction
# winget install Gyan.FFmpeg  (or brew install ffmpeg)
```

MCPs in `agent.yaml`: `salesforce-api`, `notion-mcp`, `slack-mcp`, `gmail-mcp`. CraftBot skill: `openai-whisper-api` (or local Whisper for self-host).

## Common recipes

### Recipe 1: Queue interview targets from Salesforce

```python
from simple_salesforce import Salesforce
sf = Salesforce(instance_url=os.environ["SF_INSTANCE_URL"], session_id=os.environ["SF_ACCESS_TOKEN"])
q = """
SELECT Id, Name, Account.Name, StageName, CloseDate, Competitor__c, LossReason__c
FROM Opportunity
WHERE Competitor__c != null
  AND CloseDate >= LAST_QUARTER
  AND StageName IN ('Closed Won','Closed Lost')
ORDER BY CloseDate DESC
"""
opps = sf.query_all(q)["records"]
# Aim: 3-5 won + 3-5 lost per primary competitor per quarter
```

### Recipe 2: Interview script (standard 15-20 min)

Persisted as `interview-script.md`:

```
1. Why did you choose [vendor]? Top 3 evaluation criteria?
2. What did our team do well in the eval? Top 3 strengths?
3. What did our team do poorly? Top 3 weaknesses?
4. What did [competitor] do well? Top 3 strengths?
5. What did [competitor] do poorly? Top 3 weaknesses?
6. What would have changed your decision?
7. Who was the champion / detractor inside your team?
```

### Recipe 3: Transcribe via OpenAI Whisper API

```python
from openai import OpenAI
client = OpenAI()
with open("interview-acme-deal-12345.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1", file=f, response_format="verbose_json",
        timestamp_granularities=["segment"])
# transcript.segments = list of {start, end, text}
```

For privacy-sensitive cases, use local Whisper: `pipx install openai-whisper && whisper interview.mp3 --model medium`.

### Recipe 4: LLM thematic-coding pass

```python
import anthropic
client = anthropic.Anthropic()
prompt = f"""Code this win/loss interview into themes.
Output JSON: {{
  "themes": [{{"theme":..., "kind":"won-because|lost-because|objection|champion-quote|detractor-quote", "quote":"...", "support":1-5}}]
}}
Aim for 2-3 themes total — quality over quantity.

Interview transcript:
{transcript_text}
"""
resp = client.messages.create(model="claude-sonnet-4-5-20250929",
    max_tokens=2000, messages=[{"role":"user","content":prompt}])
themes = json.loads(resp.content[0].text)
```

### Recipe 5: Push to Klue Win/Loss API (paid)

```bash
curl -X POST "$KLUE_API_BASE/win-loss/interviews" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -d '{
    "opportunity_id":"sf-006-0012345",
    "competitor_id":"acme-corp",
    "outcome":"lost",
    "interview_date":"2026-06-10",
    "themes":[
      {"label":"lost-because","content":"Acme had better integration with Snowflake."},
      {"label":"objection","content":"Our pricing too aggressive for SMB segment."}
    ]
  }'
```

Klue auto-attaches this to the matching opportunity battlecard data card.

### Recipe 6: Salesforce custom object (self-build path)

```python
sf.WinLossInterview__c.create({
    "Opportunity__c": "006...12345",
    "Competitor__c": "acme-corp",
    "Outcome__c": "Lost",
    "Themes__c": json.dumps(themes),
    "Champion__c": "jdoe@buyerco.com",
    "Interview_Date__c": "2026-06-10",
    "Recording_URL__c": "https://yourstorage/...",
})
```

### Recipe 7: Surface back to battlecard

Within 1 week of interview, patch the competitor battlecard:

```python
# Pane 3: latest deal intel (90-day rolling)
# Pane 2: objections + rebuttals (refresh if new objection lands ≥2 interviews)
# Flag PMM approval needed for any new differentiator claim
```

See `battlecard-authoring-maintenance` Recipe 5 for the patch flow.

### Recipe 8: Klue Insider Salesforce embed (paid)

Native Klue Lightning component on the Opportunity record — surfaces the matching battlecard + last-3 win/loss data cards. No code required; UI configure.

### Recipe 9: Self-build Salesforce Lightning component

```javascript
// LWC stub — pull battlecard + last-3 win/loss for the competitor
import { LightningElement, api, wire } from 'lwc';
import getBattlecard from '@salesforce/apex/CIController.getBattlecard';
import getRecentWinLoss from '@salesforce/apex/CIController.getRecentWinLoss';
export default class CIBattlecardPanel extends LightningElement {
  @api recordId;
  @wire(getBattlecard, { opportunityId: '$recordId' }) battlecard;
  @wire(getRecentWinLoss, { opportunityId: '$recordId' }) winLoss;
}
```

### Recipe 10: Quarterly win-loss roll-up

```python
# Group themes by competitor + kind across the quarter
from collections import Counter
won_reasons = Counter(t["theme"] for t in all_themes_this_q if t["kind"]=="won-because")
lost_reasons = Counter(t["theme"] for t in all_themes_this_q if t["kind"]=="lost-because")
# Top 3 each → battlecard "won-because" / "lost-because" lines for the quarter
```

### Recipe 11: Buyer-research vendor handoff

If recipient uses Klue Win/Loss / ClozeLoop / Primary Intelligence buyer-research, the vendor runs the interview + delivers transcript + theme tags. CraftBot ingests their output via API or file drop; skip Recipes 2-3.

## Examples

### Example 1: Q3 lost-deal program for Acme competitor

**Goal:** Interview 5 closed-lost-to-Acme deals + push insights to battlecard.

**Steps:**
1. Recipe 1 → list opps; filter to Acme.
2. Reach out (PMM-owned, agent assists with email draft via `gmail-mcp`).
3. For each completed interview: Recipe 3 transcribe → Recipe 4 code → Recipe 5 (paid) or Recipe 6 (self-build) push.
4. Recipe 7 → patch Acme battlecard pane 3 with rolling 90-day intel + pane 2 if new objection.
5. Recipe 10 → quarterly themes deck for QBR.

**Result:** Acme battlecard refreshed; PMM has roll-up; sales team sees "why we lose to Acme" in their CRM.

### Example 2: First win-loss program kickoff

**Goal:** No win/loss in place yet; stand up program for top 3 competitors.

**Steps:**
1. Author interview script (Recipe 2); calibrate with PMM lead.
2. Configure Salesforce custom object `WinLossInterview__c` (Recipe 6 schema).
3. Add Klue Lightning component (Recipe 8) or build LWC (Recipe 9).
4. Onboard PMM with first 3 interviews; agent handles transcription + coding.
5. Quarterly roll-up template ready for end-of-Q1.

**Result:** Program live with 1-week feedback loop from interview → battlecard.

## Edge cases / gotchas

- **Consent / recording laws** — many US states are 1-party-consent (Klue + ClozeLoop OK with rep consent); some 2-party (CA, FL, IL). Always disclose recording. SCIP forbids recording without consent.
- **Transcription PII** — interviewees disclose pricing, internal names, sometimes confidential terms. Whisper transcripts stored encrypted; access-controlled in Salesforce.
- **LLM hallucination on themes** — Whisper transcript + LLM coding can hallucinate "champion quotes." Always source-cite to transcript timestamp. Don't synthesize quotes that aren't verbatim.
- **Small-N statistical risk** — 3 interviews ≠ statistical truth. Tag themes with `support: N`; require ≥3 interviews before any battlecard claim.
- **Sample bias** — interviewees who agree are often happy customers / loud critics. Track response rate; document bias risk in QBR.
- **Klue Win/Loss vs Klue Battlecards** — Win/Loss is a separate paid module. Don't assume battlecard customer has Win/Loss.
- **ClozeLoop / Primary Intelligence handoff** — vendor's coding schema may differ from yours. Normalize before push to Salesforce.
- **Champion churn** — interview a champion 9 months later; they may have left the buyer org. Capture role + tenure at time of interview.
- **GDPR / data subject rights** — EU interviewees can request deletion; have a deletion endpoint that purges transcript + theme records.
- **Whisper accuracy in noise** — phone interviews are lower fidelity than Zoom. Use noise-reduce with `ffmpeg` `arnndn` filter pre-Whisper for low-SNR audio.

## Sources

- Klue × Salesforce — https://klue.com/blog/win-loss-battlecards-salesforce
- Klue Salesforce playbook — https://klue.com/salesforce
- Klue CI tools 2026 — https://klue.com/topics/competitive-intelligence-tools-b2b-software
- OpenAI Whisper API — https://platform.openai.com/docs/guides/speech-to-text
- role.md → "Win-loss CI playbook" (this bundle)

## Related skills

- `battlecard-authoring-maintenance` — where themes land (panes 2, 3, 6, 7)
- `kill-sheet-objection-rebuttals` — quarterly theme roll-up sources kill-sheet refresh
- `ci-program-metrics-adoption-rate` — win-rate trend per competitor
- `ci-delivery-slack-crm-klue-insider` — Salesforce data card surface
- `ethical-public-source-methodology` — consent on recording
