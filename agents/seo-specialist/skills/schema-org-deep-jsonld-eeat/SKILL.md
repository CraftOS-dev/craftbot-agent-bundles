<!--
Source: https://schema.org/docs/validator.html
Source: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
Source: https://developers.google.com/search/docs/appearance/structured-data
Depth: per-type JSON-LD + nested @graph + validator + Rich Results Test
-->
# Schema.org Deep — JSON-LD Per Type + E-E-A-T

## When to use

Reach for this skill when the user asks for: "schema markup", "JSON-LD", "structured data", "rich snippet", "Article schema", "Product schema", "FAQPage schema", "HowTo schema", "BreadcrumbList", "Organization schema", "validate my schema", "Rich Results Test", "schema for AEO". This is the depth specialist — covers 15+ schema types with required+recommended fields per type, nested `@graph` for multi-type pages, validator.schema.org + Google Rich Results Test pipeline, E-E-A-T-strengthening Author + Organization markup. Beyond marketing-agent's "add basic schema": this is the production-grade implementation.

## Setup

```bash
# Schema.org validator — free public API
curl -X POST https://validator.schema.org/validate \
  -H "Content-Type: application/ld+json" \
  -d '{"@context":"https://schema.org","@type":"Article","headline":"test"}'

# Google Rich Results Test — via Search Console API
# Needs GSC OAuth token (same as Suganthan GSC MCP)
curl -X POST "https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inspectionUrl":"https://example.com/article"}'
```

Auth requirements:
- `GSC_TOKEN` — for Rich Results Test; OAuth scope `webmasters` (same as Suganthan GSC MCP)
- No auth for validator.schema.org (free, public)

## Common recipes

