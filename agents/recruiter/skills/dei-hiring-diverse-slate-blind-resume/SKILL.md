<!--
Sources: https://www.greenhouse.io/inclusion
         https://datapeople.io/
         https://www.appliedhq.co/
         https://gapjumpers.me/
         https://textio.com/
2026 compliance overlay: NYC LL144 (bias audit + disclosure), IL AI Video Interview Act (consent),
CO SB 24-205 (impact assessments eff Feb 2026). 4/5 rule per EEOC UGESP.
Audit checklist canonical in role.md "DEI compliance audit checklist".
-->
# DEI Hiring — Diverse Slate / Blind Resume — SKILL

Operate the recruiter's DEI hiring stack: diverse-slate (Rooney Rule) enforcement, panel-diversity rule, blind-resume screening (Greenhouse Inclusion / Ashby Anonymous / Applied / GapJumpers), JD bias scrub (Textio / Datapeople / manual checklist), voluntary demographic survey, adverse-impact 4/5 rule monitoring, and quarterly DEI compliance audit. Adverse-impact interpretation defers to `legal-counsel`.

## When to use

- Per-req: enforce diverse-slate target at finalist stage; enforce panel diversity rule.
- Per-JD: scrub for bias before posting.
- Pre-loop: turn on blind screening for initial review.
- Quarterly: run `role.md` "DEI compliance audit checklist".
- Compliance: AI-screening jurisdictional check (NYC / IL / CO).
- Trigger phrases: "diverse slate", "Rooney Rule", "panel diversity", "blind resume", "JD bias", "Textio", "Applied", "GapJumpers", "demographic survey", "4/5 rule", "adverse impact", "DEI funnel".
- Defer to `legal-counsel`: adverse-impact statistical significance, EEO-1 reporting, jurisdictional AI-screening compliance, demographic-data retention.

## Setup

```bash
# ATS with native inclusion
export GREENHOUSE_API_KEY="harvest_xxx"  # Inclusion Kit ships with all plans
export ASHBY_API_KEY="xxx"               # Anonymous Screening built-in
export LEVER_API_KEY="xxx"

# JD scrub
export TEXTIO_API_KEY="xxx"
export DATAPEOPLE_API_KEY="xxx"

# Blind hiring (free fallbacks)
export APPLIED_API_KEY="xxx"             # https://www.appliedhq.co/
# GapJumpers: UI-only as of 2026
```

Auth model: all basic-auth-key pattern. Greenhouse Inclusion features are gated by plan tier; verify with `/v1/users/me`.

## Common recipes

### Recipe 1: Turn on blind screening in Greenhouse Inclusion
```bash
# Set job-level Inclusion feature flag (UI in 2025 → API in 2026):
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/jobs/<job_id>" \
  -d '{"custom_fields": {"inclusion_blind_screening": "enabled"}}'
```
Effect: at initial-screen stage, name + photo + school + dates masked in candidate cards.

### Recipe 2: Enable Anonymous Screening (Ashby)
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/job.update" \
  -d '{"jobId": "<id>", "anonymousScreening": {"enabled": true, "fieldsToHide": ["name", "school", "personalInfo"]}}'
```

### Recipe 3: Run JD through Textio bias scrub
```bash
curl -s -X POST -H "Authorization: Bearer $TEXTIO_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.textio.com/v3/flow/document/score" \
  -d '{
    "documentType": "jobDescription",
    "content": "Looking for a rockstar ninja engineer who can crush deadlines and grind 60-hr weeks...",
    "audience": "engineers"
  }'
# Returns: Tone score, gender-tone score, jargon/buzzword flags, age-coded language, must-have count.
```

### Recipe 4: Textio scrub with rewrite suggestions
```bash
curl -s -X POST -H "Authorization: Bearer $TEXTIO_API_KEY" \
  -d '{"content": "<JD>", "suggestions": "full"}' \
  "https://api.textio.com/v3/flow/document/suggest"
