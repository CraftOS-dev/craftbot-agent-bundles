<!--
Sources:
- Eventmanagerblog Run-of-Show Template: https://www.eventmanagerblog.com/run-of-show-template
- Cvent Agenda Builder: https://www.cvent.com/en/event-marketing-management/agenda-builder
- ILEA Production Standards: https://www.ileahub.com
-->
# Agenda + Run-of-Show Authoring — SKILL

Agenda is what attendees see. Run-of-show is what ops sees. Both must be authored separately, kept in sync, and printed for stage manager / AV lead / venue ops / MC. The 5-column broadcast-style cue sheet is the standard; deviate at your peril.

## When to use this skill

- New event needing minute-by-minute production plan
- Major agenda change (speaker swap, session add/drop, room reassignment)
- Hybrid event needing in-person + virtual cue synchronization
- Multi-track conference with parallel sessions + shared breaks
- Rehearsal scheduling (each speaker timed against ROS)
- Day-of stage manager / AV lead briefing

**Do NOT use this skill when:**
- Event is single keynote + Q&A (overengineered)
- Recipient has stage manager who authors ROS — coordinate, don't override
- Pure virtual webinar with single broadcast — use `live-streaming-restream-obs-streamyard` instead

## Setup

### Tools

- `notion-mcp` for ROS DB (collaborative, real-time)
- `google-sheets` for xlsx export to AV crew
- `docx` for printed binder version
- `pptx` for stage backstage briefing deck
- `using-git-worktrees` for ROS version control across rehearsals

### Data model (Notion DB)

```yaml
ros_table:
  fields:
    - time (date-time, primary)
    - duration_minutes (number)
    - item (text)
    - speaker_or_stage (relation: speaker DB OR text)
    - av_cue (text: mic, slides, music, lighting, camera)
    - room (select: main / breakout A / breakout B / lobby)
    - notes (long text: filler material, transitions, contingencies)
    - status (select: tentative / confirmed / done)
    - linked_session (relation: session DB)
```

## Common recipes

### Recipe 1: Broadcast-style 5-column cue sheet

This is THE standard format:

```markdown
| Time | Item | Speaker / Stage | A/V Cue | Notes |
|------|------|-----------------|---------|-------|
| 8:00 | Doors open + reg open | Lobby | Music in (BG playlist 1) | Greeters at door + swag pickup + dietary tag on badge |
| 8:30 | Coffee + breakfast | Pre-function | — | 50 vegan / 30 GF / 5 kosher / 3 halal |
| 9:00 | Welcome + housekeeping | Main / MC | Mics on, slides up, applause music | MC 5 min max, transition to keynote |
| 9:05 | Keynote: [Title] | Main / Speaker A | Slides up 16:9, lapel + handheld backup, lower-third "[A], [Title]", music out | 30 min + 10 min Q&A via Slido session ABC123 |
| 9:45 | Transition | Main | Music in (5s fade), lighting half-down, lower-third out | 10 min stage swap + speaker change |
| 9:55 | Panel: [Topic] | Main / 3 panelists | Slides up, 4 mics on, lower-third per panelist rotated | Moderator brief: time keeping, bridge phrases |
| 10:30 | Networking + sponsor coffee | Pre-function | Music in, lighting full, audio dampened main | Gold sponsor cart + branded napkins + cups |
| 10:50 | Resume warning | All | Bell tone + announcement: "Resume in 5 min" | Ops sweep room for stragglers |
| 11:00 | Breakout A: [Topic] | Breakout A / Speaker B | Mic on, slides up, dim house lights | 45 min + 15 min Q&A |
| 11:00 | Breakout B: [Topic] | Breakout B / Speaker C | Mic on, slides up, dim house lights | 45 min + 15 min Q&A |
| 12:00 | Lunch buffet | Pre-function | Music in (jazzy upbeat playlist), lighting full | Dietary stations: standard / vegan / GF / kosher / halal |
| 13:00 | Resume warning | All | Bell tone + announcement | |
| ... | ... | ... | ... | ... |
```

