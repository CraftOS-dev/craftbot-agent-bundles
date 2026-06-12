<!--
Source: https://www.prsa.org/article/ai-and-the-new-era-of-crisis-comms-ST-May25
SPJ Code of Ethics: https://www.spj.org/ethicscode.asp
-->
# Media Training + Spokesperson Prep — SKILL

Pre-interview spokesperson briefing: outlet + journalist research, likely-question generation (15-30 Qs), bridge phrases, attribution status (on-record / on-background / off-record), and `mcp-tts` audio drill for spokesperson rehearsal. Produces a `docx` briefing pack + audio drill files 24-72 hours before the interview.

## When to use this skill

- **Tier-1 print interview** — NYT/WSJ/Bloomberg/FT/Forbes sit-down or phone interview.
- **Podcast appearance** — long-form (30-90 min); pair with `podcast-tour-booking-for-execs` for booking flow.
- **TV/broadcast hit** — CNBC/Bloomberg TV/CNN/BBC; tighter sound-bite discipline.
- **Conference panel** — speaker prep for a moderated panel.
- **Crisis interview** — high-stakes sit-down during/after a crisis (pair with `crisis-comms-24-48-72-hour-playbook`).
- **Analyst briefing** — Gartner/Forrester/IDC (pair with `analyst-relations-gartner-forrester-idc` for the briefing process).

**Do NOT use this skill when:**
- The spokesperson is doing a written Q&A (no rehearsal needed, just draft answers).
- The "interview" is a customer-success success story video (defer to `customer-support-agent` or marketing).

## Setup

### Inputs from media list

Pull journalist + outlet from Notion media-list CRM:
- Recent articles (last 5-10)
- Outlet's editorial angle and POV
- Audience demographics
- Prior interviews with similar guests
- Attribution defaults (per role.md interaction log)

### mcp-tts (audio drill)

Already configured. Default voice: spokesperson's preferred listening voice (often a calm male/female narrator, NOT trying to mimic the spokesperson themselves).

```bash
mcp tool mcp-tts.synthesize \
  --voice "en-US-Standard-D" \
  --text "Question 1: Why did you raise this round now?" \
  --output q1.mp3
```

### elevenlabs-mcp (higher-quality voice when needed)

For executive demo reels or exec-facing rehearsal where standard TTS sounds robotic:

```bash
export ELEVENLABS_API_KEY="<key>"
elevenlabs-mcp tts --voice "Adam" --text "..." --output q1_premium.mp3
```

### docx skill (briefing pack output)

Renders the structured briefing as a Word doc for in-person review by spokesperson + PR lead.

### youtube-mcp-transcript (for podcast prep)

Pull host's last 3 episodes' transcripts to study cadence + question style.

## Common recipes

### Recipe 1: Journalist research dossier

```bash
# Pull journalist's last 10 articles
muckrack_id=$(notion query "media_list WHERE name='Casey Newton'" | jq -r .muckrack_id)

curl "$MUCKRACK_API_BASE/journalists/$muckrack_id?include=articles" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY" \
| jq '.articles[0:10] | map({title, url, date, key_argument: ""})' > dossier.json

# Scrape each article body for key arguments
for url in $(jq -r '.[].url' dossier.json); do
  body=$(firecrawl scrape --url "$url" | jq -r .markdown)
  # Claude extracts key argument + interviewee names + topical POV
  key_arg=$(claude --prompt "One sentence: what's the central argument of this article? URL: $url")
  jq --arg url "$url" --arg arg "$key_arg" \
    '(.[] | select(.url == $url) | .key_argument) = $arg' dossier.json > tmp && mv tmp dossier.json
done
```

### Recipe 2: Likely-question generation (15-30 Qs)

```python
# Inputs: dossier (journalist's last 10 articles) + outlet POV + interview topic + spokesperson role
prompt = f"""
Generate 25 likely interview questions a {journalist['outlet']} journalist would ask
of a {spokesperson['role']} at {company['name']}, given:

TOPIC: {interview['topic']}
SPOKESPERSON BACKGROUND: {spokesperson['background_summary']}
JOURNALIST'S RECENT ARGUMENTS:
{format_dossier(dossier)}

OUTLET EDITORIAL ANGLE: {outlet['angle']}

Generate questions in mix:
- 10 expected fastball (industry context, company story, news of the day)
- 8 medium-difficulty (challenge questions about strategy or competition)
- 5 hard / hostile (criticism of competitor moves, regulatory risk, market downturn)
- 2 personal / character (origin story, biggest mistake, leadership philosophy)

For each: give a 60-word recommended answer that includes
- A specific number or named example
- A bridge phrase to a key message
- A "what NOT to say" caveat

Format as markdown with ### headings.
"""

q_and_a = claude(prompt)
```

