<!--
Sources: https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026
         https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates
         https://careery.pro/blog/recruiter-outreach-templates
         https://expandi.io/blog/linkedin-recruiter-message-templates/
2026 rules: <400 chars (22% lift), 16-27 char subject (30.5% lift), view profile first
(78% acceptance lift). LinkedIn Recruiter AI assist drives +69% reply since Apr 2026.
Reply rates by function: HR/TA 12.08%, PM 10.24%, Ops 10.02%, Eng 7-9%, Sales 8-11%.
-->
# Cold InMail + Warm Intro — SKILL

Author <400-char LinkedIn InMail messages and warm-intro requests. The 2026 rules:
- Under 400 chars (22% reply lift)
- 16-27 character subject (30.5% lift)
- View candidate profile before sending (78% acceptance lift)
- Lead with candidate's interests, not the job
- AI assist enabled (+69% lift since April 2026)

Warm intros beat cold; cold-with-profile-view beats cold-without.

## When to use

- User wants to **author an InMail to a specific candidate** they've sourced.
- User wants a **warm-intro request** through a mutual connection.
- User asks "rewrite this InMail" or "why is no one replying to my outreach?".
- User wants **templates per segment** (eng IC, eng manager, exec, design, sales).
- Trigger phrases: "write an InMail", "draft outreach", "warm intro", "ask for intro", "InMail template", "subject line", "rewrite this message".

Do not use for: bulk sequence design (`passive-candidate-outreach-campaigns`); LinkedIn Boolean (`linkedin-recruiter-boolean-search-strings`); enrolling in CRM (`gem-hireez-beamery-talent-crm`).

## Setup

```bash
# This skill is template-only — no API calls; prose authoring + LinkedIn paste workflow.
# Optional: gmail-mcp for sending warm-intro requests via mutual connections.
# Optional: slack-mcp for DM warm-intro requests within internal team.

# LinkedIn Recruiter — seat required for InMail.
# LinkedIn Recruiter native AI assist (since April 2026; +69% lift) — enable in Recruiter Settings → AI tools.
```

## Common recipes

### Recipe 1: The 2026 InMail formula

```
Subject: [16-27 chars; reference candidate's work, NOT the job]
Body: [Under 400 chars]
  - Line 1: Specific reference to their work (8-15 words). NOT "I saw your profile."
  - Line 2: One-sentence company / role pitch (10-20 words).
  - Line 3: Specific ask + frictionless next step (8-15 words).
  - Sign-off: First name only. Short.
```

Total: ~300-380 chars body + ~22 chars subject. Always profile-view first.

### Recipe 2: Engineering (passive — recent OSS commit signal)

```
Subject: Your {oss_project} work

Hi {first} — saw your recent commits to {oss_project}; the {specific_pr_or_feature} change was clever. We're hiring a staff platform eng to lead our {your_domain} infra (similar problem space). Worth 20 min to compare notes? Best, {recruiter}
```

Char count: 312. Subject: 19 chars. View profile first. Send rate: 60-80% to fully-tokenized prospects (gap candidates kicked to manual).

### Recipe 3: Engineering (active — recent job change signal)

```
Subject: Quick thought, {first}

Saw you just joined {current_company} 3 mo back — congrats. Not pulling you out, but wanted to put us on your radar for 12-18 mo from now. We're a {stage} {sector} co building {what_problem}. Worth a coffee whenever? Best, {recruiter}
```

Char count: 287. Subject: 21 chars. Reply rate ~12-15% — lower direct convert but creates long-window pipeline.

### Recipe 4: Product designer (B2B SaaS, design-system depth)

```
Subject: Your {company} design system

Hi {first} — your work on the {company} design system is impressive (esp the {specific_component} doc). We're scaling a similar system at {your_co} and looking for a staff PD to lead it. Worth a 20 min chat? Best, {recruiter}
```

Char count: 292. Subject: 26 chars. Reference a specific component or doc — generic "your design work" reads as fake.

### Recipe 5: CTO / VP Eng (recent funding event signal)

```
Subject: After the {company} round

{first} — congrats on the {company} {round} round. As you scale through this next chapter, we're hiring a VP Eng for a {sector} co at the {stage} level. Different scope but similar challenges (1-on-1 with {mutual_connection} if useful). Worth 30 min? Best, {recruiter}
```

Char count: 358. Subject: 24 chars. **Warm-intro path identified before sending** is non-negotiable for execs. If `{mutual_connection}` is unset, send via warm-intro template (Recipe 8) instead.

### Recipe 6: Sales (RepVue rep, top quota signal)

