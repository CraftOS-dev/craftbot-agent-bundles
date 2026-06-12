<!--
Sources:
- Delighted API: https://delighted.com/docs/api
- Typeform API: https://www.typeform.com/developers
- Qualtrics: https://api.qualtrics.com
- SurveyMonkey API: https://developer.surveymonkey.com
- Bizzabo Analytics: https://www.bizzabo.com/blog/event-analytics
- Cvent Insights: https://www.cvent.com/en/event-marketing-management/event-analytics
- Whova Analytics: https://whova.com
- NPS standard: https://www.netpromoter.com
-->
# Event Analytics, Engagement Metrics, NPS — SKILL

End-to-end event measurement pipeline: pre-event baseline → in-event real-time metrics → post-event NPS + qualitative survey → analysis + reporting. NPS alone is reductive; pair with engagement composite + qualitative themes for full picture. Best practice: collect within 48 hours of close; recipients forget by Day 7.

## When to use this skill

- Post-event NPS + qualitative survey to all attendees
- In-event real-time monitoring (check-in queue, session attendance, Q&A engagement)
- Per-sponsor ROI report (their leads, brand impressions, meeting outcomes)
- Per-speaker performance review (session rating, attendance, Q&A volume)
- Year-over-year benchmarking for recurring events
- Pre-event baseline collection (registration funnel, marketing attribution)

**Do NOT use this skill when:**
- Pure marketing campaign measurement (defer to `marketing-agent`)
- Pipeline / revenue attribution (use `event-roi-cost-per-attendee-pipeline`)
- Crisis-mode rapid feedback (informal Slack poll faster)
- Closed-door briefing where formal survey kills relationships

## Setup

### Tools

- `cli-anything` for Delighted / Typeform / Qualtrics / SurveyMonkey REST API
- `postgresql-mcp` for analytics warehouse + cross-event comparison
- `posthog-mcp` for registration funnel + event website conversion
- `notion-mcp` for survey results archive + qualitative theme tracking
- `slack-mcp` for in-event ops alerts
- Event platform native APIs (Cvent Insights / Bizzabo / Whova)

### Delighted API (NPS)

```bash
export DELIGHTED_TOKEN="<api-key>"   # Delighted > Settings > API
# Base: https://api.delighted.com/v1/
```

### Typeform API (qualitative)

```bash
export TYPEFORM_TOKEN="<personal-access-token>"
# Base: https://api.typeform.com/
```

### Qualtrics API (enterprise alt)

```bash
export QUALTRICS_TOKEN="<api-key>"
export QUALTRICS_DC="ca1"  # data center
# Base: https://${QUALTRICS_DC}.qualtrics.com/API/v3/
```

## Common recipes

### Recipe 1: Post-event NPS via Delighted (48h post-event)

```bash
# Add attendees to Delighted survey
curl -X POST https://api.delighted.com/v1/people \
  -u "$DELIGHTED_TOKEN:" \
  -d "email=$ATTENDEE_EMAIL" \
  -d "name=$ATTENDEE_NAME" \
  -d "properties[event_name]=DevConf 2027" \
  -d "properties[attendee_type]=general" \
  -d "send=true" \
  -d "delay=86400"   # 24 hours after addition
```

Or bulk via CSV:

```bash
# Bulk NPS survey send
curl -X POST https://api.delighted.com/v1/people/batch \
  -u "$DELIGHTED_TOKEN:" \
  -F "people_file=@attendees.csv"
```

### Recipe 2: Pull NPS responses

```bash
curl -X GET https://api.delighted.com/v1/survey_responses \
  -u "$DELIGHTED_TOKEN:" \
  -G \
  -d "since=$(date -u -d '48 hours ago' +%s)"
```

Compute NPS:
```python
responses = json.loads(...)
total = len(responses)
promoters = sum(1 for r in responses if r['score'] >= 9)
detractors = sum(1 for r in responses if r['score'] <= 6)
nps = (promoters - detractors) / total * 100
print(f"NPS: {nps:.0f} (n={total}, promoters={promoters}, detractors={detractors})")
```

### Recipe 3: Typeform qualitative survey

