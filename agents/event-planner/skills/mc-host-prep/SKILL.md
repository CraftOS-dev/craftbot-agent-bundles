<!--
Sources:
- EventManagerBlog MC Host: https://www.eventmanagerblog.com/mc-host-event
- Toastmasters MC Skills: https://www.toastmasters.org
- Cvent MC Briefing: https://www.cvent.com/en/blog/events/event-emcee-tips
- Bizzabo Event MC Guide: https://www.bizzabo.com/blog/event-emcee
-->
# MC / Host Preparation — SKILL

End-to-end MC pipeline: briefing doc creation → rehearsal call → day-of cue sheet → emergency scripts → post-event debrief. The MC is the visible thread holding the event together — every transition, every awkward gap, every emergency runs through them. Treat MC prep as production prep, not improv.

## When to use this skill

- Briefing an external MC (paid host, celebrity, industry voice)
- Briefing an internal MC (executive, marketing lead, employee volunteer)
- Multi-track conference needing track-specific MCs (parallel rooms)
- Hybrid event needing in-room MC + virtual host (two-person team)
- Awards gala / dinner needing entertainment-tier MC
- Mid-event MC substitution (illness, no-show)

**Do NOT use this skill when:**
- Single internal speaker doing their own intro (no MC needed)
- Webinar with single host who is also primary content (use `live-streaming-restream-obs-streamyard`)
- AI-generated voice narration only (use `mcp-tts` / `elevenlabs-mcp`)

## Setup

### Tools

- `docx` skill for briefing doc generation
- `notion-mcp` for MC database (history, rating, contact, availability)
- `zoom-mcp` for rehearsal call
- `gmail-mcp` for delivery + day-of comms
- `google-calendar-mcp` for rehearsal scheduling
- `pptx` skill for speaker intro slide deck (per-speaker visual cue)
- `mcp-tts` / `elevenlabs-mcp` for MC voice drill (practice cadence)

## Common recipes

### Recipe 1: MC briefing document (48 hours pre-event)

```markdown
# MC Brief — DevConf 2027 — Day 1 — September 15

## Audience snapshot
- 600 attendees (200 at any one moment per track)
- 65% senior IC + 25% manager + 10% director+
- Tone: technically smart, slightly self-deprecating, no marketing speak
- Avoid: corporate buzzwords ("synergy", "leverage"), gendered defaults ("you guys"), audience-as-prop jokes

## MC role
- Welcome + housekeeping (5 min MAX — they want content, not you)
- Session transitions (30-60 sec per — name + bio sentence + ask + walk-on cue)
- Audience engagement when Q&A runs short (1-2 filler questions ready per session)
- Emergency scripts (fire, medical, AV failure) memorized
- Sponsor mentions per verbatim script (don't ad-lib brand names)

## Run-of-show (full attached as Excel)
[Linked: notion.so/devconf-2027-ros]

## Speakers — Day 1 main stage

### 9:00am — Keynote: Sarah K. "AI Infrastructure at Scale"
- Bio: Principal Engineer at Linear Capital; led AWS Bedrock infra; 8 years scaling LLM systems
- 1-sentence intro: "Sarah's been at the front of every LLM infra wave — she has the receipts and the scars."
- Ask: "Welcome Sarah K."
- Walk-on cue: music in (Lo-Fi Hip Hop intro 5 sec fade); spotlight stage left
- Post-talk filler if Q&A short: "Sarah, what's the one thing about LLM infra that everyone gets wrong at this stage?"

### 9:45am — Transition + 5-min stage swap
- MC fills: "Quick break to swap stage setup. Grab water at sponsor station 3 (Datadog Gold sponsor). Back in 5."
- Optional: 2-min audience interaction question: "Show of hands — who's running production LLM infra today?"

### 9:50am — Panel: "Building Frontier Teams"
- Moderator: Marcus L.
- Panelists: J. Park (Anthropic), K. Singh (OpenAI), L. Chen (Mistral)
- Intro: "Three of the people actually doing this — Marcus has a sharp moderating style; expect direct questions."
- Ask: "Welcome the panel — Marcus, take it away."

[... continued per session ...]

## Sponsor mentions per script (read VERBATIM)

### 10:30am coffee break sponsor mention (Datadog Gold)
"Coffee break sponsored by Datadog. They've got their team at booth #14 — drop by, they're showing how to monitor LLM costs in production. We resume at 11:00."

### 12:30pm lunch sponsor mention (Linear Platinum)
"Lunch sponsored by Linear, our Platinum sponsor. Linear is also hosting tonight's happy hour at 6pm — invite-only, but they're adding 50 walk-ins; sign up at booth #1."

## Filler material (use when Q&A runs short)

### Industry anecdotes (30-60 sec each)
1. "Funny story — I was at a meeting last week where..."
2. "I read this morning that..."
3. "If you haven't seen [recent industry news], it's worth a Twitter scroll."

### Audience interaction prompts (10-30 sec each)
1. "Show of hands — who came from outside Chicago?"
2. "Who's first DevConf?" → applause
3. "Who's here looking for talent? Recruiters, raise hands." (light, before networking break)

## Emergency scripts (memorize)

### Fire alarm
"Folks, that's a fire alarm. We need to make our way to the front exit and the assembly point at [location]. Please follow staff in yellow vests. Take it slow. We'll resume once we get the all-clear."

### Medical emergency
"We're going to take a brief pause. Please remain in your seats. Our team is handling something quietly. We'll resume in just a moment."

### AV failure
"Looks like we've got a quick technical issue. We'll be back in just a sec. While we wait — [filler question or anecdote]."

### Sponsor-related issue
Do NOT acknowledge sponsor problems from stage. Escalate to ops via radio; resolve off-stage.

## Day-of contacts
- Stage manager (your radio partner): Jordan B. — 312-555-0193
- AV lead: Riley K. — 312-555-0214
- Ops lead: Pat S. — 312-555-0078
- Catering manager: see BEO (in your binder pocket)

## Rehearsal
- Date: Sept 14, 2pm CT
- Location: venue main stage (in-person walk-through) + zoom for remote crew (link in calendar invite)
- Duration: 90 min
- Agenda: walk every transition; mic check; lighting + music cues; emergency scripts

## Logistics
- Arrival: 7:00am (45 min before doors)
- Green room: room 218 (snacks + water + charging)
- Mic check: 7:30am with Riley (AV lead)
- Wardrobe: business casual + brand colors (NO patterns — clashes on camera); 2 outfit changes if needed
- Lapel mic + handheld backup (you'll have both)
- Earpiece for stage manager comms (test during rehearsal)
- Personal sip-water on stage left (replenished each break)
```