```
Subject: Your {company} numbers

Hi {first} — RepVue surfaced you as a top-quota AE at {company}. Our $120K ACV B2B SaaS co is hiring; OTE band $230-260K. Worth 20 min for a comp + scope comparison? Best, {recruiter}
```

Char count: 245. Subject: 22 chars. RepVue comp transparency upfront drives 15-20% reply lift on sales.

### Recipe 7: Engineering re-engagement (boomerang / alumni)

```
Subject: Miss you, {first}

{first} — it's been {N} months since you left {company}. The team's grown since then; we just shipped {recent_milestone}. If your current role isn't quite right, we'd love to chat about {role_we_have} — different scope from when you were here. Coffee? Best, {recruiter}
```

Char count: 348. Subject: 17 chars. For alumni 12-18 months post-departure. See `boomerang-alumni-re-engagement` for full cadence.

### Recipe 8: Warm-intro request (via mutual connection)

```
Subject: Quick favor — {first_target}

Hi {first_mutual} — saw you're connected with {first_target} at {company_target}. We're looking to chat with them about a {role} role at our {stage} {sector} co; would you be open to a quick warm intro? Happy to share the pitch first. Best, {recruiter}
```

Sent via: Gmail (preferred — Slack DM if internal/close colleague). NOT LinkedIn InMail to mutual (consumes quota; same channel feels lazy).

### Recipe 9: Warm-intro forward template (what you send the mutual to forward)

```
Subject: {first_target} — quick intro

Hi {first_target} — {first_mutual} suggested I reach out. I'm {recruiter} at {your_co}, a {stage} {sector} co building {what_problem}. We're hiring a {role} and your background in {specific_signal} would be a strong fit. Worth a 20 min call? Calendar: {link}. Best, {recruiter}
```

Char count: 333. The mutual forwards this verbatim (or with a 1-line top note). Mutual's social capital transfers automatically.

### Recipe 10: Subject lines that work (and what to avoid)

```
WORK (16-27 chars):
- "Your {oss_project} work"              # specific to candidate's output
- "{first}, quick thought"                # casual + first name
- "{Company} hiring"                      # signals scale
- "Saw your {talk/post/repo}"             # external signal
- "{Mutual} suggested"                    # warm-intro signal
- "Your {company} numbers"                # for sales
- "After the {company} round"             # event-tied
- "Miss you, {first}"                     # alumni

AVOID:
- "Job opportunity"                       # generic; ignored
- "Hi {first} — exciting role!"           # exclamation + generic
- "Are you open to new roles?"            # transactional; cold
- "Recruiter from {your_co}"              # leads with you, not them
- "We're hiring!"                         # spam-flag risk
```

### Recipe 11: AI-assist workflow (LinkedIn Recruiter native, +69% lift since Apr 2026)

```
LinkedIn Recruiter UI → candidate profile → "AI-assisted InMail" button.
1. Select role + key signal (LinkedIn pulls from profile).
2. AI generates 3 variants; review.
3. Edit token + final pass (don't accept AI verbatim — robotic risk).
4. Send.
```

Edit at least 30% of AI-generated text. Verbatim AI sends read robotic at scale and degrade brand.

### Recipe 12: View-profile-first execution

```
Recruiter UI workflow:
1. Open candidate profile (view registers — they see "X recruiter at YourCo viewed your profile").
2. Wait 2-4 hours (lets the view-notification land).
3. Send InMail.

Result: 78% acceptance lift vs cold-send-no-view.
```

If sending via Gem / hireEZ sequence: enable "view profile before send" automation in sequence settings. Both platforms support it as of mid-2025.

### Recipe 13: Profile-view + 24-hour follow-up combo

```
Day 0: View profile + send InMail.
Day 1 (24h later): If no reply but they viewed YOUR profile back, send light follow-up via LinkedIn message (not InMail):
  "Hi {first} — just checking my note didn't get buried. {one_line_value_add}. Best, {recruiter}"
```

24-hour follow-up after mutual view drives 30-40% additional reply lift on otherwise-quiet step 1.

## Examples

### Example 1: Rewrite a low-performing InMail
**User's draft:**
> Subject: Exciting opportunity at our company!
> Hi Jane — I came across your profile and was impressed by your experience. We have an exciting opportunity at our fast-paced startup. Are you open to new roles? Would love to hop on a call. Best, Sarah

**Diagnosis:**
- Subject too long (32 chars vs 16-27 target) + generic.
- Opener generic ("came across your profile") + no specific signal.
- Pitch generic ("fast-paced startup") + transactional ("hop on a call").
- 245 chars — under limit but wastes the space.

**Rewrite:**
> Subject: Your ray-core PR
> Hi Jane — saw your scheduler-eviction patch to ray-core; clean fix. We're hiring a staff platform eng to lead similar infra at Acme (ML platform at Series B). Worth 20 min to compare notes? Best, Sarah

