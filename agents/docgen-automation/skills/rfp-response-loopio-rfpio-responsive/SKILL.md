---
name: rfp-response-loopio-rfpio-responsive
description: Automate RFP / RFI / RFQ / security questionnaire (CAIQ, SIG, SIG-Lite, DDQ) responses via Loopio, Responsive (formerly RFPIO), Qvidian, Arphie. Question extraction + answer-library matching + SME routing + portal submission. Use when the user says "fill out this RFP", "auto-respond to security questionnaire", "Loopio / Responsive / RFPIO API", "build RFP answer library", "match incoming questions to canonical answers".
---

# RFP / questionnaire response — Loopio / Responsive (RFPIO) / Arphie

This skill extracts RFP / questionnaire questions, matches them against a canonical answer library, routes low-confidence matches to SMEs, and ships the populated response. Subject-matter expertise (security, legal, finance) is delegated to the appropriate sibling agent or human.

## When to use

User says:

- "Fill out this RFP / RFI / RFQ"
- "Security questionnaire (CAIQ / SIG / SIG-Lite / VSA)"
- "DDQ (due diligence questionnaire)"
- "Loopio / Responsive / RFPIO / Qvidian / Ombud / Arphie"
- "RFP answer library"
- "Auto-match incoming questions"
- "Submit RFP via portal" (e.g., RFP360, Vendorful)

Companion skills:
- `ocr-paper-doc-extraction` — extract Qs from scanned PDF RFPs.
- `ai-summarization-clause-extraction` — long-form RFP summarization.
- `smart-form-jotform-formstack` — if RFP is delivered as a form.

## Setup

```bash
# Responsive (formerly RFPIO) — broadest enterprise default
# https://www.responsive.io/api-documentation
export RESPONSIVE_TOKEN="..."

# Loopio
# https://www.loopio.com/  (REST API on paid plans)
export LOOPIO_TOKEN="..."

# Qvidian (Upland)
# https://uplandsoftware.com/qvidian/
export QVIDIAN_API_KEY="..."

# Arphie — LLM-native (2024+)
# https://www.arphie.ai/
export ARPHIE_API_KEY="..."

# Self-built fallback (no SaaS budget)
pip install sentence-transformers pandas openpyxl python-docx
# sentence-transformers for semantic matching against your own CSV answer library
```

Auth / API keys:
- `RESPONSIVE_TOKEN` — Responsive Public API token; OAuth flow per their docs.
- `LOOPIO_TOKEN` — OAuth 2.0 access token; client_credentials grant.
- `ARPHIE_API_KEY` — bearer token.

## Common recipes

### Recipe 1: Pick the platform

| Platform | Best for | Pricing (approx 2026) | API |
|---|---|---|---|
| Responsive (RFPIO) | broadest 2026 default; large answer library | $20k-80k/year | Full REST + webhooks |
| Loopio | mid-enterprise; strong UX | $15k-50k/year | REST API |
| Qvidian | regulated industries (gov/healthcare) | quote | REST API |
| Ombud | sales-tech-stack-integrated | quote | REST |
| Arphie | LLM-native (2024+); fastest auto-fill | quote | REST |
| Self-built (CSV + sentence-transformers) | <100 RFPs/year, no SaaS budget | $0 | n/a |

### Recipe 2: Extract questions — Word / Excel input

```python
# pip install python-docx openpyxl
from docx import Document as Doc
import openpyxl

def extract_from_docx(path):
    doc = Doc(path)
    qs = []
    for tbl in doc.tables:
        for row in tbl.rows:
            cells = [c.text.strip() for c in row.cells]
            # Assume column 0 is question, column 1 is response cell
            if cells[0] and cells[0].endswith("?"):
                qs.append({"q": cells[0], "answer_cell_ref": (tbl, row)})
    return qs

def extract_from_xlsx(path, sheet, q_col, a_col):
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet]
    qs = []
    for r in range(2, ws.max_row + 1):
        q = ws.cell(r, q_col).value
        if q:
            qs.append({"q": q, "row": r, "answer_col": a_col})
    return qs, wb
```

### Recipe 3: Extract questions — scanned PDF input

```bash
# Use Gemini OCR via gemini-ocr-mcp; or Tesseract for ASCII
tesseract input/rfp-scan.pdf output/rfp-text -l eng --psm 1
# PSM 1 = automatic page segmentation with OSD
# Then split into questions via regex on numbering: ^\s*\d+\.\s+
```

For complex layouts: `easyocr-mcp` / `gemini-ocr-mcp` MCPs handle bounding boxes + structured output.

### Recipe 4: Responsive — submit RFP for auto-fill