### Recipe 3: Bridge phrases library (Claude-augmented)

Standard bridge phrases the spokesperson should rehearse:

```markdown
## When asked about a sensitive topic, bridge with:
- "What's interesting about that is..." → pivot to comfortable topic
- "The bigger picture here is..." → pivot to company strategy
- "What we're seeing on the ground is..." → pivot to customer data
- "I'll let our results speak for themselves, but..." → pivot to forward-looking

## When asked about a competitor, bridge with:
- "I respect what [competitor] is building. What we're doing differently is..."
- "The category is big enough for multiple players. Our differentiation is..."
- "We don't comment on competitor strategy. What I can tell you about us is..."

## When asked about an unconfirmed rumor, say:
- "We don't comment on speculation."
- "I can't speak to that, but I CAN tell you that..."

## When asked about a hostile angle, say:
- "I want to address that directly. Here's our perspective..."
- "Let me give you the full context on that..."
```

### Recipe 4: "If asked X, pivot to Y" matrix

```markdown
| If asked about... | Recommended pivot |
|---|---|
| Layoffs (none planned) | "We're hiring across [team]. Last 90 days we added [n]." |
| Competitor's recent funding | "Our differentiation: [3 specifics]. Customers we won this quarter: [3 names with permission]." |
| Pricing speculation | "Pricing tiers are public at [URL]. We haven't changed pricing in 18 months." |
| Internal management drama | "Our team is aligned on [shared mission]. Let me show you what we shipped this quarter." |
| Unannounced roadmap | "We share roadmap at [conference]. What I CAN share today is [public info]." |
| Customer churn | "Our net retention is [number]. Customer wins this quarter include [public names]." |
```

### Recipe 5: Attribution status discipline reminder

```markdown
## CRITICAL: confirm attribution at the START of the interview

Default: on-record (statements are for publication, attributable by name + title)

If something sensitive is about to come up, BEFORE speaking it:
"I'd like to take this next part on background — does that work?"

Wait for explicit "yes" before proceeding.

On background = published, attributed to "a senior executive at Acme"
Off the record = NOT published, journalist won't seek it elsewhere either
Deep background = context-setting only, never reproduced

Don't assume off-record. Many journalists won't accept it. If they decline, stay on-record or pivot.
```

### Recipe 6: mcp-tts audio drill

Generate audio files of each likely question, played back in random order for the spokesperson to practice cold:

```bash
# Generate one mp3 per question
jq -r '.questions[]' qa.json | while read -r q; do
  fname=$(echo "$q" | md5sum | head -c 8).mp3
  mcp tool mcp-tts.synthesize --voice "en-US-Standard-D" --text "$q" --output "drill/$fname"
done

# Random playback script
ls drill/*.mp3 | shuf | while read f; do
  echo "Q: $(jq -r --arg f "$(basename $f .mp3)" '.questions[] | select(.id == $f) | .text' qa.json)"
  mpv "$f"
  read -p "Press enter for next question..."
done
```

### Recipe 7: Mock interview transcript (Claude role-play)

```python
prompt = f"""
You are {journalist['name']}, a {journalist['title']} at {journalist['outlet']}.
You're interviewing {spokesperson['name']} for a piece about {interview['topic']}.

Conduct a 20-minute interview. Ask 10-12 questions. Follow up on weak answers.
Probe inconsistencies. Be respectful but not deferential. Push on the hardest topics:
{interview['hard_questions']}.

The spokesperson's responses will be inserted by me. Start with your opening question.
"""

# Run as a multi-turn back-and-forth; spokesperson types their answers
# Record the transcript for review
```

### Recipe 8: Briefing pack export (docx)

```python
from docx_skill import render_docx
render_docx(
    template='spokesperson-brief.docx',
    output=f'brief_{interview_id}.docx',
    data={
        'spokesperson': spokesperson,
        'outlet': outlet,
        'journalist': journalist,
        'date_time': interview_datetime,
        'dossier': dossier,
        'key_messages': [m1, m2, m3],
        'qa': q_and_a,
        'pivot_matrix': pivot_matrix,
        'attribution_reminder': attribution_text,
        'bridge_phrases': bridge_phrases,
    }
)
```

## Examples — full prep workflow

