---
name: robin-spellbook-harvey-ai-contract-review
description: AI-assisted contract review tooling — Robin AI (web + Word add-in), Spellbook (Word add-in for drafting + risk highlighting), Harvey AI (enterprise legal LLM), LegalSifter (concept detectors). Use these for first-pass redlines on contracts over 10 pages or when speed matters more than depth. Output still needs human review and the consult-an-attorney disclaimer.
---

# AI-Assisted Contract Review — Robin AI, Spellbook, Harvey, LegalSifter

These are tools the agent recommends to the user — the agent does not directly call them unless the user grants Word/web access. The agent's role: explain when to reach for each, set them up, and integrate output into the contract-review playbook.

## When to use

Reach for this skill when:

- User says "this contract is 40+ pages; can we speed up review?"
- User says "I have Robin AI / Spellbook / Harvey — how do I use it for X?"
- User wants AI-assisted markup directly in Microsoft Word.
- User wants concept-level extraction across a corpus of contracts.
- User mentions "GC-in-a-box" / "AI lawyer" / "AI redlining."

Companion to `contract-review-msa-nda-employment` — that skill drives the clause checklist; this skill drives the AI-acceleration layer.

## Setup

### Robin AI (web + Word add-in)
```bash
# Robin AI is a paid SaaS — no CLI install. User signs up at:
# https://www.robinai.com/
# Add the Microsoft Word add-in:
#   Word → Insert → Get Add-ins → search "Robin AI" → Add
# Or download from Office Store: https://appsource.microsoft.com/
```

### Spellbook (Word add-in)
```bash
# Spellbook is a Word add-in subscription
# https://www.spellbook.legal/
# Install via Office Store search "Spellbook"
# Or direct: https://appsource.microsoft.com/en-us/product/office/WA200005876
```

### Harvey AI (enterprise web)
```bash
# Harvey AI is enterprise-tier (Big Law focus); waitlist + enterprise sales
# https://www.harvey.ai/
# Not typically available for solo founders / small teams — use Robin / Spellbook instead
```

### LegalSifter (web + API)
```bash
# LegalSifter exposes a "Sifters" API for custom concept extraction
# Sign up: https://www.legalsifter.com/
# API docs: https://api.legalsifter.com/docs (enterprise)
pip install requests
```

Auth / API keys:
- `ROBIN_API_KEY` — Robin AI enterprise REST API; available on Business and Enterprise tiers.
- `SPELLBOOK_API_KEY` — Spellbook is primarily a Word add-in; programmatic access limited.
- `HARVEY_API_KEY` — enterprise only.
- `LEGALSIFTER_API_KEY` — Sifters API; enterprise pricing.
- No keys needed for the Word add-in workflow — the add-in handles auth inside Word.

## Common recipes

### Recipe 1: Robin AI — first-pass redline of an MSA
```text
Workflow (web app):
1. Sign in to https://app.robinai.com
2. Upload the MSA (PDF or DOCX).
3. Pick playbook: "MSA — Buyer-Side" or "MSA — Seller-Side".
4. Wait 2-5 minutes for AI markup.
5. Download as DOCX with tracked changes + plain-English summary.
6. Open the DOCX → review each suggested change with Track Changes ON.
```
Robin AI's strength: clause-level risk classification (e.g., "Indemnity cap is unusually low") with citation to its training corpus. Weakness: doesn't know YOUR negotiation posture or the deal context — every suggestion needs the user to accept/reject.

### Recipe 2: Spellbook — draft a clause inside Word
```text
Workflow (Word add-in):
1. Open Word; sign in to Spellbook in the Spellbook pane.
2. Place cursor where the clause should go.
3. Spellbook pane → "Draft Clause" → describe ("Mutual indemnity capped at fees paid in last 12 months; carve-outs for IP, confidentiality, willful misconduct, data breach").
4. Spellbook inserts a draft. Edit in place.
5. Re-run "Review" on the document to flag risky language.
```
Spellbook's strength: drafting NEW clauses + suggesting alternatives. Weakness: smaller training set than Robin / Harvey for review.