```bash
curl -X POST https://api.responsive.io/v1/projects \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN" \
  -F "file=@input_rfp.xlsx" \
  -F "name=Acme Corp RFP 2026-Q2" \
  -F "auto_fill=true" \
  -F "confidence_threshold=0.7"
# Returns { "project_id": "p_abc123", "status": "processing" }

# Poll for completion
curl https://api.responsive.io/v1/projects/p_abc123/status \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN"

# Download populated response
curl https://api.responsive.io/v1/projects/p_abc123/export \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN" \
  -o output_response.xlsx
```

### Recipe 5: Loopio — search answer library

```bash
curl "https://api.loopio.com/data/v2/entries?query=multi-factor+authentication" \
  -H "Authorization: Bearer $LOOPIO_TOKEN"
# Response: list of matching library entries with content + tags + last-updated
```

### Recipe 6: Loopio — auto-fill questionnaire via projects API

```bash
curl -X POST https://api.loopio.com/data/v2/projects \
  -H "Authorization: Bearer $LOOPIO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Q2 Security Questionnaire",
    "type": "RFP",
    "fileUrl": "https://uploads/.../rfp.xlsx",
    "autoMatch": true
  }'
```

### Recipe 7: Self-built — semantic matching with sentence-transformers

```python
# When no SaaS budget — works for <100 RFPs/year
# pip install sentence-transformers pandas numpy
from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")
library = pd.read_csv("answer_library.csv")   # cols: q_canonical, a, category, last_reviewed
lib_embs = model.encode(library["q_canonical"].tolist(), convert_to_tensor=True)

incoming = ["Do you support SSO/SAML?", "What is your data retention policy?"]
inc_embs = model.encode(incoming, convert_to_tensor=True)

scores = util.cos_sim(inc_embs, lib_embs)  # (n_in, n_lib)
results = []
for i, q in enumerate(incoming):
    best_idx = int(scores[i].argmax())
    confidence = float(scores[i][best_idx])
    results.append({
        "q": q,
        "matched_q": library.iloc[best_idx]["q_canonical"],
        "a": library.iloc[best_idx]["a"],
        "confidence": confidence,
        "needs_sme": confidence < 0.7
    })
pd.DataFrame(results).to_csv("matched.csv", index=False)
```

### Recipe 8: Route low-confidence to SME via Slack

```python
# slack-mcp: post message with question + suggested answer + Accept/Reject buttons
import json
from slack_sdk import WebClient
c = WebClient(token=os.environ["SLACK_TOKEN"])
for row in unmatched_rows:
    c.chat_postMessage(
        channel="#rfp-review",
        text=f"RFP Q needs review",
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Q:* {row['q']}\n*Suggested:* {row['a']}\n*Confidence:* {row['confidence']:.2f}"}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Accept"}, "value": json.dumps({"id": row["id"], "action": "accept"})},
                {"type": "button", "text": {"type": "plain_text", "text": "Edit"}, "value": json.dumps({"id": row["id"], "action": "edit"})}
            ]}
        ]
    )
```

### Recipe 9: Populate Excel answer cells from matched results

```python
# Continuing from Recipe 2 + 7
matched = pd.read_csv("matched.csv")
qs, wb = extract_from_xlsx("input_rfp.xlsx", "Questions", q_col=2, a_col=3)
ws = wb["Questions"]
for q_row in qs:
    answer = matched[matched["q"] == q_row["q"]]["a"].iloc[0]
    ws.cell(q_row["row"], q_row["answer_col"]).value = answer
wb.save("output_rfp.xlsx")
```

### Recipe 10: Portal submission via Playwright

```python
# playwright-mcp — for portal-only RFP platforms (RFP360, Vendorful)
import asyncio
from playwright.async_api import async_playwright

async def submit():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://rfp360.com/login")
        await page.fill('input[name="email"]', os.environ["RFP360_USER"])
        await page.fill('input[name="password"]', os.environ["RFP360_PASS"])
        await page.click('button[type=submit]')
        await page.goto(f"https://rfp360.com/projects/{PROJECT_ID}/submit")
        await page.set_input_files('input[type=file]', "output_rfp.xlsx")
        await page.click('button:has-text("Submit Response")')
        await browser.close()

asyncio.run(submit())
```

### Recipe 11: Update answer library after each RFP

```python
# Post-submission — capture SME edits back into library
edited = pd.read_csv("sme_edits.csv")   # cols: q, accepted_answer, was_edited
for _, row in edited.iterrows():
    if row["was_edited"]:
        # Append variant to library
        library = pd.concat([library, pd.DataFrame([{
            "q_canonical": row["q"],
            "a": row["accepted_answer"],
            "category": "auto-captured",
            "last_reviewed": datetime.utcnow().isoformat()
        }])], ignore_index=True)
library.to_csv("answer_library.csv", index=False)
```

