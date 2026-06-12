---
name: safe-convertible-note-yc-template
description: Review + draft + model YC Post-Money SAFE (default since 2018), YC Pre-Money SAFE, MFN + Pro-Rata side letters, and convertible notes (interest, maturity, cap, discount, qualified financing trigger). Dilution math + cap-table modeling. Output is a redline + dilution memo with the consult-an-attorney disclaimer.
---

# SAFE + Convertible Note — YC Templates + Cap-Table Math

## When to use

User says:

- "Review this SAFE / convertible note"
- "Draft a Post-Money SAFE"
- "MFN / pro-rata side letter"
- "Cap table impact of SAFE conversion"
- "Discount + cap math"
- "Qualified financing trigger"
- "Convertible note maturity"
- "Side letter terms"

Companion skills:
- `term-sheet-review-series-a-typical-terms` — priced rounds.
- `equity-grants-isos-rsus-83b-election` — employee equity.
- `founders-agreement-vesting-ip-assignment` — founders agreement.

## Setup

```bash
# YC SAFE documents
# https://www.ycombinator.com/documents
# Direct download:
# https://www.ycombinator.com/documents/safe_v1_5_post_money.pdf  (Post-Money standard)
# https://www.ycombinator.com/documents/safe_v1_5_post_money_cap.pdf  (Post-Money valuation cap only)
# https://www.ycombinator.com/documents/safe_v1_5_post_money_discount.pdf
# https://www.ycombinator.com/documents/safe_v1_5_post_money_mfn.pdf

# Cooley GO convertible securities
# https://www.cooleygo.com/documents/safe-and-convertible-securities/

# Convertible note templates
# https://www.cooleygo.com/documents/convertible-debt/

# Cap-table modeling
pip install pandas openpyxl numpy

# Optional: Carta / Pulley / AngelList Stack for live modeling
# Carta API: https://docs.carta.com/
# Pulley REST: https://api.pulley.com/
```

## Common recipes

### Recipe 1: YC Post-Money SAFE — the 2026 default
```text
Post-Money SAFE (introduced YC 2018; default since):
- Valuation cap based on POST-MONEY (including new SAFE money)
- SAFE holder ownership % at conversion = investment / valuation cap
- LOCKED at signing → no dilution math complexity until priced round

Standard variants:
- Cap-only: SAFE converts at cap-implied price
- Discount-only: SAFE converts at discount % off priced-round price
- Cap + Discount: SAFE gets the BETTER of cap or discount
- MFN (Most Favored Nation): adds side-letter right to swap for better future SAFE/note terms

Download: https://www.ycombinator.com/documents
```

### Recipe 2: YC Pre-Money SAFE — legacy (use only if requested)
```text
Pre-Money SAFE (original YC 2013):
- Valuation cap based on PRE-MONEY
- SAFE shares calculated at conversion: investment / SAFE conversion price
  - SAFE conversion price = min(cap-implied, discount-implied)
- Cap-implied price = Pre-Money cap / (FD shares before priced-round investors)
- Discount-implied price = (1 - discount) × priced-round price

Why fall out of favor: cap-table math gets messy with multiple SAFEs at different caps.
```

### Recipe 3: SAFE review checklist
```markdown
- [ ] Identify variant (Post-Money vs Pre-Money, Cap-only vs Discount-only vs Both, MFN side letter)
- [ ] Valuation cap amount + reasonable for stage
- [ ] Discount % (typically 15-25%; 20% common)
- [ ] Qualified Equity Financing definition (typically priced round > $1M, sometimes $2M)
- [ ] Conversion mechanics:
  - At Qualified Equity Financing: convert at cap / discount price
  - At Liquidity Event: cash out at max(investment, as-if-converted at cap)
  - At Dissolution: SAFE-holder is creditor for return of investment
- [ ] Side letters (MFN, pro-rata) — match base SAFE template
- [ ] Investor representations (accredited investor)
- [ ] Acknowledgment of risk
- [ ] Counsel review on both sides
- [ ] Disclaimer in cover memo
```

