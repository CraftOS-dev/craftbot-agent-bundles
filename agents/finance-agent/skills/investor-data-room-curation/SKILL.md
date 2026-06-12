<!--
Source: https://www.papermark.com/blog/data-room-for-investors
Source: https://visible.vc/blog/docsend-alternative/
Source: https://visible.vc/blog/docsend-vs-visible-comparison/
Reference role.md: "Investor data room playbook"
-->

# Investor data room curation — sectioned, sequenced, sanitized

Builds the data room investors actually consume. 2026 stack: Visible.vc (founder-first; free Starter), DocSend (best slide-by-slide engagement, $45-$150/mo), Papermark (open-source / self-host alt), Carta IR (only if already on Carta), Foundersuite, Orangedox, Digify. 8-section structure with NDA-gated sequencing (teaser → full).

## When to use

- Pre-fundraise data-room build (Series A/B/C).
- M&A sell-side data room.
- IPO virtual data room buildout.
- Renewal cycle for board-grade always-on data room.
- Trigger phrases: "data room", "investor data room", "DocSend", "Visible.vc", "Papermark", "diligence room", "virtual data room".

NOT for: pitch deck itself (use `pitch-deck-financial-slides`); QoE prep (use `ma-target-screen-and-qoe`).

## Setup

```bash
# Visible.vc — free Starter tier (1 data room, 2 pipelines, 2 decks)
export VISIBLE_API_KEY="<from Visible Settings>"

# DocSend (legacy; Dropbox-owned)
export DOCSEND_API_KEY="<from DocSend dev portal>"

# Papermark (self-host, open source)
docker run -d -p 3000:3000 ghcr.io/mfts/papermark:latest

# Carta IR (only via Carta dashboard)
```

## The 8-section structure (NVCA / industry standard)

```
SECTION 1 — Overview
  • Executive summary (2-3 pages)
  • Pitch deck (most recent investor version)
  • Demo video / product walkthrough
  • Founder bios
  • Company timeline / milestones

SECTION 2 — Cap Table + Equity
  • Cap table (Carta export, current)
  • SAFE / Convertible note schedule
  • Option pool detail
  • Latest 409A memo
  • Shareholder agreements / Side Letters

SECTION 3 — Financials
  • Three-statement model (current + 3-5yr forecast)
  • Last 3 years annual P&L (or LTM if pre-3yr)
  • Last 12 months monthly P&L
  • Balance sheet as of last close
  • Bank statements (last 3 months)
  • Tax returns last 2 years
  • R&D credit study (if applicable)

SECTION 4 — Customer / Cohort Metrics
  • ARR by customer (top 25)
  • Cohort retention triangle
  • NRR / GRR analysis
  • CAC / LTV by channel + segment
  • Pipeline + sales velocity
  • Customer concentration analysis

SECTION 5 — Contracts
  • Top 20 customer MSAs / order forms
  • Vendor contracts (top 10 by spend)
  • Hosting / infrastructure contracts (AWS, GCP, etc.)
  • Office leases
  • Insurance policies

SECTION 6 — IP / Legal
  • Patent filings + grants
  • Trademarks
  • Domain ownership
  • Open source license inventory (BlackDuck / FOSSA scan)
  • Pending litigation (or "None")
  • DPA / privacy compliance (GDPR, CCPA, SOC 2)

SECTION 7 — Team + Employment
  • Org chart current
  • All employment agreements (founders + key hires)
  • Confidentiality + IP assignment (PIIA) all employees
  • Severance / change-of-control agreements
  • Benefits summary
  • Compensation analysis (Carta / Pave benchmarks)

SECTION 8 — Diligence Q&A
  • Investor Q&A log (anonymized)
  • Customer references list
  • Advisor / board references
  • Press / coverage archive
```

## Sequencing — NDA-gated access

```
TIER 1 — Teaser (public-ish; pre-NDA)
  Pitch deck (redacted; customer logos generic)
  Sections 1 (Overview) — high-level

TIER 2 — Soft NDA (verbal commitment; warm intro)
  Sections 1 + 3 (Financials summary only) + 4 (Cohort summary)
  Limited cap table — % only, no dollar amounts

TIER 3 — Mutual NDA signed
  All 8 sections
  Full cap table
  Customer logos + ARR by customer
  Detailed cohort metrics
  Top contracts

TIER 4 — IOI / Term Sheet stage
  Section 8 unlocked (customer references list)
  Granular financials (drill-down)
  Source-of-truth integrations (Stripe / Xero read-only)
```

