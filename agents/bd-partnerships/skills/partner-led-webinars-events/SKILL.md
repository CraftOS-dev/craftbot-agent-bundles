<!--
Source: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate + https://www.goldcast.io/blog/co-marketing-webinars + https://www.on24.com/
Zoom Webinars + Goldcast joint event end-to-end (June 2026 SOTA).
-->
# Partner-Led Webinars + Events — SKILL

Run joint webinars and partner-led events end-to-end. **Zoom Webinars** for SMB-to-mid; **Goldcast** for SaaS-native polished events; **ON24** for enterprise. Standard joint webinar mechanic: 50/50 promotion split, co-presented agenda (problem → architecture → live demo → Q&A), follow-up assets, lead routing rules. Cross-link to `co-marketing-campaign-design` for the joint brief.

## When to use

- **Joint webinar with partner** — quarterly cadence with strategic partners.
- **Conference / trade show booth coordination** — joint booth presence.
- **Joint podcast / video series** — co-hosted content.
- **Partner-hosted event amplification** — partner's customer summit; brand sponsors / speaks.
- **Customer webinar with partner co-presenter** — sales-led customer-facing event.
- **Trigger phrases**: "joint webinar with X", "joint event", "Zoom Webinars", "Goldcast", "partner conference sponsorship".

Do NOT use this skill for: **internal webinars** (use `marketing-agent`); **the joint co-marketing brief** (use `co-marketing-campaign-design`); **MDF for event** (use `mdf-allocation-tracking`); **demo logistics** (use `sales-agent`).

## Setup

```bash
export MATON_API_KEY="<key>"
# zoom-mcp configured
# Optional direct API
export ZOOM_API_KEY="<key>"             # Zoom OAuth or JWT
export GOLDCAST_API_KEY="<key>"
export ON24_API_KEY="<key>"
# HubSpot/Salesforce for registration page + lead routing
```

## Common recipes

### Recipe 1: Zoom Webinars — create scheduled webinar

```bash
curl -X POST "https://api.zoom.us/v2/users/me/webinars" \
  -H "Authorization: Bearer $ZOOM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "topic": "Brand × Acme — Joint Revenue Stack Webinar",
    "type": 5,
    "start_time": "2026-08-21T15:00:00Z",
    "duration": 45,
    "timezone": "America/New_York",
    "agenda": "How modern revenue teams unify CDP + attribution with Brand + Acme",
    "settings": {
      "host_video": true,
      "panelists_video": true,
      "approval_type": 0,
      "registration_type": 1,
      "audio": "both",
      "auto_recording": "cloud",
      "alternative_hosts": "vp.partnerships@acme.com",
      "send_1080p_video_to_attendees": true,
      "registrants_email_notification": true
    }
  }'
```

Reference: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate.

### Recipe 2: Zoom — add panelist (partner co-presenter)

```bash
WEBINAR_ID="<from-recipe-1>"
curl -X POST "https://api.zoom.us/v2/webinars/$WEBINAR_ID/panelists" \
  -H "Authorization: Bearer $ZOOM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "panelists": [
      {"name":"Sarah Lee","email":"sarah@acme.com"},
      {"name":"Pat Brand","email":"pat@brand.com"}
    ]
  }'
```

### Recipe 3: Zoom — branding / co-branding setup

```bash
# Custom registration page logo + headers
curl -X PATCH "https://api.zoom.us/v2/webinars/$WEBINAR_ID" \
  -H "Authorization: Bearer $ZOOM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "registrants_confirmation_email": true,
      "registrants_email_notification": true,
      "language_interpretation": {"enable": false}
    }
  }'

# For co-branded experience: use Goldcast / ON24 instead — Zoom's branding is host-only
```

### Recipe 4: Registration page (HubSpot landing page)

```yaml
# Use marketing-agent cross-agent to build HubSpot landing page
landing_page_spec:
  url_brand: "https://brand.com/joint-webinar-acme-q3"
  url_acme: "https://acme.com/joint-webinar-brand-q3"
  registration_form:
    fields: ["first_name","last_name","email","company","title","country"]
    hidden_fields:
      - "utm_campaign=q3-joint-webinar-brand-acme"
      - "utm_source=brand or acme (per landing page)"
    post_submit: "Pass to Zoom Webinars registration API + your CRM"
  social_share_kit: ["LinkedIn post copy","Twitter thread","email signature link"]
```

