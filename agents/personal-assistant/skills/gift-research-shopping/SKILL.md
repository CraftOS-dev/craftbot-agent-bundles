<!--
Source: https://www.nytimes.com/wirecutter/gifts/ + https://developers.notion.com/ + https://www.amazon.com/
-->
# Gift Research + Shopping — SKILL

Find the right gift, log it, prevent repeats. Cross-store search (Amazon + Etsy + Uncommon Goods + Goldbelly + boutique stores) → compare 3-5 options → recommend → order (or surface deep-link) → log to Notion recipient DB so next-time research is faster.

## When to use this skill

- **"Find a gift for X"** — direct trigger; most common.
- **"What did I give Mom last year?"** — recipient-history lookup.
- **"Birthday in 2 weeks; need ideas"** — preemptive (from `birthday-anniversary-tracking`).
- **Holiday gift list batch** — December 1 surge.
- **Thank-you gift for client / coworker** — work / personal blend.

**Do NOT use this skill when:**
- Birthday reminders themselves — see `birthday-anniversary-tracking`.
- Restaurant gift card as gift — surface `restaurant-reservations-opentable-resy-tock` for restaurant lookup, then use this for gift card.
- Holiday card / message draft — out of this skill's scope.

## Setup

### Required MCPs (already in agent.yaml)

- `amazon-mcp` — Amazon search + price
- `ebay-mcp` — marketplace alt
- `firecrawl-mcp` — non-API stores (Uncommon Goods, Etsy, Goldbelly, boutiques)
- `notion-mcp` — gift log

### Notion Gift Log DB schema

Create once per user. Database structure:

```
| Field | Type | Notes |
|---|---|---|
| Recipient | Relation → Contacts | Who |
| Date | Date | When gifted |
| Occasion | Select | Birthday / Anniversary / Holiday / Thank-you / Just-because |
| Gift | Text | What |
| Cost | Number | $ |
| Source | URL | Where bought |
| Delivery method | Select | Hand / Shipped / Digital |
| Reaction | Select | Loved / Liked / Neutral / Negative / Unknown |
| Notes | Text | Context |
| Avoid next time | Text | What didn't work |
```

Set up via Notion UI or via `notion-mcp.create_database`.

## Common recipes

### Recipe 1: Pull recipient history

```bash
mcp tool notion.query_database \
  --database-id <gift-log-db-id> \
  --filter '{"property":"Recipient","relation":{"contains":"<recipient-page-id>"}}' \
  --sorts '[{"property":"Date","direction":"descending"}]'
```

Surface: past gifts, costs, reactions, "avoid next time" notes.

### Recipe 2: Amazon search

```bash
mcp tool amazon.search \
  --query "premium leather notebook" \
  --max-price 100 \
  --min-rating 4.3 \
  --prime-eligible true
```

### Recipe 3: Etsy search (handmade / personalized)

```bash
mcp tool firecrawl.scrape \
  --url "https://www.etsy.com/search?q=personalized+leather+wallet&order=highest_reviews" \
  --format markdown
```

Etsy has no public catalog API for individuals. Use `firecrawl-mcp`.

### Recipe 4: Uncommon Goods curated browse

```bash
mcp tool firecrawl.scrape \
  --url "https://www.uncommongoods.com/gifts-for/her-birthday" \
  --format markdown
```

### Recipe 5: Goldbelly food gift (regional restaurant)

```bash
mcp tool firecrawl.scrape \
  --url "https://www.goldbelly.com/categories/birthday-gifts" \
  --format markdown
```

### Recipe 6: NY Wirecutter for trusted picks

```bash
mcp tool firecrawl.scrape \
  --url "https://www.nytimes.com/wirecutter/gifts/best-gifts-for-mom/" \
  --format markdown
```

Wirecutter is the gold standard for researched gift guides.

### Recipe 7: Cross-source compare (3-5 options)

```python
candidates = []
candidates.extend(amazon_search("leather notebook"))
candidates.extend(etsy_scrape("personalized leather notebook"))
candidates.extend(wirecutter_picks("best notebook 2026"))

# Surface 3-5 with: price + delivery + review + personalization + reason-this-fits
for c in candidates[:5]:
    print(f"{c['name']} — ${c['price']} — delivery {c['delivery']} — {c['rating']}/5")
    print(f"  Why: {c['reason']}")
```

### Recipe 8: Recipient interest pull

If recipient has Notion contact entry with interests:

```bash
mcp tool notion.get_page --page-id <recipient-page-id>
# Returns: interests, hobbies, sizes, allergies, dislikes
```

Use these to filter candidates.

### Recipe 9: Order on Amazon (deep-link)

```bash
ASIN="B01ABC123"
echo "https://www.amazon.com/dp/$ASIN?tag=<affiliate-tag>"
```

Send to user for one-click checkout.

### Recipe 10: Order on Etsy (deep-link)

Etsy has no consumer order API. Surface deep-link:

```bash
echo "https://www.etsy.com/listing/<listing-id>"
```

### Recipe 11: Card / message draft

```markdown
Dear [Name],

[Personal opening — reference recent event / shared memory]

[1-2 sentence on what this gift means]

[Closing sentiment]

Love,
[Sender name]
```

Pre-fill 3-5 options with different tones (warm / brief / heartfelt / funny).

### Recipe 12: Update gift log after delivery

```bash
mcp tool notion.add_page \
  --parent-database <gift-log-db-id> \
  --properties '{
    "Recipient":{"relation":[{"id":"<recipient-page-id>"}]},
    "Date":{"date":{"start":"2026-06-12"}},
    "Occasion":{"select":{"name":"Birthday"}},
    "Gift":{"rich_text":[{"text":{"content":"Leather notebook — Bellroy"}}]},
    "Cost":{"number":78},
    "Source":{"url":"https://amazon.com/dp/..."},
    "Delivery method":{"select":{"name":"Shipped"}},
    "Reaction":{"select":{"name":"Unknown"}},
    "Notes":{"rich_text":[{"text":{"content":"For her writing hobby; matched her style"}}]}
  }'
```

