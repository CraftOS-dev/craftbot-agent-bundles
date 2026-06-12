---
name: interactive-guide-stonly-whatfix
description: Interactive KB guides — Stonly (decision-tree step guides), Whatfix (in-product Self-Help widget), Pendo Guides (analytics-driven walkthroughs), Shepherd.js (FOSS in-product tour). Use when a static how-to article isn't doing the job — readers need branching, in-product overlays, or click-by-click walkthroughs.
---

# Interactive guide creation (Stonly, Whatfix, Pendo, Shepherd.js)

## When to use

Reach for this skill when the user says: "users keep getting lost mid-flow", "we need a decision tree", "in-product walkthrough", "first-run tour", "Stonly", "Whatfix", "Pendo Guides", "interactive how-to", or "the article keeps getting feedback that it's confusing". Decision tree: customer-facing branching how-to → Stonly. In-product walkthrough overlaying real UI → Whatfix or Pendo. FOSS / dev-controlled → Shepherd.js. Skip if a Loom + show-notes article suffices (`video-kb-loom-tango-scribe`).

## Setup

```bash
# Shepherd.js (FOSS, drop-in JS library)
npm i shepherd.js

# Stonly — no install; embed via <script> snippet from dashboard
# Whatfix — no install; install browser extension for editor, embed JS in app
# Pendo Guides — no install; embed Pendo agent JS in product
```

Auth / env vars:
- `STONLY_API_KEY` — Stonly dashboard → integrations. Paid.
- `WHATFIX_API_TOKEN` — Whatfix Settings → API. Paid.
- `PENDO_INTEGRATION_KEY` — Pendo Admin → Integrations. Paid.
- Shepherd.js — none required (client-side library).

## Common recipes

### Recipe 1: Stonly decision-tree guide via REST

```bash
# Create a Stonly guide via REST API
curl -X POST 'https://api.stonly.com/api/v2/guides' \
  -H "Authorization: Bearer $STONLY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Set up SSO with Okta",
    "language": "en",
    "steps": [
      { "id": "start", "title": "Where do you administer Okta?",
        "options": [
          { "label": "Org Okta tenant", "next": "tenant-admin" },
          { "label": "Sandbox tenant", "next": "sandbox" }
        ]
      },
      { "id": "tenant-admin", "title": "Verify you have Super Admin role",
        "content": "<p>Log in to your Okta admin panel...</p>", "next": "saml-app" },
      { "id": "saml-app", "title": "Create the SAML app", "content": "<ol><li>...</li></ol>", "next": "verify" },
      { "id": "verify", "title": "Verify SSO login", "content": "<p>Test the SSO login...</p>" }
    ]
  }'
```

Embed in any docs page with the Stonly widget snippet (settings → install).

### Recipe 2: Embed Stonly widget in a KB article

```html
<!-- Drop into any docs page -->
<div id="stonly-widget"></div>
<script>
window.STONLY_WID = "<your-widget-id>";
(function(){var s=document.createElement('script');s.src='https://stonly.com/js/widget/v2/stonly-widget.js';document.head.appendChild(s);})();
window.Stonly.openGuide({ guide_id: "<guide_id>" });
</script>
```

Auto-launches when user clicks "Start interactive guide" on the article.

### Recipe 3: Whatfix Flow via REST

```bash
# Create a Whatfix Flow
curl -X POST 'https://api.whatfix.com/v1/flows' \
  -H "Authorization: Bearer $WHATFIX_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "First-run: configure webhooks",
    "url_pattern": "https://app.example.com/settings/webhooks*",
    "steps": [
      { "selector": "#webhook-url", "title": "Enter your endpoint URL", "position": "right" },
      { "selector": "#webhook-secret", "title": "Generate a signing secret", "position": "right" },
      { "selector": "#save-btn", "title": "Save the webhook", "position": "top" }
    ],
    "trigger": "on-page-load",
    "audience": "new-user"
  }'
```

`selector` is a CSS selector against the live app DOM; Whatfix overlays at runtime.

### Recipe 4: Embed Whatfix in your app

```html
<!-- index.html — once per app -->
<script>
(function(){var w=document.createElement('script');w.src='https://whatfix.com/embed/<your-app-id>.js';w.async=true;document.head.appendChild(w);})();
</script>
```

Then publish the Flow in the Whatfix dashboard — visitors see the overlay.

### Recipe 5: Pendo Guide via API