### Recipe 1: Article + Author + Organization + BreadcrumbList nested @graph
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://example.com/article#article",
      "headline": "Marketing Automation Guide 2026",
      "description": "Complete guide to marketing automation in 2026.",
      "datePublished": "2026-06-01T10:00:00Z",
      "dateModified": "2026-06-09T14:30:00Z",
      "author": {"@id": "https://example.com/author/jane-doe#person"},
      "publisher": {"@id": "https://example.com/#organization"},
      "image": "https://example.com/article-hero.jpg",
      "mainEntityOfPage": {"@type":"WebPage","@id":"https://example.com/article"},
      "articleSection": "Marketing",
      "wordCount": 2800,
      "keywords": ["marketing automation","email automation","crm"]
    },
    {
      "@type": "Person",
      "@id": "https://example.com/author/jane-doe#person",
      "name": "Jane Doe",
      "url": "https://example.com/author/jane-doe",
      "image": "https://example.com/jane-doe.jpg",
      "sameAs": [
        "https://twitter.com/janedoe",
        "https://linkedin.com/in/janedoe",
        "https://en.wikipedia.org/wiki/Jane_Doe"
      ],
      "jobTitle": "Marketing Director",
      "worksFor": {"@id": "https://example.com/#organization"},
      "knowsAbout": ["marketing automation","b2b marketing","email marketing"]
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Inc.",
      "url": "https://example.com",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example.com/logo.png",
        "width": 600,
        "height": 60
      },
      "sameAs": [
        "https://twitter.com/example",
        "https://linkedin.com/company/example",
        "https://en.wikipedia.org/wiki/Example_Inc"
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Home","item":"https://example.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://example.com/blog"},
        {"@type":"ListItem","position":3,"name":"Marketing Automation Guide"}
      ]
    }
  ]
}
```
Nested `@graph` keeps related entities in one block; `@id` linking enables traversal.

### Recipe 2: Product + Offer + AggregateRating + Review
```json
{
  "@context":"https://schema.org",
  "@type":"Product",
  "@id":"https://example.com/products/widget#product",
  "name":"Widget Pro 3000",
  "image":["https://example.com/widget-1.jpg","https://example.com/widget-2.jpg"],
  "description":"Industrial-grade widget with 5-year warranty.",
  "sku":"WID-3000",
  "gtin13":"0123456789012",
  "brand":{"@type":"Brand","name":"WidgetCorp"},
  "manufacturer":{"@type":"Organization","name":"WidgetCorp"},
  "offers":{
    "@type":"Offer",
    "url":"https://example.com/products/widget",
    "priceCurrency":"USD",
    "price":"99.00",
    "priceValidUntil":"2026-12-31",
    "availability":"https://schema.org/InStock",
    "itemCondition":"https://schema.org/NewCondition",
    "shippingDetails":{
      "@type":"OfferShippingDetails",
      "shippingRate":{"@type":"MonetaryAmount","value":"5.99","currency":"USD"},
      "shippingDestination":{"@type":"DefinedRegion","addressCountry":"US"}
    },
    "hasMerchantReturnPolicy":{
      "@type":"MerchantReturnPolicy",
      "applicableCountry":"US",
      "returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays":30,
      "returnMethod":"https://schema.org/ReturnByMail",
      "returnFees":"https://schema.org/FreeReturn"
    }
  },
  "aggregateRating":{
    "@type":"AggregateRating",
    "ratingValue":"4.5",
    "reviewCount":"123",
    "bestRating":"5",
    "worstRating":"1"
  },
  "review":[
    {
      "@type":"Review",
      "author":{"@type":"Person","name":"John Smith"},
      "datePublished":"2026-05-01",
      "reviewBody":"Excellent product.",
      "reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"}
    }
  ]
}
```
2026 update: `shippingDetails` + `hasMerchantReturnPolicy` now required for Merchant Listings rich results.

### Recipe 3: FAQPage
```json
{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {
      "@type":"Question",
      "name":"What is marketing automation?",
      "acceptedAnswer":{
        "@type":"Answer",
        "text":"Marketing automation is the use of software to automate repetitive marketing tasks like email campaigns, social media posting, and lead nurturing."
      }
    },
    {
      "@type":"Question",
      "name":"How much does marketing automation cost?",
      "acceptedAnswer":{
        "@type":"Answer",
        "text":"Marketing automation tools range from $0 (free tiers) to $5000+/mo for enterprise platforms."
      }
    }
  ]
}
```
NOTE: As of August 2023, Google reduced FAQ rich result eligibility to well-known authoritative sites only. Still useful for AEO citation extraction even if no SERP feature.

### Recipe 4: HowTo
```json
{
  "@context":"https://schema.org",
  "@type":"HowTo",
  "name":"How to Set Up Marketing Automation",
  "description":"Step-by-step guide to setting up marketing automation.",
  "totalTime":"PT2H",
  "tool":[{"@type":"HowToTool","name":"HubSpot account"}],
  "supply":[{"@type":"HowToSupply","name":"Email list"}],
  "step":[
    {
      "@type":"HowToStep",
      "position":1,
      "name":"Sign up for HubSpot",
      "text":"Create a free HubSpot account at hubspot.com/signup",
      "url":"https://example.com/guide#step1",
      "image":"https://example.com/step1.jpg"
    },
    {
      "@type":"HowToStep",
      "position":2,
      "name":"Import your email list",
      "text":"Upload your existing CSV email list via Contacts > Import.",
      "url":"https://example.com/guide#step2"
    }
  ]
}
```

### Recipe 5: LocalBusiness (for [city] + [service] pages)
```json
{
  "@context":"https://schema.org",
  "@type":"LocalBusiness",
  "@id":"https://example.com/plumber/new-york#localbusiness",
  "name":"Acme Plumbing — New York",
  "image":"https://example.com/plumber-ny.jpg",
  "telephone":"+1-212-555-0100",
  "priceRange":"$$",
  "address":{
    "@type":"PostalAddress",
    "streetAddress":"123 Main St",
    "addressLocality":"New York",
    "addressRegion":"NY",
    "postalCode":"10001",
    "addressCountry":"US"
  },
  "geo":{
    "@type":"GeoCoordinates",
    "latitude":40.7128,
    "longitude":-74.0060
  },
  "openingHoursSpecification":[
    {
      "@type":"OpeningHoursSpecification",
      "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens":"08:00",
      "closes":"18:00"
    }
  ],
  "areaServed":{
    "@type":"City",
    "name":"New York"
  },
  "aggregateRating":{
    "@type":"AggregateRating",
    "ratingValue":"4.7",
    "reviewCount":"89"
  }
}
```

### Recipe 6: JobPosting
```json
{
  "@context":"https://schema.org",
  "@type":"JobPosting",
  "title":"Senior SEO Specialist",
  "description":"<p>Full job description with HTML allowed.</p>",
  "datePosted":"2026-06-01",
  "validThrough":"2026-08-01T23:59:59Z",
  "employmentType":"FULL_TIME",
  "hiringOrganization":{
    "@type":"Organization",
    "name":"Example Inc.",
    "sameAs":"https://example.com",
    "logo":"https://example.com/logo.png"
  },
  "jobLocation":{
    "@type":"Place",
    "address":{
      "@type":"PostalAddress",
      "streetAddress":"123 Main St",
      "addressLocality":"New York",
      "addressRegion":"NY",
      "postalCode":"10001",
      "addressCountry":"US"
    }
  },
  "baseSalary":{
    "@type":"MonetaryAmount",
    "currency":"USD",
    "value":{
      "@type":"QuantitativeValue",
      "minValue":80000,
      "maxValue":120000,
      "unitText":"YEAR"
    }
  }
}
```
Note: `Indexing API` allows direct submission for JobPosting.

### Recipe 7: Event
```json
{
  "@context":"https://schema.org",
  "@type":"Event",
  "name":"Marketing Summit 2026",
  "startDate":"2026-09-15T09:00:00-04:00",
  "endDate":"2026-09-17T17:00:00-04:00",
  "eventStatus":"https://schema.org/EventScheduled",
  "eventAttendanceMode":"https://schema.org/MixedEventAttendanceMode",
  "location":[
    {
      "@type":"Place",
      "name":"Javits Center",
      "address":{
        "@type":"PostalAddress",
        "streetAddress":"655 W 34th St",
        "addressLocality":"New York",
        "addressRegion":"NY",
        "postalCode":"10001",
        "addressCountry":"US"
      }
    },
    {
      "@type":"VirtualLocation",
      "url":"https://example.com/livestream"
    }
  ],
  "image":["https://example.com/event-hero.jpg"],
  "description":"Annual marketing summit covering automation, AEO, and content strategy.",
  "offers":{
    "@type":"Offer",
    "url":"https://example.com/tickets",
    "price":"299",
    "priceCurrency":"USD",
    "availability":"https://schema.org/InStock",
    "validFrom":"2026-01-01T00:00:00Z"
  },
  "organizer":{"@type":"Organization","name":"Example Inc.","url":"https://example.com"}
}
```

### Recipe 8: VideoObject
```json
{
  "@context":"https://schema.org",
  "@type":"VideoObject",
  "name":"Marketing Automation Tutorial",
  "description":"Step-by-step tutorial on setting up marketing automation.",
  "thumbnailUrl":["https://example.com/video-thumb.jpg"],
  "uploadDate":"2026-06-01T10:00:00Z",
  "duration":"PT8M30S",
  "contentUrl":"https://example.com/video.mp4",
  "embedUrl":"https://www.youtube.com/embed/abc123",
  "interactionStatistic":{
    "@type":"InteractionCounter",
    "interactionType":{"@type":"WatchAction"},
    "userInteractionCount":15234
  }
}
```

### Recipe 9: Course + SoftwareApplication + Recipe (one-liner contracts)
```json
// Course
{"@context":"https://schema.org","@type":"Course","name":"...","description":"...","provider":{"@type":"Organization","name":"...","sameAs":"..."}}