### Recipe 13: Holiday batch — 12 recipients

```python
HOLIDAY_LIST = [
    {"name":"Mom","budget":150,"interests":"reading,cooking"},
    {"name":"Dad","budget":150,"interests":"woodworking,golf"},
    {"name":"Spouse","budget":300,"interests":"yoga,travel"},
    # ...
]
for r in HOLIDAY_LIST:
    history = pull_recipient_history(r['name'])
    candidates = cross_source_research(r['interests'], r['budget'])
    print(f"\n## {r['name']} (budget ${r['budget']}):")
    for c in candidates[:3]:
        print(f"  - {c['name']} ${c['price']}")
```

### Recipe 14: Gift card option

For ambivalent recipient / last-minute:

```bash
mcp tool firecrawl.scrape \
  --url "https://www.amazon.com/gift-cards"
```

Curated picks: Amazon, Sephora, REI, Apple, restaurant-specific.

## Examples

### Example 1: Mom's birthday in 2 weeks

**Goal:** Mom turns 65; she likes cooking + reading + gardening; budget $120; ship in 1 week.

**Steps:**
1. Recipe 1: pull Mom's gift history. Last: scented candle (Loved 2025), tea sampler (Liked 2024), Le Creuset cookbook (Negative 2023 — "duplicate, already owned").
2. Recipe 8: pull interests — confirm gardening uptick.
3. Recipe 7: search Wirecutter + Amazon + Etsy for gardening + cooking gifts.
4. Surface 3 options:
   - Garden tool set (Wirecutter pick) — $95 — 3-day ship — fits gardening
   - Custom cutting board with garden quote (Etsy) — $65 — 7-day ship — personalized
   - Le Creuset garlic press (Amazon Prime) — $35 — 2-day ship — kitchen complement
5. Recommend: cutting board (personal + within budget + ships in time).
6. Recipe 9: Amazon deep-link OR Etsy deep-link.
7. Recipe 11: birthday card draft.
8. Recipe 12: log to Notion after ship.

**Result:** Personalized gift + card + logged for 2027 next-time research.

### Example 2: Last-minute thank-you to coworker

**Goal:** Coworker covered a presentation; need $25 thank-you ship next-day.

**Steps:**
1. Recipe 1: no prior history.
2. Recipe 8: pull coworker interests if logged.
3. Recipe 14: gift card option — Starbucks $25.
4. Recipe 2: Amazon thank-you mug — $18 Prime.
5. Recipe 9: order Starbucks card.
6. Recipe 11: card draft.

**Result:** Thoughtful + quick + cheap.

### Example 3: Holiday batch — 12 gifts

**Goal:** Dec 1; plan all holiday gifts.

**Steps:**
1. Recipe 13: per-recipient research.
2. Recipe 7: per-recipient top 3.
3. Surface table to user.
4. User picks one per recipient.
5. Recipe 9 / 10 batch-order all.
6. Recipe 12 log all to Notion (Status: Ordered, Date: TBD).

**Result:** Holiday list done in 90 min.

## Edge cases / gotchas

- **No Etsy public API for individuals**: Use `firecrawl-mcp`; respect ToS (no aggressive scraping).
- **Amazon affiliate tag**: If you have one, embed in URL for kickback. Otherwise plain link.
- **Wirecutter paywall**: Most Wirecutter content is open; some recent picks gated. `firecrawl-mcp` may not get gated.
- **Allergy / dietary on food gifts**: ALWAYS confirm dietary before food (Goldbelly, etc.). Severe allergies = absolute no.
- **Personalization deadline**: Etsy personalized gifts often have 2-4 week lead time. Don't promise ship-in-3-days.
- **Recipient size unknown**: For clothing, don't recommend unless size known. Surface as "size needs confirming" or skip clothing.
- **Repeat gift avoidance**: Recipe 1 history is critical. Without it, will repeat gifts. Maintain log religiously.
- **Reaction logging**: User may not know reaction immediately. Update later (post-occasion check).
- **Group gifts**: For office / friend group, surface group gift platforms (Greetly / GiftCrowd) but agent doesn't run them.
- **Currency / international**: For international gift, ensure store ships to recipient country + currency match.
- **Gift wrap option**: Most retailers offer; surface as opt-in.
- **Tax / shipping surprise**: Final total > listed price due to tax + shipping. Surface estimated total.
- **Backorders / out-of-stock**: Check stock before recommending.
- **Holiday shipping deadlines**: Surface USPS / UPS / FedEx cutoffs (Dec 15 for ground; Dec 20 for 2-day; Dec 22 for overnight).
- **No-name brand risk**: Cheap Amazon brands may not be quality. Filter by review count + rating + brand recognition.
- **Discounted item authenticity**: For luxury (e.g., Bellroy, Le Creuset), buy from authorized retailers — not 3rd party.

## Sources

- [NYT Wirecutter Gifts](https://www.nytimes.com/wirecutter/gifts/)
- [Notion API](https://developers.notion.com/)
- [Amazon (search via amazon-mcp)](https://www.amazon.com/)
- [Etsy](https://www.etsy.com/)
- [Uncommon Goods](https://www.uncommongoods.com/)
- [Goldbelly](https://www.goldbelly.com/)
- [1-800-Flowers](https://www.1800flowers.com/)
- [Wirecutter Holiday Gift Guides](https://www.nytimes.com/wirecutter/gifts/best-gifts-2025/)
