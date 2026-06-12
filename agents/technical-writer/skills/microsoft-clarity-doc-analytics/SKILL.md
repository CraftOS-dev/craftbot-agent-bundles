---
name: microsoft-clarity-doc-analytics
description: Behavioral analytics for docs sites with Microsoft Clarity — free, unlimited sessions, heatmaps, click-streams, scroll depth, rage clicks, dead clicks. Native MCP server for zero-config Claude integration. Use when auditing what readers actually do.
---

# Microsoft Clarity — Doc Analytics

Microsoft Clarity is the 2026 SOTA free behavioral analytics tool for docs sites. Unlike GA4 (event counts) or Algolia Insights (search queries), Clarity captures **what readers actually do**: where they click, how far they scroll, where they rage-click, where they abandon. It's free with unlimited sessions, has a native MCP server, and integrates with Claude in one config step.

## When to use this skill

- Audit which doc pages have the highest exit rates (treat as bugs).
- Identify rage clicks and dead clicks (broken interactions).
- See scroll-depth heatmaps to know where readers stop reading.
- Replay specific sessions to see how a user struggled.
- Cross-reference behavioral signals with content gaps.

## Setup

### Install Clarity on the docs site

1. Sign up at https://clarity.microsoft.com — free, no credit card.
2. Create a project; get the project ID.
3. Add the tracking script to the docs site `<head>`:

```html
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "PROJECT_ID");
</script>
```

Per platform:

- **Mintlify:** `docs.json` → `"integrations": { "clarity": { "projectId": "PROJECT_ID" } }`.
- **Docusaurus:** `docusaurus.config.js` → add `'@microsoft/clarity-script'` plugin (community) OR inject via `headTags`.
- **MkDocs Material:** `mkdocs.yml` → `extra: { analytics: { provider: custom } }` + override partial.
- **VitePress:** `.vitepress/config.ts` → `head: [['script', {}, 'clarity script']]`.
- **Starlight:** `astro.config.mjs` → `head: [{ tag: 'script', content: 'clarity script' }]`.

### Connect the MCP server (Claude Desktop / Claude Code)

```json
// .mcp.json
{
  "mcpServers": {
    "clarity": {
      "command": "npx",
      "args": ["-y", "@microsoft/clarity-mcp-server"],
      "env": {
        "CLARITY_API_TOKEN": "<token from clarity dashboard>",
        "CLARITY_PROJECT_ID": "<project id>"
      }
    }
  }
}
```

The Clarity MCP exposes tools for:

- `list_pages` — top URLs by sessions / scroll depth / exit rate.
- `get_heatmap` — heatmap data for a URL.
- `get_session_recordings` — recordings filtered by criteria (rage clicks, dead clicks, etc).
- `get_metrics` — aggregated metrics for a date range.

Restart Claude after writing `.mcp.json`.

## Common recipes

### Recipe 1: Find high-exit pages

```
Use Clarity MCP to list the top 20 docs pages by exit rate over the last 30 days.
```

The agent calls `clarity.list_pages(metric="exit_rate", limit=20, since="30d")` and ranks them. Treat each as a doc bug.

### Recipe 2: Identify rage clicks

```
Use Clarity to surface URLs with rage-click counts > 5 in the last week.
```

Rage clicks usually mean: a heading looks clickable but isn't; a code-fence copy button is broken; a link is dead.

### Recipe 3: Scroll-depth heatmaps

```
Use Clarity to show the 25th / 50th / 75th percentile scroll depth on /quickstart.
```

If 50% of readers exit before reaching "Step 2", the content above is too long.

### Recipe 4: Replay specific session

```
Use Clarity to fetch 3 session recordings on /api-reference where the user spent > 60 seconds and exited without clicking a "Try it" button.
```

Watch the replays to find friction.

### Recipe 5: Filtered metrics

```
Compare engagement (time on page, scroll depth) for /tutorials/getting-started before and after the June 2026 rewrite.
```

The agent calls `get_metrics(url="/tutorials/getting-started", since="2026-06-01", until="2026-06-30")` and the matching prior-month query.

## Reading Clarity insights

- **Dead click rate > 2%:** broken interactive element. Fix immediately.
- **Rage click rate > 1%:** UX confusion. Investigate.
- **Quick-back rate > 15%:** the page didn't deliver. Audit the title vs content match.
- **Scroll depth p50 < 25%:** too long OR boring at the start. Tighten the hook.
- **Avg engaged time > 3 min on reference page:** the page is doing its job.

## Privacy and compliance

- Clarity strips PII automatically (form inputs, passwords, credit cards).
- GDPR-compliant; project owners can enable masked recordings for stricter compliance.
- For EU traffic, mention Clarity in the cookie consent banner.
- Set `<meta name="clarity-mask-text" content="false">` to allow text capture (default is masked for `<input>`).

## Edge cases

- **SPA route changes:** Clarity auto-tracks pushState; verify by checking the dashboard's "Pages" tab for SPA routes.
- **Authenticated docs:** Clarity captures everything inside the session — make sure your privacy policy reflects this.
- **High-traffic sites:** Clarity samples sessions if traffic exceeds project limits; check the dashboard for sampling rate.
- **Performance impact:** the tracking script is ~30KB gzipped, loads async, < 50ms TTI impact.

## Pairs well with

- `ga4-doc-analytics` — Clarity for behavior, GA4 for traffic / acquisition.
- `algolia-doc-search` — Clarity for behavior, Algolia Insights for what readers SEARCH for.

## Sources

- Clarity: https://clarity.microsoft.com/
- Clarity MCP server: https://learn.microsoft.com/en-us/clarity/third-party-integrations/clarity-mcp-server
- Clarity API: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api