312 chars, 17-char subject, specific PR reference, comparison ask. Expected reply rate: 12-18% vs original 3-5%.

### Example 2: Author warm-intro request via mutual
**Goal:** Get an intro to Jane Doe via mutual connection Sam Patel.
**Steps:**
1. Confirm mutual: LinkedIn Sales Nav → 2nd-degree → Sam Patel connected to Jane.
2. Author warm-intro request to Sam (Recipe 8); send via Gmail (not LinkedIn — keeps InMail quota for actual candidates).
3. Attach forward-ready intro (Recipe 9) Sam can paste.
4. Sam forwards → Jane replies to Sam → Sam loops you in.
5. Follow up with Jane in same thread within 24h.

**Result:** Warm-intro acceptance rate ~60-75% (vs cold InMail 8-15%).

### Example 3: Exec sourcing — VP Eng candidate without warm path
**Goal:** Need to reach a VP Eng at a Series D company; no mutual connection identified.
**Steps:**
1. Map 2nd-degree on LinkedIn Sales Nav — board members, investors, ex-colleagues.
2. If any path exists, route through warm intro (Recipes 8 + 9).
3. If NO path exists, hold the outreach 1 week to find a path. Cold InMail to execs converts ~3-5% — too low to spend the InMail quota.
4. If hold expires: use Recipe 5 with `{mutual_connection}` token replaced by an indirect signal ("we share an ex-Stripe alum cohort if useful for context").

**Result:** 60-75% warm path success > 3-5% cold path success. Patience compounds.

## Edge cases / gotchas

- **Under 400 chars is non-negotiable.** Each char above 400 drops reply rate ~0.5%. Edit ruthlessly.
- **16-27 char subject is the sweet spot.** <16 too short (cryptic); >27 truncates on mobile (the dominant LinkedIn read-channel).
- **"View profile first" must register the view notification.** Mobile-only viewing sometimes doesn't trigger the notification (LinkedIn iOS bug as of 2026). Desktop view is reliable.
- **Generic openers tank reply rate.** "I came across your profile" / "I see you work at X" / "I was impressed by your background" — all generic; 2-4% reply. Specific signals (commits, talks, papers, recent role change) → 10-18% reply.
- **AI-generated text verbatim degrades sender reputation.** Edit 30%+ before sending. AI-as-draft, not AI-as-final.
- **InMail quota: Recruiter Lite 30/mo, Recruiter Pro 100/mo, Recruiter Corporate 150/mo.** Plan against. Don't blow on warm-intro requests — those go via Gmail.
- **Subject lines with `!` flag promotional.** Avoid exclamation in subject (and body). Reads as spam.
- **The candidate's name in the subject doesn't always help.** A/B data: `{first}` in subject lifts reply ~10% when the rest is specific; lifts 0% when the rest is generic. Personalization needs to be substantive, not surface.
- **For warm-intro requests, send via Gmail, not InMail.** InMail to a mutual = waste of InMail quota AND signals lazy ("if you can't compose a real email, why should I help you?").
- **"View profile first" works for InMail acceptance but does NOT improve reply on free LinkedIn messages.** Only execute on Recruiter InMail.
- **Send-time matters.** Tuesday-Thursday 9-11am local time of the candidate is the sweet spot. Friday late or Monday early drop reply rate ~15-20%.
- **Reply-rate baselines by function (2026):** HR/TA 12.08%, PM 10.24%, Ops 10.02%, Eng 7-9%, Sales 8-11%, Marketing 9-12%. Calibrate expectations.
- **Defer to `passive-candidate-outreach-campaigns`** for sequence design — this skill authors individual messages, not multi-touch flows.
- **Defer to `cto-vp-eng-exec-sourcing`** for executive-specific framing — execs need 2-source contact verification + comp band reference in brief.
- **Disclose recruiter role + company.** Don't pretend to be a colleague. LinkedIn ToS + ethics violation.
- **For EU candidates, GDPR legitimate-interest is the basis** — pair with prompt unsub honor on reply. `operations-agent` owns compliance review.

## Sources

- ConnectSafely — LinkedIn InMail Templates Response Rates 2026: https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026
- Salesflow — LinkedIn InMail Best Practices 2026: https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates
- Careery — Recruiter Outreach Templates 2026: https://careery.pro/blog/recruiter-outreach-templates
- Expandi — Best LinkedIn Recruiter Message Templates 2026: https://expandi.io/blog/linkedin-recruiter-message-templates/
- LinkedIn Recruiter AI assist docs: https://www.linkedin.com/business/talent/blog/product-tips/linkedin-recruiter-ai-tools
