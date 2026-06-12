<!--
Source: https://developer.doordash.com/en-US/ + https://developer.uber.com/ + https://docs.instacart.com/
-->
# Errand Routing — DoorDash / Uber Eats / Instacart / Shipt — SKILL

Compare price + availability across delivery platforms, then surface the best option as a deep-link or browser-automation flow. No public consumer-ordering APIs exist (each platform reserves transaction surface to themselves) — agent does price compare + recommendation + user-completion.

## When to use this skill

- **"Order dinner / lunch / groceries"** — single-trip food/grocery delivery.
- **"Cheapest groceries this week"** — multi-store comparison.
- **"Multi-stop errand" (drugstore + dry-cleaner + pickup)** — TaskRabbit pattern.
- **Last-minute "I forgot X for tonight's dinner"** — Same-day delivery rescue.

**Do NOT use this skill when:**
- Restaurant reservation (sit-down) — see `restaurant-reservations-opentable-resy-tock`.
- Gift research (delivery is tangential) — see `gift-research-shopping`.
- Scheduling household appointments — see `family-calendar-coordination`.

## Pick the right platform

| Need | Platform | Why |
|---|---|---|
| Largest US food delivery + retail (DashMart) | **DoorDash** | Largest network; DashPass |
| Food + groceries (Cornershop) + Uber One | **Uber Eats** | Loyalty integration with Uber |
| Costco / Whole Foods / H-E-B / Wegmans groceries | **Instacart** | Best for full-grocery delivery |
| Target + Costco specifically | **Shipt** | Target-owned |
| Multi-stop errands; handyman | **TaskRabbit** | Hourly worker booking |
| White-glove concierge | **Sandwich** | Premium; everything done for you |
| Amazon brand goods + general retail | **Amazon Fresh / Same-Day** | Prime ecosystem |

## Setup

### DoorDash Drive (Partner API — not consumer)

DoorDash Drive is fulfillment for partner-businesses, not consumer ordering.

```bash
# Partner credentials required: https://developer.doordash.com/en-US/
# Not applicable for individual consumers.
```

### Uber Direct (Partner API)

Same pattern. Not consumer-facing.

### Instacart Connect (Partner)

Connect API is partner only.

### Browser automation via `playwright-mcp`

Primary consumer path: navigate + extract + surface deep-link.

```bash
mcp tool playwright.navigate \
  --url "https://www.doordash.com/store/<restaurant>"
mcp tool playwright.snapshot
```

### `firecrawl-mcp` for menu / price scrape

```bash
mcp tool firecrawl.scrape \
  --url "https://www.instacart.com/store/costco/storefront" \
  --format markdown
```

## Common recipes

### Recipe 1: Multi-platform price compare (single item)

```bash
ITEM="organic chicken breast 2lb"

for store in costco wholefoods kroger; do
  mcp tool firecrawl.scrape \
    --url "https://www.instacart.com/store/$store/search?q=$(echo $ITEM | sed 's/ /+/g')" \
    --format markdown > "${store}.md"
done

# Then parse + compare prices
```

### Recipe 2: DoorDash deep-link for restaurant

```bash
# Build user-clickable URL
echo "https://www.doordash.com/store/<restaurant-slug>"
```

Send via `gmail-mcp` or copy to clipboard for user.

### Recipe 3: Uber Eats deep-link

```bash
echo "https://www.ubereats.com/store/<restaurant-slug>"
```

### Recipe 4: Instacart deep-link for grocery order

```bash
echo "https://www.instacart.com/store/costco/storefront"
```

### Recipe 5: Restaurant + menu lookup

```bash
mcp tool firecrawl.scrape \
  --url "https://www.doordash.com/store/<restaurant-slug>" \
  --format markdown > menu.md

# Extract structured items + prices
```

### Recipe 6: Grocery list → Instacart pre-fill

Instacart accepts shared lists via URL. Not directly via API, but user can:
1. Build the list in Notion / Apple Reminders.
2. Export as plain text.
3. Open Instacart, paste into search-and-add.

```bash
# Build list
mcp tool apple-reminders.list --list "Groceries" --include-completed false > list.txt

# Format for paste-in
cat list.txt | awk '{print $0}'
```

### Recipe 7: TaskRabbit booking (multi-stop errand)

TaskRabbit has no direct API for individuals. Build the task brief + surface deep-link:

```markdown
**TaskRabbit brief**
- Tasks: Pick up dry cleaning at Rinse Soma, drop at home; pick up package from FedEx Ship & Save
- Date/time: 2026-06-12 between 12-3pm
- Address: home @ <address>
- Budget: $40-60
- Notes: Ring buzzer 2B
```

User books at https://www.taskrabbit.com/.

### Recipe 8: Schedule order time

For DoorDash / Uber Eats, can schedule:

```bash
# Surface schedule-for URL
SCHEDULED_TIME="2026-06-12T18:30"
echo "Schedule via DoorDash: https://www.doordash.com/store/<>/?scheduled_for=$SCHEDULED_TIME"
```

### Recipe 9: Track delivery via order email

After user completes order, agent watches Gmail for delivery confirmation:

