<!--
Source: https://docsend.com + https://carta.com/best-cap-table-software/
Investor data room curation — DocSend + Google Drive + index page
-->
# Investor Data Room — Curation + Tracked Sharing

DocSend for analytics-tracked sharing (who opened what, time spent per page) with Google Drive as the backup. Standard structure: company / financials / cap-table / legal / product / customers / team / IP folders. Index page in Notion serves as the navigable map. Used for fundraise diligence, M&A, board materials archive.

## When to use

- Opening a fundraise — diligence data room.
- Pre-M&A diligence for an acquirer or as the seller.
- Board materials archive setup (mirror of fundraise data room).
- Refresh of a stale data room (annually or pre-round).

Trigger phrases: "data room", "diligence folder", "DocSend setup", "fundraise prep", "Series B data room", "M&A data room".

## Setup

```bash
# DocSend API
curl -fsSL "https://api.docsend.com/v1/me" \
  -H "Authorization: Bearer $DOCSEND_API_KEY"

# Google Drive MCP
mcp tool google-drive.list_folders --parent root
```

Auth / API key requirements:
- `DOCSEND_API_KEY` — DocSend → Settings → API (paid tier, ~$15-150/mo).
- `GOOGLE_OAUTH_TOKEN` — for Drive access (workspace admin).
- `NOTION_API_KEY` — for the index page.

## Common recipes

### Recipe 1: Standard data room folder structure (Google Drive)

```bash
mcp tool google-drive.create_folder --parent root --name "Data Room — Series B"

for folder in "00 - Index" "01 - Company" "02 - Financials" "03 - Cap Table" \
              "04 - Legal" "05 - Product" "06 - Customers" "07 - Team" \
              "08 - IP + Tech" "09 - Market + Competitive" "10 - References"; do
  mcp tool google-drive.create_folder --parent "<root-data-room-id>" --name "$folder"
done
```

### Recipe 2: Per-folder content checklist

```markdown
## 01 - Company
- [ ] One-pager
- [ ] Pitch deck (latest version)
- [ ] Company strategy doc
- [ ] Board composition + bios
- [ ] Articles of incorporation

## 02 - Financials
- [ ] 3-yr historical financials (P&L, BS, CF)
- [ ] FP&A model (5-yr forward)
- [ ] Monthly metrics (MRR / churn / cohorts) — 24 months
- [ ] Unit economics (CAC, LTV, payback)
- [ ] Audit report (if available)

## 03 - Cap Table
- [ ] Carta / Pulley link or PDF export
- [ ] 409A latest
- [ ] Option pool ledger
- [ ] SAFE / convertible note ledger

## 04 - Legal
- [ ] Articles + bylaws
- [ ] All board consents
- [ ] All stockholder consents
- [ ] Material contracts (customer top-10, vendor top-10)
- [ ] IP assignments (every employee)
- [ ] Employee NDAs

## 05 - Product
- [ ] Product roadmap (12-18 month)
- [ ] Architecture diagram
- [ ] Tech stack list
- [ ] Security overview (SOC 2 if available)

## 06 - Customers
- [ ] Top 10 customer list (revenue, contract length)
- [ ] Cohort retention table
- [ ] NPS / CSAT scores
- [ ] Logo wall

## 07 - Team
- [ ] Org chart
- [ ] Headcount plan (12-month)
- [ ] Founder bios + LinkedIn
- [ ] Key hire bios

## 08 - IP + Tech
- [ ] Patents (filed + granted)
- [ ] Trademarks
- [ ] Domain portfolio
- [ ] Open-source license inventory

## 09 - Market + Competitive
- [ ] TAM / SAM / SOM analysis
- [ ] Competitive matrix
- [ ] Wardley map
- [ ] Industry reports cited

## 10 - References
- [ ] Customer references (3-5 with contact)
- [ ] Investor references
- [ ] Advisor list
```

### Recipe 3: Create the Notion index page

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<fundraise-hub>"}' \
  --properties '{"title":[{"text":{"content":"Data Room Index — Series B"}}]}' \
  --children-markdown './data-room-index.md'