### Recipe 4: Post-Money SAFE math (single SAFE)
```python
# post_money_safe.py
investment = 500_000   # $500k SAFE
cap = 10_000_000       # $10M post-money cap
discount = 0.20        # 20% discount

# Locked at signing:
ownership_pct = investment / cap
print(f"SAFE holder ownership at priced round: {ownership_pct:.2%}")  # 5%

# At Series A with $30M post-money:
series_a_post_money = 30_000_000
# Cap-implied: SAFE gets cap-priced shares
cap_implied_share_price = cap / fd_shares_post_safe_pre_a  # depends on existing cap table
# Discount-implied:
series_a_price = series_a_post_money / total_shares_post_money_at_series_a
discount_implied_price = series_a_price * (1 - discount)

safe_conversion_price = min(cap_implied_share_price, discount_implied_price)
safe_shares = investment / safe_conversion_price
print(f"SAFE shares at Series A: {safe_shares:.0f}")
```

### Recipe 5: Multiple SAFEs at different caps — stacking
```python
import pandas as pd
safes = pd.DataFrame([
    {"holder": "Angel A", "investment": 250_000, "cap": 5_000_000, "discount": 0.20, "mfn": True},
    {"holder": "Angel B", "investment": 100_000, "cap": 6_000_000, "discount": 0.20, "mfn": False},
    {"holder": "Fund C", "investment": 1_000_000, "cap": 8_000_000, "discount": 0.20, "mfn": True},
])

# Post-Money math is simpler — each SAFE's ownership locked at investment/cap
safes["locked_ownership_pct"] = safes["investment"] / safes["cap"]
print(safes)
# Total SAFE ownership = sum of locked_ownership_pct = % of post-money pool at Series A

# Pre-Money math (legacy): each SAFE converts at its own conversion price, total dilution depends on existing cap table + option pool refresh
```

### Recipe 6: MFN (Most Favored Nation) side letter
```markdown
# Most Favored Nation Side Letter

If the Company subsequently issues SAFEs or convertible notes with better terms (lower cap, higher discount, more investor-friendly other terms) before the Qualified Equity Financing, the holder of this SAFE may elect to swap their existing SAFE for one with the new terms.

"Better terms" includes:
- Lower valuation cap
- Higher discount %
- Pro-rata rights
- Side letter rights
- Other materially better terms

Notification: Company must notify existing MFN holders within 14 days of any new SAFE / note issuance.
Election: MFN holder has 30 days to elect.
Swap mechanics: original SAFE cancelled; new SAFE issued at original investment amount; new terms apply.
```

### Recipe 7: Pro-Rata side letter
```markdown
# Pro-Rata Rights Side Letter

The holder of this SAFE shall have the right to purchase additional securities in the next priced equity financing (and potentially each subsequent priced round) sufficient to maintain their then-current ownership percentage on a fully-diluted basis.

Pro-rata participation:
- Calculation: Holder's pre-round FD % × new shares issued in priced round
- Notification: Company gives 15 days' notice of priced round + pro-rata allotment
- Election: Holder elects within 15 days
- Pricing: Same per-share price as new investors

Subject to:
- Lead investor's pro-rata participation
- Standard QFR / accredited investor reqs
```

### Recipe 8: Convertible note review
```markdown
- [ ] Principal amount
- [ ] Interest rate (typical 5-8% simple; sometimes accrued)
- [ ] Maturity date (typically 18-24 months from issuance)
- [ ] Conversion trigger (typical qualified financing > $1-2M)
- [ ] Conversion price = min(cap-implied, discount × priced-round price)
- [ ] Valuation cap
- [ ] Discount % (typical 15-25%)
- [ ] Maturity behavior:
  - Auto-convert at last priced-round price?
  - Conversion to common at last priced-round price?
  - Repayment of principal + accrued interest?
  - Mandatory conversion at cap-implied price?
- [ ] Liquidity event behavior (cash out at multiple, e.g., 1-1.5x of principal)
- [ ] Subordination (debt vs equity ordering on dissolution)
- [ ] Information rights
- [ ] Pro-rata rights
- [ ] Default + cure provisions
- [ ] Governing law
- [ ] Disclaimer in cover memo
```

### Recipe 9: SAFE vs Convertible note — pick the right tool
| Term | SAFE | Convertible Note |
|---|---|---|
| Interest | None | 5-8% typical |
| Maturity | None | 18-24 months |
| Repayment risk | None — equity-like | Yes — debt obligation |
| Conversion mechanic | Triggered at QEF; otherwise stays as SAFE | Triggered at QEF or maturity |
| Subordination | Equity-like; creditor priority over equity | Debt-like; ahead of equity but behind senior debt |
| Speed of execution | Faster (5-15 page template) | Slower (10-20 page note + purchase agreement) |
| Use when | Standard early-stage round | Investor demands debt features OR bridge before known priced round |

