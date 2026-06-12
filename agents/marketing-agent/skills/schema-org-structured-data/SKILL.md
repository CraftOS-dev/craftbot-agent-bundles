<!--
Source: https://schema.org/docs/validator.html
Google Rich Results Test: https://search.google.com/test/rich-results
-->
# Schema.org Structured Data — SKILL

JSON-LD generation patterns for Article, Product, FAQ, HowTo, BreadcrumbList, Organization, LocalBusiness, Event, VideoObject. Validated via Schema.org's validator API and Google's Rich Results Test. SOTA for AI search citation eligibility, rich snippets, and on-page SEO compliance.

## When to use this skill

- **Every new blog post / page** — Article + BreadcrumbList minimum.
- **FAQ sections** — FAQPage schema (eligible for FAQ rich snippets).
- **How-to / tutorial content** — HowTo schema (step-by-step rich snippets).
- **Product pages** (e-com / SaaS) — Product schema with price, availability, reviews.
- **Local business / events** — LocalBusiness, Event schemas.
- **AI search citation optimization** (AEO/GEO) — structured data improves retrieval.
- **Validation** before commit / publish.

**Do NOT use this skill when:**
- **Microdata or RDFa** required by legacy systems — only JSON-LD here (Google's preferred format).
- **Validating site-wide** — use `suganthan-gsc-audit` skill `rich_results_status`.

## Setup

### Validation endpoints

```bash
# Schema.org official validator API
curl -X POST https://validator.schema.org/validate \
  -H "Content-Type: application/json" \
  -d @schema.json

# Google Rich Results Test (no public API; use Lighthouse audit for programmatic check)
# Or paste into https://search.google.com/test/rich-results
```

### Tools

- `cli-anything` for curl
- `jsonschema` python lib for local pre-validation (optional)

## Common recipes

### Recipe 1: Article schema (blog post)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Set Up Marketing Automation in 2026",
  "description": "Step-by-step guide to choosing and implementing marketing automation.",
  "image": [
    "https://yourbrand.com/blog/featured.jpg",
    "https://yourbrand.com/blog/featured-1x1.jpg",
    "https://yourbrand.com/blog/featured-16x9.jpg"
  ],
  "datePublished": "2026-06-09T08:00:00+00:00",
  "dateModified": "2026-06-09T08:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://yourbrand.com/team/jane-smith",
    "sameAs": [
      "https://www.linkedin.com/in/janesmith",
      "https://twitter.com/janesmith"
    ],
    "jobTitle": "Head of Marketing",
    "knowsAbout": ["marketing automation","email marketing"]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Your Brand",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yourbrand.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://yourbrand.com/blog/marketing-automation-2026"
  }
}
```

Embed in `<head>`:

```html
<script type="application/ld+json">
{...the JSON above...}
</script>
```

### Recipe 2: BreadcrumbList (always pair with Article/Product)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Home","item":"https://yourbrand.com/"},
    {"@type":"ListItem","position":2,"name":"Blog","item":"https://yourbrand.com/blog"},
    {"@type":"ListItem","position":3,"name":"Marketing Automation 2026","item":"https://yourbrand.com/blog/marketing-automation-2026"}
  ]
}
```

### Recipe 3: FAQPage (for FAQ-rich blog posts)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is marketing automation?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Marketing automation is software that handles repetitive marketing tasks — emails, social posts, ad campaigns — based on user behavior triggers. It frees marketers from manual work and enables personalization at scale."
      }
    },
    {
      "@type": "Question",
      "name": "How is marketing automation different from CRM?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "CRM stores customer data and tracks sales interactions; marketing automation acts on that data to send the right message at the right time. They're complementary, not competing."
      }
    }
  ]
}
```

### Recipe 4: HowTo (tutorial content)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to set up SPF, DKIM, and DMARC for your domain",
  "description": "A 30-minute setup to qualify for Google + Yahoo + Microsoft deliverability requirements.",
  "totalTime": "PT30M",
  "supply": [
    {"@type":"HowToSupply","name":"DNS access at registrar"},
    {"@type":"HowToSupply","name":"ESP DKIM key (from Klaviyo or HubSpot settings)"}
  ],
  "tool": [
    {"@type":"HowToTool","name":"dig command-line tool"}
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Add SPF record",
      "text": "In your DNS, add a TXT record at the apex: v=spf1 include:_spf.google.com include:_spf.klaviyo.com ~all",
      "image": "https://yourbrand.com/screenshots/spf-record.png"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Add DKIM record",
      "text": "Copy DKIM key from your ESP. Add TXT record at klaviyo._domainkey.yourdomain.com with the key value.",
      "image": "https://yourbrand.com/screenshots/dkim-record.png"
    }
  ]
}
```

