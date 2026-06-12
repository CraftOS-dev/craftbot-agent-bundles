<!--
Source: https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-generator/
Source: https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#hreflang
Source: https://developers.google.com/search/docs/specialty/international/localized-versions
Depth: hreflang at-scale verification, return-tag reciprocity, language-code correctness
-->
# Hreflang — i18n Implementation + Verification

## When to use

Reach for this skill when the user asks for: "hreflang setup", "international SEO", "i18n SEO", "hreflang return tag missing", "language code wrong", "es-MX or es-mx", "x-default usage", "multi-region SEO", "reciprocity check". This is the depth specialist — covers ISO 639-1 + ISO 3166-1 alpha-2 correctness, reciprocity (every alternate must declare reciprocal), x-default semantics, sitemap-based hreflang at scale, Aleyda Solis tester. Beyond marketing-agent's "add hreflang tags": this is the production-grade verification + monitoring.

## Setup

```bash
# Screaming Frog (primary hreflang exports)
screamingfrogseospider --help

# Aleyda Solis Hreflang Tester — free
curl "https://app.hreflangchecker.com/api/v1/check?url=https://example.com/" \
  -H "Accept: application/json"

# Merkle Hreflang Tags Tool (free alt)
# https://technicalseo.com/tools/hreflang/

# DeepL MCP for content translation (when shipping per-language variants)
export DEEPL_API_KEY="<from www.deepl.com/account>"
```

Auth requirements:
- Screaming Frog license
- Aleyda + Merkle — free public tools
- `DEEPL_API_KEY` — DeepL Pro $5.50+/mo per 1M chars

## Common recipes

### Recipe 1: HTML head hreflang implementation
```html
<!-- On https://example.com/page (English US default) -->
<link rel="alternate" hreflang="en-US" href="https://example.com/page" />
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/page" />
<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page" />
<link rel="alternate" hreflang="es-ES" href="https://example.com/es-es/page" />
<link rel="alternate" hreflang="fr-FR" href="https://example.com/fr/page" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page" />
<link rel="canonical" href="https://example.com/page" />
```
**Rules:**
- Self-referencing: every page references ITSELF in the hreflang set
- Reciprocity: every alternate must declare reciprocal hreflang back to this page
- Self-canonical: each language variant has self-referencing canonical (NEVER canonical to default language)

### Recipe 2: HTTP header hreflang (for PDFs and non-HTML)
```bash
# Apache .htaccess
<FilesMatch "\.pdf$">
  Header set Link "<https://example.com/en/doc.pdf>; rel=\"alternate\"; hreflang=\"en-US\", <https://example.com/es-mx/doc.pdf>; rel=\"alternate\"; hreflang=\"es-MX\""
</FilesMatch>

# Nginx
add_header Link "<https://example.com/en/doc.pdf>; rel=\"alternate\"; hreflang=\"en-US\", <https://example.com/es-mx/doc.pdf>; rel=\"alternate\"; hreflang=\"es-MX\"";
```

### Recipe 3: XML sitemap hreflang (best at scale, 50K URL cap per sitemap)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page"/>
    <xhtml:link rel="alternate" hreflang="en-GB" href="https://example.com/uk/page"/>
    <xhtml:link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page"/>
  </url>
  <url>
    <loc>https://example.com/uk/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page"/>
    <xhtml:link rel="alternate" hreflang="en-GB" href="https://example.com/uk/page"/>
    <xhtml:link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page"/>
  </url>
</urlset>
```

### Recipe 4: SF hreflang exports
```bash
screamingfrogseospider \
  --crawl https://example.com \
  --headless \
  --export-tabs "Hreflang:All,Hreflang:Missing Return Tag,Hreflang:Inconsistent Language Confirmation Links,Hreflang:Incorrect Language and Region,Hreflang:Missing Self Reference,Hreflang:Missing X-Default,Hreflang:Non-Indexable Confirmation Links,Hreflang:Confirmation Links to Non-200 Responses" \
  --output-folder ./hreflang-out
```
The 8 hreflang tabs cover every common implementation defect.

### Recipe 5: Reciprocity verification (Python)
```python
import pandas as pd

# Load SF hreflang export
hreflang = pd.read_csv('./hreflang-out/hreflang_all.csv')
# Columns: Source URL, Target URL, hreflang Value, Type (header/html/sitemap)

# Build directed graph of hreflang declarations
declarations = set()
for _, row in hreflang.iterrows():
    declarations.add((row['Source URL'], row['Target URL'], row['hreflang Value']))

# Reciprocity check
missing_returns = []
for src, tgt, hl in declarations:
    # For every src→tgt with hreflang hl, there must be tgt→src with hl mapping to src's region
    # Get src's hreflang value (the source's own region/lang)
    src_hl_set = [d[2] for d in declarations if d[0] == src and d[1] == src]
    if not src_hl_set: continue
    src_hl = src_hl_set[0]

    reciprocal = (tgt, src, src_hl)
    if reciprocal not in declarations:
        missing_returns.append({'source': src, 'target': tgt, 'expected_return_hl': src_hl})