YC standard advice 2026: use SAFE unless investor specifically requires note.

### Recipe 10: Dilution modeling — Python cap table
```python
import pandas as pd

# Initial cap table (pre-SAFE)
cap_table = pd.DataFrame([
    {"holder": "Founder A", "shares": 5_000_000, "type": "common"},
    {"holder": "Founder B", "shares": 5_000_000, "type": "common"},
    {"holder": "Option pool (unallocated)", "shares": 2_000_000, "type": "option"},
])

# SAFEs
safes = [
    {"holder": "Angel A", "investment": 250_000, "cap": 5_000_000, "discount": 0.20},
    {"holder": "Angel B", "investment": 500_000, "cap": 8_000_000, "discount": 0.20},
]

# Priced Series A: $10M @ $30M post-money
series_a_investment = 10_000_000
series_a_post_money = 30_000_000

# Step 1: Convert SAFEs first
# Each Post-Money SAFE locks ownership = investment / cap
total_safe_ownership = sum(s["investment"] / s["cap"] for s in safes)
# = 250k/5M + 500k/8M = 5% + 6.25% = 11.25%

# Step 2: Series A ownership = investment / post_money
series_a_ownership = series_a_investment / series_a_post_money  # = 33.33%

# Step 3: Existing pool = remainder = 100% - SAFE_total - Series_A
existing_ownership = 1 - total_safe_ownership - series_a_ownership  # = 55.42%

# Founder dilution (assuming pre-SAFE = 100%): they now hold 55.42% × 10M/12M = 46.18% combined
# Option pool refresh (10% post-money) would come out of existing → further dilute founders

print(f"SAFE total: {total_safe_ownership:.2%}")
print(f"Series A: {series_a_ownership:.2%}")
print(f"Existing (including option pool): {existing_ownership:.2%}")
```

### Recipe 11: Standard founder negotiation levers on SAFE
```text
- Lower cap (founder pushes UP, investor pushes DOWN)
- Lower discount % (founder pushes DOWN, investor pushes UP)
- Higher Qualified Financing threshold ($2M better than $1M for founder — fewer auto-triggers)
- No MFN side letter
- No pro-rata side letter
- Standard YC variant (don't draft custom — investors trust standard)
- No additional reps / warranties beyond YC template
```

### Recipe 12: When NOT to use a SAFE
```text
- Late-stage company (Series B+) → use priced round
- International investors / non-US issuer → securities law complications
- Investor is a fund with strict mandate against SAFEs → use convertible note instead
- Tax-advantaged structures (QSBS §1202) — confirm SAFE preserves QSBS holding period
- Strategic / corporate investor with IP / commercial considerations → priced round more appropriate
```

### Recipe 13: Memo skeleton — SAFE review
```markdown
# SAFE Review Memo — <Investor / Round>

**Reviewed by:** Legal Counsel (AI agent)
**Date:** 2026-06-09

## Round summary
- Total raise: $<X>M
- Number of SAFEs: <N>
- Standard YC template: Yes / No (specify variant: Post-Money / Cap-only / Cap+Discount / MFN)
- Lead investor:
- Co-investors:

## Terms
| SAFE | Investment | Cap | Discount | MFN? | Pro-rata? |
|---|---|---|---|---|---|
| Angel A | $250k | $5M post | 20% | Yes | No |

## Dilution at exit scenarios
- $30M Series A: SAFE = 11.25%, founders dilute to ~46% combined
- $50M Series A: SAFE = 11.25% (locked), founders dilute to ~57%
- Liquidity event before priced round: SAFE = $500k cash out (1x return)

## Flags
- (None typical for standard YC template)
- (If non-standard: flag deviation)

## Recommendation
- Accept (standard YC template, market terms)
- OR: counter-propose <change>

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney before signing or executing SAFE or convertible note documents.
```

## Examples

### Example 1: First-time founder raising Pre-seed $750k
**Goal:** Use Post-Money SAFE Cap + Discount across 3-5 angels.
**Steps:**
1. Recipe 1 confirm Post-Money default.
2. Download YC Cap + Discount template.
3. Set cap (e.g., $8M post-money), discount (20%), QFR ($1M+).
4. Each angel signs the same SAFE (only investment $ varies).
5. Two angels demand MFN side letter (Recipe 6); accept.
6. Recipe 10 model dilution at Series A scenarios.
7. Recipe 13 memo per angel.
8. Add disclaimer; route to user's licensed attorney.

