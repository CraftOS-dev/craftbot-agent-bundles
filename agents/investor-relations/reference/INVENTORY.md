# investor-relations — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) and from cross-referencing the sibling `finance-agent/reference/SOTA_USE_CASES.md` which shares the underlying capital-markets / cap-table / investor data room stack.

## Adjacent v1 agent mirrored

- `agent_bundle/agents/finance-agent/` — strategic finance / fractional CFO. The `investor-relations` agent is a PEER (not a replacement) — capability split:
  - **finance-agent owns:** financial modeling, term sheet review, 409A negotiation, capital allocation, capital structure, FX hedging, treasury yield, IPO readiness modeling, M&A valuation modeling, board CFO financial package (the numbers).
  - **investor-relations owns:** monthly/quarterly investor updates (cadence + voice + distribution), earnings call script + Q&A prep, public-company SEC filing drafting support (10-K/10-Q/8-K/proxy/S-1 *drafting*), analyst relations + briefings, IR website + earnings press release, roadshow + NDR logistics, 13F shareholder tracking, shareholder Q&A maintenance, ESG-for-investors reporting (GRI/SASB/TCFD), investor day / capital markets day, quiet period management, embargoed disclosure protocols, M&A communications to street, fund-of-funds + LP reporting, dividend / buyback / secondary comms.
  - **Shared (consult both):** investor updates (finance-agent drafts the financial slides + CFO-voice numbers; investor-relations sets cadence + audience segmentation + distribution + IR-platform mechanics), board package (finance-agent owns financial slides; investor-relations owns investor-attendee Q&A + post-board investor digest), data room curation (finance-agent owns financials + cap table sections; investor-relations owns NDA flow + access sequencing + DocSend engagement analytics interpretation).

## Sibling agents and hand-offs

- `ceo-agent` — owns board management + exec strategy + the CEO-voice narrative. Investor-relations partners with CEO on earnings call script (CEO opens, CFO does financials, IR runs Q&A flow + analyst routing).
- `finance-agent` — owns financial modeling + capital allocation + treasury + term sheet review + 409A. Investor-relations consumes finance-agent's numbers; finance-agent consumes investor-relations' analyst-Q-pulse + 13F holder churn.
- `legal-counsel` — owns binding SEC filings sign-off (10-K/10-Q/8-K/proxy are filed by counsel; agent drafts), Reg FD + Reg G interpretation, securities-law disclosure decisions, insider-trading window mechanics. Investor-relations defers binding to counsel; drafts to a counsel-reviewable bar.
- `compliance-agent` — owns governance framework selection (ISS/Glass Lewis policy alignment, ESG framework choice GRI/SASB/TCFD), proxy advisory firm engagement, Reg-FD playbook design. Investor-relations executes the playbook compliance designs.

## Research method

For Round 1 (this pass), SOTA tools were identified via web search (June 2026 fresh queries) against:

1. Private-company investor update platforms (Visible.vc, DocSend, Papermark, AngelList Updates, Carta Investor Reporting, Foundersuite, Capboard, Sturppy).
2. Pitch / deck platforms (Pitch.com, Beautiful.ai, Gamma, Tome).
3. Public-company IR platforms + SEC filing tools (Workiva, Q4 Inc., Notified, Intelligize, Donnelley RDG, Toppan Merrill, OnSemiCDP, Stream NYSE, Nasdaq IR).
4. Equity analyst research databases (AlphaSense, Sentieo, Tegus expert-call platform, PitchBook, S&P Capital IQ, FactSet, Refinitiv, Bloomberg Terminal).
5. Proxy + governance (Glass Lewis, ISS Voting Insights, Diligent Boards, Boardvantage, Computershare).
6. News + media monitoring (Mention.com, Brandwatch, Talkwalker, Meltwater, Google Alerts, Cision).
7. ESG reporting frameworks (GRI Standards 2025, SASB Standards via IFRS S1/S2, TCFD, MSCI ESG Ratings, Sustainalytics, S&P Global ESG, CDP).
8. Earnings call mechanics + transcripts (Notified earnings call platform, OpenExchange virtual events, AlphaSense earnings call transcripts).
9. Reg FD / Reg G / quiet period rules (SEC interpretations, NIRI Standards of Practice, Investor Relations Society UK, securities-law firm guidance — Cooley, Wilson Sonsini, Latham & Watkins, Davis Polk).
10. 13F holdings + shareholder identification (Whale Wisdom, 13F Info, OnSemiCDP, SEC EDGAR XBRL).
11. Investor-day mechanics + capital markets day playbooks (Q4 Inc., Notified, ICR Inc., FTI Consulting).
12. Fund-of-funds + LP reporting (Visible.vc LP variant, ILPA standards, Allvue, Carta LP Reporting, Affinity).

## For future tightening

Pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` (look for `investor-relations`, `ir-officer`, `corporate-communications`, `analyst-relations`, `proxy-advisor` slugs) into `reference/agents/`, and 6-10 reference skills (look for `earnings-call-script`, `10-k-drafting`, `proxy-statement`, `investor-update`, `analyst-briefing`, `esg-reporting`, `roadshow-logistics`, `quiet-period-mgmt`) into `reference/skills/`.

For the v1 round, the deferred-research model (web search + sibling-agent cross-reference) was used to keep round-1 momentum. The SOTA mapping in `reference/SOTA_USE_CASES.md` is comprehensive enough to drive `agent.yaml`, `soul.md`, and `role.md` at the methodology bar (≥90% fulfillment), with each row citing a 2025-2026 source URL.
