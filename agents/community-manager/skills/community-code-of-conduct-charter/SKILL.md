<!--
Sources: https://www.contributor-covenant.org/version/2/1/code_of_conduct/ + https://opensource.guide/code-of-conduct/ + https://meta.discourse.org/c/welcome-feedback/24 + https://discord.com/safety
-->
# Community Charter + Code of Conduct — SKILL

Charter (purpose + audience + rules + tone + dispute process) + Code of Conduct (banned behaviors + escalation + enforcement table). Use Contributor Covenant 2.1 as base for OSS; adapt for SaaS / brand / Web3. Publish to Notion source-of-truth + per-platform copy (Discord pinned, Circle About, Slack canvas, Discourse FAQ).

## When to use

- New community launch — charter is the foundation, before invite goes out.
- Existing community with recurring mod incidents — symptom of missing/unclear CoC.
- Brand voice/tone changes (rebrand, new audience segment).
- M&A: merging two communities with different norms.
- Regulatory / Trust-and-Safety audit requires documented enforcement.
- Volunteer mod expansion — need a written rulebook to delegate.

Trigger phrases: "code of conduct", "community charter", "community rules", "moderation policy", "Contributor Covenant".

## Setup

```bash
# Notion MCP — source of truth
mcp tool notion.create_page --parent_id $COMM_DB \
  --title "Charter + Code of Conduct" \
  --properties '{"Status": "Draft", "Version": "1.0"}'

# Git for versioning rule packs
mcp tool git-commit.commit \
  --files "policies/CODE_OF_CONDUCT.md" \
  --message "CoC v1.0 — initial draft"

# Vale prose linter for tone consistency
vale --config vale.ini policies/
```

Workspace prerequisites:
- Notion DB `Community Policies` with cols `Doc | Version | Status | Owner | Last reviewed`.
- Git repo for policy versioning (especially OSS communities).
- Optional Vale style guide for community voice.

## Common recipes

### Recipe 1: Charter intake (10 questions)

1. **Purpose** — why does this community exist? (one sentence)
2. **Audience** — who is the ideal member? (3 archetypes)
3. **Out-of-scope** — who is this not for? (filters bad fits early)
4. **Vibe** — adjectives (e.g., "rigorous, friendly, opinionated", "calm, beginner-safe")
5. **Self-promotion stance** — never / Fridays-only / approved members / open
6. **Politics + off-topic** — banned / contained channel / allowed
7. **AI-generated content** — banned / labeled / allowed without disclosure
8. **Languages** — English-only / multi-lang channels / auto-translated
9. **Mod team** — who, decision rights, escalation chain
10. **Enforcement appetite** — quick-ban culture vs warning-heavy

### Recipe 2: Generate Charter (template)

```markdown
# $COMMUNITY_NAME — Charter

## Why we exist
$ONE_SENTENCE_PURPOSE.

## Who this is for
- Archetype A: ...
- Archetype B: ...
- Archetype C: ...

## Who this isn't for
- $OUT_OF_SCOPE.

## How we behave
- Be specific over vague — share actual code, screenshots, links.
- Lead with curiosity — assume good intent.
- No-promo zone except on $PROMO_DAY. (See #promo-friday.)
- Disagreement is healthy; contempt is not.

## How decisions happen
- Day-to-day: mod team consensus.
- Policy changes: 7-day RFC in #meta with member input.
- Disputes: escalation chain → mod → lead mod → owner.

## Living document
Charter rev'd quarterly. Member feedback channel: #meta-suggestions.
```

### Recipe 3: Generate Code of Conduct (Contributor Covenant 2.1 base)

```markdown
# Code of Conduct

## Our Pledge
[Contributor Covenant 2.1 pledge — verbatim]

## Our Standards
**Examples of positive behavior:**
- Demonstrating empathy and kindness
- Respecting differing opinions, viewpoints, experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility, apologizing, learning from mistakes

**Examples of unacceptable behavior:**
- Trolling, insulting / derogatory comments
- Public or private harassment
- Publishing private info ("doxing")
- Sexualized language / imagery, sexual attention
- AI-generated content posted without disclosure
- Spam, self-promo outside designated channels
- Sustained off-topic derailment

## Enforcement
Reports: $REPORT_EMAIL or DM to mod role.
Response SLA: acknowledged in 24h; resolved in 7d.

## Enforcement Ladder
| Tier | Behavior | Action |
|---|---|---|
| 1 | Minor (off-topic, light tone) | Private warning |
| 2 | Repeated minor / single rude | 24h mute + warning |
| 3 | Harassment / doxing / hate speech | Permanent ban, no appeal |
| 4 | Spam / scam / bot | Immediate ban + IP/domain flag |

## Attribution
Adapted from Contributor Covenant v2.1.
```

### Recipe 4: Per-platform publish

```bash
# Discord — pinned in #rules + welcome reaction-gate
mcp tool discord-mcp-full.create_message \
  --channel_id $RULES_CH \
  --content "$(cat policies/CODE_OF_CONDUCT.md)" \
  --pin true

# Circle — pin in "About" + create per-space rule
curl -X POST -H "Authorization: Bearer $CIRCLE_TOKEN" \
  https://app.circle.so/api/v1/community/about \
  -d "{\"body\": $(jq -Rs . < policies/CHARTER.md)}"

# Slack — canvas in #welcome
mcp tool slack.canvases_create \
  --channel_id $WELCOME --title "Code of Conduct" \
  --content "$(cat policies/CODE_OF_CONDUCT.md)"

# Discourse — FAQ page
curl -X PUT -H "Api-Key: $DISCOURSE_KEY" -H "Api-Username: $USERNAME" \
  -d "title=Community Guidelines&raw=$(cat policies/CODE_OF_CONDUCT.md)" \
  https://forum.brand.com/admin/site_texts/faq.json
```