```bash
# Create survey
curl -X POST https://api.typeform.com/forms \
  -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  -d '{
    "title": "DevConf 2027 — Your Feedback",
    "settings": {"is_public": true, "show_progress_bar": true},
    "fields": [
      {
        "type": "rating",
        "title": "How likely are you to recommend DevConf to a colleague?",
        "properties": {"steps": 10, "shape": "star"}
      },
      {
        "type": "long_text",
        "title": "Top 3 highlights of DevConf 2027?"
      },
      {
        "type": "long_text",
        "title": "Top 1 thing we could improve for 2028?"
      },
      {
        "type": "multiple_choice",
        "title": "Which session was your favorite?",
        "properties": {"choices": [{"label": "Sarah K. keynote"}, {"label": "Panel: Building Frontier Teams"}, ...]}
      },
      {
        "type": "yes_no",
        "title": "Can we use your verbatim feedback in marketing materials?"
      }
    ]
  }'

# Get share URL → embed in post-event email
```

### Recipe 4: Pre-event registration funnel (PostHog)

```sql
-- posthog-mcp HogQL: registration funnel
SELECT
  step,
  count() AS users,
  count() * 100.0 / FIRST_VALUE(count()) OVER (ORDER BY step_order) AS conversion_pct
FROM (
  SELECT
    person_id,
    CASE
      WHEN event = 'event_page_view' THEN 1
      WHEN event = 'registration_form_started' THEN 2
      WHEN event = 'registration_form_completed' THEN 3
      WHEN event = 'payment_completed' THEN 4
    END AS step_order,
    event AS step
  FROM events
  WHERE properties.event_name = 'DevConf 2027'
    AND timestamp > now() - interval '90 days'
)
GROUP BY step, step_order
ORDER BY step_order;
```

### Recipe 5: In-event session attendance tracking

```python
# Pull per-session attendance from event platform
sessions = whova.get_event_sessions('devconf-2027')

for s in sessions:
    attendance = whova.get_session_attendance(s['id'])
    postgres.insert('session_attendance', {
        'event_id': 'devconf-2027',
        'session_id': s['id'],
        'session_title': s['title'],
        'capacity': s['capacity'],
        'attended': len(attendance['attendees']),
        'attendance_pct': len(attendance['attendees']) / s['capacity'],
        'avg_duration_min': sum(a['duration'] for a in attendance['attendees']) / len(attendance['attendees'])
    })
```

### Recipe 6: Engagement composite score

```sql
-- postgresql-mcp: per-attendee engagement composite
SELECT
  a.attendee_id,
  -- Session attendance (40%)
  COUNT(DISTINCT sa.session_id)::float / (SELECT COUNT(*) FROM sessions WHERE event_id = 'devconf-2027') AS session_attendance_rate,
  -- Q&A participation (20%)
  COUNT(DISTINCT q.id) AS questions_asked,
  -- Networking connections (20%)
  COUNT(DISTINCT m.id) AS meetings_held,
  -- Sponsor visits (10%)
  COUNT(DISTINCT sv.sponsor_id) AS sponsor_visits,
  -- App usage (10%)
  EXTRACT(epoch FROM SUM(app.session_duration)) / 60 AS app_minutes,
  -- Composite (0-100)
  (
    COUNT(DISTINCT sa.session_id)::float / (SELECT COUNT(*) FROM sessions WHERE event_id = 'devconf-2027') * 40 +
    LEAST(COUNT(DISTINCT q.id), 5) / 5.0 * 20 +
    LEAST(COUNT(DISTINCT m.id), 5) / 5.0 * 20 +
    LEAST(COUNT(DISTINCT sv.sponsor_id), 5) / 5.0 * 10 +
    LEAST(EXTRACT(epoch FROM SUM(app.session_duration)) / 60, 120) / 120.0 * 10
  ) AS engagement_score
FROM attendees a
LEFT JOIN session_attendance sa ON sa.attendee_id = a.attendee_id
LEFT JOIN qa_questions q ON q.author_id = a.attendee_id
LEFT JOIN meetings m ON m.attendee_id = a.attendee_id
LEFT JOIN sponsor_visits sv ON sv.attendee_id = a.attendee_id
LEFT JOIN app_sessions app ON app.attendee_id = a.attendee_id
WHERE a.event_id = 'devconf-2027'
GROUP BY a.attendee_id;
```