### Recipe 12: Cite-check CAIQ / SIG answers

For CAIQ (Consensus Assessment Initiative Questionnaire) / SIG (Shared Assessments) answers, cite source policies:

```text
Q: Do you have a documented incident response plan?
A: Yes. See Section 4.2 of our SOC 2 Type II report dated 2025-10-31 (auditor: Schellman & Co). Plan reviewed annually; last drill 2026-Q1.
```

Always include: policy doc reference + version + auditor + last review date.

## Examples

### Example 1: Enterprise security questionnaire (SIG-Lite, ~150 questions)

**Goal:** Auto-fill SIG-Lite from existing security policies + SME review of low-confidence.
**Steps:**
1. Recipe 2 — extract Qs from SIG-Lite Excel.
2. Recipe 7 — semantic match against `answer_library.csv` (300+ canonical Qs).
3. Recipe 8 — route confidence <0.7 (≈20 Qs) to security team via Slack.
4. Recipe 9 — populate cells with matched + SME-approved answers.
5. Recipe 11 — capture SME edits back into library.
6. Submit via email or portal.

**Result:** 150-Q SIG-Lite filled in <2 hours vs 2-day manual.

### Example 2: Mid-market RFP via Responsive

**Goal:** Auto-respond to a 60-Q RFP using Responsive answer library.
**Steps:**
1. Recipe 4 — POST `/projects` with file + auto_fill=true.
2. Wait for `status=completed` webhook.
3. Recipe 4 — download populated xlsx.
4. Human reviewer spot-checks low-confidence Qs (Responsive flags inline).
5. Submit.

**Result:** 60-Q RFP turned around in 1 day instead of 1 week.

### Example 3: Scanned-PDF RFP from a regulator

**Goal:** Govt RFP delivered as scanned PDF; no Excel format.
**Steps:**
1. Recipe 3 — OCR via Gemini / Tesseract.
2. Split into numbered Qs.
3. Recipe 7 — semantic match.
4. Manually compile into target Word response template.
5. Submit via portal (Recipe 10).

**Result:** Paper-RFP digitized + answered without manual transcription.

## Edge cases / gotchas

- **Question extraction misses sub-questions.** Many RFPs use `1.a / 1.b / 1.c` nesting; flat numeric extractors miss them. Use a recursive parser.
- **Excel merged cells.** RFPs often merge cells across rows; openpyxl reads only top-left value. Use `for r in ws.iter_rows(values_only=False)` and handle `MergedCell` explicitly.
- **Confidence threshold tuning.** 0.7 is a starting point; calibrate per library quality. Too high → too many SME escalations; too low → wrong answers slip through.
- **Stale answers in library.** Security postures evolve (new SOC 2, new pen test). Add `last_reviewed` field; reject answers older than 12 months.
- **CAIQ vs SIG vs SIG-Lite vs VSA.** Each has a different question format + numbering. Maintain a question-format-mapping table.
- **Portal session expiration.** RFP portals often log out after 15-30 min idle. Playwright scripts need re-auth logic.
- **No vendor lock-in escape.** Migrating from Responsive → Loopio requires manual re-tagging; export-then-import doesn't preserve hierarchical taxonomy.
- **Sensitive answers.** Don't auto-fill questions like "Has your company ever been breached?" — always SME-route.
- **Auto-fill ≠ truth.** Always have a human sign-off before submission. The agent never submits unilaterally on regulator/government RFPs.
- **Excel formula breakage.** When inserting answers, preserve existing formulas; use `ws.cell(r, c).value = ...` not `.formula`.
- **Multi-tenant Loopio workspaces.** `library_id` differs per workspace; never hardcode.
- **Arphie / new LLM-native platforms.** Hallucination risk. Always human-review LLM-suggested answers before submission.

## Sources

- [Responsive (RFPIO) API](https://www.responsive.io/api-documentation) — REST API.
- [Loopio](https://www.loopio.com/) — RFP platform.
- [Qvidian (Upland)](https://uplandsoftware.com/qvidian/) — regulated-industry RFP.
- [Arphie](https://www.arphie.ai/) — LLM-native RFP (2024+).
- [Shared Assessments SIG](https://sharedassessments.org/) — SIG / SIG-Lite reference.
- [Cloud Security Alliance CAIQ](https://cloudsecurityalliance.org/research/cloud-controls-matrix/) — CAIQ + CCM.
- [sentence-transformers](https://www.sbert.net/) — open-source semantic similarity.
- [Playwright](https://playwright.dev/) — portal automation.
- Sister skills: `ocr-paper-doc-extraction`, `ai-summarization-clause-extraction`, `smart-form-jotform-formstack`.
