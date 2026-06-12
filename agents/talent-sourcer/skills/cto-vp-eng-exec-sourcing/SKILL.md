<!--
Sources: https://rocketreach.co/
         https://www.lusha.com/api
         https://www.findymail.com/blog/best-email-finder-tools/
Exec sourcing: 2nd-degree warm + Sales Nav + Lusha (verified exec phones) +
RocketReach (700M+ contacts) + ContactOut (alt email + cell). 2-source verification
mandatory. Defer comp + offer to ceo-agent.
-->
# CTO / VP-Eng Executive Sourcing — SKILL

Source executive engineering leaders (CTO, VP Eng, Head of Engineering) via a 3-layer target list (competitors + acquired startups + megacap senior tier), Lusha/RocketReach/ContactOut for 2-source contact verification, warm-intro-mandatory routing, brief packet handoff to ceo-agent. Defer compensation strategy + offer structure to ceo-agent.

## When to use

- User wants to **source a CTO, VP Engineering, Head of Engineering, or SVP** candidate.
- User asks "find me 10 VP Eng candidates for our Series C".
- User wants to **build an exec target list with warm-intro paths identified**.
- User wants **verified executive contact info** (phone, personal email, alt-channel).
- Trigger phrases: "exec sourcing", "CTO search", "VP Eng candidate", "executive contact verification", "warm intro to {exec}", "C-suite source".

Do not use for: IC / manager-level sourcing (`linkedin-recruiter-boolean-search-strings` + `passive-candidate-outreach-campaigns`); compensation strategy (`ceo-agent`); board-level recruiting (defer to `ceo-agent` + executive search firm).

## Setup

```bash
# Lusha — verified executive direct phones + business emails.
# https://www.lusha.com/api
export LUSHA_API_KEY="xxx"

# RocketReach — 700M+ professional contact DB.
# https://rocketreach.co/
export ROCKETREACH_API_KEY="xxx"

# ContactOut — alt email (personal) + cell + Chrome extension.
# https://contactout.com/
export CONTACTOUT_API_KEY="xxx"

# Findymail — <5% bounce rate; pairs well as 2-source check.
export FINDYMAIL_API_KEY="xxx"

# Pave / Carta Total Comp / Levels.fyi — exec comp benchmark reference (paid).
# Comp negotiation deferred to ceo-agent; this skill just references bands.
```

## Common recipes

### Recipe 1: Build the 3-layer exec target list

```python
def build_exec_target_list(role_brief):
    """
    Layer 1: Direct competitors (same sector + stage).
    Layer 2: Acquired startups 2-3 years post-acquisition (talent looking again).
    Layer 3: Late-stage / megacap engineering orgs (Google L7+, Meta E7+, Stripe / Snowflake / Databricks senior).
    """
    targets = []

    # Layer 1: Competitors via Crunchbase
    competitors = crunchbase_search(
        sector=role_brief["sector"],
        stage=role_brief["stage"],
        headcount=role_brief["headcount_range"]
    )
    # Per competitor: LinkedIn Sales Nav search for CTO / VP Eng
    for c in competitors:
        execs = linkedin_sales_nav_search(
            current_company=c["name"],
            current_title="CTO OR 'VP Engineering' OR 'Head of Engineering'"
        )
        targets.extend([{**e, "layer": 1, "source": c["name"]} for e in execs])

    # Layer 2: Acquired startups 2-3y post-acquisition
    acquired = crunchbase_search_acquisitions(
        years_ago_range=(2, 3),
        sector=role_brief["sector"]
    )
    for a in acquired:
        # Pre-acquisition CTO / co-founder often still at acquirer in senior role
        founders = crunchbase_get_founders(a["id"])
        for f in founders:
            current = linkedin_lookup(f["linkedin_url"])
            if current["seniority"] in ["VP", "Director", "Staff"]:
                targets.append({**f, **current, "layer": 2, "source": a["name"]})

    # Layer 3: Megacap senior — Google L7+ / Meta E7+ / Stripe / Snowflake / Databricks
    megacap_seniors = linkedin_sales_nav_search(
        current_company="Google OR Meta OR Stripe OR Snowflake OR Databricks",
        title="Engineering Director OR 'Director, Engineering' OR 'Sr Director, Engineering'",
        tenure_at_current="3+yr"
    )
    targets.extend([{**e, "layer": 3, "source": e["current_company"]} for e in megacap_seniors])

    return targets
```

### Recipe 2: Score candidates by movement signal