print(f"Missing return tags: {len(missing_returns)}")
```

### Recipe 6: Language code correctness check
```python
import re

VALID_LANG_CODES = ['en','es','fr','de','it','pt','nl','ru','ja','zh','ko','ar','hi','tr','pl','sv','da','no','fi','el','he','th','vi','id','ms','cs','sk','hu','ro','bg','uk','hr','sr','sl','et','lv','lt','mt','ga','is','mk','sq','bs','ca','eu','gl','cy','x-default']
VALID_REGION_CODES = ['US','GB','CA','AU','NZ','IE','ZA','MX','ES','AR','CO','CL','PE','VE','BR','PT','FR','BE','CH','LU','MC','DE','AT','LI','IT','VA','SM','NL','RU','JP','CN','TW','HK','SG','KR','SA','AE','EG','IN','TR','PL','SE','DK','NO','FI','GR','IL','TH','VN','ID','MY','CZ','SK','HU','RO','BG','UA','HR','RS','SI','EE','LV','LT','MT']

def is_valid_hreflang(value):
    if value == 'x-default': return True
    parts = value.split('-')
    if len(parts) == 1:
        return parts[0].lower() in VALID_LANG_CODES
    if len(parts) == 2:
        return parts[0].lower() in VALID_LANG_CODES and parts[1].upper() in VALID_REGION_CODES
    return False

invalid = hreflang[~hreflang['hreflang Value'].apply(is_valid_hreflang)]
print(f"Invalid hreflang codes: {len(invalid)}")
print(invalid[['Source URL','hreflang Value']].head(20))
```

### Recipe 7: Aleyda Solis hreflang tester (single URL deep)
```bash
# Browser tool — go to https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-tester/
# Or API equivalent:
curl "https://app.hreflangchecker.com/api/v1/check?url=https://example.com/page" \
  -H "Accept: application/json"

# Returns:
# - hreflang declarations found
# - reciprocity status per declaration
# - canonical conflicts
# - language code validity
```

### Recipe 8: x-default usage decision tree
```
x-default = the page shown when no other locale matches.

Common patterns:
1. English homepage as global default:
   <link rel="alternate" hreflang="x-default" href="https://example.com/" />

2. Language selector page (when no English fallback):
   <link rel="alternate" hreflang="x-default" href="https://example.com/select-region" />

3. NEVER use x-default as fallback for missing translations:
   BAD: page only exists in English, declare x-default pointing to English
   GOOD: when page exists in EN+ES+FR only — explicitly declare all three; omit x-default OR point x-default to language selector

x-default is the EXPLICIT DEFAULT, not a fallback declaration.
```

### Recipe 9: Common-mistake check pipeline
```python
def hreflang_audit(crawl_export):
    issues = []

    # Mistake 1: Hreflang to non-canonical URL
    for _, row in crawl_export.iterrows():
        if '?utm_' in row['hreflang URL'] or '?ref=' in row['hreflang URL']:
            issues.append({'type':'tracking_param_in_hreflang','source':row['Source URL'],'hreflang_url':row['hreflang URL']})

    # Mistake 2: Redirects in hreflang
    redirect_targets = [r['Source URL'] for _, r in crawl_export.iterrows() if r.get('Status Code',200) in [301,302,307,308]]
    for _, row in crawl_export.iterrows():
        if row['hreflang URL'] in redirect_targets:
            issues.append({'type':'hreflang_to_redirect','source':row['Source URL'],'redirected_url':row['hreflang URL']})

    # Mistake 3: Wrong code format (en_US vs en-US, english vs en)
    bad_codes = crawl_export[~crawl_export['hreflang Value'].str.match(r'^[a-z]{2}(-[A-Z]{2})?$|^x-default$')]
    for _, row in bad_codes.iterrows():
        issues.append({'type':'bad_code_format','source':row['Source URL'],'value':row['hreflang Value']})

    # Mistake 4: Self-reference missing
    sources_in_hreflang = set()
    for _, row in crawl_export.iterrows():
        if row['Source URL'] == row['hreflang URL']:
            sources_in_hreflang.add(row['Source URL'])
    all_sources = set(crawl_export['Source URL'])
    missing_self = all_sources - sources_in_hreflang
    for url in missing_self:
        issues.append({'type':'missing_self_reference','source':url})

    return issues
```

### Recipe 10: Per-country content variant — DeepL translation
```bash
# Translate EN → ES-MX (Mexican Spanish)
curl -X POST https://api.deepl.com/v2/translate \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "text=<source HTML or text>" \
  -d "target_lang=ES" \
  -d "formality=less" \
  -d "tag_handling=html"

# DeepL doesn't distinguish ES-MX vs ES-ES via API as of 2026 — use Spanish + locale-specific terms post-translation
```

### Recipe 11: Hreflang at scale — sitemap generation
```python
# For 50K-URL multi-language site, generate hreflang sitemaps
import xml.etree.ElementTree as ET

