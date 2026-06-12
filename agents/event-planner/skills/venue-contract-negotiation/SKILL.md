<!--
Sources:
- MPI Anatomy of a Venue Contract: https://www.mpi.org/blog/article/the-anatomy-of-a-venue-contract
- Eventmanagerblog Event Contract Guide: https://www.eventmanagerblog.com/event-contract
- ASAE Contract Templates: https://www.asaecenter.org/resources/articles/contract-templates
-->
# Venue Contract Negotiation (Redline) — SKILL

Every venue contract has clauses worth $10K-$500K depending on how they're worded. This skill is the redline workflow: parse venue draft → flag load-bearing clauses → generate negotiation summary email → output redlined Word doc for legal review.

## When to use this skill

- Venue has sent a draft contract or LOI (letter of intent)
- Renewal of a returning venue with potentially stale terms
- Sponsor-paid venue (your sponsor sources a venue; you still need to redline)
- Force majeure update on an existing contract (e.g., adding new pandemic language)
- Recipient's legal team wants a pre-review with risk-flagged clauses

**Do NOT use this skill when:**
- No contract exists yet → use `venue-sourcing-cvent-splash-bizzabo` to source first
- Contract is already signed → contract enforcement / dispute is `operations-agent` / legal
- Venue is confirmed verbal-only → request written contract FIRST

## Setup

### Tools required

- `docx` skill for redline document output
- `gmail-mcp` for negotiation email
- `notion-mcp` for clause-by-clause tracker
- `gemini-ocr-mcp` if contract is scanned PDF

### Inputs

- Venue's draft contract (Word, PDF, or scanned)
- Event basics: total budget, headcount, dates, format
- Risk tolerance (low / medium / high — typically low for first-time events)

## Common recipes

### Recipe 1: Parse contract → extract load-bearing clauses

If PDF scanned:

```bash
mcp tool gemini-ocr.extract --file "venue_contract_draft.pdf" --output markdown
```

Then identify these 12 clauses (always present, sometimes hidden):

1. **F&B minimum** (food + beverage floor)
2. **Attrition clause** (room-block penalty)
3. **Force majeure** (cancellation triggers)
4. **Cancellation schedule** (sliding by lead time)
5. **Outside vendor allowance** (A/V, catering, decor, security)
6. **Deposit + payment schedule**
7. **Insurance + indemnification**
8. **Recording / livestream rights**
9. **Guest room rate + room block terms**
10. **Date hold / right of first refusal**
11. **Setup + teardown windows** (move-in / move-out hours)
12. **Confidentiality + non-disclosure**

### Recipe 2: F&B minimum redline

**Problem**: Venue offers "$50,000 F&B minimum" — this is a guaranteed-revenue floor. You'll spend more if attendees buy more; you owe the difference if you spend less.

**Redline rules**:
- Push back if F&B minimum > 70% of projected F&B spend
- Avoid F&B minimum + room rate minimum bundle (pick one)
- Add language: "F&B minimum exclusive of service charge and tax" (NOT inclusive)
- Add language: "Discounted F&B credit applies toward minimum"

**Redlined text** (example):
```
Original: "Client agrees to a Food and Beverage minimum of $50,000 inclusive of service charge."
Redline: "Client agrees to a Food and Beverage minimum of $35,000 exclusive of service
charge and tax. Hotel-discounted F&B credits and complimentary items
(e.g., coffee breaks for sponsored sessions) count toward the minimum."
```

### Recipe 3: Attrition clause redline

**Problem**: Venue's attrition often defaults to 100% pickup with no sliding scale.

**Redline rules**:
- Sliding scale from 80%: ≥80% pickup = 0% penalty, 70-80% = 25% of unsold × rack, <70% = 50% × rack
- Add re-marketing clause: venue must attempt to resell unsold rooms before charging attrition
- Cap rack rate used for calculation at booking-time rate (not current rate)
- Make attrition % count individual bookings (not just block bookings)

