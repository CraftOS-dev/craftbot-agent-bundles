<!--
Source: https://vale.sh/
Vale per-platform style packs: role.md "Brand voice per platform"
-->
# Brand Voice Consistency — Per-Platform Vale Style Packs — SKILL

Vale prose linter with `styles/Brand/<Platform>.yml` per channel. LinkedIn = formal-but-human / X = punchy / TikTok = casual / Threads = conversational / IG = warm narrative / Reddit = community-fluent / Bluesky = tech-savvy. Common ban list across all (corporate jargon, AI-slop). 60% of marketing materials fail brand guidelines without enforcement. Gate publish on zero errors.

## When to use this skill

- **Pre-publish QA** on every post variant before Buffer cascade.
- **First-time brand voice rollout** — author per-platform packs.
- **Brand voice audit** of existing content corpus.
- **Vendor / agency content review** — automate the catch.
- **Multi-brand support** — separate `styles/<BrandA>/`, `styles/<BrandB>/`.

**Do NOT use this skill when:**
- Grammar / spelling only — LanguageTool or write-good.
- SEO content scoring — Surfer SEO / Clearscope.
- Translation quality — `deepl-mcp` cross-check.

## Setup

### Install Vale

```bash
uvx vale --version            # via uvx (cross-platform)
brew install vale             # macOS
choco install vale            # Windows
sudo snap install vale        # Linux
```

### Project layout

```
.
├── .vale.ini
└── styles/
    └── Brand/
        ├── LinkedIn.yml      # formal-but-human, no slang, 1-3 emoji max
        ├── X.yml             # punchy, contractions OK, 1-2 emoji
        ├── TikTok.yml        # casual, on-trend slang, 3-5 emoji
        ├── Threads.yml       # conversational, informal, 2-4 emoji
        ├── Instagram.yml     # warm narrative, 2-4 emoji
        ├── Reddit.yml        # community-fluent, sub-specific
        ├── Bluesky.yml       # tech-savvy, decentralized-friendly
        └── Common.yml        # banned across all (corporate, AI-slop)
```

### `.vale.ini`

```ini
StylesPath = styles
MinAlertLevel = warning
Vocab = Brand

[content/post-linkedin.md]
BasedOnStyles = Brand, LinkedInVoice

[content/post-x.md]
BasedOnStyles = Brand, XVoice

[content/post-tiktok.md]
BasedOnStyles = Brand, TikTokVoice

[content/post-threads.md]
BasedOnStyles = Brand, ThreadsVoice

[content/post-instagram.md]
BasedOnStyles = Brand, InstagramVoice

[content/post-reddit.md]
BasedOnStyles = Brand, RedditVoice

[content/post-bluesky.md]
BasedOnStyles = Brand, BlueskyVoice

[content/post-*.md]
BasedOnStyles = Brand
TokenIgnores = (https?://\S+), (#\w+), (@\w+)
BlockIgnores = (?s)^```.*?```
```

## Common recipes

### Recipe 1: Common (banned across all) — `styles/Brand/Common.yml`

```yaml
extends: existence
message: "Banned phrase across all platforms: '%s'. Cut or rewrite."
level: error
ignorecase: true
tokens:
  - "leverage"
  - "utilize"
  - "synergize"
  - "ideate"
  - "circle back"
  - "ping me"
  - "in today's fast-paced world"
  - "in a world where"
  - "look no further"
  - "without a doubt"
  - "it's no secret that"
  - "best-in-class"
  - "game-changing"
  - "great question"
  - "certainly"
  - "absolutely"
```

### Recipe 2: LinkedIn pack — `styles/Brand/LinkedIn.yml`

```yaml
---
# LinkedIn voice: formal-but-human, 1300-1900 chars, hook in first 210
extends: existence
message: "LinkedIn voice violation: '%s'"
level: error
ignorecase: true
tokens:
  - "I'm humbled to announce"
  - "Excited to announce"
  - "Beyond grateful to share"
---
# Companion rules (separate files for occurrence-based):
# styles/Brand/LinkedInEmoji.yml
extends: occurrence
message: "LinkedIn: max 3 emoji per post"
level: warning
max: 3
scope: file
tokens:
  - "[\U0001F300-\U0001FAFF]"
```

### Recipe 3: X (Twitter) pack — `styles/Brand/X.yml`