### Recipe 5: Zoom — programmatic registration (from HubSpot form submit)

```bash
curl -X POST "https://api.zoom.us/v2/webinars/$WEBINAR_ID/registrants" \
  -H "Authorization: Bearer $ZOOM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "email":"sarah@globex.com",
    "first_name":"Sarah",
    "last_name":"Lee",
    "org":"Globex Corp",
    "job_title":"VP Sales",
    "country":"US",
    "custom_questions":[
      {"title":"How did you hear about us?","value":"Brand"}
    ]
  }'
```

Returns join URL; sent to registrant by Zoom automatically.

### Recipe 6: Goldcast — premium event platform (alternative to Zoom)

```bash
# Create event
curl -X POST "https://api.goldcast.io/v1/events" \
  -H "Authorization: Bearer $GOLDCAST_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title":"Brand × Acme Summit",
    "starts_at":"2026-08-21T15:00:00Z",
    "ends_at":"2026-08-21T16:30:00Z",
    "type":"webinar",
    "branding":{"theme":"co-branded","primary_color":"#1A2B3C","logos":["brand.png","acme.png"]},
    "registration_required":true,
    "agenda":[
      {"title":"Welcome + intros","duration_min":5},
      {"title":"The revenue-stack problem","duration_min":10},
      {"title":"Architecture overview","duration_min":10},
      {"title":"Live demo: Brand × Acme","duration_min":15},
      {"title":"Q&A","duration_min":10}
    ]
  }'
```

Goldcast advantages: co-branded UX, networking lounges, real-time analytics. ~$25K+/yr.

Reference: https://www.goldcast.io.

### Recipe 7: ON24 — enterprise webinar platform

```bash
curl -X POST "https://api.on24.com/v3/events" \
  -H "Authorization: $ON24_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title":"Brand × Acme Enterprise Summit",
    "scheduledStartTime":"2026-08-21T15:00:00Z",
    "registrationFormUrl":"https://event.on24.com/register/...",
    "tracks":[{"name":"Main","durationMinutes":45}]
  }'
```

ON24 advantages: deep analytics, lead-scoring integration, enterprise compliance. ~$30K+/yr.

### Recipe 8: Lead routing rules (registration → dual-CRM)

```python
# Webhook handler for Zoom registration event
def on_registration(reg):
    domain = reg["email"].split("@")[1]
    full_name = f"{reg['first_name']} {reg['last_name']}"

    # Route classification
    if is_brand_customer(domain):
        # Brand customer → already in Brand CRM; create lead in Acme CRM
        post_to_acme_crm(reg)
    elif is_acme_customer(domain):
        # Acme customer → create lead in Brand CRM
        post_to_brand_crm(reg)
    elif is_joint_customer(domain):
        # Joint customer → tag as "engaged" in both
        tag_in_brand_crm(reg, "joint_customer_engaged")
        tag_in_acme_crm(reg, "joint_customer_engaged")
    else:
        # New prospect → both
        post_to_brand_crm(reg)
        post_to_acme_crm(reg)

    # UTM source determines attribution
    primary_attribution = "brand" if "utm_source=brand" in reg.get("source_url","") else "acme"
    tag_attribution(reg, primary_attribution)
```

### Recipe 9: Co-presenter prep doc (canonical template)

```yaml
co_presenter_doc:
  webinar: "Brand × Acme — Joint Revenue Stack"
  date: "2026-08-21"

  agenda_with_owners:
    - {section:"Welcome + intros", duration:5, owner:"Brand (Pat)"}
    - {section:"The revenue-stack problem", duration:10, owner:"Brand (Pat)"}
    - {section:"Acme CDP architecture", duration:10, owner:"Acme (Sarah)"}
    - {section:"Live demo (joint integration)", duration:15, owner:"Both — Pat drives, Sarah narrates"}
    - {section:"Q&A", duration:10, owner:"Both"}
    - {section:"Wrap + CTAs", duration:5, owner:"Both"}

  pre_event:
    - "Wed 1-week before: dry run 30 min"
    - "Mon day-of: tech check 15 min"
    - "Tue 30 min before: in greenroom"

  during_event:
    - "Mute when not speaking"
    - "Both visible on camera during intros + Q&A"
    - "Demo: Pat shares screen; Sarah narrates customer-side"

  post_event:
    - "30 min post: short thank-you note to attendees"
    - "Day 1: send recording link + slides"
    - "Day 7: send follow-up CTA + demo links"

  ctas:
    primary_brand: "Book a demo with Brand"
    primary_acme: "Sign up for Acme Trial"
    secondary: "Download joint solution brief"
```