**Redlined text**:
```
Original: "Failure to achieve 100% pickup of the contracted block results in
attrition charges at the published rack rate for all unbooked rooms."

Redline: "Pickup levels and corresponding charges are:
  - ≥80% pickup: No attrition charges
  - 70%-79.99% pickup: 25% of unsold rooms × contracted group rate
  - <70% pickup: 50% of unsold rooms × contracted group rate
  Pickup includes all rooms reserved by attendees via the group booking code,
  whether inside or outside the block.
  Hotel agrees to make a good faith effort to re-sell unsold block rooms.
  Re-sold rooms reduce the attrition obligation 1-for-1."
```

### Recipe 4: Force majeure redline

**Problem**: Post-2020, "Acts of God" is no longer sufficient. Must explicitly enumerate.

**Redline rules**:
- Enumerate: pandemic / epidemic / health emergency, civil unrest / riots, extreme weather (hurricane / blizzard / flood), government shutdown / travel ban / visa restriction, terrorism, cyberattack on venue infrastructure
- Full deposit refund if invoked >90 days out
- Pro-rata refund if invoked 30-90 days out
- Mutual force majeure (either party can invoke)
- WHO / CDC / NOAA / State Department advisory as objective trigger

**Redlined text**:
```
"Force Majeure events include but are not limited to: pandemic or epidemic
(as declared by the WHO, CDC, or governmental health authority); civil
unrest or riot affecting venue access; severe weather (hurricane, blizzard,
flood, tornado, or wildfire as warned by NOAA or local authority);
government action including travel restrictions, visa denials, or border
closures; acts of terrorism; or cyberattack rendering venue inoperable.
Upon invocation:
- If invoked >90 days before event: 100% of deposits refunded
- If invoked 30-90 days before event: 50% of deposits refunded
- If invoked <30 days before event: deposit retained, event rescheduled
  to mutually agreed date within 12 months at no additional charge
- Mutual: either party may invoke upon notice within 7 days of the event."
```

### Recipe 5: Cancellation schedule redline

**Standard ask** (sliding scale):
- \>365 days out: 10% (deposit forfeit)
- 180-365 days: 25%
- 90-180 days: 50%
- 60-90 days: 75%
- <60 days: 100%

Push for full refund on extreme weather / force majeure regardless of timing.

### Recipe 6: Outside vendor allowance redline

**A/V**: Venues mandate in-house A/V at 2-3x market rate. ALWAYS push for outside-vendor allowance:

```
Original: "All A/V services must be provided by Hotel's in-house A/V vendor [X]."

Redline: "Client may use an outside A/V vendor for production, livestream,
lighting, and recording. Hotel may charge a reasonable rigging fee not to
exceed $X,XXX per day. Hotel-provided in-house A/V remains available at
Client's election. Client's outside vendor must show proof of liability
insurance ($2M per occurrence)."
```

**Catering**: Most venues mandate in-house catering. Push for allowance for:
- Kosher / halal / dietary-specific specialists
- Sponsor-provided coffee bar (in-kind)
- Specialty desserts / wedding cake from outside

### Recipe 7: Generate negotiation summary email

```bash
mcp tool docx.create --output "venue_contract_redline.docx" \
  --content "$(cat redline_template.md)"

mcp tool gmail.send_email \
  --to "venue_sales@hotel.com" \
  --cc "legal@recipient.com" \
  --subject "Re: Q3 Summit Contract — Redline + Negotiation Points" \
  --body "$(cat negotiation_summary.md)" \
  --attachments "venue_contract_redline.docx"
```

Negotiation summary template:

```markdown
Hi <name>,

Thanks for sending the contract draft. We've reviewed it and have a few items
we'd like to negotiate before signature. Attached is a redlined version with
our proposed changes; key points below:

1. **F&B Minimum** — Reduce from $50K to $35K (exclusive of service charge);
   our projected F&B spend is $45K, so $35K leaves modest cushion.

2. **Attrition** — Move to sliding scale starting at 80% pickup with
   re-marketing clause. Current language exposes us to 100% rack rate.

3. **Force Majeure** — Update language to enumerate pandemic / civil unrest /
   weather / travel restrictions explicitly. Post-2020 standard.

4. **Outside A/V** — Allow outside production vendor with reasonable rigging fee.
   Current language locks us to in-house at 2.5x market rate.

5. **Cancellation** — Sliding scale per lead time (proposed in redline).

Happy to schedule a 30-min call to walk through. Open to compromise on most points,
but #3 and #4 are critical given current market conditions.

Best,
<sender>
```

