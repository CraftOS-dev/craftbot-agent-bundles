# legal-counsel — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening, pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills into `reference/skills/`. Candidate agents to mirror once available:

- Legal counsel / contracts reviewer (any of: VoltAgent legal-counsel, msitarzewski legal-advisor, wshobson legal/compliance plugin agents)
- Compliance auditor (SOC2 / GDPR / CCPA)
- IP / trademark / patent search
- Equity grants / cap table specialist

## Sources considered but not downloaded

- **Anthropic skills repo** — no published `legal` skills as of June 2026.
- **wshobson plugins** — no dedicated `legal` plugin yet; closest is `compliance-and-governance` (not yet downloaded).
- **VoltAgent categories** — `08-finance-and-legal` houses a `legal-advisor` and `contract-reviewer`; queued for v1 refresh.

## SOTA tooling sources

Primary research lanes for the agent's day-to-day stack (each cited per use case in `SOTA_USE_CASES.md`):

1. **Contract review / CLM** — Ironclad, Robin AI, Spellbook, Harvey AI, LegalSifter, Diligen, Kira (Litera), eBrevia, ZUVA, Lexion, Evisort, LinkSquares, Concord, ContractWorks.
2. **E-signing** — DocuSign, Adobe Sign, Dropbox Sign (HelloSign), PandaDoc.
3. **Template libraries** — Bonterms, Common Paper, Y Combinator SAFE, Cooley GO, Stripe Atlas, Clerky.
4. **IP search** — USPTO TESS, USPTO Patent Public Search, Google Patents, Lens.org, WIPO Global Brand Database, Trademarkia.
5. **Privacy / GDPR / CCPA generators** — Iubenda, Termly, Cookiebot, Osano, OneTrust, TrustArc.
6. **SOC2 / compliance automation** — Drata, Vanta, SecureFrame, Thoropass, Sprinto, Tugboat Logic, AuditBoard.
7. **Cap table / equity (legal side)** — Carta, Pulley, AngelList Stack.
8. **Regulatory / case research** — LexisNexis, Westlaw, Bloomberg Law, Thomson Reuters CoCounsel (Casetext), Fastcase, Justia (free), CourtListener (free), SEC EDGAR.

Each tool used as a SOTA mechanism in this agent has a canonical URL recorded in `SOURCES.md` "SOTA tool sources (June 2026)" and in the per-use-case rows of `SOTA_USE_CASES.md`.