```bash
mcp tool gmail.search \
  --query "from:no-reply@doordash.com subject:order from:today" \
  --max-results 5
```

Pull tracking link; surface to user.

### Recipe 10: Recurring grocery order

Set up via `n8n-workflow-automation`:

```yaml
- trigger: every Sunday 10am
- step: notion.get_grocery_list
- step: format for Instacart
- step: surface "Open Instacart pre-filled" deep-link
- step: send via gmail-mcp
```

### Recipe 11: "Where's my order?" status check

```bash
mcp tool gmail.search \
  --query "from:noreply@doordash.com OR from:no-reply@ubereats.com subject:order newer_than:1d"
```

Extract latest status from most-recent thread.

### Recipe 12: Apple Shortcuts integration

For iOS users, Siri Shortcut: "Order dinner from <fav restaurant>" → opens DoorDash on the restaurant page.

```bash
# Generate Shortcuts URL
echo "shortcuts://x-callback-url/run-shortcut?name=OrderDinner&input=Carbone"
```

### Recipe 13: Cost analysis — meal delivery vs grocery

```python
WEEKLY_ORDERS_MOST_RECENT = [...]
total_delivery = sum(o['total'] for o in WEEKLY_ORDERS_MOST_RECENT)
total_groceries = ... # from Lunch Money / Actual Budget
print(f"Delivery: ${total_delivery}; Groceries: ${total_groceries}")
```

Recommend balance if delivery exceeds grocery + suggest meal planning.

## Examples

### Example 1: Quick dinner — compare 3 platforms

**Goal:** "Order Thai food for tonight, fastest delivery."

**Steps:**
1. Recipe 1: search "Thai" across DoorDash, Uber Eats, Postmates (now Uber Eats).
2. Compare: prep time + delivery fee + ETA + restaurant rating.
3. Recommend: "Lemongrass — 35min ETA, $3.99 delivery on DoorDash."
4. Recipe 2: surface DoorDash deep-link.
5. Recipe 9: track confirmation after.

**Result:** Best option surfaced; user clicks once.

### Example 2: Weekly Costco order

**Goal:** Build + submit recurring Costco order.

**Steps:**
1. Recipe 10: pull grocery list from Notion.
2. Recipe 4: surface Instacart Costco deep-link.
3. Recipe 6: format list for paste-into Instacart search.
4. User adds + checks out.
5. Recipe 9: track delivery email.

**Result:** Order placed in <5 min vs 20 min freehand.

### Example 3: Multi-stop errand

**Goal:** "Need someone to pick up dry cleaning + package + ice for tonight's party."

**Steps:**
1. Recipe 7: format TaskRabbit brief.
2. Surface link with brief copy-paste.
3. User books on TaskRabbit.
4. Recipe 11: agent tracks via Gmail.

**Result:** TaskRabbit gig dispatched.

## Edge cases / gotchas

- **No consumer ordering APIs**: All recipes are search + recommend + surface deep-link. Don't promise automated placement.
- **DashPass / Uber One stacking**: Per-user loyalty programs — agent recommends matching the user's existing subscription.
- **Pricing parity**: Same restaurant on multiple platforms often has different prices (platform-set markups). Compare line by line.
- **Delivery fee + service fee + tip + tax**: The "menu price" doesn't equal cart total. Surface the cart-total estimate when possible.
- **Tip etiquette**: Default 15-20% in US. Surface tip estimate.
- **Tracking confirmation email**: For Gmail-only tracking, ensure user's email is the one used at checkout.
- **Instacart batching**: Multi-store Instacart orders can batch with one shopper; cheaper but slower.
- **Schedule vs ASAP**: Schedule-for window saves money + supply chain — recommend if 1h+ flexibility.
- **TaskRabbit rate**: Average $30-60/hr + 7% service fee. Source: https://www.taskrabbit.com/services
- **Sandwich tier**: Premium concierge $40-60/hr; only recommend for very-white-glove. Source: https://www.sandwich.co/
- **Amazon Fresh delivery window**: Requires Prime; limited to selected cities.
- **Same-day vs next-day**: Same-day in Amazon Same-Day = $9.99/order or free Prime if >$25.
- **No-touch / contact-free**: All platforms default to leave-at-door; verify if signature needed.
- **Refund / missing items**: Each platform's policy differs. DoorDash 30-day window; Instacart immediate refund for missing.
- **Sub policy**: Instacart shoppers may substitute. User should set substitution rules pre-order; agent surfaces this.
- **Restaurant hours**: Don't recommend a restaurant after hours. Verify hours before recommending.
- **Allergies**: For severe allergies, recommend user call restaurant directly + add explicit notes in order. Surface this prominently.

## Sources

- [DoorDash Developer](https://developer.doordash.com/en-US/)
- [Uber Direct](https://developer.uber.com/)
- [Instacart Connect](https://docs.instacart.com/)
- [Shipt](https://www.shipt.com/)
- [TaskRabbit](https://www.taskrabbit.com/)
- [Sandwich](https://www.sandwich.co/)
- [Amazon Fresh](https://www.amazon.com/amazonfresh)