// SoftwareApplication
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"...","applicationCategory":"BusinessApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.5","ratingCount":"100"}}

// Recipe
{"@context":"https://schema.org","@type":"Recipe","name":"...","image":["..."],"author":{"@type":"Person","name":"..."},"datePublished":"...","prepTime":"PT15M","cookTime":"PT30M","recipeYield":"4 servings","recipeIngredient":["..."],"recipeInstructions":[{"@type":"HowToStep","text":"..."}],"nutrition":{"@type":"NutritionInformation","calories":"250 calories"}}
```

### Recipe 10: Validation pipeline (validator.schema.org + Rich Results Test)
```bash
# Step 1: validator.schema.org syntax + type check
curl -X POST "https://validator.schema.org/validate" \
  -H "Content-Type: application/ld+json" \
  --data-binary @schema.json

# Step 2: Google Rich Results Test (eligibility)
curl -X POST "https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inspectionUrl":"https://example.com/article","languageCode":"en-US"}'

# Step 3: parse response for "detectedItems" + "verdict"
# verdict.verdict = "PASS" / "FAIL" / "PARTIAL"
```

### Recipe 11: Bulk validation across a sitemap
```python
import json, requests

def validate_url(url, gsc_token):
    r = requests.post(
        'https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run',
        headers={'Authorization': f'Bearer {gsc_token}'},
        json={'inspectionUrl': url}
    )
    data = r.json()
    return {
        'url': url,
        'verdict': data.get('richResultsResult',{}).get('verdict',{}).get('verdict'),
        'detected_items': data.get('richResultsResult',{}).get('detectedItems',[]),
        'errors': data.get('richResultsResult',{}).get('issues',[])
    }

