---
name: contract-redlining-automation
description: Generate track-change Word redlines + AI clause suggestions — Spellbook (Word add-in), Robin AI, Harvey AI, Ironclad AI Assist, DraftWise, programmatic via python-docx + redlines lib. Pre-canned redline playbooks (vendor-favorable → customer-favorable). Use when the user says "redline this contract", "track changes", "Spellbook / Robin AI / Harvey / DraftWise", "AI redlines", "python-docx track changes", "redlines library".
---

# Contract redlining automation — Spellbook / Robin AI / python-docx / redlines

This skill ships the redline pipeline. AI add-ins (Spellbook, Robin AI, DraftWise) for human-in-the-loop in Word; programmatic (`python-docx` + `redlines`) for diff-based batch redlines.

## When to use

User says:

- "Redline this MSA per our playbook"
- "Track changes Word output"
- "Compare V1 vs V2 with track changes"
- "Spellbook / Robin AI / Harvey AI / DraftWise"
- "python-docx redlines"
- "AI clause suggestions in Word"
- "Apply our standard fallback positions"

Companion skills:
- `ai-summarization-clause-extraction` — finds where to redline.
- `contract-template-authoring-msa-nda` — source of standard / fallback language.
- `e-signature-docusign-adobe-sign-pandadoc` — sign once accepted.
- Always hand off binding interpretation to `legal-counsel`.

## Setup

```bash
# python-docx (Word edit)
pip install python-docx

# redlines (pip lib for inline diff in Word)
pip install redlines

# diff-match-patch (Google's diff algorithm)
pip install diff-match-patch

# Track-change generation via python-docx-redlining (lower-level)
pip install python-docx-redlining

# Spellbook — Word add-in (paid; no SDK)
# https://www.spellbook.legal/

# Robin AI — REST API (enterprise tier)
# https://www.robinai.com/

# Harvey AI — enterprise (typically white-glove)
# https://www.harvey.ai/

# DraftWise — Word add-in (paid; team plans)
# https://draftwise.com/

# Ironclad AI Assist — bundled in Ironclad
# https://ironcladapp.com/products/ai/
```

## Common recipes

### Recipe 1: Pick the tool

| Tool | Best for | Cost (approx 2026) | Strength |
|---|---|---|---|
| Spellbook | Solo / small firm; Word add-in | $99/user/mo | Clause suggest + fallback; broad market |
| Robin AI | Mid-market in-house teams | Enterprise | Negotiation playbook + tracked changes |
| Harvey AI | BigLaw + Fortune 500 | Enterprise | LLM stack purpose-built for law |
| DraftWise | Law firms (negotiation insight) | $79/user/mo+ | Precedent + clause comparison |
| Ironclad AI Assist | Existing Ironclad customers | Bundled | In-CLM workflow |
| LegalOn (US) | Mid-market in-house | $100/user/mo+ | Issue spotter + redlines |
| python-docx + redlines | Programmatic / batch | Free | Diff-based; no AI |
| Manual + AI prompting | Ad-hoc | API cost | Use Claude/Gemini suggestions, paste into Word |

Default: Spellbook for solo / small teams; Robin AI for mid-market; programmatic python-docx for batch.

### Recipe 2: python-docx — basic track-change insertion (XML-level)

```python
# python-docx doesn't natively expose track changes; use raw XML
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document("acme-msa.docx")
def add_ins(para, new_text, author="Reviewer"):
    """Insert tracked-change addition at end of a paragraph."""
    ins = OxmlElement("w:ins")
    ins.set(qn("w:id"), "1")
    ins.set(qn("w:author"), author)
    ins.set(qn("w:date"), datetime.datetime.now().isoformat() + "Z")
    r = OxmlElement("w:r")
    rt = OxmlElement("w:t")
    rt.text = new_text
    rt.set(qn("xml:space"), "preserve")
    r.append(rt)
    ins.append(r)
    para._p.append(ins)

# Example: append clause to §4
for para in doc.paragraphs:
    if "Section 4" in para.text:
        add_ins(para, " Notwithstanding the foregoing, this Section shall survive termination for a period of 3 years.")
        break
doc.save("acme-msa-redlined.docx")
```

### Recipe 3: redlines lib — text-level diff with markup

```python
from redlines import Redlines

original = "Customer shall pay all fees due within 30 days of invoice."
revised  = "Customer shall pay all fees due within 45 days of invoice."
r = Redlines(original, revised)
print(r.output_markdown)
# → Customer shall pay all fees due within <del>30</del><ins>45</ins> days of invoice.
print(r.output_rich)         # for HTML / console
```