### Recipe 2: Rehearsal call (24-48 hours pre-event)

```bash
# Schedule via zoom-mcp
mcp tool zoom.create_meeting \
  --topic "DevConf 2027 — MC Rehearsal" \
  --start "2027-09-14T14:00:00-05:00" \
  --duration 90 \
  --attendees "mc@vendor.com,stage-manager@us.com,av-lead@us.com,ops-lead@us.com" \
  --agenda "$(cat mc_rehearsal_agenda.md)"
```

```markdown
# MC Rehearsal Agenda (90 min)

## 0:00 — Welcome + brief overview (10 min)
- Brief on event format, audience, tone
- MC asks questions, takes notes

## 0:10 — Walk every transition (45 min)
- Read each session intro out loud
- Practice ask + walk-on cue with AV
- Confirm sponsor mention scripts (verbatim)
- Time each transition

## 0:55 — Emergency scripts (10 min)
- Read fire / medical / AV scripts out loud
- Pause for memorization check

## 1:05 — Filler material rehearsal (10 min)
- Run through 2-3 industry anecdotes for cadence
- Test audience interaction prompts

## 1:15 — Tech check (15 min)
- Mic check (lapel + handheld + battery)
- Earpiece comms with stage manager
- Lighting + music cue confirmation
```

### Recipe 3: Day-of cue sheet (printed binder)

Print 3 copies: 1 for MC podium, 1 for stage manager backstage, 1 for green room.

```
| Time | Item | MC Action | Cue | AV |
|------|------|-----------|-----|----|
| 8:55 | Pre-show music fade | Step on stage | Lights up 8:59 | Music out 8:59:55 |
| 9:00 | Welcome + housekeeping | "Welcome to DevConf 2027..." (5 min MAX) | — | Slides: Welcome graphic |
| 9:05 | Intro Sarah K. | "Sarah's been at the front..." | Music in (5 sec) | Lower-third: "Sarah K." |
| 9:06 | Sarah on stage | Step off; sit stage left | Sarah owns mic | Slides: Sarah's deck |
| 9:36 | Q&A start | Approach mic | Hold mic for audience | — |
| 9:40 | Q&A close (or filler) | "One last question — Sarah..." | — | — |
| 9:45 | Transition | "Quick break, back in 5" | Music in (5 sec) | Stage swap |
| 9:50 | Intro panel | "Three of the people actually doing this..." | — | Lower-third: panel names |
[...]
```

### Recipe 4: Multi-MC coordination (parallel tracks)

For multi-track conferences, each track gets its own MC. Synchronize via:

```markdown
# Track MC Coordination — DevConf 2027

## Main stage MC: Alex R.
- Owns: opening keynote + 2 panels + closing
- Standardizes brand voice + sponsor mentions for full conference

## Track A MC (AI/ML): Jordan F.
- Owns: 6 breakouts + 2 lightning sessions
- Briefed by Alex on tone consistency
- Reports to Alex for emergency comms

## Track B MC (Infra): Sam T.
- Owns: 6 breakouts + 2 lightning sessions

## Coordination meeting: Sept 13, 3pm — all MCs join Alex's lead
- Walk shared sponsor mentions
- Walk emergency scripts
- Confirm radio + earpiece comms tree
- Decide standard transition cadence
```