### Recipe 3: Spellbook — risk-highlight existing contract
```text
Workflow:
1. Open existing contract DOCX in Word.
2. Spellbook pane → "Review" → pick risk profile.
3. Spellbook highlights risky terms in yellow/red and inserts comments.
4. Walk top-to-bottom; for each comment, decide accept / modify / reject.
5. Export to PDF for the memo.
```

### Recipe 4: LegalSifter — extract concepts across a corpus
```python
import requests
import os

API = "https://api.legalsifter.com/v1"
key = os.environ["LEGALSIFTER_API_KEY"]
headers = {"Authorization": f"Bearer {key}"}

# Upload a contract
with open("contract.pdf", "rb") as f:
    upload = requests.post(f"{API}/documents", headers=headers, files={"file": f})

doc_id = upload.json()["id"]

# Run a Sifter set (e.g., "MSA Buyer-Side" or custom)
sift = requests.post(
    f"{API}/documents/{doc_id}/sift",
    headers=headers,
    json={"sifter_set": "msa-buyer-side"}
)
results = sift.json()
for concept in results["concepts"]:
    print(concept["name"], concept["passage"], concept["risk"])
```
Use for: "show me every indemnity clause across 50 vendor contracts" or "find all auto-renewal terms." Custom Sifters = enterprise feature.

### Recipe 5: Robin AI REST API (enterprise tier)
```bash
# https://docs.robinai.com (enterprise tier)
curl -X POST https://api.robinai.com/v1/reviews \
  -H "Authorization: Bearer $ROBIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "document_url": "https://your-storage/contract.pdf",
    "playbook": "msa-buyer-side",
    "callback_url": "https://your-app/webhook"
  }'

# Poll for completion
curl -H "Authorization: Bearer $ROBIN_API_KEY" \
  https://api.robinai.com/v1/reviews/<review-id>
```

### Recipe 6: Pick the right tool for the contract
| Contract | Length | Recommended tool |
|---|---|---|
| MSA / SaaS / Cloud / Vendor | 10+ pp | Robin AI (review) + Spellbook (draft new clauses) |
| NDA (Common Paper / Bonterms) | <5 pp | Manual; no AI needed |
| Employment / Contractor | 5-15 pp | Spellbook (in Word) + state-law check |
| DPA / privacy | 5-20 pp | Manual + `dpa-data-processing-agreement` skill |
| Term sheet | 1-5 pp | Manual + `term-sheet-review-series-a-typical-terms` |
| SAFE / note | 4-8 pp | Manual + `safe-convertible-note-yc-template` |
| Corpus extraction (50+ contracts) | varies | LegalSifter (Sifters API) |
| Big-Law-scale matter | any | Harvey AI (if user has access) |

### Recipe 7: Integrate Robin output into the memo
```python
# Parse Robin's DOCX comments + tracked changes into the flag table format
# used by contract-review-msa-nda-employment Recipe 4
from docx import Document
doc = Document("robin_redline.docx")

flags = []
for para in doc.paragraphs:
    for run in para.runs:
        if run.font.color and run.font.color.rgb:  # highlighted text
            flags.append({
                "section": para.text[:60],
                "issue": run.text,
                "tier": "TBD"
            })

# Hand off to the contract-review skill for human prioritization
```

### Recipe 8: Cost / pricing reference (June 2026)
| Tool | Pricing (approx) | Tier |
|---|---|---|
| Robin AI | $50-200/user/mo (web); enterprise quote (API) | Solo → enterprise |
| Spellbook | $89-159/user/mo | Solo / SMB |
| Harvey AI | Enterprise quote (typically $5k+/mo) | Big Law / enterprise |
| LegalSifter | Enterprise quote | Enterprise |

Always confirm current pricing on vendor sites — these change.

## Examples