### Recipe 5: Product (e-com)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Marketing Automation Platform — Pro Plan",
  "image": ["https://yourbrand.com/product/hero.jpg"],
  "description": "Marketing automation for teams of 5-50. Unlimited emails, advanced segmentation, A/B testing.",
  "sku": "MAP-PRO-001",
  "brand": {"@type":"Brand","name":"Your Brand"},
  "offers": {
    "@type": "Offer",
    "url": "https://yourbrand.com/pricing/pro",
    "priceCurrency": "USD",
    "price": "99.00",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "412",
    "bestRating": "5"
  }
}
```

Note: Google requires actual reviews on the page to honor `aggregateRating`. Don't invent.

### Recipe 6: Organization (site-wide)

Add to every page:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Brand",
  "url": "https://yourbrand.com",
  "logo": "https://yourbrand.com/logo.png",
  "sameAs": [
    "https://twitter.com/yourbrand",
    "https://www.linkedin.com/company/yourbrand",
    "https://www.instagram.com/yourbrand"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer support",
    "areaServed": "US",
    "availableLanguage": ["English","French"]
  }
}
```

### Recipe 7: VideoObject (embedded videos in blog)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to set up Klaviyo welcome flow",
  "description": "5-minute tutorial...",
  "thumbnailUrl": "https://yourbrand.com/video/thumb.jpg",
  "uploadDate": "2026-06-09T08:00:00+00:00",
  "duration": "PT5M30S",
  "contentUrl": "https://yourbrand.com/videos/welcome-flow.mp4",
  "embedUrl": "https://www.youtube.com/embed/<id>",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": {"@type":"WatchAction"},
    "userInteractionCount": 4321
  }
}
```

### Recipe 8: Event (webinar / launch)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Marketing Automation Best Practices Webinar",
  "startDate": "2026-07-15T18:00:00+00:00",
  "endDate": "2026-07-15T19:00:00+00:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://yourbrand.com/webinar/q3"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Your Brand",
    "url": "https://yourbrand.com"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://yourbrand.com/webinar/q3/register",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-06-01T00:00:00+00:00"
  }
}
```

### Recipe 9: Validation (Schema.org validator API)

```bash
curl -X POST "https://validator.schema.org/validate" \
  -H "Content-Type: application/json" \
  -d @article-schema.json \
| jq '{valid: .schemaOrgValid, errors: .errors, warnings: .warnings}'
```

Returns valid=true/false + diagnostic messages.

### Recipe 10: Validation (Google Rich Results — programmatic via Lighthouse)

```bash
# Lighthouse SEO audit includes structured-data validation
npx lighthouse https://yourbrand.com/blog/post --output=json --only-categories=seo \
| jq '.audits["structured-data"].details.items'
```

## Examples — full blog post structured data bundle

A blog post should embed 3 schemas:

```html
<head>
  ...
  <!-- Organization (site-wide) -->
  <script type="application/ld+json">
  { "@context":"https://schema.org", "@type":"Organization", ... }
  </script>

  <!-- BreadcrumbList -->
  <script type="application/ld+json">
  { "@context":"https://schema.org", "@type":"BreadcrumbList", ... }
  </script>

  <!-- Article -->
  <script type="application/ld+json">
  { "@context":"https://schema.org", "@type":"Article", ... }
  </script>

  <!-- Conditional: FAQPage if post has FAQ section -->
  <script type="application/ld+json">
  { "@context":"https://schema.org", "@type":"FAQPage", ... }
  </script>
</head>
```

