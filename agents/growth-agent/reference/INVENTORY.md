# growth-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

The agent is positioned as a **compounding-side counterpart** to `marketing-agent` (channel breadth). Where marketing-agent goes wide (SEO, social, ads, content, brand), growth-agent goes deep on the parts of growth that compound: loops, activation, retention, experimentation infrastructure, PLG, attribution.

For future tightening: pull 4-6 reference agents (Reforge growth model templates, Lenny's PLG library, Andrew Chen's loop catalog, Brian Balfour's 4-Fits, msitarzewski/agency-agents `growth-hacker`, VoltAgent `growth-loops`) into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Provenance summary (Round 1, June 2026)

| Source | What it informed |
|---|---|
| VoltAgent — growth-loops | 5 loop types, loop design process, viral coefficient (K), funnel-vs-loop framing |
| msitarzewski — growth-hacker | Growth strategy (funnel + retention + LTV), experimentation framework, success metrics (Day 7/30/90 retention, CAC payback, LTV:CAC, K-factor, experiment velocity) |
| Reforge / Brian Balfour 4-Fits | Market-product, product-channel, channel-model, model-market fit framework (referenced) |
| Lenny's Newsletter PLG library | Activation event vs aha moment, time-to-value benchmarks, retention curve diagnosis |
| Andrew Chen — The Cold Start Problem | Network-effect loops, atomic-network thinking |
| Pocus PQL Guide | PQL framework, scoring concepts, hand-off to sales |
| Web-research SOTA URLs | Statsig, Amplitude, Mixpanel, PostHog, GrowthBook, Robyn, Meridian, Hightouch, Userpilot, Appcues, Pendo, Intercom Fin, Sprig, Survicate, Customer.io, Braze, Iterable, ReferralCandy, GrowSurf, lifelines (Python survival analysis) — see SOURCES.md SOTA tool table for full list |
