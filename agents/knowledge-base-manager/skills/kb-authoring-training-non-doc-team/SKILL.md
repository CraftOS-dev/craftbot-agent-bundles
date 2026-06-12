---
name: kb-authoring-training-non-doc-team
description: Train non-writers to contribute KB articles — one-page authoring checklist, opinionated templates per content type, Vale-as-tutor (failing lint = teaching moment), office hours + leaderboard. Use when engineers/CS/PM need to write but produce poor articles.
---

# KB authoring training — for the team that's not the docs team

## When to use

User says "engineers write bad docs", "train our team to write articles", "set up office hours for docs", "give them a checklist", "templates for KB articles", "make Vale teach". Reach AFTER governance is set up (Vale rules exist) and BEFORE expecting major content output.

## Setup

```bash
# Vale (for teach-by-failing-lint)
brew install vale

# Cookiecutter / hygen for templates
pipx install cookiecutter
# or
npm i -g hygen

# Slack workflow for "office hours" (no install; configure in Slack admin)
```

Auth / API key requirements: none for templates; `SLACK_BOT_TOKEN` if automating leaderboard.

## Common recipes

### Recipe 1: One-page authoring checklist (10 rules max)

```markdown
# docs/AUTHORING_CHECKLIST.md

Before you click Merge:

1. **Pick one Diataxis tier.** Tutorial / How-to / Concept / Reference. Don't mix.
2. **Title answers the user's question.** "How do I X?" or "X reference" or "Why X?"
3. **Lede under 50 words.** What this article is for + what you'll learn.
4. **Code fences specify language.** ` ```bash ` not ` ``` `.
5. **Every command is copy-paste runnable.** No `<your-key-here>` ambiguity.
6. **One sentence per line.** Easier review, fewer merge conflicts.
7. **No screenshots of text.** Use real text in a code block.
8. **Frontmatter complete.** title, slug, status=draft, owner, last_verified, tags, diataxis.
9. **Last verified stamped.** `last_verified: 2026-06-09`.
10. **Vale passes.** `vale docs/your-file.md` shows no warnings.
```

### Recipe 2: Per-tier templates (cookiecutter)

```bash
# Template for a How-to article
mkdir -p templates/how-to/{{cookiecutter.slug}}
cat > templates/how-to/cookiecutter.json <<'EOF'
{"slug":"new-task","title":"How to do new task","owner":"you@example.com","tags":["misc"]}
EOF
cat > templates/how-to/{{cookiecutter.slug}}/index.md <<'EOF'
---
title: {{cookiecutter.title}}
slug: how-to/{{cookiecutter.slug}}
status: draft
owner: {{cookiecutter.owner}}
last_verified: {{ "now"|strftime("%Y-%m-%d") }}
diataxis: how-to
tags: [{{cookiecutter.tags|join(", ")}}]
---

# {{cookiecutter.title}}

## Before you start

- You have X set up.
- You have permission Y.

## Steps

1. Do A.

   ```bash
   echo "command"
   ```

2. Do B.

3. Verify by running:

   ```bash
   echo "verify"
   ```

## Troubleshooting

- **Error: ...** — fix is ...

## Related

- Concept: Why X works this way
- Reference: X options
EOF
```

```bash
# Use it
cookiecutter templates/how-to/
```

### Recipe 3: Tutorial template

```markdown
---
title: "Build your first {feature}"
slug: get-started/first-{feature}
status: draft
diataxis: tutorial
---

# Build your first {feature}

By the end, you'll have {concrete result}.

## What you need

- Account
- 10 minutes

## Step 1 — {do thing}

We'll start by ... [Why this step matters in 1 line.]

```bash
cmd
```

Verify: `cmd-to-check` returns `expected`.

## Step 2 — {do thing}

[etc.]

## What you built

You now have {concrete result}. Next: try the [{related how-to}](../how-to/...).
```

### Recipe 4: Reference template

```markdown
---
title: {Resource} reference
slug: reference/{resource}
status: draft
diataxis: reference
---

# {Resource} reference

Complete listing. For task-oriented use, see [How-to / {Resource}](../how-to/...).

## Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | UUID. |
| `name` | string | yes | 1-64 chars. |

## Endpoints

### `GET /v1/{resources}`
...

### `POST /v1/{resources}`
...

## Error codes

| Code | Meaning | Action |
|---|---|---|
| 400 | Invalid body | Fix and retry. |
```

### Recipe 5: Concept template

```markdown
---
title: "How {topic} works"
slug: concept/how-{topic}-works
status: draft
diataxis: explanation
---

# How {topic} works

## The problem this solves

[1-2 paragraphs of the user-facing problem.]

## The mental model

[Diagram via drawio-mcp. 1-paragraph plain-language explanation.]

## Trade-offs

- We chose X over Y because ...

## Where to go next

- How-to: [Do thing with {topic}](../how-to/...)
- Reference: [{Topic} options](../reference/...)
```