```yaml
# Punchy, ≤ 280 chars, hook in first 7 words
extends: occurrence
message: "X: too many hashtags (max 2)"
level: warning
max: 2
tokens:
  - "#\\w+"
---
# Companion: styles/Brand/XLength.yml
extends: occurrence
message: "X: post over 280 chars"
level: error
max: 280
scope: file
tokens:
  - "."
```

### Recipe 4: TikTok pack — `styles/Brand/TikTok.yml`

```yaml
# Casual, 100-150 char caption, 3-5 hashtags, no #fyp
extends: existence
message: "TikTok: do NOT use #fyp — algorithm ignores"
level: error
ignorecase: true
tokens:
  - "#fyp"
  - "#foryoupage"
  - "#foryou"
---
# styles/Brand/TikTokHashtagCount.yml
extends: occurrence
message: "TikTok: hashtags must be 3-5 (found %s)"
level: warning
min: 3
max: 5
tokens:
  - "#\\w+"
```

### Recipe 5: Threads pack — `styles/Brand/Threads.yml`

```yaml
# Conversational, 500 chars max
extends: occurrence
message: "Threads: post over 500 chars"
level: error
max: 500
scope: file
tokens:
  - "."
```

### Recipe 6: Instagram pack — `styles/Brand/Instagram.yml`

```yaml
# Warm narrative, 138-150 chars first chunk, 20-30 hashtags
extends: occurrence
message: "IG: hashtags must be 20-30 (found %s)"
level: warning
min: 20
max: 30
tokens:
  - "#\\w+"
```

### Recipe 7: Reddit pack — `styles/Brand/Reddit.yml`

```yaml
# Community-fluent, no hashtags, title 300 chars
extends: existence
message: "Reddit: no hashtags in post body"
level: error
tokens:
  - "#\\w+"
```

### Recipe 8: Bluesky pack — `styles/Brand/Bluesky.yml`

```yaml
# Tech-savvy, 300 char max
extends: occurrence
message: "Bluesky: post over 300 chars"
level: error
max: 300
scope: file
tokens:
  - "."
```

### Recipe 9: Run Vale per platform variant

```bash
# In platform-native-content-creation flow:
for platform in linkedin x tiktok threads instagram reddit bluesky; do
  echo "${variants[$platform]}" > /tmp/post-$platform.md
  uvx vale --config=.vale.ini \
    --output=JSON \
    --filter='.Level=="error"' \
    /tmp/post-$platform.md > /tmp/vale-$platform.json
done

# Aggregate errors
total_errors=0
for f in /tmp/vale-*.json; do
  errs=$(jq 'map(length) | add // 0' "$f")
  total_errors=$((total_errors + errs))
done
[ "$total_errors" -eq 0 ] || { echo "Vale errors: $total_errors — block publish"; exit 1; }
```

### Recipe 10: Auto-fix safe substitutions

```bash
uvx vale --fix content/post-linkedin.md
```

Substitution rules with explicit single-target swaps auto-fix; rules with `(use judgment)` placeholders don't.

### Recipe 11: Brand vocabulary whitelist — `styles/Brand/vocab.txt`

```
PowerBrand
PowerBrandX
TeamPower
PowerAPI
PowerCLI
SaaS
B2B
B2C
SMB
DTC
ICP
NPS
MRR
ARR
```

Words in `vocab.txt` skip spell-check + capitalization rules.

### Recipe 12: CI integration

```yaml
# .github/workflows/vale.yml
on: pull_request
jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          version: 3.6.0
          files: content/
          fail_on_error: true
          reporter: github-pr-review
```

## Examples

### Example A: One brief → 7 platform variants → all pass Vale

```yaml
brief: "Launching V3 with AI-powered lead scoring"

variants:
  linkedin: |
    A V3 launch from us at PowerBrand. AI lead scoring went from preview to GA today.
    (3 paragraph proof points + CTA)
    Hashtags: #salestech #leadgen #b2bsaas
  x: |
    V3 of PowerBrand is live. AI lead scoring shipping today.
    What 3 features matter most? Reply with your stack.
  tiktok: "POV: you're a sales leader and AI just started scoring your leads"
  threads: |
    V3 went out today. The one feature we kept iterating on for 6 months:
    AI lead scoring. Here's what it does differently...
  instagram: "AI lead scoring — finally GA. Tap to see how. 25-tag basket below."
  reddit: "[Discussion] We just shipped AI lead scoring. Stack walk + honest tradeoffs."
  bluesky: "PowerBrand V3 ships. AI lead scoring is the headline feature. Notes: <link>"

vale_run: all pass — ship via Buffer cascade
```