### Recipe 8: Concession tracking (Notion)

```bash
mcp tool notion.create_database --name "venue-contract-concessions" --properties '{
  "Clause": "title",
  "Original": "text",
  "Our Redline": "text",
  "Venue Counter": "text",
  "Final": "text",
  "Value Estimate ($)": "number",
  "Status": "select:open|countered|agreed|conceded"
}'
```

Track every clause through to signature; post-event, post-mortem to inform next year's redline.

## Examples

### Example A: Hotel contract for 350-attendee, 3-night summit

Issues found in original draft:
- F&B minimum $80K (vs projected $65K) → redlined to $55K
- Attrition 100% rack rate (vs sliding scale) → redlined to 80% threshold
- Force majeure says "Acts of God" only → enumerated explicitly
- Mandatory in-house A/V at quoted $45K (vs $18K market) → outside-vendor allowance added
- Cancellation: full 100% from signature (vs sliding) → sliding scale added

Total redline value: ~$50K in concessions.

### Example B: Conference center for tech conference, 800 attendees

Different concerns from hotels:
- F&B more flexible (often outside catering allowed)
- Bigger AV concern (large stages, multi-room synchronized streaming)
- Setup/teardown windows critical (move-in often 24-36 hr before; move-out same day)
- Wifi capacity must be in writing (≥500Mbps wired uplink + ≥10K simultaneous connections)

### Example C: Unique venue (industrial loft, popup, museum)

- Insurance often higher requirement (venue's GL may be lower than hotel's)
- Recipient may need higher liability insurance
- Force majeure language often template; needs significant rewrite
- Permits + alcohol license often venue's responsibility but verify
- Sound ordinance compliance (local laws on event noise) — VENUE responsibility to disclose

## Edge cases

### Venue refuses to redline
Walk away threshold: if venue refuses to budge on force majeure language, run the other venue options from `venue-sourcing-cvent-splash-bizzabo`. F&B and attrition are negotiable; force majeure is a deal-breaker post-2020.

### Sponsor-paid venue
If sponsor sources venue, you still redline. Sponsor pays venue but recipient bears reputational + operational risk. Add sponsor as additional party to contract OR require sponsor to share contract verbatim.

### Multi-day event with single contract
Some venues offer "campus" rate for multi-day or multi-room booking. Clarify what's included per day (move-in days, breakfast, breaks, dinner).

### Repeat-year multi-event discount
For recurring events at same venue, negotiate multi-year master agreement with annual reaffirmation. Lock rates; build in escalator (e.g., CPI + 2%).

### Legal team review
Always route final redline through recipient's legal counsel before signing. This skill prepares the redline; legal approves.

### Booking outside US (international venue)
Different contract conventions: e.g., UK uses "service charge" (12.5-15% mandatory) instead of US-style tip; Asia uses "++" for service + tax. Adjust F&B minimum calculations accordingly.

### Tax-exempt nonprofit recipient
Provide W-9 + tax-exempt certificate; venue may waive sales tax on F&B (save 8-15%).

### Venue insolvency / change of ownership
Add clause: "In event of change of venue ownership or insolvency, Client may
cancel with full refund of deposits paid." Has happened in 2020-2024 with several
hotel chains; protect against it.

## Sources

- **MPI Anatomy of a Venue Contract**: https://www.mpi.org/blog/article/the-anatomy-of-a-venue-contract
- **Eventmanagerblog Contract Guide**: https://www.eventmanagerblog.com/event-contract
- **ASAE Contract Templates**: https://www.asaecenter.org/resources/articles/contract-templates
- **HVS Hotel Contract Best Practices**: https://www.hvs.com/articles
- **PCMA Convene Magazine Contract Series**: https://www.pcma.org/convene/
