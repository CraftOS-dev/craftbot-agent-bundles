<!--
Source: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
Source: https://developers.google.com/knowledge-graph
Source: https://developers.google.com/search/docs/appearance/structured-data/article
Depth: E-E-A-T scoring rubric + Knowledge Graph API + Person/Organization schema deep
-->
# E-E-A-T — Author Bio + Source Authority

## When to use

Reach for this skill when the user asks for: "E-E-A-T audit", "author entity check", "Person schema", "verify author with Google Knowledge Graph", "build author authority", "YMYL content quality", "source citation density", "expertise signals", "trustworthiness score". This is the depth specialist — scores every published article against a 10-point E-E-A-T rubric (named author, bio page, Person schema, KG entity, outbound citations, original imagery/data, dateModified, Organization schema, YMYL reviewer credit). Cross-references author entities via Google Knowledge Graph API; builds author entity via Wikipedia + LinkedIn + Crunchbase linkage.

## Setup

```bash
# Google Knowledge Graph API — entity verification
export KG_KEY="<from console.cloud.google.com/apis/credentials>"
# Enable: console.cloud.google.com/apis/library/kgsearch.googleapis.com

# Schema validator (see schema-org-deep-jsonld-eeat skill)
# Free, public

# Screaming Frog custom extraction for author meta
screamingfrogseospider --help
```

Auth requirements:
- `KG_KEY` — free; 100K queries/day quota

## Common recipes

### Recipe 1: E-E-A-T scoring rubric (10-point per article)
```python
def eeat_score(article):
    score = 0
    checks = {}

    # 1. Named author visible above-the-fold
    checks['named_author'] = bool(article.get('author_name'))
    score += int(checks['named_author'])

    # 2. Author bio page exists + linked
    checks['author_bio_page'] = bool(article.get('author_bio_url')) and url_exists(article['author_bio_url'])
    score += int(checks['author_bio_page'])

    # 3. Person schema (JSON-LD)
    checks['person_schema'] = has_person_schema(article['url'])
    score += int(checks['person_schema'])

    # 4. Author has Google Knowledge Graph entity
    checks['kg_entity'] = verify_kg_entity(article['author_name'])
    score += int(checks['kg_entity'])

    # 5. ≥2 authoritative outbound citations
    checks['outbound_citations'] = count_outbound_citations(article['url']) >= 2
    score += int(checks['outbound_citations'])

    # 6. ≥1 original image
    checks['original_image'] = has_original_image(article['url'])  # not stock
    score += int(checks['original_image'])

    # 7. Original data / quotes from named experts
    checks['original_data'] = has_original_data_or_quotes(article['url'])
    score += int(checks['original_data'])

    # 8. Date-last-reviewed visible
    checks['date_visible'] = has_visible_date_modified(article['url'])
    score += int(checks['date_visible'])

    # 9. Organization schema on homepage + Article
    checks['org_schema'] = has_organization_schema(article['url'])
    score += int(checks['org_schema'])

    # 10. YMYL reviewer credit (only required for YMYL content)
    if article.get('is_ymyl'):
        checks['reviewer_credit'] = bool(article.get('reviewer_name')) and bool(article.get('reviewer_credentials'))
        score += int(checks['reviewer_credit'])
    else:
        checks['reviewer_credit'] = 'N/A'
        # If not YMYL, max possible score = 9

    verdict = 'PASS' if score >= 8 else 'BORDERLINE' if score >= 6 else 'FAIL'
    return {'score': score, 'checks': checks, 'verdict': verdict}
```

### Recipe 2: Google Knowledge Graph API — author entity verification
```bash
curl "https://kgsearch.googleapis.com/v1/entities:search?query=Jane+Doe&key=$KG_KEY&limit=5&types=Person"
```