**Result:** Clean Post-Money SAFE raise with documented dilution paths.

### Example 2: Reviewing an investor-drafted convertible note
**Goal:** Investor wants $2M convertible note at $20M cap, 7% interest, 24mo maturity, automatic conversion at QEF > $5M.
**Steps:**
1. Recipe 8 review checklist.
2. Flag: QEF threshold at $5M is high (typical $1-2M) → investor wants to avoid premature trigger.
3. Recipe 10 model dilution at QEF scenario.
4. Negotiate QEF down to $2M.
5. Confirm 24mo maturity behavior (auto-convert at last priced-round price preferred).
6. Recipe 13 memo with redlines.
7. Add disclaimer; route to user's licensed attorney.

**Result:** Negotiated note with founder-acceptable trigger threshold.

## Edge cases / gotchas

- **Don't customize the YC SAFE.** Investors trust the standard form; custom edits trigger expensive deep review on every side. Use the variant (cap-only, discount-only, cap+discount, MFN) and only customize via side letter.
- **Post-Money vs Pre-Money confusion.** Make sure all SAFEs in same round use SAME variant. Mixing Post + Pre creates dilution math hell.
- **MFN can backfire.** If you offer a better-term SAFE later, MFN holders swap → all your SAFE holders now have the lower cap. Easy to over-dilute.
- **Pro-rata rights only on the NEXT round** by default. Some investors want pro-rata "all future rounds" — push back; market is single round.
- **QSBS §1202 holding period.** SAFE may or may not start QSBS holding period at issuance vs conversion — fact-specific. Consult tax counsel for QSBS optimization.
- **Multiple SAFE caps stack.** Total SAFE % at conversion can exceed founder expectations if multiple low-cap SAFEs. Always model BEFORE accepting next SAFE.
- **Note maturity defaults to debt.** If a convertible note matures without QEF, it's still a debt obligation. Negotiate maturity behavior carefully (auto-convert at last round? Repay?).
- **Sub-ordination matters in distress.** Convertible notes are debt → ahead of equity in dissolution but behind secured creditors. SAFEs are equity-like → behind all debt.
- **Securities Act Rule 506(b) vs 506(c).** Rule 506(b) = no general solicitation; 506(c) = general solicitation but ALL investors must be accredited + verified. Pick one path.
- **State Blue Sky filings.** Form D required within 15 days of first sale. Each state may have filing fee (e.g., $300 NY).
- **Foreign investor + SAFE.** Tax + securities complications. Use convertible note or priced round for non-US investors.
- **Outstanding SAFEs influence Series A.** Lead VC will model dilution INCLUDING SAFEs. If SAFE total exceeds 15-20%, VC may push for low pre-money or option pool refresh on existing holders.
- **Strategic / corporate investors** often want side letters that aren't in YC template (board observer, ROFR, info rights). Push back hard; these belong in priced round, not SAFE.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney before signing, filing, or executing SAFE, convertible note, or side letter documents.**

## Sources

- [Y Combinator Documents](https://www.ycombinator.com/documents) — standard YC SAFE templates.
- [YC Post-Money SAFE User Guide](https://www.ycombinator.com/documents#:~:text=safe%20user%20guide) — guide.
- [Cooley GO SAFE + Convertible Securities](https://www.cooleygo.com/documents/safe-and-convertible-securities/) — alt templates.
- [Cooley GO Convertible Notes](https://www.cooleygo.com/documents/convertible-debt/) — convertible note template.
- [Carta — SAFE / Convertible](https://carta.com/learn/safes/) — modeling reference.
- [NVCA Model Documents](https://nvca.org/model-legal-documents/) — priced-round benchmark.
- [SEC Rule 506(b) + 506(c) — Reg D](https://www.sec.gov/education/smallbusiness/exemptofferings/rule506) — securities exemptions.
- [IRC §1202 — QSBS](https://www.law.cornell.edu/uscode/text/26/1202) — qualified small business stock.
- Sister skills: `term-sheet-review-series-a-typical-terms`, `equity-grants-isos-rsus-83b-election`, `founders-agreement-vesting-ip-assignment`.