```bash
# Create a Pendo Guide
curl -X POST 'https://app.pendo.io/api/v1/guide' \
  -H "X-Pendo-Integration-Key: $PENDO_INTEGRATION_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Webhook first-run",
    "appId": "<app_id>",
    "audience": { "rule": "user.role == \"admin\" AND visits.first_visit.days_ago < 7" },
    "showAfterCondition": { "event": "Page Load", "pagePath": "/settings/webhooks" },
    "isMultiStep": true,
    "steps": [
      { "type": "lightbox", "title": "Configure your first webhook", "content": "<p>Walks you through...</p>" },
      { "type": "tooltip", "selector": "#webhook-url", "title": "Endpoint URL" }
    ]
  }'
```

### Recipe 6: Shepherd.js tour in 30 lines

```js
import Shepherd from 'shepherd.js';
import 'shepherd.js/dist/css/shepherd.css';

const tour = new Shepherd.Tour({
  defaultStepOptions: {
    cancelIcon: { enabled: true },
    classes: 'shepherd-theme-arrows',
    scrollTo: { behavior: 'smooth', block: 'center' },
  },
  useModalOverlay: true,
});

tour.addStep({
  id: 'step-1',
  title: 'Webhook endpoint',
  text: 'Paste your endpoint URL here.',
  attachTo: { element: '#webhook-url', on: 'right' },
  buttons: [{ text: 'Next', action: tour.next }],
});

tour.addStep({
  id: 'step-2',
  title: 'Signing secret',
  text: 'Generate a signing secret — keep it private.',
  attachTo: { element: '#webhook-secret', on: 'right' },
  buttons: [
    { text: 'Back', action: tour.back },
    { text: 'Next', action: tour.next },
  ],
});

tour.addStep({
  id: 'step-3',
  title: 'Save',
  text: 'Click save to register the webhook.',
  attachTo: { element: '#save-btn', on: 'top' },
  buttons: [{ text: 'Done', action: tour.complete }],
});

if (!localStorage.getItem('webhook-tour-done')) {
  tour.on('complete', () => localStorage.setItem('webhook-tour-done', 'true'));
  tour.start();
}
```

### Recipe 7: Pull Stonly analytics — completion + drop-off per step

```bash
curl -X GET "https://api.stonly.com/api/v2/guides/<guide_id>/analytics?start=$(date -d '30 days ago' --iso-8601)" \
  -H "Authorization: Bearer $STONLY_API_KEY" \
  | jq '{
      completion_rate: .completion_rate,
      avg_steps_to_complete: .avg_steps_to_complete,
      drop_off_per_step: .step_analytics | map({step: .step_id, drop_off_pct: .drop_off_pct})
    }'
```

Steps with >30% drop-off are content bugs — fix or split.

### Recipe 8: Whatfix analytics

```bash
curl -X GET "https://api.whatfix.com/v1/flows/<flow_id>/analytics?range=30d" \
  -H "Authorization: Bearer $WHATFIX_API_TOKEN" \
  | jq '{ views, starts, completions, abandonment_rate: ((.starts - .completions) / .starts) }'
```

### Recipe 9: A/B test guide variant via Pendo segments

```bash
# Create two Guide variants targeting two audience segments
curl -X POST 'https://app.pendo.io/api/v1/guide' \
  -H "X-Pendo-Integration-Key: $PENDO_INTEGRATION_KEY" \
  -d '{"name":"Webhook flow A","audience":{"rule":"user.cohort == \"A\""}, ...}'

curl -X POST 'https://app.pendo.io/api/v1/guide' \
  -H "X-Pendo-Integration-Key: $PENDO_INTEGRATION_KEY" \
  -d '{"name":"Webhook flow B","audience":{"rule":"user.cohort == \"B\""}, ...}'

# Compare completion-rate after 14d in Pendo UI or via analytics API
```

### Recipe 10: Convert a static how-to into a Stonly decision tree

```bash
# Read the markdown, build the JSON
python -c "
import frontmatter, json
m = frontmatter.load('docs/how-to/sso-okta.md')
# Heuristic: convert ## headings to steps, > Note: to tooltips
sections = m.content.split('\n## ')
steps = [{'id': f'step-{i}', 'title': s.split('\n')[0], 'content': '\n'.join(s.split('\n')[1:])} for i, s in enumerate(sections)]
for i in range(len(steps) - 1):
    steps[i]['next'] = f'step-{i+1}'
print(json.dumps({'title': m['title'], 'language': 'en', 'steps': steps}))
" | curl -X POST 'https://api.stonly.com/api/v2/guides' \
    -H "Authorization: Bearer $STONLY_API_KEY" \
    -H 'Content-Type: application/json' \
    -d @-
```