# Sample 50 URLs per template
sample_urls = pick_sample_urls_from_sitemap('https://example.com/sitemap.xml', n=50)
results = [validate_url(u, gsc_token) for u in sample_urls]

# Aggregate: % PASS per detected type
import pandas as pd
df = pd.DataFrame(results)
print(df.groupby('verdict').size())
```

## Examples

### Example 1: Implement Article + Person + Organization across a 500-post blog
**Goal:** Every blog post has nested `@graph` JSON-LD passing validator + Rich Results Test.

**Steps:**
1. Define content model fields (author name, author bio URL, author social, org name, org logo).
2. Template Recipe 1 in your CMS / framework — inject JSON-LD `<script>` in `<head>`.
3. Recipe 10: validate sample of 10 posts.
4. Recipe 11: bulk validate full 500 → fix any FAIL/PARTIAL.
5. Ship + monitor in GSC > Enhancements > Articles.

**Result:** 500 posts eligible for Article rich result + AEO citation-friendly entity markup.

### Example 2: Add Merchant Listings schema to PDP for product carousel SERP feature
**Goal:** Get product carousel SERP feature on e-comm category SERPs.

**Steps:**
1. Recipe 2 with all 2026-required fields (shippingDetails, hasMerchantReturnPolicy).
2. Recipe 10 validation per product.
3. Connect Merchant Center to Search Console (Settings > Merchant Center).
4. Monitor in GSC > Enhancements > Merchant Listings → eligibility growth.

**Result:** Product carousel eligibility; ~10-30% CTR uplift on category SERPs.

## Edge cases / gotchas

- **JSON-LD only (Microdata + RDFa deprecated by Google 2024)** — never mix formats; JSON-LD in `<head>` or end of `<body>`.
- **`@id` linking only works within same `@graph`** — for cross-page references use full URL with fragment.
- **`dateModified` resets — Google may de-rank if abused** — only update when content materially changes.
- **`Person.sameAs` Wikipedia/Wikidata link massively boosts author entity recognition** — see `eeat-author-bio-source-authority` skill.
- **FAQPage SERP feature reduced Aug 2023** — only well-known sites get rich result; still useful for AEO.
- **HowTo SERP feature removed mobile Aug 2023** — desktop still shows. Schema still useful for AEO.
- **`AggregateRating` requires real reviews on-page** — Google validates review existence + match. Fake reviews = manual action.
- **Schema for hidden content = penalty** — content behind tabs that load via JS shouldn't have schema. See `role.md` "Antipattern 4".
- **`priceValidUntil` required for Product/Offer** — without it, Merchant Listings disqualified.
- **`Product.gtin*` / `Product.mpn`** — at least one identifier required for Merchant Listings.
- **`Article.image` must be high-res (≥1200px wide)** — for Top Stories eligibility.
- **`BreadcrumbList.item` last element can omit `item`** — current page implied.
- **Validator.schema.org vs Google Rich Results Test divergence** — schema.org validates the SPEC; Google validates ELIGIBILITY for specific rich results. Both must pass.

## Sources

- [Schema.org Validator](https://schema.org/docs/validator.html)
- [Google Search Central — structured data search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [Google Search Central — structured data general](https://developers.google.com/search/docs/appearance/structured-data)
- [Google Rich Results Test API](https://developers.google.com/webmaster-tools/v1/urlTestingTools.richResults)
- [Google — Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Google — Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product)
- [Google — Merchant Listings (shipping + return)](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing)
- [Google — FAQ structured data (limited 2023+)](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Google — HowTo structured data (desktop only)](https://developers.google.com/search/docs/appearance/structured-data/how-to)
- [Google — JobPosting structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- [Google — LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google — Event structured data](https://developers.google.com/search/docs/appearance/structured-data/event)