Then convert markup → docx track changes via XML wrapping.

### Recipe 4: Full document diff → tracked-change Word

```python
# Given v1.docx and v2.docx, produce v2-tracked.docx with v1→v2 changes marked
from docx import Document
from redlines import Redlines

doc_v1 = Document("v1.docx")
doc_v2 = Document("v2.docx")
v1_paras = [p.text for p in doc_v1.paragraphs]
v2_paras = [p.text for p in doc_v2.paragraphs]

doc_out = Document("v2.docx")  # base structure
for i, p in enumerate(doc_out.paragraphs):
    if i < len(v1_paras) and v1_paras[i] != v2_paras[i]:
        # Mark this paragraph with tracked deletion of v1 + insertion of v2
        r = Redlines(v1_paras[i], v2_paras[i])
        # Replace para runs with mix of <w:del> + <w:ins>
        apply_tracked_changes(p, v1_paras[i], v2_paras[i])
doc_out.save("v2-tracked.docx")
```

### Recipe 5: Playbook-driven redlines (vendor-favorable → customer-favorable)

```python
PLAYBOOK = [
    {
        "find": r"Customer agrees to indemnify Vendor for any and all",
        "replace": "Customer agrees to indemnify Vendor solely for third-party claims arising from Customer's gross negligence or willful misconduct in connection with",
        "comment": "Cap indemnity to third-party claims; align with mutual carve-out."
    },
    {
        "find": r"Vendor's liability shall not exceed the fees paid in the prior twelve \(12\) months",
        "replace": "Vendor's liability shall not exceed two (2) times the fees paid in the prior twelve (12) months",
        "comment": "Push from 1x to 2x cap; standard ask."
    },
    {
        "find": r"This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least ninety \(90\) days",
        "replace": "This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least thirty (30) days",
        "comment": "Reduce non-renewal notice 90→30 days."
    },
]
for rule in PLAYBOOK:
    apply_redline(doc, rule)
```

### Recipe 6: Robin AI — REST request for redlines

```bash
curl -X POST https://api.robinai.com/v1/contracts/redline \
  -H "Authorization: Bearer $ROBIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_text": "<base64 docx>",
    "playbook_id": "vendor_pb_2026_q2",
    "party_role": "customer"
  }'
# Returns tracked-change docx + per-clause rationale
```

### Recipe 7: Spellbook — Word add-in workflow

User flow (no API; UI-driven):
1. Open contract in Word.
2. Spellbook task pane → Review → "Suggest issues".
3. Spellbook flags non-standard clauses + suggests fallbacks.
4. Accept / reject each suggestion → Word tracks the change.
5. Save + send for counter-signature.

Best for: solo lawyers + small firms; per-doc AI assist.

### Recipe 8: DraftWise — precedent-based suggestions

DraftWise compares your draft against precedent clauses in your firm's database. UI-driven; surfaces redlines from prior similar contracts as suggestions.

### Recipe 9: Accept/reject programmatically

```python
from docx import Document
from docx.oxml.ns import qn

doc = Document("redlined.docx")
# Accept all insertions, reject all deletions
for ins in doc.element.findall(".//" + qn("w:ins")):
    # Promote the contained run to a normal run
    parent = ins.getparent()
    idx = list(parent).index(ins)
    for child in list(ins):
        parent.insert(idx, child)
        idx += 1
    parent.remove(ins)
for delete in doc.element.findall(".//" + qn("w:del")):
    parent = delete.getparent()
    parent.remove(delete)
doc.save("accepted.docx")
```

### Recipe 10: AI suggestion via Claude (no add-in)

```python
import anthropic
client = anthropic.Anthropic()
clause_text = "Customer shall pay all fees due within 30 days of invoice."
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=1000,
    system="You are senior commercial counsel. Suggest 2-3 fallback positions for this clause; specify which is most-favored vs middle-ground.",
    messages=[{"role":"user","content": f"Clause to redline: {clause_text}\n\nParty role: vendor.\nGoal: protect cash flow."}]
)
print(resp.content[0].text)
```

### Recipe 11: Batch redline of N similar contracts (renewal cycle)

```python
PLAYBOOK = [...]
for path in glob.glob("renewals/*.docx"):
    doc = Document(path)
    for rule in PLAYBOOK:
        apply_redline(doc, rule)
    doc.save(path.replace("renewals/", "redlined/"))
```

### Recipe 12: Diff report (HTML side-by-side)

