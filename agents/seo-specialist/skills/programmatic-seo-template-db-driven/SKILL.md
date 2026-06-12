<!--
Source: https://ahrefs.com/blog/programmatic-seo/
Source: https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration
Source: https://docs.astro.build/en/guides/content-collections/
Source: https://suganthan.com/blog/google-search-console-mcp-server/
Depth: full programmatic SEO playbook (template + DB + uniqueness + indexing rollout)
-->
# Programmatic SEO — Template + DB-Driven Page Generation

## When to use

Reach for this skill when the user asks for: "programmatic SEO", "build 10,000 pages from a database", "city + service template", "year-in-review pages at scale", "directory site SEO", "pSEO playbook", "Next.js ISR for SEO", "Astro SSG content collection". This is the depth specialist for template-driven mass page generation — covers templatable intent identification, data-source-readiness criteria (≥30% per-page uniqueness), Next.js/Astro stack recommendation, batch Indexing API submission. Hand off frontend build to `frontend-engineer` after brief.

## Setup

```bash
# Postgres for data backbone — via postgresql-mcp
psql --version  # confirm client installed

# Next.js scaffold (most common pSEO stack)
npx create-next-app@latest my-pseo-site --typescript --app

# Astro alt for evergreen SSG
npm create astro@latest my-pseo-site -- --template minimal --typescript

# Indexing API via Suganthan GSC MCP
npx suganthan-gsc-mcp@2.2.2 --help
```

Auth requirements:
- `POSTGRES_URL` — for `postgresql-mcp`; recipient owns DB
- `GSC_OAUTH_*` — for Indexing API; see `suganthan-gsc-cannibalization-decay-indexing` skill
- Hosting: Vercel (Next.js ISR) / Netlify (Astro SSG) / Cloudflare Pages

## Common recipes

### Recipe 1: Templatable intent identification
```bash
# Step 1: identify the template via Ahrefs
mcp tool ahrefs.keywords_explorer \
  --keyword "best plumber in" \
  --country "US" \
  --limit 500 \
  --include_metrics '["volume","difficulty","intent"]'

# Look for: hundreds of [city] + service variants with consistent volume (5-500/mo each)
# Aggregate MSV = sum across all variants → must exceed build effort threshold
```

### Recipe 2: Aggregate MSV calculation
```python
import pandas as pd

kws = pd.read_json('kws.json')
# Filter to template-matching kws
template_kws = kws[kws['keyword'].str.match(r'best plumber in \w+')]
aggregate_msv = template_kws['volume'].sum()
print(f"Aggregate MSV: {aggregate_msv:,}/mo across {len(template_kws)} variants")

# Threshold: aggregate MSV ≥ 50K/mo justifies ≥1K page build
# Below 10K/mo aggregate — pSEO probably not worth the build effort
```

### Recipe 3: Data source schema in Postgres
```sql
-- Example: cities table for "[city] + [service]" template
CREATE TABLE cities (
  slug TEXT PRIMARY KEY,             -- 'new-york-ny'
  name TEXT NOT NULL,                -- 'New York'
  state TEXT,                        -- 'NY'
  population INT,
  median_income INT,
  neighborhoods JSONB,               -- ['Manhattan','Brooklyn',...]
  zip_codes TEXT[],
  latitude DECIMAL(10,7),
  longitude DECIMAL(10,7),
  nearest_landmarks JSONB            -- [{name,distance_mi},...]
);

CREATE TABLE services (
  slug TEXT PRIMARY KEY,             -- 'plumber'
  name TEXT,                         -- 'Plumber'
  avg_hourly_rate INT,
  faq JSONB                          -- [{q,a},...]
);

CREATE TABLE city_service_reviews (
  city_slug TEXT REFERENCES cities,
  service_slug TEXT REFERENCES services,
  reviews JSONB,                     -- [{author,rating,text},...] - REAL data per page
  count INT,
  avg_rating DECIMAL(3,2),
  PRIMARY KEY (city_slug, service_slug)
);
```

### Recipe 4: Uniqueness verification (shingling n-gram overlap)
```python
# Verify ≥30% unique content per page (sub-30% = thin content penalty risk)
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def shingle_overlap(text1, text2, n=5):
    vec = CountVectorizer(ngram_range=(n,n), analyzer='word', lowercase=True)
    X = vec.fit_transform([text1, text2])
    shared = (X[0].toarray() * X[1].toarray() > 0).sum()
    total = (X[0].toarray() + X[1].toarray() > 0).sum()
    return shared / total if total > 0 else 0

# Cross-pair sample of generated pages
import itertools
pages = ['<rendered page 1 html>', '<rendered page 2 html>', '<rendered page 3 html>']
for p1, p2 in itertools.combinations(pages, 2):
    overlap = shingle_overlap(p1, p2)
    assert overlap < 0.7, f"Overlap {overlap:.2f} too high — sub-30% unique"
```

