# finance-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) and from cross-referencing the sibling `finance-controller/reference/SOTA_USE_CASES.md` which shares the underlying accounting/billing/banking/cap-table stack.

## Adjacent v1 agent mirrored

- `agent_bundle/agents/finance-controller/` — operational/tactical finance (bookkeeping, monthly close, AR/AP, 13-week cash). The `finance-agent` is a PAIR — strategic finance / fractional CFO — NOT a replacement. Capability split:
  - **finance-controller owns:** bookkeeping, monthly close, ASC 606 mechanics, AR/AP, audit prep, sales tax, vendor audits, runway computation from closed books.
  - **finance-agent owns:** capital allocation, fundraising strategy (SAFE/priced/venture debt/RBF/secondaries), M&A consideration, FP&A long-range planning, term sheet review, IPO readiness, treasury yield strategy, optimal capital structure, equity comp design, market sizing, scenario/Monte Carlo modeling, board CFO package, investor relations strategy.
  - **Shared (consult both):** investor updates (controller drafts metric pack; agent shapes narrative + asks), unit economics (controller computes; agent interprets vs strategic posture), fundraising data room (controller assembles operational artifacts; agent leads narrative + term sheet review).

## Research method

For Round 1 (this pass), SOTA tools were identified via web search (June 2026 fresh queries) against:

1. Strategic finance / fractional CFO platforms (Knolli, Pry/Brex, Runway, Mosaic, Causal, Cube, Drivetrain).
2. Investor research databases (PitchBook, CB Insights, Crunchbase, Tracxn, AngelList Pro).
3. Cap-table / 409A / equity comp (Carta, Pulley, AngelList Stack, Cooley GO, NVCA Model Documents Oct 2025 update).
4. Investor data room + reporting (Visible.vc, DocSend, Carta IR, Foundersuite, Papermark).
5. Capital sources beyond VC (Stripe Capital, Capchase, Pipe.com, Founderpath, Wayflyer, Lighter Capital, ECL/Re-cap, Bigfoot Capital).
6. Treasury / yield (Rho, Mercury Treasury, Brex Yield, Wealthfront Cash, Public.com Treasury, Meow, TreasuryDirect).
7. M&A / corp dev (DealRoom, Intralinks, Finsider, EisnerAmper QoE, Bain/McKinsey/BCG public playbooks).
8. International / FX (Wise Business, Airwallex, Revolut Business, Mercury International, OANDA, XE).
9. Tax (MainStreet, Neo.tax, Haven, Stripe Tax, QSBS strategy guides — Wilson Sonsini, Cooley, Davis Wright Tremaine 2025 Big Beautiful Bill update).
10. Public/private equity research (Damodaran NYU 2026 datasets, SEC EDGAR, Yahoo Finance, S&P Capital IQ).
11. NVCA Model Documents (Oct 2025 update — tranched financings, anti-dilution, liquidation preference defaults).
12. IPO readiness (Cross Country Consulting, Carta, Deloitte free IPO readiness tool, EisnerAmper guide).

## For future tightening

Pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` (look for `cfo`, `strategic-finance`, `fundraising`, `corporate-finance` slugs) into `reference/agents/`, and 6-10 reference skills (look for `fundraising-strategy`, `term-sheet-review`, `cap-table-modeling`, `pitch-deck-financials`, `qoe-analysis`, `fpa-modeling`, `capital-allocation`, `m-and-a-due-diligence`) into `reference/skills/`.

For the v1 round, the deferred-research model (web search + sibling-agent cross-reference) was used to keep round-1 momentum. The SOTA mapping in `reference/SOTA_USE_CASES.md` is comprehensive enough to drive `agent.yaml`, `soul.md`, and `role.md` at the methodology bar (≥90% fulfillment), with each row citing a 2025-2026 source URL.