### Example 1: 60-page vendor SaaS MSA, founder is buyer
**Goal:** Reduce review time from 6 hours to 2 hours.
**Steps:**
1. Upload MSA to Robin AI web app (Recipe 1) with playbook "MSA — Buyer-Side."
2. Download DOCX redline; open in Word.
3. Pair with `contract-review-msa-nda-employment` Recipe 2 clause checklist — walk each Robin flag and confirm against the checklist.
4. For draft alternative language, run Spellbook (Recipe 2) on each red-flag clause.
5. Produce memo + redline per `contract-review-msa-nda-employment` Recipe 6.
6. Append disclaimer; ship to user's licensed counsel for final review.

**Result:** Redline + memo ready for counterparty negotiation, in ~2 hours instead of ~6.

### Example 2: Drafting a custom indemnity clause
**Goal:** Insert a mutual indemnity clause with specific carve-outs into a Word contract.
**Steps:**
1. Open contract in Word.
2. Place cursor where the indemnity section should go.
3. Spellbook pane → "Draft Clause" → describe carve-outs.
4. Accept the draft; edit any vendor-specific language.
5. Save with track changes off; export PDF for review.

**Result:** A custom indemnity clause drafted in ~2 minutes vs ~15 manual.

### Example 3: Extract auto-renewal terms across 30 vendor contracts
**Goal:** Find every auto-renewal clause across a vendor contract repository for the CFO.
**Steps:**
1. Upload all 30 contracts to LegalSifter (Recipe 4).
2. Run the "Auto-Renewal" Sifter.
3. Export results to CSV.
4. Mark notice deadlines on a shared calendar.

**Result:** A CSV mapping each contract to its non-renewal deadline.

## Edge cases / gotchas

- **AI output is suggestion, not authority.** Robin / Spellbook / Harvey reflect training-corpus tendencies — not your deal context. Always review every suggestion against the playbook in `contract-review-msa-nda-employment`.
- **Confidentiality / data residency.** Robin AI, Spellbook, Harvey all process contract text on their servers. Verify the vendor's data residency + retention before uploading sensitive deal documents. Enterprise tiers offer EU / SOC 2 / customer-data-not-used-for-training options.
- **Privilege does NOT attach.** AI agent output is not protected by attorney-client privilege. Treat uploads as if they could be discoverable. For highly sensitive matters, route through licensed counsel who maintains privilege.
- **Word add-in version drift.** Office Insider builds occasionally break add-ins. If Spellbook / Robin add-in stops working, check Office build version (File → Account → About Word). Roll back to current channel if needed.
- **Robin / Spellbook may surface false-positive flags.** Especially on industry-specific terms (e.g., healthcare BAA terms, FedRAMP-required clauses). Cross-check against domain skills.
- **LegalSifter requires Sifter training for accuracy.** Off-the-shelf Sifters work for common clauses; custom concepts (e.g., "indemnity carve-out for AI hallucination") need training data — enterprise feature.
- **Harvey AI is gated.** Most solo founders / small teams cannot access Harvey. Don't recommend it as a first-line tool; use Robin / Spellbook.
- **API rate limits.** Robin's enterprise API caps at a tenant-specific rate; LegalSifter caps per Sifter run. Budget time for large batch reviews.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing binding legal documents.**

## Sources

- [Robin AI](https://www.robinai.com/) — contract review platform; Word add-in + REST API (enterprise).
- [Spellbook](https://www.spellbook.legal/) — AI legal copilot for Word.
- [Harvey AI](https://www.harvey.ai/) — enterprise legal-specialized LLM.
- [LegalSifter](https://www.legalsifter.com/) — AI contract concept extraction (Sifters).
- [Office Add-ins (Microsoft AppSource)](https://appsource.microsoft.com/) — install paths for Word add-ins.
- [Robin AI Documentation](https://docs.robinai.com) — REST API reference (enterprise tier).
- [Spellbook Help Center](https://help.spellbook.legal/) — Word add-in workflow.
- Sister skill: `contract-review-msa-nda-employment` (clause checklist + redline format).