### Recipe 5: Next.js ISR template page
```typescript
// app/[city]/[service]/page.tsx (Next.js 15 App Router)
import { notFound } from 'next/navigation';
import { db } from '@/lib/db';

export const revalidate = 86400; // 24h ISR

export async function generateStaticParams() {
  const params = await db.query(`
    SELECT c.slug as city, s.slug as service
    FROM cities c CROSS JOIN services s
    WHERE c.population > 50000  -- prioritize larger cities first wave
  `);
  return params.rows;
}

export async function generateMetadata({ params }) {
  const { city, service } = await params;
  const data = await getCityService(city, service);
  return {
    title: `Best ${data.serviceName} in ${data.cityName} | 2026 Reviews`,
    description: `Top-rated ${data.serviceName}s in ${data.cityName}, ${data.state}. ${data.reviewCount} verified reviews · avg ${data.avgRating}/5 stars.`,
    alternates: { canonical: `https://example.com/${city}/${service}` },
    openGraph: { /*...*/ },
  };
}

export default async function Page({ params }) {
  const { city, service } = await params;
  const data = await getCityService(city, service);
  if (!data) notFound();

  return (
    <article>
      <h1>Best {data.serviceName} in {data.cityName}, {data.state}</h1>
      <p>{data.cityName} has {data.population.toLocaleString()} residents,
         median income ${data.medianIncome.toLocaleString()}. Average {data.serviceName} rate:
         ${data.avgHourlyRate}/hr.</p>
      <h2>Top-rated {data.serviceName}s in {data.cityName}</h2>
      <ReviewList reviews={data.reviews} />  {/* REAL reviews — uniqueness driver */}
      <h2>Neighborhoods served</h2>
      <ul>{data.neighborhoods.map(n => <li key={n}>{n}</li>)}</ul>
      <h2>FAQ for {data.serviceName} in {data.cityName}</h2>
      <Faq items={data.faq} />               {/* per-city FAQ */}
      <Schema data={data} />                  {/* JSON-LD */}
    </article>
  );
}
```

### Recipe 6: Astro SSG template page (alt to Next.js)
```typescript
// src/pages/[city]/[service].astro
---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const cities = await getCollection('cities');
  const services = await getCollection('services');
  return cities.flatMap(c =>
    services.map(s => ({
      params: { city: c.slug, service: s.slug },
      props: { city: c.data, service: s.data, reviews: getReviews(c.slug, s.slug) }
    }))
  );
}

const { city, service, reviews } = Astro.props;
---
<html lang="en">
  <head>
    <title>{`Best ${service.name} in ${city.name} | 2026 Reviews`}</title>
    <link rel="canonical" href={`https://example.com/${city.slug}/${service.slug}`} />
  </head>
  <body>
    <h1>Best {service.name} in {city.name}</h1>
    <!-- per-page unique data -->
  </body>
</html>
```

### Recipe 7: Per-page JSON-LD (LocalBusiness + AggregateRating)
```typescript
// JSON-LD per programmatic page
const schema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": `${data.serviceName} in ${data.cityName}`,
  "address": {
    "@type": "PostalAddress",
    "addressLocality": data.cityName,
    "addressRegion": data.state,
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": data.latitude,
    "longitude": data.longitude
  },
  "aggregateRating": data.reviewCount > 0 ? {
    "@type": "AggregateRating",
    "ratingValue": data.avgRating.toFixed(1),
    "reviewCount": data.reviewCount
  } : undefined,
};

