---
name: term-sheet-review-series-a-typical-terms
description: Review Series A (or later) term sheets against NVCA model + Carta / Aumni 2026 market data. Cover liquidation preference, anti-dilution, board composition, protective provisions, pro-rata, drag-along, founder vesting refresh, option pool. Output is a deviation-from-market memo with the consult-an-attorney disclaimer.
---

# Term Sheet Review — Series A Typical Terms

## When to use

User says:

- "Review this term sheet"
- "What's market for [term] in 2026?"
- "Liquidation preference negotiation"
- "Anti-dilution / weighted average"
- "Board composition"
- "Protective provisions"
- "Pro-rata rights for investors"
- "Drag-along provisions"
- "Option pool refresh"
- "Founder vesting refresh"

Companion skills:
- `safe-convertible-note-yc-template` — pre-priced rounds.
- `founders-agreement-vesting-ip-assignment` — founder vesting.
- `equity-grants-isos-rsus-83b-election` — option pool grants.

## Setup

```bash
# NVCA Model Documents — Series A benchmark
# https://nvca.org/model-legal-documents/

# Carta — current market data
# https://carta.com/learn/startups/state-of-private-markets/

# Aumni / Carta — venture term benchmarks
# https://www.aumni.fund/

# Cooley GO term sheet template
# https://www.cooleygo.com/documents/term-sheets/

# Python helpers for modeling
pip install pandas numpy openpyxl
```

## Common recipes

### Recipe 1: NVCA model documents — the benchmark
```text
NVCA (National Venture Capital Association) publishes model:
- Term Sheet
- Stock Purchase Agreement
- Restated Certificate of Incorporation
- Investor Rights Agreement
- Voting Agreement
- Right of First Refusal + Co-Sale Agreement
- Management Rights Letter
- Indemnification Agreement

These represent "market" for US Series A.
Download: https://nvca.org/model-legal-documents/
```

### Recipe 2: Term sheet review — clause-by-clause decision table