```python
def score_exec_candidate(c):
    """Score 0-100 for likely-to-move + role-fit."""
    score = 0

    # Tenure at level — 3-5y at exec level signals open to move
    tenure = c.get("years_at_current_role", 0)
    if 3 <= tenure <= 5:
        score += 25
    elif tenure < 2:
        score += 5
    elif tenure > 7:
        score += 10  # boomerang-style — stable + recognized

    # Recent funding event at current employer — predicts opportunity OR dissatisfaction
    if c.get("current_company_funded_in_90d"):
        score += 20
    elif c.get("current_company_funded_in_180d"):
        score += 10

    # Recent acquisition — earn-out vesting likely complete; openness rises
    if c.get("acquired_2_3y_ago"):
        score += 20

    # Domain depth match
    if c.get("sector_match") == "exact":
        score += 25
    elif c.get("sector_match") == "adjacent":
        score += 12

    # Geography / remote-OK
    if c.get("geography_match"):
        score += 10

    return score
```

Cutoffs: ≥70 = high-priority; 50-69 = medium; <50 = skip.

### Recipe 3: 2-source contact verification (mandatory for exec outreach)

```bash
# Source 1: Lusha — verified business email + direct phone
curl -X GET "https://api.lusha.com/v2/person" \
  -H "api_key: $LUSHA_API_KEY" \
  -G --data-urlencode "linkedinUrl=https://linkedin.com/in/janedoe"

# Source 2: RocketReach — alt email + cell
curl "https://api.rocketreach.co/v2/api/lookupProfile?api_key=$ROCKETREACH_API_KEY&linkedin_url=https://linkedin.com/in/janedoe"

# Source 3 (alt): ContactOut — best on personal email when business unknown
curl -X POST "https://api.contactout.com/v1/people/linkedin" \
  -H "Authorization: $CONTACTOUT_API_KEY" \
  -d '{"linkedin_url": "https://linkedin.com/in/janedoe"}'

# Verification rule:
# Source 1 email == Source 2 email → high confidence (use email)
# Source 1 email != Source 2 email → cross-check via Findymail
# < 2 sources confirm → SKIP outreach (sender rep > volume for execs)
```

Reject candidates without 2-source confirmation. Exec sender reputation is sacred — 1 bounce to a board member's network destroys 6 months of brand.

### Recipe 4: Findymail third-source check (when sources 1+2 disagree)

```bash
curl -X POST "https://app.findymail.com/api/search" \
  -H "Authorization: Bearer $FINDYMAIL_API_KEY" \
  -d '{
    "linkedin_url": "https://linkedin.com/in/janedoe",
    "first_name": "Jane",
    "last_name": "Doe",
    "company": "Stripe"
  }'

# Findymail proprietary verification — <5% bounce rate
# Use as tiebreaker when Lusha + RocketReach disagree
```

### Recipe 5: Identify warm-intro path per candidate

```python
def find_warm_intro_path(target_exec, your_co):
    """Find a mutual board member, investor, ex-colleague, or school cohort."""
    paths = []

    # Path 1: Mutual board member or investor
    target_board = crunchbase_get_board(target_exec["current_company"])
    your_co_board = crunchbase_get_board(your_co)
    mutual_board = set(target_board) & set(your_co_board)
    if mutual_board:
        paths.append({"type": "board_member", "via": mutual_board, "strength": 9})

    # Path 2: Shared past-employer alum cohort
    target_history = linkedin_get_work_history(target_exec)
    your_team_history = linkedin_get_team_work_history(your_co)
    shared_companies = set(c["name"] for c in target_history) & set(c["name"] for c in your_team_history)
    if shared_companies:
        paths.append({"type": "alum", "via": shared_companies, "strength": 7})

    # Path 3: Shared school + cohort year
    target_schools = linkedin_get_education(target_exec)
    your_team_schools = linkedin_get_team_education(your_co)
    shared_school_cohorts = [
        (s, t) for s, t in itertools.product(target_schools, your_team_schools)
        if s["school"] == t["school"] and abs(s["grad_year"] - t["grad_year"]) <= 2
    ]
    if shared_school_cohorts:
        paths.append({"type": "school_cohort", "via": shared_school_cohorts, "strength": 5})

    # Path 4: Mutual investor (smaller funds with concentrated portfolios)
    your_investors = crunchbase_get_investors(your_co)
    target_investors = crunchbase_get_investors(target_exec["current_company"])
    mutual_investors = set(your_investors) & set(target_investors)
    if mutual_investors:
        paths.append({"type": "investor", "via": mutual_investors, "strength": 8})

    return sorted(paths, key=lambda p: -p["strength"])
```