# Apply suggested replacements (e.g., "rockstar" → "highly-skilled"; "ninja" → "expert").
```

### Recipe 5: Manual JD bias checklist (free fallback)
```text
[ ] Gendered words scrub — "manpower" "guru" "ninja" "rockstar" "dominant"
[ ] Age-coded language — "digital native" "recent grad" "fresh out of college"
[ ] Demand-coded — "relentless" "crush" "grind" "60-hr weeks" "fast-paced" (mild OK; excess flags)
[ ] Must-have count ≤8 — every must-have above 8 cuts female + URM applicant rate ~3%
[ ] Comp band stated where legally required (CA SB 1162, NY pay transparency, CO Equal Pay)
[ ] Remote / hybrid stated clearly
[ ] No degree gate unless legally required ("bachelor's preferred" not "required")
[ ] EEO statement at bottom (boilerplate template)
[ ] No pronouns in role title ("he or she will own X" → "the person in this role will own X")
```

### Recipe 6: Diverse-slate compliance per req (Greenhouse, aggregated)
```python
import requests, os
# Pull demographic-tagged applications per req (aggregated, never per-candidate)
data = requests.get(
  f"https://harvest.greenhouse.io/v1/jobs/<job_id>/eeoc?stage=onsite",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
# Compute % URM at onsite stage; target 30-50% per role family
total = sum(d["count"] for d in data)
urm = sum(d["count"] for d in data if d["race_ethnicity"] in {"black","hispanic_latino","native_american","two_or_more"})
print(f"% URM at onsite: {urm/max(1,total):.1%}  (target 30-50%)")
```

### Recipe 7: Panel diversity rule check
```python
# For each scheduled interview panel, verify ≥1 underrepresented interviewer staffed.
# Interviewer demographic data is sensitive — store in HRIS not ATS; pull from HRIS:
# panel_demographics = hris.get_panel_composition(application_id)
# rule: any(p['urm'] for p in panel_demographics) → comply
# Otherwise: document why unstaffable (small team) + flag for HM mitigation
```

### Recipe 8: Adverse impact 4/5 rule per role family
```python
import pandas as pd
# Selection rate = % advanced from stage A → stage B
df = pd.read_csv("funnel_by_eeo.csv")
# columns: role_family, eeo_category, applied, advanced
df["sel_rate"] = df["advanced"] / df["applied"]
for rf in df["role_family"].unique():
  sub = df[df["role_family"] == rf]
  maj = sub[sub["eeo_category"] == "white_male"]["sel_rate"].iloc[0]
  for _, row in sub.iterrows():
    ratio = row["sel_rate"] / max(0.001, maj)
    if ratio < 0.80:
      print(f"4/5 violation: {rf} / {row['eeo_category']}: {ratio:.2f} (selection rate {row['sel_rate']:.1%} vs majority {maj:.1%})")
      # Hand off to legal-counsel for statistical significance test
```

### Recipe 9: GapJumpers-style work-sample task (free path)
```bash
# GapJumpers blind work-sample model: candidate solves task → reviewer scores → identity revealed.
# Free reproduction: Greenhouse take-home → blind reviewer assignment via "anonymous reviewer" feature.
# Use only for IC-junior+ tech roles; not for senior IC+ (live-pair preferred per technical-interview-karat-codesignal-coderpad).
```

### Recipe 10: Applied (free blind-screening platform)
```bash
# Applied platform: question-based screening (not resume-based) with chunk-randomized review.
# Setup: create company account at https://www.appliedhq.co/, add role, define 4-6 question prompts.
# Candidates answer; reviewers see only answers (no name / school / experience).
# Export shortlist to ATS via CSV → import as Greenhouse candidates.
```

### Recipe 11: Quarterly DEI audit (per role.md checklist)
```bash
# Pull each item from role.md "DEI compliance audit checklist (quarterly)":
# - Diverse-slate %, onsite URM %, panel diversity %, JD scrub coverage
# - Voluntary demographic survey opt-in rate
# - Blind-resume screening coverage %
# - 4/5 rule violations (flag to legal-counsel)
# - AI screening bias-audit currency (NYC LL144 annual)
# - Diverse-channel sourcing %
# - HM structured-interview training completion %
# Output → 1-page quarterly DEI pulse → leadership + legal-counsel review.
```

### Recipe 12: AI-screening jurisdictional disclosure (NYC LL144 + IL + CO)
```text
# Required language for candidate disclosure when AI tool ranks/scores:
"This application uses an automated employment decision tool (AEDT) to assist in screening.
A summary of the most recent bias audit is available at: <link>.
You may request an accommodation or alternative selection process by contacting <email>.
[NYC LL144 / IL AI Video Interview Act / CO SB 24-205 disclosure block]"
# Defer exact wording to legal-counsel per jurisdiction; bias audit must be ≤12 months old.
```

## Examples

### Example 1: New req — DEI configuration end-to-end
**Goal:** New Series-B Senior Backend req with DEI controls turned on day 1.
**Steps:**
1. JD scrub: Recipe 3 (Textio) OR Recipe 5 (manual checklist). Re-write until tone score >75 + ≤8 must-haves.
2. Recipe 1: enable Greenhouse Inclusion blind screening.
3. Coordinate with `talent-sourcer` for diverse-channel sourcing (/dev/color, Code2040, Black Founders, Lesbians Who Tech).
4. Pre-loop: confirm panel diversity rule (Recipe 7) staffable — if not, document gap + propose mitigation.
5. Mid-loop: Recipe 6 checks % URM at onsite ≥ target; if below, slow finalist stage until slate complete.

**Result:** Diverse slate met; structured blind-screened initial review; defensible audit trail.

### Example 2: Quarterly DEI audit
**Goal:** Pulse + action plan for leadership.
**Steps:**
1. Recipe 11 pulls every checklist item.
2. Cross-reference with `recruiting-metrics-time-to-fill-offer-accept` source-of-hire by EEO-1.
3. Recipe 8 flags 4/5 violations → hand to `legal-counsel`.
4. Output: 1-page pulse + 3 action items.

**Result:** Leadership sees DEI health; legal reviews flags; actions get owners.

### Example 3: AI screening tool deployment with compliance
**Goal:** Pinpoint AI / Eightfold deploying for top-of-funnel ranking.
**Steps:**
1. Confirm tool has current (≤12 mo) bias audit (NYC LL144). If not — block deployment.
2. Update candidate-disclosure wording (Recipe 12) in apply page + auto-ack email.
3. Document impact assessment per CO SB 24-205 (eff Feb 2026).
4. Human-in-the-loop final decision; never AI-only reject.
5. Annual bias audit refresh.

**Result:** Compliant deployment; reduced bias risk; audit-defensible.

## Edge cases / gotchas

- **"Diverse slate" is not a quota.** Aspirational target; never auto-advance a candidate to hit a number — that creates Title VII exposure. Defer to `legal-counsel` on framing.
- **Panel diversity unstaffability.** Small teams (<10 engineers) may not have URM interviewers; document the gap + interim mitigation (skip-level cross-team interviewer). Don't fake compliance.
- **Demographic survey opt-in rate.** Below 30% → data isn't reliable. Push opt-in via clear language at apply + explainer of how data is used (aggregated only, not for decisions).
- **Greenhouse Inclusion masking limits.** Mask name/photo/school/dates; cannot mask everything (resume narrative may reveal demographic signals like college affinity groups). Reviewer training still required.
- **Blind screening is initial-stage only.** Once interviewing starts, identity is revealed. Blind isn't a panacea; structured interview kit + rubric matters more long-run.
- **Textio is paid + opinionated.** Manual checklist (Recipe 5) is a strong free fallback; cuts ~80% of paid value at $0.
- **JD must-have inflation.** Engineering JDs often hit 12-18 must-haves; ≤8 is the threshold. Cull aggressively; nice-to-haves go to nice-to-have.
- **Differential referral bonuses.** "Extra $1K for URM referral" creates Title VII exposure — opt-in DEI bonus must be structured carefully. **Defer to `legal-counsel`** before launching.
- **4/5 rule false positives.** Small N (<50 selected) generates noise; do statistical significance test before acting. **`legal-counsel` interprets**.
- **AI screening audits stale fast.** NYC LL144 requires audit ≤12 months old. Vendor delays update → pull deployment; don't operate non-compliant.
- **CO SB 24-205 (eff Feb 2026).** Impact assessment required for AEDTs; covers any AI tool affecting consequential decisions. New compliance overhead — coordinate `legal-counsel` for first deployment.
- **Defer to `legal-counsel`** for: adverse-impact statistical significance, 4/5 rule action, jurisdictional AEDT compliance (NYC / IL / CO), differential bonus structure, EEO-1 reporting format, demographic-data retention.

## Sources

- [Greenhouse Inclusion](https://www.greenhouse.io/inclusion)
- [Ashby Anonymous Screening](https://www.ashbyhq.com/learn/articles/anonymous-screening)
- [Textio](https://textio.com/)
- [Datapeople](https://datapeople.io/)
- [Applied (blind hiring)](https://www.appliedhq.co/)
- [GapJumpers](https://gapjumpers.me/)
- [EEOC Uniform Guidelines on Employee Selection Procedures (4/5 rule)](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XIV/part-1607)
- [NYC Local Law 144](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page)
- [Illinois AI Video Interview Act](https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=4015)
- [Colorado SB 24-205](https://leg.colorado.gov/bills/sb24-205)
- [SHRM diverse-slate guidance](https://www.shrm.org/topics-tools/news/talent-acquisition/diverse-slate-hiring)