### Recipe 10: Post-event flow

```yaml
post_event_flow:
  recording:
    - "Zoom auto-record to cloud (Recipe 1)"
    - "Download MP4 within 24h"
    - "Edit out tech glitches via video-creator cross-agent"
    - "Upload to YouTube unlisted + Vimeo for embed"

  follow_up_email:
    timing: "30 min post-event"
    sender: "Both sides (Pat + Sarah)"
    content:
      - "Thank you note"
      - "Recording link"
      - "Slides PDF"
      - "Joint solution brief"
      - "Both demo CTAs"

  attendee_segments:
    attended_live: "Hot — book demo within 14 days"
    registered_no_show: "Warm — send recording + nurture seq"
    drop_off: "Watched < 5 min — light touch only"

  metrics_capture:
    - "Registrants, attendees, attendance rate"
    - "Average watch time, engagement"
    - "Q&A questions asked (intent signal)"
    - "Poll responses"
    - "Demo clicks per side"
```

### Recipe 11: Joint event types (decision matrix)

```yaml
event_types:
  joint_webinar:
    duration: "45-60 min"
    cost: "$1-3K (Zoom + design)"
    audience: "100-1000 attendees"
    use_when: "Quarterly joint thought-leadership; demo-driven; broad audience"
  joint_workshop:
    duration: "90 min"
    cost: "$1-2K"
    audience: "20-50 hands-on"
    use_when: "Deep technical content; converts to high-quality leads"
  joint_summit:
    duration: "Half-day to 2 days"
    cost: "$10-50K (Goldcast/ON24)"
    audience: "200-2000"
    use_when: "Strategic moment; major joint announcement; customer + prospect mix"
  joint_podcast_series:
    duration: "30-45 min per episode"
    cost: "$2-5K"
    audience: "1-5K subscribers"
    use_when: "Long-term thought-leadership; recurring touch"
  partner_conference_sponsorship:
    cost: "$10-100K (MDF-eligible)"
    audience: "1000-10K at partner's event"
    use_when: "Co-sell motion via partner's ecosystem"
  joint_dinner_or_roundtable:
    duration: "2-3 hr"
    cost: "$5-15K"
    audience: "12-25 strategic accounts"
    use_when: "ABM tier-1 motion; relationship-focused"
```

### Recipe 12: Joint webinar series cadence

```yaml
quarterly_series:
  q1: "January — Year ahead + roadmap"
  q2: "April — Customer story spotlight"
  q3: "July — Live integration deep-dive"
  q4: "October — Annual best-of + new feature reveal"

per_event_calendar:
  T_minus_6w: "Webinar topic + co-presenter sign-off + JMA (Recipe 9 of co-marketing-campaign-design)"
  T_minus_5w: "Landing page live (Recipe 4); promotional copy approved"
  T_minus_4w: "First promotion (both audiences); registration page open"
  T_minus_2w: "Mid-promotion; LinkedIn ads via marketing-agent"
  T_minus_1w: "Dry run (30 min); reminder email"
  T_minus_2d: "Reminder email + LinkedIn final push"
  T: "Event day; ops checklist + post-event email scheduled"
  T_plus_1d: "Send recording + slides"
  T_plus_7d: "Follow-up CTAs; segment-based outreach"
  T_plus_14d: "Pipeline impact rollup; cross-team retro"
```

## Examples

### Example 1: First joint webinar with new integration partner

**Goal:** Brand × Acme; Aug 21, 45-min, target 300 registrants + 120 attend.