### Recipe 6: Vale-as-tutor — friendly error messages

```yaml
# .vale/styles/Brand/HelpfulError.yml
extends: existence
message: |
  This sentence reads as passive. Try active voice:
  "The system processes the request" → "The system processes requests"
  See https://docs.example.com/internal/style-guide#voice
level: suggestion
tokens:
  - '\b(?:is|are|was|were|been|being|be)\s+\w+ed\b'
```

The message itself teaches the rule + links to the style guide.

### Recipe 7: Hygen alternative for engineer workflows

```bash
hygen init self
hygen generator new article
# edit _templates/article/new/{prompt.js, hello.ejs.t}
hygen article new --title "Add SSO Okta"
```

### Recipe 8: Office hours Slack workflow

In Slack: Tools → Workflow Builder → new workflow:
- Trigger: emoji reaction `:writing_hand:` on a message in #engineering
- Action: post in #docs-office-hours pinging @docs-team with the source message link

### Recipe 9: PR template enforcing checklist

```markdown
# .github/PULL_REQUEST_TEMPLATE/docs.md
## Authoring checklist
- [ ] Single Diataxis tier
- [ ] Title answers the user's question
- [ ] Lede under 50 words
- [ ] All commands runnable
- [ ] Frontmatter complete (status, owner, last_verified)
- [ ] Vale passes locally
- [ ] Added to sidebar/nav

Related work:
- closes #
```

### Recipe 10: Monthly contributor leaderboard

```bash
LEADERS=$(git log --since='30 days ago' --pretty='%an' -- docs/ \
  | sort | uniq -c | sort -rn | head -5 \
  | awk '{print NR". "$2" ("$1" commits)"}')

curl -X POST "$SLACK_WEBHOOK_DOCS" \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"📚 Top KB contributors this month:\n$LEADERS\"}"
```

### Recipe 11: Welcome packet for new contributors

```markdown
# docs/_internal/CONTRIBUTOR_WELCOME.md
Welcome! Here's the 30-min onboarding:
1. Read `AUTHORING_CHECKLIST.md` (5 min).
2. Skim `STYLE_GUIDE.md` (10 min).
3. Pick a template — `cookiecutter templates/how-to/` (1 min).
4. Write your first article.
5. Run `vale docs/your-file.md`.
6. Open PR; docs-team reviewer will help.

Office hours: Tuesdays 4pm in #docs-office-hours.
```

## Examples

### Example 1: Onboard 10 engineers as KB contributors

**Goal:** Engineers stop sending docs PRs that miss frontmatter, mix tiers, and break Vale.

**Steps:**
1. Publish 1-page checklist (Recipe 1).
2. Ship cookiecutter templates for 4 tiers (Recipes 2-5).
3. Tune Vale error messages to teach (Recipe 6).
4. PR template (Recipe 9).
5. Office hours workflow (Recipe 8).
6. Monthly leaderboard (Recipe 10).

**Result:** First-PR-pass rate goes from ~30% to ~80%.

### Example 2: Office-hours rotation for SMEs

**Goal:** Engineers can grab 15 min of writer help.

**Steps:**
1. Calendar event "KB Office Hours" Tue/Thu 4pm.
2. Slack channel #docs-office-hours.
3. Workflow: react `:writing_hand:` → auto-thread (Recipe 8).
4. Docs team rotates host.

**Result:** Engineers unblocked within 24h.

## Edge cases / gotchas

- **Templates too rigid** — leave editorial freedom on prose; structure is non-negotiable, voice is not.
- **Vale messages too long** — keep <120 chars; use a single doc URL.
- **Cookiecutter on Windows** — Path separators differ; use forward slashes in templates.
- **Leaderboard gaming** — small PRs > meaningful work. Weight by lines changed only loosely; recognize quality publicly.
- **Office hours empty** — start with 1 hour/week; expand based on demand. Empty hours kill momentum.
- **PR template ignored** — make the docs-folder require it via CODEOWNERS + a Required Check that grep'd the boxes.
- **Don't autofix prose** — Vale `--fix` mangles intent. Auto-fix structure (markdownlint), not voice.
- **Tone in onboarding** — friendly, not bureaucratic. "Welcome!" beats "Compliance requirements."

## Sources

- Diataxis framework: https://diataxis.fr/
- Write the Docs style guides: https://www.writethedocs.org/guide/writing/style-guides/
- Vale custom styles: https://vale.sh/docs/topics/styles/
- Cookiecutter: https://cookiecutter.readthedocs.io/
- hygen: https://www.hygen.io/
- GitHub PR templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- Microsoft Writing Style Guide: https://learn.microsoft.com/en-us/style-guide/welcome/
- Google developer docs style: https://developers.google.com/style