```python
from redlines import Redlines
from pathlib import Path

v1 = Path("v1.txt").read_text()
v2 = Path("v2.txt").read_text()
r = Redlines(v1, v2, markdown_style="red_green")
Path("diff.html").write_text(r.output_rich)
```

Hand to legal as a quick visual review.

### Recipe 13: Counter-redline + comment chain

```python
# When counterparty redlines, we redline their redlines; preserve chain
# Open their docx (track changes visible); use python-docx to add <w:ins>/<w:del>
# with our author name on top — preserves the negotiation history
```

Avoid "accept all then redline" — destroys the audit chain.

## Examples

### Example 1: Inbound vendor contract → playbook redline

**Goal:** Receive vendor's MSA draft; apply our customer-favorable playbook.
**Steps:**
1. Recipe 11 — batch loop or single-doc.
2. Recipe 5 — playbook rules applied as tracked changes.
3. Recipe 12 — HTML side-by-side for VP review.
4. Manual review by legal counsel.
5. Recipe 9 — accept/reject post-review.
6. Send back to vendor; counter-redline cycle.

**Result:** First-pass redlines in seconds; reduce legal review time 60-80%.

### Example 2: AI-assisted negotiation in Word (Spellbook)

**Goal:** Solo GC reviewing 30 contracts/week.
**Steps:**
1. Recipe 7 — Spellbook task pane.
2. Accept/reject suggestions inline.
3. Track-change docx out to counterparty.

**Result:** Higher leverage per attorney; consistent positions.

### Example 3: M&A diligence — redline 200 contracts to standard form

**Goal:** Acquirer wants 200 acquired-target contracts re-aligned with their template.
**Steps:**
1. Recipe 6 — Robin AI batch via REST.
2. Receive 200 redlined Word docs.
3. Recipe 12 — HTML reports for each.
4. `legal-counsel` reviews top 20 by deal value.

**Result:** Standardized contract base post-acquisition.

## Edge cases / gotchas

- **python-docx + track changes is fragile.** XML schema differs across Word versions; test on Word 2019, 2021, 365.
- **Don't strip prior track changes blindly.** They're audit trail; layer on top.
- **Author + date attribution.** Every `<w:ins>` / `<w:del>` should have `w:author` + `w:date` — review history depends on it.
- **Style + numbering disruption.** Edits inside numbered lists can break list numbering; preserve `numPr` references.
- **Markdown round-trip loses formatting.** Don't markdown → docx; edit in docx XML.
- **AI fallback positions need legal review.** Always hand off to `legal-counsel` before sending.
- **Redline conflict.** Two people editing the same paragraph — Word merges via track changes; design workflow to single-track at a time.
- **Field codes + cross-references.** Word fields (like "Page 5 of N") can break on redline if not handled.
- **Tables.** Track changes inside table cells; XML manipulation must scope to cell content.
- **Comments vs redlines.** Comments are sidebar annotations; redlines are textual changes. Use both: comment for rationale, redline for the change.
- **AI hallucinated clauses.** Verify quoted "standard market" benchmarks; many are made up by LLM.
- **Robin AI / Spellbook tier required.** Free demos lack the playbook + analytics; verify license.
- **Confidentiality of LLM-routed contracts.** Cloud LLM-based redliners send the doc to vendor; ensure DPA + retention policy + zero-retention if available.
- **Numbering after section insertion.** Inserting §4.1.bis affects renumbering; check downstream cross-refs.
- **Counterparty's Word version.** Older Word may render redlines differently; export as PDF for review if unsure.
- **Bilingual contracts.** Track changes in two languages — match language tags on every redline.

## Sources

- [Spellbook docs](https://www.spellbook.legal/) — Word add-in + workflow.
- [Robin AI](https://www.robinai.com/) — mid-market AI redlines.
- [Harvey AI](https://www.harvey.ai/) — enterprise legal AI.
- [DraftWise](https://draftwise.com/) — precedent-based suggestions.
- [Ironclad AI Assist](https://ironcladapp.com/products/ai/) — Ironclad-integrated.
- [LegalOn](https://www.legalontech.com/) — US in-house redline tool.
- [redlines lib](https://github.com/MaxHumber/redlines) — Python diff for markdown / HTML.
- [python-docx](https://python-docx.readthedocs.io/) — Word manipulation.
- [docx schema reference (OOXML)](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-docx/) — for XML-level track changes.
- [diff-match-patch](https://github.com/google/diff-match-patch) — Google's diff algorithm.
- Sister skills: `ai-summarization-clause-extraction`, `contract-template-authoring-msa-nda`, `e-signature-docusign-adobe-sign-pandadoc`, `legal-counsel`.