**Steps:**
1. T-6w — Topic agreed; co-presenters identified; JMA via co-marketing skill.
2. T-5w — Recipe 1 webinar created in Zoom.
3. T-5w — Recipe 4 landing page via marketing-agent.
4. T-4w — Promotion launches; UTM-tagged links.
5. T-1w — Recipe 9 dry run; tech check.
6. T-2d — Final reminder; 380 registered (above goal).
7. T — Event runs; 145 attend (above goal); Q&A active.
8. T+1d — Recipe 10 follow-up; recording + slides sent.
9. T+7d — Segmented follow-up CTAs.
10. T+14d — 23 SQLs; 4 closed in subsequent 90 days.

**Result:** Joint webinar exceeds goals; pipeline $580K attributed.

### Example 2: Goldcast premium summit

**Goal:** Half-day joint summit; 5 partners co-present; need co-branded fidelity + networking.

**Steps:**
1. Recipe 6 — Goldcast event created.
2. Multi-track agenda; co-branded theme.
3. Networking lounges per partner.
4. Real-time chat moderated by BD.
5. Post-event: per-attendee engagement scores → CRM lead scoring boost.

**Result:** 800 registrations; 350 attend; premium UX drives 60+ SQLs.

### Example 3: Partner conference sponsorship

**Goal:** Sponsor Acme's customer summit; 1500 expected; booth + speaking slot.

**Steps:**
1. MDF approved (cross to `mdf-allocation-tracking`).
2. Booth design via `canva-mcp` / `figma-mcp`.
3. Speaking session abstract submitted to Acme; accepted.
4. Pre-event: outbound to Acme attendees to schedule booth meetings.
5. Onsite: Recipe 9-style booth ops + lead capture.
6. Post-event: leads in Brand CRM tagged "acme-summit-2026"; nurture seq.

**Result:** 80 leads from booth; 35 meetings booked; 8 closed in 90 days.

## Edge cases / gotchas

- **Zoom branding limits** — Zoom Webinars supports host logo + registration page color theme but not deep co-branding. Use Goldcast or ON24 for premium co-branding.
- **Time zone selection** — picking time zone is political. Target audience TZ; recording covers others.
- **Co-presenter no-show** — backup presenter on both sides; warm-up the backup; document contingency.
- **Tech failure during demo** — pre-record demo as backup; switch to backup if live fails.
- **Q&A questions** — moderate offline; cherry-pick best 5-7; promise written follow-up for rest.
- **Lead routing complexity** — joint customer that registers via Brand vs Acme path: who gets the lead? Document in Recipe 8.
- **Double-opt-in for joint leads** — required under GDPR + CASL; bake into landing page.
- **Zoom registration vs attended event** — only attended counts as engaged; flag in CRM.
- **Recording rights** — JMA must include recording rights; default = both sides can redistribute.
- **Slack-channel for ops** — recommended `#webinar-ops-{date}` for both sides during live.
- **Dry run discipline** — don't skip; live tech issues come from skipped dry runs.
- **Engagement-time-on-page** — Goldcast/ON24 expose this; Zoom hides it. Use Goldcast/ON24 for ABM scoring.
- **Recording asset reuse** — 60-min webinar → 60-sec social clip + 15-sec sales POV + 2-min teaser. Plan during editing.
- **Time zone TZ-confusing email reminders** — Zoom honors registrant TZ; verify.
- **Mid-event speaker drop** — backup presenter ready; pre-pause if needed.
- **Customer protection** — don't pitch live in customer-segment events; education-only.
- **Sponsorship contract** for partner conferences must specify deliverables (booth size, speaking slot, lead list, MDF-eligible activity).
- **Event-platform analytics differ** — Zoom: light; Goldcast: rich; ON24: deepest. Plan analytics needs.
- **Auto-recorded MP4 file size** is large — pre-arrange storage path.

## Sources

- Zoom Webinars API: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate
- Zoom Panelists: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistCreate
- Zoom Registrants: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantCreate
- Goldcast docs: https://www.goldcast.io/
- Goldcast co-marketing blog: https://www.goldcast.io/blog/co-marketing-webinars
- ON24 platform: https://www.on24.com/
- Restream + Demio alternatives: https://restream.io/ + https://demio.com/
- Joint-webinar mechanics — Forrester: https://www.forrester.com/blogs/category/marketing/
- HubSpot landing-page best practices: https://blog.hubspot.com/marketing/landing-page-best-practices