```

Template:
```markdown
# Data Room — Series B (2027)

## Navigation
| Folder | Drive | DocSend | Status |
|---|---|---|---|
| 01 Company | [link] | [tracked] | Complete |
| 02 Financials | [link] | [tracked] | Complete |
| 03 Cap Table | [link] | [tracked] | Pending 409A refresh |
| 04 Legal | [link] | [tracked] | Complete |
| ... | | | |

## Access management
- Investor list: [Notion DB link]
- Access requested by: [name, firm, date]
- Granted: [date, by whom]
- Revoked: [date, reason]

## Latest changes
- 2027-04-15 — Added Q1 cohort retention table
- 2027-04-10 — Refreshed cap table post-option grant
```

### Recipe 4: Upload + DocSend-track a document

```bash
# 1. Upload to DocSend
DOC_ID=$(curl -X POST "https://api.docsend.com/v1/documents" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
  -F "file=@./financials-2027-Q1.pdf" \
  -F "title=Financials Q1 2027" \
  | jq -r '.id')

# 2. Create a tracked link
LINK=$(curl -X POST "https://api.docsend.com/v1/documents/$DOC_ID/links" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
  -d '{
    "name":"Series B — Lead VC review",
    "verification":"email",
    "passcode":"<optional>",
    "expires":"2027-07-01"
  }' | jq -r '.url')

echo "Share with lead: $LINK"
```

### Recipe 5: Per-investor tracked link (granular analytics)

```bash
# Create a unique link per investor for engagement-by-investor tracking
for INVESTOR in "sequoia.com" "accel.com" "a16z.com"; do
  curl -X POST "https://api.docsend.com/v1/documents/$DOC_ID/links" \
    -H "Authorization: Bearer $DOCSEND_API_KEY" \
    -d "{\"name\":\"Series B — $INVESTOR\",\"verification\":\"email\",\"email_domains\":[\"$INVESTOR\"]}"
done
```

### Recipe 6: Pull engagement analytics

```bash
curl -fsSL "https://api.docsend.com/v1/documents/$DOC_ID/visits" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
| jq '.visits[] | {visitor_email, time_on_doc, pages_viewed, last_page, viewed_at}'
```

Use this to: (a) prioritize follow-up with high-engagement investors, (b) identify which sections are most-viewed (signals their interest area).

### Recipe 7: Share Drive folder with investor

```bash
mcp tool google-drive.share \
  --folder "<data-room-root>" \
  --email "investor@vc.com" \
  --role reader \
  --notify true \
  --message "Data room access for Series B diligence. Index page: [Notion link]. Reach out with questions."
```

### Recipe 8: Watermark every PDF before upload

```bash
# Add per-recipient watermark — discourages leaks
for INVESTOR in "Sequoia" "Accel" "a16z"; do
  pdftk financials-2027-Q1.pdf stamp watermark.pdf output "fin-$INVESTOR.pdf"
  # Replace watermark.pdf with text containing investor name
done
```

### Recipe 9: Audit log — who accessed what when

```bash
curl -fsSL "https://api.docsend.com/v1/audit-logs?days=30" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
| jq -r '.logs[] | "\(.timestamp) | \(.action) | \(.document) | \(.user)"' \
| tee data-room-audit-2027-04.log

mcp tool notion.update_page --page-id "<audit-page>" --append "$(cat data-room-audit-2027-04.log)"
```

### Recipe 10: Refresh stale data room (annual)

```bash
# Find documents older than 90 days
curl -fsSL "https://api.docsend.com/v1/documents?older_than=90d" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
| jq '.documents[] | {title, last_updated, id}' \
| tee stale-docs.json

# Surface to CEO for refresh decisions
mcp tool notion.create_page --parent "<fundraise-hub>" \
  --properties '{"title":[{"text":{"content":"Stale data room refresh"}}]}' \
  --children-markdown "Review and refresh: $(cat stale-docs.json)"