XHTML = 'http://www.w3.org/1999/xhtml'
ET.register_namespace('xhtml', XHTML)

urlset = ET.Element('urlset', {'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})

# pages = [{'url':'https://example.com/p1','alts':{'en-US':'https://example.com/p1','es-MX':'https://example.com/es-mx/p1',...}}]
for page in pages:
    url_el = ET.SubElement(urlset, 'url')
    ET.SubElement(url_el, 'loc').text = page['url']
    for hl, alt_url in page['alts'].items():
        ET.SubElement(url_el, f'{{{XHTML}}}link', {'rel':'alternate','hreflang':hl,'href':alt_url})
    ET.SubElement(url_el, f'{{{XHTML}}}link', {'rel':'alternate','hreflang':'x-default','href':page['url']})

ET.ElementTree(urlset).write('sitemap-hreflang.xml', xml_declaration=True, encoding='UTF-8')
```

## Examples

### Example 1: Audit existing multi-region site (EN + ES-MX + FR)
**Goal:** Find all hreflang defects on a 5000-URL site.

**Steps:**
1. Recipe 4: SF crawl with all 8 hreflang exports.
2. Recipe 5: pandas reciprocity check → list missing return tags.
3. Recipe 6: language code validity check.
4. Recipe 9: common-mistake pipeline.
5. Recipe 7: Aleyda spot-check on top-traffic URLs.
6. Output: hreflang audit report with per-URL action list.

**Result:** Audit report; pass to `frontend-engineer` for HTML / sitemap fixes.

### Example 2: New region launch (adding DE-DE to existing EN+ES setup)
**Goal:** Plan hreflang implementation for new German region.

**Steps:**
1. Recipe 10: DeepL translate existing EN pages to DE.
2. Build URL pattern: `https://example.com/de/<slug>`.
3. Update existing EN + ES pages with new DE alternates (every page).
4. Update existing sitemap.xml with new DE entries (Recipe 11).
5. After launch: Recipe 4 SF crawl → confirm reciprocity.
6. Submit DE sitemap via Suganthan GSC.

**Result:** New region launched with correct hreflang from day one.

### Example 3: Sitemap-based hreflang for 50K URL site
**Goal:** Implement hreflang via sitemap (HTML head approach too slow to maintain).

**Steps:**
1. Generate per-language sitemaps via Recipe 11.
2. Chunk into 50K-URL files (sitemap index for files > 50K).
3. Submit sitemap to GSC via Suganthan GSC.
4. Recipe 4: SF crawl with sitemap discovery → confirm SF sees hreflang from sitemap.
5. Monthly Recipe 9 audit.

**Result:** Scalable hreflang management; no per-page HTML updates needed.

## Edge cases / gotchas

- **Reciprocity is MANDATORY** — Google ignores hreflang if return tag missing. SF "Missing Return Tag" must be empty before declaring success.
- **ISO 639-1 (2-letter lang) only** — `english`/`spanish` invalid; must be `en`/`es`. ISO 639-2 (3-letter) also invalid for hreflang.
- **ISO 3166-1 alpha-2 (2-letter region) only** — `us`/`mexico` invalid; must be `US`/`MX`. Region uppercase, language lowercase.
- **Underscore not allowed** — `en_US` invalid; must be `en-US`. Use HYPHEN.
- **Hreflang to non-canonical URL** — points to tracking-param version = Google ignores. Strip params.
- **Hreflang to redirect** — points to URL that 301s = chain hop, signal loss. Point to final URL.
- **x-default is NOT a fallback for missing translations** — it's the explicit default destination.
- **Self-reference required** — page must reference itself in its own hreflang set. Common omission.
- **Sitemap hreflang doesn't replace canonical** — both must exist; canonical lives only in HTML or HTTP header (not sitemap).
- **DeepL lacks regional Spanish variants** — `es-ES` vs `es-MX` requires post-translation locale tweaks.
- **Hreflang cluster validation** — Google clusters URLs that share hreflang declarations. If a URL is in cluster A and also references URL in cluster B, both clusters break.
- **`en-001` (English worldwide)** — non-standard but Google supports it; use sparingly.
- **Subdomain vs subfolder hreflang** — both work; subfolder consolidates authority better (see `role.md` "Subdomain vs subfolder strategy").

## Sources

- [Google Search Central — localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google Search Central — hreflang sitemap format](https://developers.google.com/search/docs/specialty/international/localized-versions#xml)
- [Aleyda Solis hreflang tags generator + tester](https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-generator/)
- [Aleyda Solis — hreflang at scale](https://www.aleydasolis.com/english/blog/international-seo/hreflang-implementation-at-scale/)
- [Screaming Frog hreflang configuration](https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#hreflang)
- [Merkle Hreflang Tags Testing Tool](https://technicalseo.com/tools/hreflang/)
- [DeepL API translation docs](https://developers.deepl.com/)
- [ISO 639-1 language codes](https://www.iso.org/iso-639-language-codes.html)
- [ISO 3166-1 alpha-2 country codes](https://www.iso.org/iso-3166-country-codes.html)
