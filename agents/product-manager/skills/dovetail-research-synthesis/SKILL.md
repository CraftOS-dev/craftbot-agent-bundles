<!--
Source: https://dovetail.com/help/api
Dovetail v3 API, GA 2025-2026
-->
# Dovetail Research Synthesis — SKILL

Dovetail v3 is the SOTA research repository (interview transcripts + tagged highlights + AI-assisted theme extraction). This pack covers uploading transcripts, tagging, querying highlights by tag, and aggregating themes into Notion repos.

## When to use

- Synthesizing 5+ customer interviews into 3-7 themes.
- Tagging interview transcripts by JTBD outcome, pain point, or product area.
- Producing the "8 of 11 founders mentioned X" theme counts for PRDs.
- Building a continuous research backlog (Teresa Torres opportunity-solution-tree style).
- Cross-linking research highlights to Linear issues or Notion PRDs.

Trigger phrases: "synthesize these interviews", "find the top themes", "tag this transcript", "what did customers say about X", "summarize research on Y".

**Fallback:** Notably (notably.ai) is the free alt — same shape (REST API + tags), narrower feature set. Use Notably when `DOVETAIL_API_TOKEN` is absent.

## Setup

```bash
# Dovetail REST API — no native MCP yet (June 2026); use cli-anything + curl
curl -fsSL "https://dovetail.com/api/v1/users/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

Auth:
- `DOVETAIL_API_TOKEN` — workspace token from https://dovetail.com/settings/api. Paid plan ($199/mo+ Business; $99/mo Starter).
- For Notably fallback: `NOTABLY_API_KEY` from https://app.notably.ai/settings/api (free tier ample for solo founders).

API surface (Dovetail v1):
- `POST /projects` / `GET /projects/{id}`
- `POST /projects/{id}/notes` (upload transcript)
- `POST /tags` / `GET /tags`
- `POST /highlights` / `GET /projects/{id}/highlights?tag=X`
- `POST /insights` (synthesized theme cards)
- `GET /search?q=X&project_id=...`

## Common recipes

### Recipe 1: Create a project for an interview round

```bash
curl -X POST "https://dovetail.com/api/v1/projects" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Solo-Founder Onboarding Q3 2026",
    "description": "11 interviews with $29/mo plan users; D7-retention focus",
    "tags": ["q3-2026","onboarding","solo-founder"]
  }'
```

### Recipe 2: Upload a transcript (Fathom / Otter / tl;dv export)

```bash
# Dovetail accepts plain-text or VTT. Fathom exports VTT directly.
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/notes" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Interview P3 — Sara, marketplace seller" \
  -F "participants=Sara" \
  -F "date=2026-06-02" \
  -F "file=@./transcripts/P3-sara.vtt"
```

### Recipe 3: AI auto-tag transcript

```bash
# Dovetail's "Insights AI" suggests tags from a taxonomy
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/notes/$NOTE_ID/auto-tag" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -d '{"taxonomyId":"<taxonomy-id>","model":"claude-sonnet"}'
```

### Recipe 4: Query highlights by tag

```bash
# Pull every quote tagged "onboarding-friction" across all interviews in the project
curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/highlights?tag=onboarding-friction" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '.highlights[] | {participant, quote: .text, source_note: .note.title, timestamp}'
```

### Recipe 5: Count theme occurrences (for "X of Y" claims)

```bash
# Get unique interviewees mentioning a tag
curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/highlights?tag=inbox-overload" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '[.highlights[].note.participants[]] | unique | length'

# Total interviews in the project
curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/notes" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '.notes | length'

# → "8 of 11 founders" — write this directly into the PRD problem statement
```

### Recipe 6: Create an Insight card (synthesized theme)

```bash
curl -X POST "https://dovetail.com/api/v1/insights" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -d '{
    "projectId": "'$PROJECT_ID'",
    "title": "Onboarding friction — solo founders drop after step 2",
    "description": "8/11 founders cited friction at the workspace-setup step. Common cause: unclear what to do next.",
    "highlights": ["<hl1>","<hl2>","<hl3>"],
    "tags": ["theme:onboarding-friction","priority:high"]
  }'
```

### Recipe 7: Export themes to Notion research repo

```bash
# 1. Pull insights from Dovetail
DOV_INSIGHTS=$(curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/insights" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN")

# 2. For each insight, create a Notion repo entry
echo "$DOV_INSIGHTS" | jq -c '.insights[]' | while read insight; do
  TITLE=$(echo "$insight" | jq -r '.title')
  DESC=$(echo "$insight" | jq -r '.description')
  mcp tool notion.create_page \
    --parent '{"database_id":"<research-repo-db>"}' \
    --properties "{\"Topic\":{\"title\":[{\"text\":{\"content\":\"$TITLE\"}}]},\"Method\":{\"select\":{\"name\":\"Interview\"}},\"Sample size\":{\"number\":11}}" \
    --children "[{\"type\":\"paragraph\",\"paragraph\":{\"rich_text\":[{\"text\":{\"content\":\"$DESC\"}}]}}]"