### Recipe 5: Hybrid event MC + virtual host pairing

For hybrid events, in-room MC + virtual host work as a team.

```markdown
# In-Room MC (Alex R.)
- Welcomes in-room audience
- Manages on-stage cues
- Triggers Q&A from in-room mics
- Bridges to virtual when relevant: "Let's pull a question from Slido — virtual host, what's coming in?"

# Virtual Host (Jordan F. — remote)
- Welcomes virtual audience separately
- Monitors Slido / chat for questions
- Pre-screens virtual audience video Q&A
- Bridges virtual to in-room: "We've got Maya on video from London — Alex, want to bring her up?"

# Radio comm: shared backchannel via Slack ops channel
```

### Recipe 6: AI voice drill for cadence practice

```bash
# Generate audio version of MC script for cadence reference
mcp tool elevenlabs.text_to_speech \
  --text "$(cat mc_script_day1.md)" \
  --voice "antoni" \
  --output mc_day1_reference.mp3

# MC listens to reference, practices matching cadence
```

## Examples

### Example A: External celebrity MC (high-budget conference)

```
MC: Industry podcast host
Fee: $15,000 + travel + lodging
Brief sent: 7 days out (vs 48 hours for in-house)
Rehearsal: 48 hours out (virtual) + day-of mic check
Day-of: 1-hour green room briefing + sip-water station
Post-event: thank-you note + future-engagement option
```

### Example B: Internal MC (employee volunteer)

```
MC: Marketing director
Compensation: comp time + dinner stipend
Brief sent: 14 days out (longer prep for non-pro)
Rehearsal: 14 days out + 48 hours out (2 calls)
Tech check: comfortable with lapel mic + slide remote
Day-of: full coffee + breakfast + green room with stylist option
```

### Example C: Substitution at 6am day-of (MC sick)

```
1. Notify ops lead immediately (5:45am)
2. Activate backup MC (pre-identified at briefing stage)
3. Backup studies brief in 90 min (shorter version: only first 2 hours)
4. Skip rehearsal; emergency runbook covers transitions
5. Stage manager carries more cue weight day-of
6. Reduce on-camera MC time; lean on speakers carrying their own intros
```

## Edge cases

### MC late on first day
Have a deputy MC (often the conference chair / executive sponsor) memorize the opening script as backup. Activate at 8:30am if MC not on-site.

### MC mispronounces speaker name
Confirm phonetic pronunciation at briefing AND rehearsal. Include phonetic spelling in cue sheet (e.g., "Saurabh = sow-RUBB"). Speakers feel respected when names are said right.

### MC dad-jokes on stage
External MCs sometimes ad-lib jokes that don't match audience. Pre-brief on what NOT to joke about (politics, religion, audience members by name, gendered humor). Stage manager has authority to radio MC to dial back.

### MC over-extends housekeeping
Common pitfall: MCs talk too long at opening. Hard cap at 5 min. If MC over-runs at rehearsal, coach explicitly: "we will be at minute 6, that's too long."

### MC tries to mention non-sponsor brand
Document sponsor brands explicitly in script. Brief MC to never name vendors outside sponsor list (avoids inadvertent endorsement that conflicts with sponsorship contracts).

### MC's bio in event materials
MC bio appears in attendee app + website + opening slide. Verify with MC at contracting; include in run-of-show appendix.

### MC payment + IRS form
External MCs: 1099 form for US tax compliance. Send 5 days post-event. Coordinate with `operations-agent` for AP.

### MC owns recording rights
External MCs: include in contract that recording is owned by event (not MC). Avoid future use restrictions.

### Substitute speaker on the fly
If a speaker no-shows, MC needs filler material AND backup speaker option. Brief MC on which sessions can be combined / shortened if needed.

### MC voice strain
Multi-day events: MC voice fatigue is real. Schedule rest periods + hydration. For 3-day events, consider rotating MCs.

### Translation / interpretation for non-English speakers
If the event has live interpretation, MC briefs interpreter on jokes, idioms, names. Interpreter sits in green room during MC briefing.

### Q&A microphone fumbling
Standing mic in audience is faster than runner mic. Provide mic stand at center aisle for Q&A; brief MC on "step to the mic" prompt.

## Sources

- **EventManagerBlog MC Host**: https://www.eventmanagerblog.com/mc-host-event
- **Toastmasters MC Skills**: https://www.toastmasters.org
- **Cvent MC Briefing**: https://www.cvent.com/en/blog/events/event-emcee-tips
- **Bizzabo Event MC Guide**: https://www.bizzabo.com/blog/event-emcee
- **PCMA on Hosts**: https://www.pcma.org
- **mcp-tts / elevenlabs-mcp**: voice drill tooling (in agent.yaml)