Generate programmatically:

```python
from datetime import datetime
def article_schema(post):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post['title'],
        "description": post['meta_description'],
        "image": [post['featured_image']],
        "datePublished": post['published_at'],
        "dateModified": post['updated_at'],
        "author": {
            "@type": "Person",
            "name": post['author']['name'],
            "url": post['author']['profile_url'],
            "sameAs": post['author']['social_urls'],
        },
        "publisher": ORG_PUBLISHER,
        "mainEntityOfPage": {"@type":"WebPage","@id":post['url']},
    }

def faqpage_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type":"Question",
                "name":q['question'],
                "acceptedAnswer":{"@type":"Answer","text":q['answer']},
            }
            for q in faqs
        ],
    }
```

## Edge cases

### Multiple schemas same page
Combine into `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {"@type":"Article", ...},
    {"@type":"BreadcrumbList", ...},
    {"@type":"FAQPage", ...}
  ]
}
```

Or use multiple `<script>` blocks. Both work.

### Required vs recommended fields
Google's Rich Results docs distinguish:
- **Required**: missing = no rich result (e.g., `Article.headline`)
- **Recommended**: missing = weaker eligibility (e.g., `Article.author.sameAs`)
- **Optional**: nice to have

Always include all required + most recommended.

### Image requirements
For Article rich results:
- Min 1200px wide
- 1:1 / 4:3 / 16:9 aspect ratios all accepted (provide 3 if possible)
- HTTPS only
- Crawlable (not behind login)

### Date formats
ISO 8601 with timezone: `2026-06-09T08:00:00+00:00` or `2026-06-09T08:00:00Z`. Schema validator is lenient; some Google features require explicit timezone.

### Duration formats
ISO 8601 duration: `PT30M` (30 min), `PT1H30M` (90 min), `P1DT3H` (1 day 3 hr).

### URL canonical-ization
`@id` in `mainEntityOfPage` MUST match the canonical URL exactly (including trailing slash, query params, protocol). Mismatches cause Google to ignore the schema.

### FAQ content matching
Google validates that the FAQ schema text matches text actually visible on the page. Hidden FAQ entries that only appear in schema = manual penalty risk.

### HowTo + video pairing
HowTo + embedded VideoObject = video carousel in Search. Embed video AND mark with VideoObject schema.

### Multiple authors
Use array:

```json
"author": [
  {"@type":"Person","name":"Jane","url":"..."},
  {"@type":"Person","name":"John","url":"..."}
]
```

### AI search citation patterns
What makes content AI-citation-friendly:
- Clean Article schema with `author.sameAs` linking to LinkedIn/Twitter (E-E-A-T)
- FAQ schema for direct-quote-friendly chunks
- HowTo schema for step-by-step retrieval
- Clear `dateModified` for freshness signals
- `mainEntity` of FAQPage = the page itself

### Don't use deprecated schemas
- `Recipe.cookingMethod` (deprecated, use `Recipe.recipeCategory`)
- `Article.articleBody` (still works but use directly in HTML body)
- `Place.geo.boxIcon` (deprecated)

Check schema.org for current state.

### `Review` schema in 2026
Google deprecated `LocalBusiness.review` for individual reviews — now only `AggregateRating` accepted. Use review platforms (Trustpilot, G2) for individual reviews; aggregate on-site.

### Multilingual schema
Use `inLanguage`:

```json
"inLanguage": "fr-FR"
```

And/or use `hreflang` HTML tags for the page itself.

## Sources

- **Schema.org docs**: https://schema.org/docs/schemas.html
- **Validator API**: https://schema.org/docs/validator.html
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Google Search Central structured data guide**: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- **JSON-LD format**: https://json-ld.org/
- **AEO/GEO structured data effect**: https://developers.google.com/search/docs/appearance/ai-features