done
```

### Recipe 8: Cross-link a highlight to a Linear issue

```bash
# Use the highlight's permalink in the Linear issue body
HL_URL=$(curl -fsSL "https://dovetail.com/api/v1/highlights/$HIGHLIGHT_ID" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" | jq -r '.permalink')

mcp tool linear.create_issue \
  --teamKey "PROD" \
  --title "Fix onboarding step 2 confusion" \
  --description "Validated by interview: $HL_URL"
```

### Recipe 9: Notably fallback (free)

```bash
# Same shape; Notably uses /projects and /tags but slightly different field names
curl -X POST "https://api.notably.ai/v1/projects/$PROJECT_ID/transcripts" \
  -H "Authorization: Bearer $NOTABLY_API_KEY" \
  -F "file=@./transcripts/P3-sara.txt" \
  -F "title=P3 — Sara"

curl -fsSL "https://api.notably.ai/v1/projects/$PROJECT_ID/observations?tag=onboarding-friction" \
  -H "Authorization: Bearer $NOTABLY_API_KEY"
```

### Recipe 10: Build a tag taxonomy from scratch

```bash
# Create a parent taxonomy then nested tags
curl -X POST "https://dovetail.com/api/v1/tags" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -d '{"name":"jtbd","parent":null}'

# Sub-tags per JTBD outcome
for outcome in "find-customer-reply" "block-distractions" "track-deadlines"; do
  curl -X POST "https://dovetail.com/api/v1/tags" \
    -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
    -d "{\"name\":\"$outcome\",\"parent\":\"jtbd\"}"
done
```

## Examples

### Example 1: Synthesize a 5-interview round into a PRD problem statement
**Goal:** Convert raw transcripts into a citation-rich PRD problem section.

**Steps:**
1. Upload all 5 transcripts (Recipe 2).
2. Auto-tag (Recipe 3); clean up.
3. Query highlights per tag; cluster into 3-7 themes (Recipe 4).
4. Count occurrences for each theme (Recipe 5).
5. Create Insight cards (Recipe 6).
6. Sync themes to Notion research DB (Recipe 7).
7. Write the PRD problem section with explicit counts: "8 of 11 founders cited onboarding friction."

**Result:** PRD problem section is cited, defensible, and traceable back to raw transcripts.

### Example 2: Continuous discovery (weekly cadence)
**Goal:** Run Teresa Torres style weekly customer touchpoints into the same Dovetail project.

**Steps:**
1. Weekly: upload 1-2 new interviews.
2. Re-run auto-tag.
3. Watch theme counts climb; flag once a theme hits 5+ interviewees (signal to scope).
4. Promote winning themes to Insight cards.
5. Insights become Linear issues for the next discovery cycle.

**Result:** Living theme list that drives next-quarter roadmap candidates.

## Edge cases / gotchas

- **Paid plan only (Dovetail).** Starter ($99/mo) supports the API. Notably is the free fallback (still has REST API).
- **AI auto-tag accuracy.** ~70-80% on first pass; manual cleanup is mandatory. Don't trust unverified tags for "X of Y" claims.
- **Tag taxonomy hygiene.** Without a published taxonomy, tag drift balloons (15+ near-duplicate tags). Start with 10-15 parent tags, sub-tags below.
- **Transcript file formats.** Best results from Fathom VTT or Otter SRT (speaker labels intact). Plain text without speakers degrades AI tagging.
- **PII redaction.** Dovetail does NOT redact PII automatically. Strip emails/names from transcripts before upload if compliance requires.
- **Rate limits.** 60 req/min on the v1 API; bulk uploads should be sequential, not parallel.
- **Highlight permalinks** require Dovetail SSO for read access (unless you've enabled public-share); for internal cross-links this is fine.
- **5+ interviews is the floor.** Theme claims with N<5 are anecdotal; agent should flag and push for more interviews before scoping.
- **Notably API field names differ.** Dovetail uses `highlights`, Notably uses `observations`. Code abstracted recipe 9 vs 4 to handle both.

## Sources

- [Dovetail API docs](https://dovetail.com/help/api)
- [Dovetail v3 release notes](https://dovetail.com/blog/dovetail-v3)
- [Dovetail Insights AI](https://dovetail.com/help/insights-ai)
- [Notably API (free alt)](https://www.notably.ai/api)
- [Teresa Torres continuous discovery](https://www.producttalk.org/continuous-discovery)
- [Rob Fitzpatrick — The Mom Test](http://momtestbook.com)