## Common recipes

### Recipe 1 — Folder structure (file-organizer)

```bash
# Build canonical structure
mkdir -p data_room/{01_Overview,02_CapTable,03_Financials,04_Cohort_Metrics,05_Contracts,06_IP_Legal,07_Team,08_Diligence_QA}
mkdir -p data_room/03_Financials/{annual,monthly,model,banking,tax}
mkdir -p data_room/05_Contracts/{customer,vendor,infrastructure,lease,insurance}
mkdir -p data_room/06_IP_Legal/{patents,trademarks,litigation,compliance}
mkdir -p data_room/07_Team/{org_chart,agreements,PIIA,benefits,comp}
```

### Recipe 2 — Visible.vc data room upload

```bash
# Create data room
curl -X POST "https://api.visible.vc/v1/datarooms" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Series A","nda_required":true}'

# Upload file to section
curl -X POST "https://api.visible.vc/v1/datarooms/$DR_ID/files" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -F "file=@03_Financials/annual/2025_P&L.pdf" \
  -F "section_id=03_Financials"
```

### Recipe 3 — DocSend granular tracking

```bash
# Upload + share link with email gating
curl -X POST "https://docsend.com/api/v1/documents" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
  -F "file=@pitch_deck.pdf" \
  -F "verify_email=true" \
  -F "track_engagement=true"

# Get engagement analytics
curl "https://docsend.com/api/v1/documents/$DOC_ID/views" \
  -H "Authorization: Bearer $DOCSEND_API_KEY"
```

### Recipe 4 — Papermark self-host (open-source)

```bash
# Clone + run
git clone https://github.com/mfts/papermark.git
cd papermark
cp .env.example .env  # set NEXTAUTH_SECRET, DATABASE_URL
docker-compose up -d
# Access at http://localhost:3000
```

### Recipe 5 — Watermark + dynamic NDA

```python
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def watermark_pdf(input_pdf, output_pdf, recipient_email):
    # Create watermark
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 24)
    c.setFillColorRGB(0.7, 0.7, 0.7, alpha=0.3)
    c.saveState(); c.translate(300, 400); c.rotate(45)
    c.drawCentredString(0, 0, f"Confidential — {recipient_email}")
    c.restoreState()
    c.save()
    buffer.seek(0)

    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    watermark = PdfReader(buffer).pages[0]
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)
    with open(output_pdf, "wb") as f:
        writer.write(f)
```

### Recipe 6 — Cap table sanitization (% only)

```python
import pandas as pd

def sanitize_cap_table(df, redact_dollars=True):
    sanitized = df.copy()
    if redact_dollars:
        for col in ["amount_invested", "share_price", "preferred_price"]:
            if col in sanitized.columns: sanitized[col] = "[REDACTED]"
    # Keep ownership %, share class, vesting
    return sanitized[["holder_name_anon", "share_class", "ownership_pct", "vesting_start", "vesting_end"]]
```

### Recipe 7 — Q&A log template

```markdown
# Diligence Q&A Log — Acme Series A

| Date | Investor | Question | Answer | File ref |
|------|----------|----------|--------|----------|
| 2026-06-08 | FundX | "What's your top-1 customer concentration?" | 12% (Stripe — multi-year MSA expiring 2028) | 04_Cohort_Metrics/customer_concentration.xlsx |
| 2026-06-09 | FundY | "Why GM decline Q1?" | One-time hosting migration cost; normalized Q2 | 03_Financials/Q1_explanation_memo.pdf |
```

### Recipe 8 — Engagement-based prioritization

```python
import pandas as pd

def engagement_priority(views_df):
    """views_df: investor × file × time_spent_seconds"""
    investor_summary = views_df.groupby("investor").agg(
        total_time_min=("time_spent_seconds", lambda x: x.sum()/60),
        files_viewed=("file", "nunique"),
        last_visit=("viewed_at", "max"),
    ).sort_values("total_time_min", ascending=False)
    return investor_summary

# Top engagers get founder follow-up first
```

### Recipe 9 — Data room readiness checklist