// Inject as <script type="application/ld+json">{JSON.stringify(schema)}</script>
```

### Recipe 8: Sitemap generation (chunked, 50K URL cap per file)
```typescript
// app/sitemap.ts (Next.js 15)
import type { MetadataRoute } from 'next';
import { db } from '@/lib/db';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const rows = await db.query(`SELECT c.slug, s.slug FROM cities c CROSS JOIN services s LIMIT 50000`);
  return rows.rows.map(({ city, service }) => ({
    url: `https://example.com/${city}/${service}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));
}

// For >50K URLs: use sitemap index pattern
// app/sitemap-0.xml.ts, sitemap-1.xml.ts, ... + app/sitemap.xml.ts as index
```

### Recipe 9: Batch Indexing API rollout (200/day quota)
```bash
# Generate URL chunks
python3 -c "
import psycopg2
conn = psycopg2.connect('$POSTGRES_URL')
cur = conn.cursor()
cur.execute('SELECT slug FROM city_service_pages WHERE submitted=false ORDER BY priority DESC LIMIT 200')
urls = [f'https://example.com/{row[0]}' for row in cur.fetchall()]
open('/tmp/today-batch.txt','w').write('\n'.join(urls))
"

# Submit via Suganthan GSC MCP
mcp tool suganthan-gsc.submit_batch \
  --urls_file "@/tmp/today-batch.txt" \
  --type "URL_UPDATED"

# Mirror to Bing IndexNow
while read url; do
  curl -X POST "https://www.bing.com/indexnow?url=$url&key=$INDEXNOW_KEY"
done < /tmp/today-batch.txt

# Mark submitted in DB
psql $POSTGRES_URL -c "UPDATE city_service_pages SET submitted=true WHERE slug IN (...)"
```

### Recipe 10: Crawl-budget projection
```python
# How many days for Googlebot to crawl all 250K pages?
total_urls = 250000
googlebot_velocity_per_day = 8000  # check via GSC > Settings > Crawl Stats

days_to_full_crawl = total_urls / googlebot_velocity_per_day
print(f"Passive crawl: {days_to_full_crawl:.0f} days")

# With Indexing API (200/day): 250000 / 200 = 1250 days — way too slow
# Solution: apply for Indexing API quota increase to 5000/day → 50 days
# OR ship in waves: highest-MSV cluster first (top 10K), let crawl handle the long tail
```

## Examples

### Example 1: Build 50K-page city-service directory site
**Goal:** Launch directory site with 1000 cities × 50 services = 50K pages.

**Steps:**
1. Recipe 1+2: Confirm aggregate MSV ≥ 100K/mo across template variants.
2. Recipe 3: Postgres schema with cities + services + real reviews + per-city FAQs.
3. Recipe 4: Verify ≥30% per-page uniqueness via shingling on sample of 100 pages.
4. Recipe 5: Next.js ISR template, 24h revalidate.
5. Hand off to `frontend-engineer` for production build + Vercel deploy.
6. Recipe 8: Sitemap chunked into 5 × 10K files.
7. Recipe 9: 250 URLs/day rollout via Indexing API + IndexNow (~7 months to full submission); request quota increase.

**Result:** 50K pages indexed in 60-120 days; projected ~30K/mo organic clicks at full ramp.

### Example 2: Year-in-review programmatic series
**Goal:** "[year] + best [SaaS category] tools" × 10 years × 100 categories = 1000 pages.

**Steps:**
1. Recipe 1: Confirm volume via Ahrefs.
2. Recipe 3: Tables — years, categories, year_category_facts (annual market data, regulation changes, product launches).
3. Recipe 6: Astro SSG (evergreen) — build at year roll + monthly refresh trigger.
4. Recipe 7: Article schema per page.
5. Recipe 9: 200/day rollout (5 days for full submission).

**Result:** Evergreen library; refreshes annually with new year data.

## Edge cases / gotchas

- **Sub-30% per-page uniqueness = thin content penalty risk** — Google's John Mueller has reaffirmed this in office hours. Recipe 4 enforces.
- **Real data > template-injected metadata** — population numbers alone don't count as uniqueness. Need real reviews, real prices, real images, real local facts.
- **ISR revalidate too short = crawl-budget waste** — sub-24h ISR causes Googlebot to re-fetch unchanged pages; 24h-72h is the sweet spot.
- **ISR revalidate too long = stale content** — for inventory / pricing pages keep ≤24h; for evergreen guides ≥7 days fine.
- **Sitemap 50K URL cap is hard rule** — chunk via sitemap index. Each sitemap also has 50MB raw size cap.
- **Indexing API 200/day per property** — apply for higher at https://support.google.com/webmasters/contact/indexing-api-quota with use-case justification.
- **JS-rendered programmatic pages risk indexing delay** — prefer SSR/SSG over CSR; verify with Search Console URL Inspection (`js-rendering-csr-ssr-ssg-isr-indexing-impact` skill).
- **Cannibalization across template variants** — `[city] + [service]` and `best [service] in [city]` may compete. Pick ONE URL pattern; canonical to it.
- **Doorway page risk** — programmatic pages crossing into "doorway" territory if every page is a thin gateway to one shared landing. Each page must satisfy unique intent.
- **Hosting cost at scale** — 250K Next.js ISR pages on Vercel can exceed $500/mo function invocations. Move to Cloudflare Workers + KV for cheaper edge caching, or Astro SSG for $0 hosting on Cloudflare Pages.
- **`generateStaticParams` build time** — Next.js building 250K pages at build time takes 30-90min. Use ISR with `dynamicParams=true` to defer build.

## Sources

- [Ahrefs programmatic SEO playbook](https://ahrefs.com/blog/programmatic-seo/)
- [Next.js Incremental Static Regeneration](https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration)
- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Google Search Central — doorway pages](https://developers.google.com/search/docs/essentials/spam-policies#doorway-pages)
- [Google Search Central — sitemaps format](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- [Bing IndexNow documentation](https://www.indexnow.org/documentation)
- [Vercel Next.js ISR best practices](https://vercel.com/docs/incremental-static-regeneration)