### Recipe 2: Cue type vocabulary (standardize)

```yaml
mic_cues:
  - "Mic ON: <speaker name> lapel + handheld backup"
  - "Mic OFF: <speaker name>"

slide_cues:
  - "Slides UP: <session title> (16:9)"
  - "Slides OUT: black screen"

music_cues:
  - "Music IN: <track name> (loop / fade-in 5s)"
  - "Music OUT: (fade-out 3s)"

lighting_cues:
  - "Lights FULL"
  - "Lights HALF" (between sessions)
  - "Lights STAGE-ONLY" (during talk)
  - "Lights FULL-DOWN" (during transition)

camera_cues:  # hybrid events
  - "CAM 1: wide on stage"
  - "CAM 2: tight on speaker"
  - "CAM 3: audience reaction"
  - "MULTI-CAM: switch every 8 sec"

lower_third_cues:
  - "L3 ON: <name>, <title>"
  - "L3 OFF"

stream_cues:  # hybrid
  - "STREAM CUT TO: break slide"
  - "STREAM CUT BACK: stage"
  - "CAPTION OVERLAY: ON"
```

### Recipe 3: Multi-room (parallel tracks) coordination

For multi-track conferences with shared breaks:

```python
# Notion DB filter view per room
main_stage = notion.query(ros_db, filter={room: 'main'})
breakout_a = notion.query(ros_db, filter={room: 'breakout_a'})
breakout_b = notion.query(ros_db, filter={room: 'breakout_b'})

# Export per-room for room-specific stage manager
for room, rows in [(main_stage, 'main'), (breakout_a, 'breakout_a'), (breakout_b, 'breakout_b')]:
    google_sheets.export(rows, f'ros_{room}.xlsx')
```

Sync coordination at shared transitions (lunch, breaks) — all rooms must conclude session within 5-min window.

### Recipe 4: Contingency built into ROS

Each session row should have a hidden "contingency" column:

```yaml
session_row:
  ... regular cues ...
  contingency:
    speaker_no_show: "MC fill 5 min anecdote + Q&A extension OR move next session forward"
    av_failure: "Backup mic + USB slides + analog whiteboard fallback"
    catering_delay: "Extend Q&A 5 min, add intermission OR sponsor product demo"
    medical_emergency: "Pause program; runner contacts EMT; resume after clear"
    fire_alarm: "Full evac to assembly point; MC pre-written script"
```

### Recipe 5: Speaker briefing extracted from ROS

For each speaker, extract their slice of ROS:

```bash
mcp tool notion.query_database \
  --database "ros" \
  --filter "{speaker_or_stage: 'Speaker A'}"

# Generate per-speaker cue sheet:
mcp tool docx.create --output "speaker_a_cue_sheet.docx" \
  --content "<extracted rows formatted as personalized brief>"

mcp tool gmail.send_email \
  --to "speaker_a@example.com" \
  --subject "Your day-of cue sheet — Q3 Summit" \
  --body "Hi Speaker A, attached is your personalized cue sheet for the event..."
```

### Recipe 6: Stage manager binder

Print physical binder (3-ring, color-tabbed):

```
Tab 1: Full ROS (chronological)
Tab 2: Per-room ROS
Tab 3: Emergency action plan (see crisis playbook)
Tab 4: Vendor contact tree (AV / catering / venue / security)
Tab 5: Speaker bios + photos
Tab 6: Sponsor mention scripts (for MC)
Tab 7: Filler material (anecdotes, audience engagement)
```

### Recipe 7: Real-time updates during event

Stage manager updates Notion DB in real-time during event. Changes sync to all crew via:

```python
# Notion webhook on row update
@webhook('notion_ros_update')
def on_ros_change(row):
    if row.status == 'done':
        slack.send_message(channel='av-crew', text=f'Session done: {row.item}')
    elif row.duration_overrun > 5:
        slack.send_message(channel='ops', text=f':warning: {row.item} running {row.duration_overrun}min long')
```