```python
import requests

def verify_kg_entity(name, kg_key=KG_KEY):
    r = requests.get(
        'https://kgsearch.googleapis.com/v1/entities:search',
        params={'query': name, 'key': kg_key, 'limit': 5, 'types': 'Person'}
    )
    items = r.json().get('itemListElement', [])
    if not items: return {'recognized': False, 'score': 0}

    top = items[0]
    return {
        'recognized': top['resultScore'] >= 100,
        'score': top['resultScore'],
        'kg_id': top['result'].get('@id'),
        'description': top['result'].get('description'),
        'detailed_description': top['result'].get('detailedDescription',{}).get('articleBody','')[:200],
    }

# Score thresholds:
# > 100 = strong recognition
# 50-100 = borderline (entity exists but weak)
# < 50 = no entity OR very weak
```

### Recipe 3: SF custom extraction for author meta
```bash
# Extract author + JSON-LD across all articles
cat > /tmp/sf-eeat-extract.txt <<EOF
Author Name|//meta[@name='author']/@content|XPath
Author Schema|//script[@type='application/ld+json']/text()|XPath
Date Modified|//meta[@property='article:modified_time']/@content|XPath
Date Modified Visible|//time[@itemprop='dateModified']/@datetime|XPath
EOF

screamingfrogseospider \
  --crawl https://example.com/blog \
  --headless \
  --use-custom-extraction /tmp/sf-eeat-extract.txt \
  --export-tabs "Internal:All,Custom Extraction:All" \
  --output-folder ./eeat-crawl
```

### Recipe 4: Person schema template (passes E-E-A-T)
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/author/jane-doe#person",
  "name": "Jane Doe",
  "url": "https://example.com/author/jane-doe",
  "image": "https://example.com/jane-doe.jpg",
  "sameAs": [
    "https://twitter.com/janedoe",
    "https://linkedin.com/in/janedoe",
    "https://en.wikipedia.org/wiki/Jane_Doe",
    "https://www.crunchbase.com/person/jane-doe",
    "https://orcid.org/0000-0000-0000-0000"
  ],
  "jobTitle": "Senior SEO Specialist",
  "worksFor": {"@type":"Organization","@id":"https://example.com/#organization"},
  "knowsAbout": ["search engine optimization","content marketing","technical SEO"],
  "alumniOf": {"@type":"EducationalOrganization","name":"Stanford University"},
  "award": ["Search Marketing Awards 2024 Best SEO Specialist"],
  "description": "Jane Doe is a Senior SEO Specialist with 12 years of experience in technical SEO and content strategy."
}
```
`sameAs` is the entity-builder field — every URL listed reinforces the entity identity to Google's KG.

### Recipe 5: Author bio page template (must exist for E-E-A-T)
```html
<!-- https://example.com/author/jane-doe -->
<article itemscope itemtype="https://schema.org/ProfilePage">
  <h1>Jane Doe</h1>
  <p itemprop="description">Senior SEO Specialist at Example Inc. with 12 years of experience in technical SEO, content marketing, and AEO. Featured in Search Engine Journal, Moz Blog, and Ahrefs.</p>

  <section>
    <h2>Background</h2>
    <p>Jane started her SEO career at HubSpot in 2014, leading content strategy for the marketing automation product line. She joined Example Inc. in 2020 as Senior SEO Specialist.</p>
    <p>Jane holds a BS in Computer Science from Stanford University (2014) and is certified in Google Analytics, Ahrefs, and SEMrush.</p>
  </section>

  <section>
    <h2>Featured publications</h2>
    <ul>
      <li><a href="https://www.searchenginejournal.com/...">SEO Migration Checklist — Search Engine Journal</a></li>
      <li><a href="https://moz.com/blog/...">Anchor Text Optimization — Moz Blog</a></li>
    </ul>
  </section>

  <section>
    <h2>Articles by Jane</h2>
    <!-- list of all articles authored on this domain -->
  </section>

  <section>
    <h2>Connect</h2>
    <a href="https://linkedin.com/in/janedoe" rel="me">LinkedIn</a> |
    <a href="https://twitter.com/janedoe" rel="me">Twitter</a> |
    <a href="https://en.wikipedia.org/wiki/Jane_Doe" rel="me">Wikipedia</a>
  </section>

  <!-- Person JSON-LD (Recipe 4) -->
</article>
```

### Recipe 6: Author entity build playbook (when KG score < 100)
```
Score < 100 = entity not recognized OR weak. Build via:

1. Wikipedia stub:
   - Must meet notability threshold (https://en.wikipedia.org/wiki/Wikipedia:Notability)
   - Stub at https://en.wikipedia.org/wiki/Jane_Doe
   - Cite secondary sources

2. LinkedIn:
   - Consistent name + photo + bio across all entries
   - Headline matches Person.jobTitle

3. Crunchbase (if founder/exec):
   - https://crunchbase.com/person/jane-doe
   - Cross-link from Wikipedia + LinkedIn

4. ORCID (if academic):
   - https://orcid.org/0000-XXXX-XXXX-XXXX

5. Google Scholar (if published research):
   - Verified scholar profile

6. Cross-link all in Person schema sameAs (Recipe 4)

7. Wait 60-90 days for Google KG ingestion

8. Re-verify via Recipe 2 → confirm score ≥ 100
```

### Recipe 7: Outbound citation density check
```python
from bs4 import BeautifulSoup

def count_outbound_citations(url, our_domain):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Filter to in-content links (skip footer/nav/sidebar)
    content_area = soup.select_one('main, article, [role=main]') or soup
    links = content_area.find_all('a', href=True)

    outbound = [l for l in links if l['href'].startswith('http') and our_domain not in l['href']]

    # Score by authority
    high_auth_count = 0
    for link in outbound:
        href = link['href']
        if any(href.split('//')[1].startswith(d) for d in ['www.gov','www.edu']) or '.gov/' in href or '.edu/' in href:
            high_auth_count += 1

    return {
        'total_outbound': len(outbound),
        'high_authority_outbound': high_auth_count,
        'passes_eeat': len(outbound) >= 2,
    }
```

### Recipe 8: YMYL content classifier
```python
YMYL_KEYWORDS = [
    # Health
    'medical','health','disease','treatment','symptoms','medication','dosage','therapy',
    # Finance
    'investment','tax','mortgage','loan','retirement','401k','ira','insurance','crypto',
    # Legal
    'legal','attorney','lawsuit','divorce','custody','immigration','contract',
    # Safety
    'safety','danger','emergency','poison','toxic',
    # Current events
    'election','political','government'
]

def is_ymyl(article):
    text = article.get('content','').lower()
    title = article.get('title','').lower()
    return any(kw in text or kw in title for kw in YMYL_KEYWORDS)

# YMYL content requires:
# - Named reviewer with credentials (e.g., "Reviewed by Dr. Jane Doe, MD, board-certified internist")
# - Reviewer schema (separate Person + reviewer field on Article)
# - Higher source citation density (≥3 outbound, .gov / .edu / peer-reviewed preferred)
```

### Recipe 9: Bulk E-E-A-T audit across a blog
```python
import pandas as pd

blog_urls = pd.read_csv('./eeat-crawl/internal_all.csv')
blog_urls = blog_urls[blog_urls['Address'].str.contains('/blog/')]

results = []
for _, row in blog_urls.iterrows():
    article = {
        'url': row['Address'],
        'author_name': row.get('Author Name'),
        'author_bio_url': construct_bio_url(row.get('Author Name')),
        'is_ymyl': is_ymyl({'title': row['Title 1'], 'content': ''}),
    }
    score = eeat_score(article)
    results.append({**article, **score})

df = pd.DataFrame(results)
print(df['verdict'].value_counts())
print(df[df['verdict']=='FAIL'].head(20))
```

### Recipe 10: Organization schema (for E-E-A-T base layer)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example Inc.",
  "alternateName": ["Example", "Example Co"],
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "image": "https://example.com/og-image.jpg",
  "description": "Example Inc. is a SaaS company providing marketing automation tools to B2B teams.",
  "foundingDate": "2014-01-01",
  "founder": {"@type":"Person","name":"Founder Name"},
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103",
    "addressCountry": "US"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-415-555-0100",
    "contactType": "customer service",
    "email": "support@example.com",
    "availableLanguage": ["en","es"]
  },
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example",
    "https://en.wikipedia.org/wiki/Example_Inc",
    "https://www.crunchbase.com/organization/example",
    "https://www.glassdoor.com/Overview/Working-at-Example-EI_IE0000000.htm"
  ],
  "areaServed": "Worldwide",
  "knowsAbout": ["marketing automation","B2B SaaS","CRM"]
}
```

## Examples

### Example 1: E-E-A-T audit across 500 blog articles
**Goal:** Find articles failing E-E-A-T to prioritize remediation.

**Steps:**
1. Recipe 3: SF custom extraction for author + schema + dates.
2. Recipe 9: bulk scoring per article.
3. Identify FAIL + BORDERLINE.
4. Per article: identify which checks failed (Recipe 1 output).
5. Generate remediation plan: add author bios, add Person schema, etc.
6. Hand off to content team / `frontend-engineer` per defect.

**Result:** Prioritized E-E-A-T improvement backlog.

### Example 2: New author launch (no Knowledge Graph entity)
**Goal:** New author hired; build entity for KG recognition.

**Steps:**
1. Recipe 2: confirm score < 50 (no entity).
2. Recipe 5: launch author bio page.
3. Recipe 4: Person schema with placeholders.
4. Recipe 6: build via Wikipedia stub + LinkedIn + Crunchbase.
5. Update Person sameAs to all 5+ profiles.
6. Wait 90 days.
7. Recipe 2 re-check → confirm score ≥ 100.

**Result:** Author recognized as entity; E-E-A-T uplift across all articles by this author.

### Example 3: YMYL content quality audit
**Goal:** Health-content site has potential E-E-A-T issues.

**Steps:**
1. Recipe 8: classify articles as YMYL.
2. Recipe 1 with YMYL flag → reviewer credit check.
3. For YMYL articles missing reviewer: assign medical reviewer; add Reviewer Person to schema.
4. Recipe 7: verify ≥3 authoritative citations per YMYL article.
5. Block publication of new YMYL content failing checks.

**Result:** YMYL section meets Google quality rater guidelines.

## Edge cases / gotchas

- **KG entity score is heuristic** — > 100 strong, but <100 doesn't mean ignored. Borderline (50-100) still helps.
- **Author bio page must be unique URL** — not just an info-box on each article. Standalone page at `/author/<slug>`.
- **`sameAs` not bidirectional automatically** — Wikipedia linking to your site doesn't auto-create the reciprocal; verify external profiles cross-link.
- **Wikipedia notability** — many authors won't meet Wikipedia's notability threshold. Don't fake stubs (they'll be deleted + reputation risk).
- **YMYL boundary fuzzy** — "money/health/safety/legal" the obvious YMYL; "career advice" / "parenting" softer YMYL. Err toward applying YMYL rules when unsure.
- **Reviewer credit pattern** — "Reviewed by [Name], [Credentials]" visible at top + Reviewer Person schema.
- **Stock images don't fail E-E-A-T but original images help** — at minimum, 1 original image (custom screenshot, custom diagram).
- **Original data > regurgitating studies** — survey, internal data, customer quotes. LLMs and Google reward originality.
- **dateModified gaming** — updating dateModified without content changes = quality rater flag. Only update when content changes.
- **Article schema `author` field** — must reference Person `@id`, not plain string.
- **`knowsAbout`** — list 3-7 topics; over-listing (20+) looks gamey.
- **`alumniOf` + `award`** — additional entity-building signals; include when accurate.
- **AI-generated bio = E-E-A-T failure** — author bios must be authentic.

## Sources

- [Google Search Central — creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Knowledge Graph API](https://developers.google.com/knowledge-graph)
- [Google — Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Google — quality rater guidelines](https://developers.google.com/search/blog/2019/10/core-updates)
- [Schema.org Person type](https://schema.org/Person)
- [Schema.org Organization type](https://schema.org/Organization)
- [Wikipedia notability guidelines](https://en.wikipedia.org/wiki/Wikipedia:Notability)
- [Google — quality rater guidelines PDF](https://services.google.com/fh/files/misc/hsw-sqrg.pdf)
- [Search Engine Journal — E-E-A-T guide 2026](https://www.searchenginejournal.com/google-eeat/)