### Example B: First-time rollout

```bash
# Initial pass: lots of violations expected
uvx vale --output=JSON content/ > initial_audit.json
jq '{total: length, errors: map(select(.[].Level=="error")) | length, warnings: map(select(.[].Level=="warning")) | length}' initial_audit.json

# Auto-fix safe
uvx vale --fix content/

# Manual review remainder, 2-3 week cleanup window
# Grandfather legacy content
echo 'content/legacy/**' > .valeignore
echo 'content/imported/**' >> .valeignore
```

### Example C: Multi-brand setup

```ini
# .vale.ini
StylesPath = styles

[content/brandA/post-linkedin.md]
BasedOnStyles = Brand, BrandA, LinkedInVoice

[content/brandB/post-linkedin.md]
BasedOnStyles = Brand, BrandB, LinkedInVoice
```

`styles/BrandA/vocab.txt` and `styles/BrandB/vocab.txt` differ per brand.

## Edge cases

### Code blocks + URLs in social posts
`BlockIgnores` skips fenced code; `TokenIgnores` skips URLs / hashtags / mentions. Tune per platform — TikTok variants almost never have code blocks; LinkedIn carousels may include snippets.

### Severity calibration
- `error` — non-negotiable (AI-slop, banned-words, hashtag count violations)
- `warning` — preference (emoji density, hedging overload)
- `suggestion` — info (length recommendations)

Block CI on `error` only.

### False positives on brand-relevant slang
TikTok variants use "lowkey" / "no cap" / etc. — whitelist in TikTok-pack `vocab` or scope the Common.yml rules to skip TikTok files.

### Multi-language
Vale strongest in English. For Spanish / Portuguese / Italian content, use `[lang:es]` scope override OR per-language style files.

### Vocabulary drift
Brand adds new product names / terms quarterly. Update `vocab.txt` proactively; don't wait for false positives.

### Performance
Vale processes ~1000 files/sec. Per-post variant lint ~5ms. No CI delay.

### Author voice vs brand voice
Guest authors (executives, founders) may have signature phrases. Allow per-file override via `[scope:exclude]` directive in `.vale.ini`.

### Emoji rule false positives
Single emoji counter regex `[\U0001F300-\U0001FAFF]` may miss newer Unicode blocks. Test with `uvx vale --no-exit /tmp/test.md` on emoji-heavy text and adjust ranges.

### Hashtag count rules
`occurrence` rule counts within scope `file` by default. For "20-30 IG hashtags in caption" specifically — `scope: file` works for single-post-per-file convention.

### Rule debugging
```bash
uvx vale ls-config            # show effective config
uvx vale --no-exit content/   # don't exit on errors
```

### Update existing styles
```bash
uvx vale sync                 # update from packages in .vale.ini
```

### Substitution-rule "use judgment" cases
Use parenthetical placeholders for cases where automatic swap is unsafe:

```yaml
swap:
  "best-in-class": "(cut or be specific about what's best)"
  "robust": "(strong, reliable, or describe specifics)"
```

### Cross-platform paste-trap
Author writes for LinkedIn, copies to X. Common.yml catches the corporate-slop pattern; per-platform Vale runs catch the LinkedIn-emoji / hashtag mismatch on X.

### Approval gate UX
If Vale errors block publish at 2pm window, approval cycle restarts. Use Vale as morning-of catch (post-draft, pre-Buffer) to allow time for revision.

### AI-generated content drift
AI-drafted variants ship 3-5x the AI-slop count vs human-drafted. Strict Common.yml gate is the AI-slop filter. Don't relax.

## Sources

- **Vale prose linter**: https://vale.sh/
- **Vale docs / styles**: https://vale.sh/docs/topics/styles/
- **Vale GitHub Action**: https://github.com/errata-ai/vale-action
- **Vale styles registry**: https://vale.sh/explorer/
- **60% brand-guideline failure (Envive 2026)**: https://www.atomwriter.com/blog/brand-voice-consistency-social-media-linkedin-twitter-tiktok/
- **Role.md "Brand voice per platform"**: per-platform Vale style packs