| Term | Founder-friendly market (2026) | Investor-friendly variations | Negotiation lever |
|---|---|---|---|
| Liquidation preference | 1x non-participating | 1x participating with cap; 1.5-2x non-participating | Cap on participation; convert-to-common option |
| Anti-dilution | Broad-based weighted average | Narrow-based WA; full ratchet | Carve-outs (option pool refresh, conversions) |
| Pro-rata rights | Major investors only | All investors | Define "major investor" by check size |
| Board composition | Common 2 / Pref 1 / Independent 0 (3 total) or 5 total | Pref majority | Independent director seat |
| Protective provisions | Standard NVCA list | Expanded list (M&A, hire/fire CEO, budget, dividends, debt) | Trim to material items |
| Drag-along | Above majority of common + majority of preferred | Majority of preferred alone | Founder consent required (or board) |
| Tag-along / co-sale | Standard — pref can sell pro-rata if common sells | — | — |
| ROFR | Standard — company first, then investors | — | — |
| Information rights | Major investors only | All investors | Define major; restrict to financials + budget |
| Founder vesting | 4-year / 1-year cliff with double-trigger acceleration | Single trigger | Acceleration on CoC + termination |
| Option pool | Pre-money pool — 10-15% | Pre-money pool — 15-20% | Negotiate against post-money pool (investor dilution) |
| Dividends | Non-cumulative when declared | Cumulative | Reject cumulative |
| Conversion | 1:1 + adjustments | — | — |
| Pay-to-play | Standard NVCA carrot (lose pref status if don't participate pro-rata in down rounds) | Stick (forced conversion to common) | Negotiate carrot vs stick |
| Redemption rights | None | Investor put after 5-7 years | Push to remove or extend |
| Founder reverse vesting / refresh | Often refreshed at A with new 3-4 year vest | — | Acceleration on involuntary termination |

### Recipe 3: Liquidation preference math
```python
# liq_pref.py
# 1x non-participating: investor gets max(invested, as-if-converted at exit)
def liq_pref_1x_non_participating(invested, ownership_pct, exit_value):
    as_if_converted = ownership_pct * exit_value
    return max(invested, as_if_converted)

# 1x participating (no cap): investor gets invested THEN pro-rata of remainder
def liq_pref_1x_participating(invested, ownership_pct, exit_value):
    remainder = exit_value - invested
    return invested + ownership_pct * remainder

# 1x participating with 3x cap
def liq_pref_1x_participating_capped(invested, ownership_pct, exit_value, cap_multiple=3):
    participating_amount = invested + ownership_pct * (exit_value - invested)
    capped = min(participating_amount, invested * cap_multiple)
    # Investor optimizes between participating cap vs as-if-converted
    return max(capped, ownership_pct * exit_value)

# Example: $10M invested, 33% post-money, exit at $50M
print(liq_pref_1x_non_participating(10_000_000, 0.33, 50_000_000))  # $16.5M (as-if-converted)
print(liq_pref_1x_participating(10_000_000, 0.33, 50_000_000))  # $23.2M ($10M + 33% × $40M)
print(liq_pref_1x_participating_capped(10_000_000, 0.33, 50_000_000, 3))  # min($23.2M, $30M cap) = $23.2M
```

### Recipe 4: Anti-dilution — broad-based weighted average
```python
# anti_dilution.py
# Broad-based weighted average — market default in 2026
# Adjusted conversion price = OldCP × (OS + NB) / (OS + (NM/OldCP))
# Where:
# OS = Outstanding shares before new round (on FD basis)
# NB = Shares hypothetically issued at old conversion price for new money
# NM = New money raised
# OldCP = Old conversion price

def broad_based_wa_anti_dilution(
    old_cp, new_share_price, new_money, fd_shares_before
):
    if new_share_price >= old_cp:
        return old_cp  # no down-round; no adjustment
    nb = new_money / old_cp  # shares at old price
    return old_cp * (fd_shares_before + nb) / (fd_shares_before + (new_money / new_share_price))

# Example: $1 OldCP, $0.50 new price (down round), $5M new money, 50M FD
new_cp = broad_based_wa_anti_dilution(1.0, 0.50, 5_000_000, 50_000_000)
print(f"New CP: ${new_cp:.4f}")  # somewhere between $0.50 and $1
```

### Recipe 5: Option pool refresh dilution
```text
PRE-MONEY pool (favors investor):
- Pool refresh comes OUT OF pre-money valuation
- Existing holders (founders) take the dilution
- 10-15% pool refresh is market for Series A
- 20% sometimes if hiring plan justifies

POST-MONEY pool (favors founder):
- Pool refresh comes OUT OF post-money valuation
- All holders dilute pro-rata (including new investor)
- Investor will negotiate this hard

Founder negotiation: justify the pool size to actual hiring plan (1-2 year runway).
Don't accept arbitrary "15% post-money pool" if you don't need to hire 15% worth of equity.
```

### Recipe 6: Board composition — typical Series A
```text
Series A board (5 seats is common, 3 also seen):
- 2 Common (Founders / Common-elected)
- 1 Preferred (Series A lead investor designee)
- 1 Independent (mutually agreed; often industry expert)
- 1 CEO (often a Common seat — same as one of the founders)

OR 3-seat board:
- 1 Common (Founder/CEO)
- 1 Preferred (Series A lead)
- 1 Independent (mutually agreed)

Investor-friendly: 2 Preferred (lead + co-lead) + 1 Common + 1 Independent + 1 mutually agreed
Founder-friendly: 2 Common + 1 Preferred + 0 Independent

Founder leverage: keep board small early; expand at Series B/C.
```

### Recipe 7: Protective provisions — what's market
```text
NVCA standard PP (subset; preferred must consent):
- Amend charter / bylaws in a way adverse to preferred
- Authorize / issue new preferred series with priority equal or senior
- Reclassify common stock
- Pay dividends on common (besides preferred dividends)
- Repurchase shares (except at cost on departure)
- Merger / sale of company
- Liquidation / dissolution
- Increase / decrease authorized shares
- Change number of directors

Investor-expanded:
- Hire / fire CEO
- Budget approval
- Senior debt > $X
- Material agreements > $X
- Change of business plan
- Change of jurisdiction
- IPO (usually all-stockholder vote)

Push back on operational matters — these belong to the board, not preferred protective provisions.
```

### Recipe 8: Pro-rata rights — major investor definition
```text
Pro-rata = right to participate in next financing to maintain ownership %.

Market: only "Major Investors" get pro-rata.
- Major Investor = pref holder owning at least $X invested OR Y shares
- Threshold typically $250k-$1M

Investor-favorable: all investors get pro-rata (creates messy follow-on rounds).
Founder-favorable: only lead + larger investors get pro-rata.

Pro-rata + super-pro-rata: occasionally, investor wants right to participate at greater than pro-rata in next round (e.g., 2x pro-rata). Resist — keep at 1x pro-rata.
```

### Recipe 9: Founder vesting refresh at Series A
```text
Common pattern:
- Founders had 4-year vest with 1-year cliff at incorporation
- At Series A, 50-75% may be vested already
- Investors push for REFRESH: re-vest some portion over 3-4 years
- Compromise: take credit for time already served, vest remainder over 3 years

Acceleration:
- Single trigger (CoC alone): 25-50% of unvested
- Double trigger (CoC + involuntary termination within 12mo): 100%
- Negotiate double trigger as default; single is harder to get
```

### Recipe 10: Drag-along clause
```text
Drag-along: when a majority approves a sale, minority must also sell.

Market: above majority of common + majority of preferred (separate votes).
Investor-favorable: majority of preferred alone (founders can be dragged into sale they don't want).

Founder protection:
- Require founder consent OR board approval
- Carve-out for fair-market-value sales only
- Excluded if proceeds below some threshold ($X per common share)
```

### Recipe 11: Sample term sheet review memo
```markdown
# Series A Term Sheet Review — <Lead Investor>

**Reviewed by:** Legal Counsel (AI agent)
**Date:** 2026-06-09

## Round summary
- Pre-money: $<X>M
- New investment: $<Y>M
- Post-money: $<X+Y>M
- Option pool refresh: <Z>% pre-money
- Lead: <Investor>; co-lead/follow-on: <Investors>

## Material terms vs market (Recipe 2 table)

### LIQUIDATION PREFERENCE
- Proposed: 1x non-participating
- Market: 1x non-participating
- Verdict: ✓ Market

### ANTI-DILUTION
- Proposed: Broad-based weighted average
- Market: Broad-based weighted average
- Verdict: ✓ Market

### BOARD COMPOSITION
- Proposed: 2 Pref + 2 Common + 1 Independent (5 total)
- Market: 1 Pref + 2 Common + 1 Independent (4 or 5)
- Verdict: ⚠ Investor-favorable. Push back to 1 Pref seat + 1 mutually-agreed Independent.

### PROTECTIVE PROVISIONS
- Proposed: NVCA standard + hire/fire CEO + annual budget
- Market: NVCA standard
- Verdict: ⚠ Hire/fire CEO and budget belong at board, not preferred PP. Strike.

### OPTION POOL REFRESH
- Proposed: 15% pre-money
- Market: 10-15% pre-money
- Verdict: ✓ Market. Justify size to hiring plan to avoid 20%.

### FOUNDER VESTING REFRESH
- Proposed: Credit for time served + 3-year re-vest of remainder
- Acceleration: Double trigger (CoC + termination)
- Verdict: ✓ Market

### REDEMPTION RIGHTS
- Proposed: None
- Verdict: ✓ Market

### PAY-TO-PLAY
- Proposed: Standard NVCA carrot
- Verdict: ✓ Market

### DRAG-ALONG
- Proposed: Above majority of common + majority of preferred
- Verdict: ✓ Market

## Recommended counter-proposals
1. Board: 1 Pref + 2 Common + 1 Independent + 1 mutually-agreed (4 seats with 1 vacant for later)
2. Strike "hire/fire CEO" + "annual budget" from PP
3. Cap pro-rata at $500k threshold for Major Investor

## Dilution model (Recipe 3-5)
- Founder ownership post-Series A: <%>
- Post-option-pool refresh: <%>

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney before signing or executing a term sheet or definitive agreements.
```

### Recipe 12: Carta / Aumni 2026 benchmark check
```text
Always pull current data before negotiating:
- Carta State of Private Markets: https://carta.com/learn/startups/state-of-private-markets/
- Carta Series A median terms by stage/sector
- Aumni: https://www.aumni.fund/

Latest data points show what's actually trading in market vs textbook "norms."
```

### Recipe 13: Exploding offers + standstill agreement
```text
Lead investor sometimes wants "exclusivity" or "no-shop" period:
- Standstill: founder agrees not to shop the deal for 30-60 days
- Acceptable IF you're already committed to this lead
- AVOID if you want to keep options open

Standstill carve-outs:
- Receive (don't solicit) unsolicited inquiries
- Respond to corporate development inquiries
- Founder may inform existing investors of round
```

## Examples

### Example 1: First-time founder reviewing Series A term sheet
**Goal:** Understand and negotiate a Tier 2 VC's term sheet.
**Steps:**
1. Recipe 1 pull NVCA model for comparison.
2. Recipe 2 walk decision table.
3. Recipe 11 build the memo.
4. Recipe 3-5 model dilution + liquidation outcomes.
5. Recipe 12 benchmark vs Carta data.
6. Negotiate counter-proposals via founder-friendly lawyer.
7. Add disclaimer; route to user's licensed VC counsel.

**Result:** Founder enters negotiation with quantified deviation memo.

### Example 2: Down-round Series B term sheet review
**Goal:** Series B at lower valuation than Series A; anti-dilution triggers.
**Steps:**
1. Recipe 4 calculate broad-based WA adjustment.
2. Confirm carve-outs (option pool refresh, employee grants below FMV) preserved.
3. Recipe 11 memo emphasizing dilution impact + anti-dilution outcomes.
4. Negotiate Pay-to-Play (carrot) — if existing investors don't participate, lose preferred status.

**Result:** Founder navigates anti-dilution with informed pushback.

## Edge cases / gotchas

- **"1x non-participating" doesn't mean low risk.** Investor still gets the BETTER of preference vs as-if-converted. At high exits, as-if-converted wins. At low exits, preference wins.
- **Participating preferred = double-dip.** Investor gets both preference AND pro-rata of remainder. Cap reduces this. Avoid uncapped participating in 2026.
- **Anti-dilution full-ratchet is catastrophic.** Full ratchet adjusts conversion price down to NEW round price (regardless of size). Reject; insist on broad-based WA.
- **Drag-along can force a sale founders oppose.** Build in safeguards: founder consent (or board approval), minimum threshold per share, no drag below FMV.
- **Option pool refresh dilutes FOUNDERS, not new investors** when pre-money. Push for 10% if hiring plan justifies; resist 20%.
- **Protective provisions = preferred VETO.** Anything in PP requires preferred consent (separate from board). Don't accept operational items in PP.
- **Information rights at all investors = expensive.** Quarterly financials + budget + projections multiplied across 20+ investors. Define "Major Investor" to limit.
- **Founder vesting refresh** — sometimes investor wants 100% re-vest with no credit. Push hard for credit for time served + acceleration.
- **Single trigger acceleration** — increasingly difficult to get post-2020. Double trigger is market.
- **Redemption rights** — investor's "right to demand company buy back shares." Avoid. Creates fixed-income obligation on cap table.
- **NDA on term sheet.** Don't sign NDA that prevents shopping the deal until you're committed.
- **No-shop period** — 30 days market; 60+ unusual. Time-box it.
- **Founder secondary** — selling founder shares at Series A is hot in 2024+ but investor pushback common. Negotiate carefully if requesting.
- **Information rights survive termination of investor relationship?** Some agreements grant rights until "investor sells all shares." Be specific.
- **Side letters proliferate.** MFN + pro-rata + observer + information rights — each side letter is leverage. Push back on extras.
- **Indemnification side agreements.** Some investors demand director indemnity beyond charter — generally fine; may want D&O insurance.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney before signing, filing, or executing a term sheet or definitive agreements.**

## Sources

- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents/) — Series A canonical benchmark.
- [Cooley GO Term Sheets](https://www.cooleygo.com/documents/term-sheets/) — alt template.
- [Carta State of Private Markets](https://carta.com/learn/startups/state-of-private-markets/) — quarterly market data.
- [Aumni Fund](https://www.aumni.fund/) — venture data + benchmarks.
- [Holloway Guide to Raising Venture Capital](https://www.holloway.com/g/raising-venture-capital) — practical guide.
- [Brad Feld + Jason Mendelson — Venture Deals](https://www.amazon.com/Venture-Deals-Smarter-Lawyer-Capitalist/dp/1119594820/) — book.
- [YC Equity Calculator](https://www.ycombinator.com/library) — dilution modeling.
- Sister skills: `safe-convertible-note-yc-template`, `founders-agreement-vesting-ip-assignment`, `equity-grants-isos-rsus-83b-election`.