### Recipe 5: Discord welcome-screen reaction-gate

```bash
# Member must react ✅ to charter pin before being given Verified role
mcp tool discord-mcp-full.add_reaction \
  --channel_id $RULES_CH --message_id $RULES_PIN --emoji "✅"

# Reaction handler (via Carl-bot reaction-roles)
# emoji ✅ → role 'Verified' → grants access to all other channels
```

### Recipe 6: Slack canvas + acknowledgement

```bash
# Pin canvas + custom field "CoC ack" on profile
mcp tool slack.users_profile_set \
  --user_id $USER_ID \
  --profile '{"fields": {"Xf123": {"value": "CoC acknowledged 2026-06-15"}}}'
```

### Recipe 7: Discourse trust-level alignment

Discourse TL0→TL4 maps cleanly to enforcement ladder:
- TL0 (new): can post but rate-limited; auto-mod queues new-user posts.
- TL1 (basic): full posting after 10min/3 topics read.
- TL2 (member): can edit wiki, send PMs, post in restricted categories.
- TL3 (regular): flagged by community — auto-bestowed.
- TL4 (leader): manually granted; mod-light powers.

Configure: Admin → Settings → "Trust levels" → align with CoC.

### Recipe 8: AI-content disclosure rule

```markdown
**AI-Generated Content Rule (added 2026-01-15)**

Posts wholly or substantially generated by AI must:
1. Disclose at the top: `*Drafted with AI*`
2. Be tagged `#ai-content`
3. Be limited to relevant channels (`#ai-experiments`, `#ai-help`)

Repeated undisclosed AI posts → tier 2 enforcement.
```

### Recipe 9: Vale style check on rule docs

```ini
# vale.ini
StylesPath = styles
MinAlertLevel = suggestion
[*.md]
BasedOnStyles = write-good, alex
write-good.E-Prime = NO
alex.Profanity = YES
```

```bash
vale policies/
# Run pre-commit to keep policies welcoming + accessible.
```

### Recipe 10: Quarterly review cron

```python
# Pull-request reminder every 90 days
from datetime import datetime, timedelta

def needs_review(doc_path):
    last_reviewed = git_last_modified(doc_path)
    return datetime.now() - last_reviewed > timedelta(days=90)

for p in glob('policies/*.md'):
    if needs_review(p):
        notify_slack(f"Policy stale: {p} — needs quarterly review")
```

## Examples

### Example 1: New OSS dev-tool community

**Goal:** Open-source SDK with 50 contributors, going public on GitHub Discussions + Discord.

**Steps:**
1. Charter intake (Recipe 1) — purpose: "ship + support dev-tool", vibe: "rigorous, technical, code-first".
2. CoC = Contributor Covenant 2.1 verbatim + ladder (Recipe 3).
3. Publish to `CODE_OF_CONDUCT.md` in repo + Discord pin + Discourse FAQ (Recipe 4).
4. Discord reaction-gate `✅` for Verified role (Recipe 5).
5. Quarterly review cron (Recipe 10).

**Result:** Mod team can point to ladder when enforcing; member onboarding hits 30% activation.

### Example 2: B2C creator paid Discord

**Goal:** 1k-member paid Discord around a YouTuber's audience.

**Steps:**
1. Charter intake — vibe: "casual, friendly, no-toxicity"; politics banned; AI labeled.
2. CoC abbreviated to 5 rules + 4-tier ladder.
3. Publish to Discord pin + DM to existing members.
4. Carl-bot reaction-role for Verified (Recipe 5).
5. AI-disclosure rule added (Recipe 8).

**Result:** 3-month mod-incidents down 60% via clearer rules.

## Edge cases / gotchas

- **Don't copy-paste without adapting** — Contributor Covenant is OSS-focused; SaaS/B2C needs adjustments (self-promo channel, sales-bot policy).
- **Enforcement gap > rules gap** — having rules without acting on them undermines the entire CoC.
- **AI content rule is a 2025-2026 must** — without it, low-effort AI content floods.
- **Cultural context** — for international communities, translate CoC + have native-speaker mods review tone.
- **Reaction-gate accessibility** — screen-readers handle reactions poorly; offer typed `!verify` alt.
- **Public vs private enforcement** — bans should be communicated privately; only repeat-offender public callouts are okay.
- **Appeal process gaps** — even Tier 3+ should have an appeal path (e.g., email owner after 30 days).
- **Document mod actions** — keep a private ban log with rationale; protects mods from retaliation accusations.
- **Trust-level abuse on Discourse** — TL3 auto-bestowal can be gamed; manually review monthly.
- **Charter ≠ Code of Conduct** — keep them separate docs; charter is "who we are", CoC is "what's not allowed".

## Sources

- [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)
- [Open Source Guide — CoC](https://opensource.guide/code-of-conduct/)
- [Discourse trust levels](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/)
- [Discord Safety](https://discord.com/safety)
- [Slack canvases API](https://api.slack.com/methods/canvases.create)
- [Vale prose linter](https://vale.sh/)