### Recipe 8: Version control via git worktrees

Each rehearsal updates ROS; use git worktrees to version control:

```bash
# Pre-rehearsal 1 (T-14 days)
git worktree add ../ros-rehearsal-1 rehearsal-1
cd ../ros-rehearsal-1
# Make changes
git commit -am "Rehearsal 1 updates: speaker A timing, transition music"

# Pre-rehearsal 2 (T-7 days)
git worktree add ../ros-rehearsal-2 rehearsal-2
# Make changes
git commit -am "Rehearsal 2 updates: cut intro 2min"

# Final (day-of)
git checkout main
git merge rehearsal-1 rehearsal-2
git tag day-of-final
```

## Examples

### Example A: Single-track summit, 200 attendees, full day

ROS spans 8:00am-6:00pm with 90-min lunch + 2 networking breaks. ~25 rows. 1 stage manager binder + 1 AV binder + 1 MC binder + 4 speaker briefs.

### Example B: Multi-track conference, 500 attendees, 3 days

ROS per day, per room. ~80 rows per day. 9 binders (3 stage managers + 3 AV binders + 3 MC binders) + 20+ speaker briefs.

### Example C: Hybrid keynote with simultaneous Q&A bridge

Special row for bridge tech:

```markdown
| 9:05 | Keynote: [Title] | Main / Speaker A | Slides up, lapel mic, multi-cam, STREAM CAM 1 wide → Cam 2 tight, captions ON | Slido for Q&A both sides — moderator queues top 5 via Slido moderator app |
| 9:35 | Q&A | Main / Speaker A + Moderator | Mic 1 on speaker, mic 2 on moderator, audience mic ON via runner, STREAM CAM 3 audience cut on Q | Moderator reads Slido questions; bridge to virtual via Brella matchmaker chat for follow-up |
```

## Edge cases

### Speaker overrun (live)
MC has instruction: at 5 min remaining, hold up cue card. At 0 min, MC interrupts with "Thank you so much, [Speaker]. We need to transition to give attendees a chance for Q&A in 2 minutes."

### Tech delay (slides won't load, mic dead)
Stage manager has clear command: "Hold the audience" (MC fills) OR "Cut to break" (10-min unscheduled break). Don't dither.

### Last-minute speaker swap
Update ROS row + notify AV lead + MC + venue ops via Slack + radio. Reprint affected binder pages.

### Unannounced VIP guest (executive arrives mid-event)
Reserved VIP seat + stage manager radio: "VIP [name] arrived. Walk-on at next break." MC acknowledges from stage briefly.

### Audio bleed from adjacent room
For multi-track, schedule loud sessions (panel + audience clapping) at staggered times across rooms. Use audio engineer to mute adjacent room mics during loud moments.

### Caption overlay sync (hybrid)
CART captioner has dedicated audio feed; captions delayed ~2-3 sec from speaker. Acceptable on stream; brief CART captioner pre-event with jargon glossary.

### Speaker requests slide changes mid-event
Have backup laptop with their slides pre-loaded; speakers should not handle their own laptop on stage.

### Stage manager unavailable day-of (illness)
Backup stage manager has full briefing + binder access. Identify backup at T-14 days.

### ROS vs Agenda discrepancy
Agenda is what attendees see; ROS includes contingencies, music cues, lighting, etc. Agenda is exported FROM ROS (filter to just visible items). Avoid maintaining two separate documents.

### International event with multi-language tracks
ROS in English (universal AV language); session content in target language. Captioner provides translation overlay for non-English sessions.

## Sources

- **Eventmanagerblog Run-of-Show Template**: https://www.eventmanagerblog.com/run-of-show-template
- **Cvent Agenda Builder**: https://www.cvent.com/en/event-marketing-management/agenda-builder
- **ILEA Production Standards**: https://www.ileahub.com
- **InfoComm Tech Manager Guide**: https://www.avixa.org/resources
- **Stage Manager's Toolkit (Lawrence Stern)**: industry-standard reference