### Recipe 7: Speaker performance review

```sql
SELECT
  s.speaker_id,
  s.speaker_name,
  s.session_title,
  sa.attended,
  sa.attendance_pct,
  q.questions_count,
  AVG(sr.rating) AS avg_rating,
  COUNT(DISTINCT yr.viewer_id) AS recording_views_7d
FROM speakers s
LEFT JOIN session_attendance sa ON sa.session_id = s.session_id
LEFT JOIN qa_questions q ON q.session_id = s.session_id
LEFT JOIN session_ratings sr ON sr.session_id = s.session_id
LEFT JOIN youtube_recordings yr ON yr.session_id = s.session_id AND yr.watched_at < (sa.event_date + interval '7 days')
WHERE s.event_id = 'devconf-2027'
GROUP BY s.speaker_id, s.speaker_name, s.session_title, sa.attended, sa.attendance_pct, q.questions_count
ORDER BY avg_rating DESC;
```

### Recipe 8: Per-sponsor ROI report

```python
sponsors = notion.query_db('sponsors-2027')
for sponsor in sponsors:
    leads_captured = cvent.get_leads(sponsor_id=sponsor.id)
    booth_visits = cvent.get_booth_visits(sponsor_id=sponsor.id)
    meetings_held = brella.get_meetings(sponsor_id=sponsor.id)
    impressions = compute_brand_impressions(sponsor)  # logo placements x visibility hours

    report = render_template('sponsor_roi.md',
                             sponsor=sponsor,
                             leads=leads_captured,
                             booth_visits=booth_visits,
                             meetings=meetings_held,
                             impressions=impressions)

    mcp_tool('gmail.send_email',
             to=sponsor.contact_email,
             subject=f"DevConf 2027 — your post-event report",
             body=report)
```

### Recipe 9: Qualitative theme extraction (LLM-assisted)

```python
# Pull all verbatim responses
verbatims = typeform.get_responses(form_id='devconf-2027-survey', field='long_text')

# Cluster themes via Claude
themes = claude_classify(verbatims, prompt='''
Classify each verbatim into one of these themes:
- Speaker quality
- Networking opportunity
- Catering
- Venue
- Schedule pacing
- Sponsor experience
- Accessibility
- App experience
- Cost / value
- Other
Return JSON: {verbatim_id: theme}
''')

# Summarize per theme
for theme, vs in groupby(verbatims, key=themes):
    summary = claude_summarize(vs, prompt=f'Summarize the top 3 messages in this theme: {theme}')
    notion.create_db_row('qualitative-themes', {
        'event': 'devconf-2027', 'theme': theme,
        'count': len(vs), 'summary': summary, 'verbatims': [v.id for v in vs]
    })
```

### Recipe 10: Cross-event benchmarking

```sql
-- Year-over-year NPS + engagement comparison
SELECT
  year,
  COUNT(*) AS registered,
  COUNT(DISTINCT CASE WHEN attended THEN attendee_id END) AS attended,
  AVG(nps_score) AS avg_nps,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY engagement_score) AS median_engagement,
  AVG(cost_per_attendee) AS cost_per_attendee
FROM event_history
WHERE event_name = 'DevConf' AND year BETWEEN 2023 AND 2027
GROUP BY year
ORDER BY year;
```

### Recipe 11: In-event real-time ops alert

```python
# Continuous check-in queue monitoring
while event_active():
    queue_depth = cvent.get_checkin_queue_depth()
    if queue_depth > 50 OR cvent.get_wait_minutes() > 5:
        slack.send_alert(channel='ops',
                         text=f"Check-in queue: {queue_depth} attendees, {cvent.get_wait_minutes()} min wait")
    time.sleep(60)
```

## Examples

### Example A: 600-attendee post-event NPS + qualitative (48-hour cycle)