## Examples

### Example 1: SSO setup decision tree for customers across IdPs

**Goal:** Single guide that branches Okta / Auth0 / Azure AD; embed in docs.

**Steps:**
1. Define decision tree: first step = "Which IdP?" → branches.
2. Build via Recipe 1.
3. Embed widget on `docs/how-to/authentication/sso.md` (Recipe 2).
4. Track per-step drop-off (Recipe 7).
5. Iterate the step with highest drop-off.

**Result:** One canonical SSO guide for three IdPs; users no longer pick the wrong IdP article.

### Example 2: Whatfix Self-Help on webhook config — first-run

**Goal:** New users to webhooks setting page see overlay walkthrough.

**Steps:**
1. Identify the 3 critical selectors in the webhooks settings page.
2. Build the Flow via Recipe 3.
3. Embed Whatfix in app via Recipe 4.
4. Audience: `new-user` (first 7 days).
5. Monitor completion 14d (Recipe 8).

**Result:** First-run dropoff on webhooks page falls; activation rate climbs.

### Example 3: FOSS Shepherd.js tour for an OSS dev tool

**Goal:** No-budget docs site needs first-run tour for CLI install + first command.

**Steps:**
1. `npm i shepherd.js` (Setup).
2. Write the tour (Recipe 6).
3. Gate with `localStorage` so the tour shows once.
4. Add a "Restart tour" link in the docs nav for users who want it again.

**Result:** Free in-product onboarding without paying for Stonly/Whatfix/Pendo.

## Edge cases / gotchas

- **Stonly / Whatfix / Pendo are paid** — entry tiers ~$200-500/mo. Shepherd.js is the FOSS escape hatch.
- **Whatfix selectors break on SPA route changes** — use stable `data-whatfix-id` attrs in the app HTML rather than IDs that may change.
- **Pendo guide preview vs prod** — preview mode uses the dashboard URL; production requires the agent JS embedded. Don't test in dashboard only.
- **Shepherd.js z-index conflicts** — modal overlays may render below your app's own modals. Set `Shepherd.activeTour.options.useModalOverlay = false` and style your own.
- **Decision-tree explosion** — keep branching factor ≤3 per step; deep trees lose users. Use tags instead of nested branches for cross-cutting cases.
- **Stonly content lives in Stonly** — content not in your repo; redirect map + backup snapshots needed. Pull JSON via Recipe 10 on a cron.
- **In-product walkthroughs need DOM stability** — every CSS change in the app risks Flow drift. Add a lint that asserts critical `data-*` attrs are present.
- **Mobile coverage** — Stonly + Whatfix have mobile SDKs for native apps; check before assuming web overlay works in your mobile app.
- **Accessibility** — Shepherd.js and Stonly are keyboard-navigable; verify with `axe` against your live tour.
- **Localization** — Stonly supports per-language guide bundles; Whatfix supports translations per Flow; Pendo supports localized content packs. Translate the tour the same way you translate docs.
- **Don't auto-start on every page load** — once-per-user (localStorage key, Recipe 6) or gated by `audience` (Pendo/Whatfix); auto-replay annoys returning users.
- **Don't overlap with Intercom Tours / Appcues** — pick one tour platform per product; multi-overlay confuses users.
- **GDPR** — Stonly + Whatfix + Pendo each store user IDs; verify your data-processing addendum + cookie banner.

## Sources

- [Stonly API docs](https://stonly.com/help/en/category/api-1hjhf32/)
- [Stonly install JS snippet](https://stonly.com/help/en/installation-on-website-rvmpzd/)
- [Whatfix developer docs](https://docs.whatfix.com/)
- [Whatfix Flow API](https://docs.whatfix.com/admin-and-analytics-guide/analytics/whatfix-api.html)
- [Pendo Guides docs](https://help.pendo.io/resources/support-library/guides/)
- [Pendo Integrations API](https://developers.pendo.io/)
- [Shepherd.js docs](https://shepherdjs.dev/docs/)
- [Shepherd.js GitHub](https://github.com/shepherd-pro/shepherd)
- [Decision-tree-style guide pattern](https://stonly.com/blog/decision-tree-style-knowledge-base/)