If no path exists → either hold outreach until a path is found OR defer exec to executive search firm. Warm intros for execs are non-negotiable.

### Recipe 6: Warm-intro request to the mutual

```
Subject: Quick favor — {first_target}

Hi {first_mutual} — saw you're connected with {first_target} ({title} at {company_target}). I'm at {your_co} ({stage} {sector}). We're hiring a {role} and {first_target}'s background in {specific_signal} would be a strong fit. Worth a warm intro? Happy to share the brief first. Best, {recruiter}
```

Sent via Gmail (NOT InMail). If mutual is internal team member: send via Slack DM via `slack-mcp`.

### Recipe 7: Forward-ready exec brief (what the mutual sends)

```
Subject: {first_target} — quick intro

Hi {first_target} — {first_mutual} suggested I reach out. I'm {your_co} ({stage} {sector}, {brief_company_pitch}). We're hiring our first VP Eng to {scope} — I think your work on {specific_signal} at {company_target} maps directly.

Brief outline:
- {1 bullet — what we've built}
- {1 bullet — funding + runway}
- {1 bullet — comp band, with deferral to negotiation}

Worth a 30 min call? Calendar: {link}. Best, {ceo_or_recruiter}
```

The mutual forwards verbatim (or with a 1-line top note). Their social capital transfers.

### Recipe 8: Direct cold InMail (when warm path absent)

```
Subject: After the {company} round

{first} — congrats on the {company} {round} round. As you scale through this next chapter, we're hiring a VP Eng for a {sector} co at the {stage} level. Different scope but similar challenges. Worth 30 min? Best, {recruiter}
```

Acceptance rate cold-to-exec: 3-5% (vs 60-75% warm-intro). Use only when warm path proven absent.

### Recipe 9: Brief packet for ceo-agent handoff

For each viable exec candidate, produce a brief packet:

```markdown
# {Candidate Name} — VP Eng Brief — {Date}

## Profile snapshot
- Current: {role} at {company} ({tenure})
- Past: {1-2 highlights — Stripe S2, Acquia M&A, etc.}
- Domain depth: {1-2 sentences — what specifically maps}
- LinkedIn: {url} | GitHub: {url} | Personal: {url}

## Contact (2-source verified)
- Email: {primary} (source 1: Lusha verified, source 2: RocketReach guessed → reconfirmed via Findymail)
- Phone: {primary} (source 1: Lusha verified)

## Signal of fit (3 bullets)
- {bullet 1}
- {bullet 2}
- {bullet 3}

## Warm-intro path
- Primary: {name} ({type: board_member / investor / alum / school_cohort}, strength {1-10})
- Secondary: {name} ({type}, strength {1-10})

## Movement signal (per Recipe 2)
- Score: {0-100}
- Tenure at level: {N years}
- Recent funding event at current: {yes/no, details}

## Comp context
- Pave / Carta Total Comp band for VP Eng at {stage} {sector}: {range}
- DEFER actual offer structure + equity grant to ceo-agent

## Recommended action
- {Warm intro path X via mutual Y} — drafted ask attached
- OR {Direct InMail if warm absent — drafted attached}
- OR {Skip — score <50 or contact <2-source}
```

Hand packet to `ceo-agent` (parent — exec hiring strategy + comp philosophy + offer structure). This skill stops at the brief.

### Recipe 10: Pave / Carta / Levels.fyi comp band reference (read-only)

```bash
# Pave (paid integration; pricing custom)
# Carta Total Comp (paid)
# Levels.fyi (free read; structured data for some companies)
curl "https://www.levels.fyi/leaderboard/Director-Of-Engineering/?country=254"

# Reference bands in brief packet only. NEVER quote comp in outreach without ceo-agent sign-off.
```

## Examples

### Example 1: Source VP Eng for Series C SaaS startup
**Goal:** Build target list of 30 candidates; verify contact; identify warm paths; brief packet to CEO.
**Steps:**
1. Build 3-layer target list (Recipe 1): 12 from competitors, 10 from acquired startups, 8 from megacap senior. Total 30.
2. Score per Recipe 2 → 18 candidates ≥70.
3. 2-source contact verify per Recipe 3 → 14 candidates pass (4 fail; skip).
4. Warm-intro path per Recipe 5 → 9 have paths; 5 don't.
5. For the 9 with paths: draft warm-intro request (Recipe 6) + forward-ready brief (Recipe 7).
6. For the 5 without paths: hold 1 week to find paths; if still none, draft direct cold InMail (Recipe 8) — accept lower convert.
7. Brief packet per Recipe 9 → 14 packets → handoff to ceo-agent.