```yaml
interview: Casey Newton (Platformer) interview with Acme CEO on AI safety
timeline: 5 business days lead time

day_-5:
  - pull journalist dossier (last 10 articles)
  - pull outlet POV summary
  - confirm interview topic + format (phone / sit-down / video)
  - confirm attribution default (assume on-record)
  - notion log row created

day_-4:
  - generate 25 likely questions + recommended answers
  - build "if asked X pivot to Y" matrix
  - identify 3 key messages
  - export draft brief as docx for PR lead review

day_-3:
  - PR lead reviews brief; edits
  - mcp-tts drill files generated for spokesperson
  - spokesperson confirms 30 min/day for rehearsal x 3 days

day_-2:
  - mock interview with PR lead playing journalist (recorded)
  - playback review: identify weak answers; redraft

day_-1:
  - final brief locked
  - mcp-tts drill 1 more pass (cold)
  - prep room logistics (room booking, tech check, water)

day_0:
  - silent 30 min before; hydrate; no last-min additions
  - confirm attribution default in opening
  - record (if permitted) for post-interview review
  - PR lead listens / observes if possible

day_+1:
  - post-interview debrief (what worked, what didn't)
  - update key-message recall in notion
  - schedule next interview if it went well; or remediate if not
```

## Edge cases

### Hostile journalist
If pre-interview research surfaces hostile angles (the journalist has a clear axe to grind), have a frank conversation:
- Offer to provide context off-record FIRST (rare exception)
- Prepare more bridge phrases per question
- Consider declining if risk > reward; route to a friendlier outlet

### Spokesperson is the CEO + the story is about them personally
Hand off voice to `ceo-agent` for the executive-personal angle. PR-comms agent still handles outlet/journalist research + logistics.

### Live broadcast (TV) — tight sound-bite discipline
TV expects 8-15 second sound bites. Rehearse answers in that compressed form. Key message must fit in one sentence. Drop the supporting detail.

```markdown
## Print version (60 words):
"Our Q1 results show [3 supporting data points]. We're growing because..."

## Broadcast version (15 sec):
"In Q1 we grew 40%. Customers came to us because [single reason]."
```

### Crisis interview — extra discipline
- Spokesperson rehearses "what I CAN say" vs "what I CAN'T say" boundaries with legal
- Acknowledge → take ownership → forward action → commit to next update
- Don't speculate. Don't deflect. Don't blame.
- Pair with `crisis-comms-24-48-72-hour-playbook` for the underlying playbook

### Podcast vs print interview
Podcast: 30-90 min, conversational, story-driven. Print: 20-30 min, more probing.
Podcast prep: study host's last 3 episodes via `youtube-mcp-transcript`. Print prep: study journalist's writing style + recent arguments.

### Mock interview is uncomfortable
Spokespeople resist mock interviews ("I'll be fine"). They're wrong. Insist on at least one full 20-min mock per high-stakes interview. The discomfort of the mock is preferable to the discomfort of a bad real interview.

### Attribution mistakes are unforgivable
If spokesperson accidentally says something "off-record" without confirming first, treat as on-record. Brief them HARD on this: "If you want it off-record, say so BEFORE you say the thing — and wait for journalist to agree explicitly."

### Recording the prep session (with consent)
If spokesperson consents, record the mock interview via Zoom; pull transcript via `zoom-mcp`. Replay highlights. Generate Q&A doc from the actual answers (not just hypothetical).

### "What's your favorite question?" trap
Many journalists open with a softball. Spokesperson relaxes. Then hostile follow-up. Brief: there is no softball; treat every question as substantive.

### Re-prep for repeat interviews with same journalist
Pull prior interaction log from Notion (Recipe 5). Check what was committed-to last time. Don't contradict.

### Bridging without sounding evasive
Bridge phrase should connect logically: "What's interesting about that is..." works only if the bridge connects to the same general topic. Pure deflection ("Let me tell you about something else") sounds evasive on transcript.

### Premium voice for executive presence rehearsal
For C-suite spokespersons preparing for high-stakes appearances, ElevenLabs (premium TTS) produces more natural intonation than standard mcp-tts. Worth the per-character cost for top 3-5 interviews/year per exec.

## Sources

- **PRSA AI + crisis comms**: https://www.prsa.org/article/ai-and-the-new-era-of-crisis-comms-ST-May25
- **SPJ Code of Ethics (attribution rules)**: https://www.spj.org/ethicscode.asp
- **Muck Rack API for journalist dossiers**: https://muckrack.com/pr-software/api
- **mcp-tts (TTS for drills)**: https://github.com/modelcontextprotocol/servers
- **ElevenLabs API**: https://elevenlabs.io/docs/api-reference
- **role.md spokesperson playbook**: internal