```
T+24h: Thank-you email to all (with photo + recording teaser)
T+48h: Delighted NPS + Typeform qualitative survey
T+72h: First-tranche responses arrive
T+5d: 60% response rate target
T+7d: Final analysis + verbatims for marketing
T+14d: ROI report drafted

Results:
- NPS: 58 (vs target 50, vs benchmark 50-70 for conferences)
- Engagement composite median: 68/100
- Top theme: "Sarah K. keynote was the highlight" (28% of verbatims)
- Top critique: "Lunch line was too long" (12% of verbatims)
- Verbatim quotes for marketing: 12 collected with permission
```

### Example B: Per-sponsor ROI report (Gold sponsor "Datadog")

```
Datadog Gold Sponsor — DevConf 2027

Investment: $35,000
Leads captured: 240 (opt-in)
Decision-maker leads: 96 (40%)
Booth visits: 580 unique
Meetings held: 3 (Brella pre-booked)
Brand impressions: ~14,000 (stage + lanyards + app)
Estimated pipeline (10% MQL→opp × $80K avg × 25% close): $480K
ROI: 13.7x
Renewal recommendation: Platinum 2028 ($75K)
```

### Example C: Year-over-year benchmarking

```
DevConf YoY (2024 → 2027)
- Registered: 250 → 350 → 450 → 600 (+34% YoY avg)
- NPS: 42 → 51 → 55 → 58
- Engagement composite: 52 → 60 → 63 → 68
- Cost per attendee: $1,800 → $1,650 → $1,500 → $1,400
- Sponsor renewal rate: 50% → 65% → 78% → 82%
```

## Edge cases

### Survey fatigue
If attendees received 3+ surveys from this org in 30 days, response rate collapses. Stagger surveys across events. Use Delighted "throttle by recipient" feature.

### Low NPS sample size
For <50 responses, NPS is noisy. Report total response count alongside NPS. Don't compare to benchmark with n<100.

### Detractor follow-up
Detractors (NPS 0-6) often have specific complaints. Auto-trigger 1:1 follow-up: "We see you rated 4 — would you share more?" Resolve before they post on social.

### Verbatim privacy
Default: verbatims private. To use in marketing, explicit per-verbatim opt-in (Typeform yes/no question).

### Speaker rating bias
First-speaker effect: first session of day gets higher ratings (fresh audience). Last session lower (fatigue). Normalize ratings by session-of-day position.

### Sponsor lead quality dispute
Sponsors sometimes complain "leads weren't qualified." Pre-event set expectations: opt-in leads only, BDR follow-up required, MQL → opp typically 8-15%.

### NPS gaming
If org pushes "rate us 10!" too hard, scores inflate but qualitative deteriorates. Trust the verbatim themes more than the number.

### Multi-event NPS aggregation
Aggregating NPS across multiple events is invalid (different audiences, different value props). Report per-event NPS individually.

### Attendance accuracy
Whova / Bizzabo apps may over-count "attendance" if attendees join then leave immediately. Filter by minimum duration (>10 min).

### Engagement composite weighting
The weights (40/20/20/10/10) are subjective. Document the formula in every report so YoY comparisons are valid. Don't change mid-stream.

### Speaker self-rating bias
Speakers reviewing their own session rating skew positive (don't auto-share). Aggregate speaker performance for committee review, not self-distribution.

### Cross-channel attribution
Attendees registered via paid LinkedIn vs organic search may have different NPS distributions. Segment for analysis.

### Survey completion incentives
$25 gift card for survey completion = +30-40% response rate but selects for incentive-seekers. Use for low-volume scenarios; avoid for representative samples.

## Sources

- **Delighted**: https://delighted.com | API: https://delighted.com/docs/api
- **Typeform**: https://www.typeform.com | API: https://www.typeform.com/developers
- **Qualtrics**: https://api.qualtrics.com
- **SurveyMonkey**: https://developer.surveymonkey.com
- **Bizzabo Analytics**: https://www.bizzabo.com/blog/event-analytics
- **Cvent Insights**: https://www.cvent.com/en/event-marketing-management/event-analytics
- **Whova Analytics**: https://whova.com
- **NPS Reference**: https://www.netpromoter.com