**Result:** 14 high-fit, verified-contact, warm-path-identified VP Eng candidates within 5 working days. CEO owns from here.

### Example 2: 2-source disagreement — Lusha vs RocketReach
**Goal:** Verify jane@stripe.com (Lusha) vs jdoe@stripe.com (RocketReach).
**Steps:**
1. Recipe 4: Findymail third-source check.
2. Findymail returns jane.doe@stripe.com — tiebreaker via SMTP-verify + role-pattern (`firstname.lastname`).
3. Final: jane.doe@stripe.com. Lusha was right at signal but used wrong handle format.
4. Verify via brief LinkedIn message ("checking I have the right contact: is jane.doe@stripe.com still active?") — boring but bulletproof.

**Result:** Confirmed email; outreach to verified address only.

### Example 3: No warm path exists for top candidate
**Goal:** Candidate scores 85 but no mutual board/investor/alum/school cohort.
**Steps:**
1. Confirm via Recipe 5 — exhaustive search, no path found.
2. Hold outreach 7 days; rerun Recipe 5 weekly (paths change as team grows).
3. If still no path after 14 days: present to CEO with 2 options:
   - (a) Direct cold InMail (acceptance ~3-5%; brand-acceptable).
   - (b) Defer to executive search firm ($30-50k retainer; +brand cost).
4. CEO decides.

**Result:** Clear escalation path; no rogue cold outreach to high-stakes exec without ceo-agent sign-off.

## Edge cases / gotchas

- **Warm intros for execs are NON-NEGOTIABLE for high-stakes candidates.** Direct cold InMail to a VP Eng at a peer Series C company hurts brand more than it helps. Hold or defer.
- **2-source verification is mandatory.** 1 bounce to a board member's network destroys 6 months of brand. Sender reputation > volume.
- **Lusha + RocketReach + ContactOut all have GDPR controversy in EU.** Personal email outreach to EU execs: defer to `operations-agent` for compliance review.
- **Exec candidates frequently have multiple personas** — corporate LinkedIn (sanitized) vs personal blog vs Twitter / X. Source signals from all three.
- **NEVER negotiate comp in cold outreach.** Mention "comp band $X-Y" only if explicitly authorized by ceo-agent. Otherwise: "compensation competitive at this stage".
- **Founder candidates are open to "VP" titles** if scope matches but RARELY accept titles below VP. Title-deflation is the most-common deal-killer.
- **"In transition" exec candidates** — recently exited, currently advising/board work. Strong signal for full-time return at right co; but verify intent (some are happy advising).
- **Acquired-2-3y-ago founders are at peak openness window.** Earn-out vested; new acquirer culture proven; ready for next.
- **Megacap senior (L7+ Google, E7+ Meta) candidates are golden handcuffs.** Comp at megacap is so high that ANY startup VP role is comp-decline. Frame around: scope + equity upside + speed-to-decision + impact. Comp parity unrealistic.
- **Executive search firms (Heidrick, Spencer Stuart, Egon Zehnder) own the top-10% exec pool.** Don't compete; partner or defer.
- **GitHub commits aren't useful for exec sourcing.** VPs don't commit at scale; founder/CTO candidates may. Validate signal via talks, board roles, M&A history, published thought leadership.
- **Hand off everything substantive to `ceo-agent`.** This skill produces brief + verified contact + warm-intro draft. CEO owns negotiation, equity structure, and final approval.
- **Hand off interview pipeline + scorecards + offer-letter draft** to parent `operations-agent`'s `hiring-pipeline-greenhouse-ashby-lever` skill.
- **Defer comp benchmark sourcing (Pave / Carta)** to `ceo-agent`'s compensation skill — this skill only references published bands.

## Sources

- RocketReach — Lead Intelligence Email + Phone Finder: https://rocketreach.co/
- Lusha API: https://www.lusha.com/api
- ContactOut: https://contactout.com/
- Findymail — Best Email Finder Tools 2026: https://www.findymail.com/blog/best-email-finder-tools/
- Crunchbase Enterprise API (board + investor data): https://www.crunchbase.com/api
- Pave (exec comp benchmark): https://www.pave.com/
- Carta Total Comp: https://carta.com/total-comp/
- Levels.fyi: https://www.levels.fyi