```

### Recipe 11: Revoke access post-round

```bash
# After round closes, revoke non-winning investor access
for LINK_ID in $(curl -fsSL "https://api.docsend.com/v1/links?status=active" -H "Authorization: Bearer $DOCSEND_API_KEY" | jq -r '.links[] | select(.investor != "lead") | .id'); do
  curl -X DELETE "https://api.docsend.com/v1/links/$LINK_ID" -H "Authorization: Bearer $DOCSEND_API_KEY"
done

mcp tool google-drive.remove_share --folder "<data-room>" --email "<non-winning-investor>"
```

### Recipe 12: Free fallback — Google Drive only

```bash
# If no DocSend budget, use Drive native with permission audit
mcp tool google-drive.list_permissions --folder "<data-room>" \
| jq -r '.permissions[] | "\(.emailAddress) | \(.role) | \(.expirationTime // "no expiry")"' \
| tee drive-access-audit.csv

# Set 90-day expiry on all investor shares
mcp tool google-drive.update_permission \
  --permission-id "<investor-perm-id>" \
  --expiration-time "2027-08-01T00:00:00Z"
```

## Examples

### Example 1: Series B fundraise data room from scratch

**Goal:** Open Series B, 4 weeks of prep, polished data room.

**Steps:**
1. Create folder structure (Recipe 1).
2. Populate each folder against checklist (Recipe 2). Track gaps.
3. Build Notion index (Recipe 3).
4. Upload financials + cap table + legal core docs to DocSend (Recipe 4).
5. Create per-investor tracked links for top 10 targets (Recipe 5).
6. Share Drive folder for non-tracked docs (Recipe 7).
7. Set 90-day expiry on all shares (Recipe 12).
8. Weekly engagement review during round (Recipe 6).
9. Post-round revoke (Recipe 11).

**Result:** Tracked diligence, engagement-driven follow-up, audit log for compliance.

### Example 2: M&A seller-side data room

**Goal:** Acquirer requests diligence; lead with structure.

**Steps:**
1. Mirror standard structure (Recipe 1) but add M&A-specific: customer churn waterfall, contract assignability matrix, employee retention plans.
2. Watermark every PDF with acquirer name (Recipe 8).
3. Use email-verified DocSend links only — no public sharing.
4. Daily engagement check (Recipe 6) — pace acquirer's diligence.

**Result:** Negotiation leverage from data discipline.

## Edge cases / gotchas

- **No watermark = leak risk.** M&A and competitive fundraise — always watermark per recipient.
- **DocSend has free tier limits.** Free covers 4 docs / month. Series A+ needs paid for tracked links at scale.
- **Drive sharing is forever by default.** Set expiry on every investor share. Revoke post-round.
- **Cap table out-of-date = killer.** Refresh 409A and cap table every 6 months OR before any round opens.
- **IP assignments missing = deal killer.** Every employee + contractor must have signed IP assignment. Build the checklist.
- **Customer contract assignability matters in M&A.** Many SaaS contracts forbid assignment without consent. Audit early.
- **One source of truth.** If a number is in financials AND cap table AND board pack, it MUST match. Auditors will check.
- **Audit log retention.** DocSend keeps logs 90-180 days depending on plan. Export monthly to Notion (Recipe 9).
- **Permission inheritance in Drive.** Sharing a folder shares children. Be deliberate about subfolder shares.
- **Pre-round preview deck vs full data room.** Don't share the full data room on first conversation. Start with the deck. Open data room post-term sheet.
- **GDPR / PII risk.** Customer lists may contain PII. Redact for non-NDA investors.
- **Watermark + screenshots.** Watermarks deter but don't prevent. For high-sensitivity docs, use DocSend "no download" mode.

## Sources

- [DocSend (Dropbox)](https://docsend.com)
- [Carta — Best Cap Table Software 2026](https://carta.com/best-cap-table-software/)
- [Visible.vc data room guide](https://visible.vc/blog/investor-data-room/)
- [Cooley GO — Founder fundraising docs](https://www.cooleygo.com/)
- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents/)