```python
CHECKLIST = {
    "01_Overview": ["pitch_deck.pdf", "executive_summary.pdf", "demo_video.mp4"],
    "02_CapTable": ["cap_table_export.xlsx", "409a_memo.pdf", "safe_schedule.xlsx"],
    "03_Financials": ["3stmt_model.xlsx", "last_3yr_p&l.pdf", "ttm_monthly.pdf", "bank_statements/", "tax_returns/"],
    "04_Cohort_Metrics": ["arr_by_customer.xlsx", "cohort_triangle.xlsx", "nrr_grr_analysis.pdf"],
    "05_Contracts": ["top20_customer_msas/", "top10_vendor_contracts/", "hosting_contract.pdf"],
    "06_IP_Legal": ["patent_filings/", "trademark_register.pdf", "fossa_oss_report.pdf"],
    "07_Team": ["org_chart.png", "employment_agreements/", "piia/", "comp_benchmarks.pdf"],
    "08_Diligence_QA": ["qa_log.md", "customer_references.xlsx"]
}

def check_readiness(data_room_path):
    import os
    missing = {}
    for section, files in CHECKLIST.items():
        section_path = os.path.join(data_room_path, section)
        if not os.path.isdir(section_path):
            missing[section] = files
            continue
        for f in files:
            if not os.path.exists(os.path.join(section_path, f.rstrip("/"))):
                missing.setdefault(section, []).append(f)
    return missing
```

## Examples

### Example 1: Series B data room build (2 weeks pre-launch)

**Goal:** Investor-ready data room.

**Steps:**
1. Recipe 1 → folder structure.
2. Recipe 9 → checklist; fill gaps.
3. Recipe 2 → upload to Visible.vc.
4. Recipe 5 → watermark every PDF dynamically per investor.
5. Recipe 6 → sanitize cap table for tier 2 access.
6. Recipe 7 → Q&A log template; populate during process.
7. Recipe 8 → weekly engagement review; prioritize follow-ups.

**Result:** Tier-gated, watermarked, tracked data room.

### Example 2: M&A sell-side data room

**Goal:** Strategic acquirer diligence.

**Steps:**
1. Recipe 1 + 9 → full 8-section structure.
2. Recipe 5 → high-security watermarking.
3. Add Section 9: integration analysis (synergies, employee retention).
4. Stage access: stage 1 (LOI prep) — sections 1+3; stage 2 (NDA + LOI) — all sections; stage 3 (exclusivity) — Q&A unlimited.
5. Recipe 8 → identify most-engaged bidder.

**Result:** Process control + diligence facility.

## Edge cases / gotchas

- **DocSend slide-by-slide spying.** Founders love it; some investors find it intrusive. Disclose if you're tracking.
- **NDA enforcement.** Most data rooms don't enforce NDA; they just gate access. Real enforcement = legal action post-leak.
- **Carta IR is bundled.** Free if you're on Carta cap-table. But no NDA, no granular watermarking. Use as complement, not replacement.
- **Papermark self-host.** Open source; full control + privacy. But you maintain the server.
- **Sensitive doc redaction.** Customer logos, dollar amounts in cap table, salary specifics, FBR / IRS audit letters. Redact before uploading.
- **Watermark performance.** Dynamic per-recipient watermarks slow large PDFs. Pre-render top 5-10 docs per investor.
- **Visible.vc tier limits.** Free Starter: 1 data room. Paid plans needed for multi-room (Series B+ companies running M&A + fundraise simultaneously).
- **Customer references gating.** Reserve for IOI / term sheet stage. Premature reference calls burn customer goodwill.
- **Bank statements last 3 months only.** Older = not material; older statements expose patterns you don't want exposed.
- **Tax returns — only LAST 2 years.** Older = not relevant; older returns may show pre-pivot data that confuses diligence.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Papermark 2026 data room guide: https://www.papermark.com/blog/data-room-for-investors
- Visible.vc DocSend alternative: https://visible.vc/blog/docsend-alternative/
- Visible vs DocSend: https://visible.vc/blog/docsend-vs-visible-comparison/
- Visible.vc Data Rooms: https://visible.vc/product/data-rooms/
- DocSend API: https://docsend.com/api/v1/docs
- Papermark GitHub: https://github.com/mfts/papermark
- Carta IR: https://carta.com/investor-relations/

## Related skills

- `pitch-deck-financial-slides` — primary asset in Section 1.
- `three-statement-financial-model-tied` — Section 3 master file.
- `term-sheet-nvca-grade-review` — diligence triggered post-term-sheet.
- `ma-target-screen-and-qoe` — sell-side version of this skill.
