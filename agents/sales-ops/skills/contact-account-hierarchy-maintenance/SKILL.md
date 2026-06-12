<!--
Source: https://help.salesforce.com/s/articleView?id=sf.account_hierarchy.htm + https://www.dnb.com/business-credit/dun-and-bradstreet-direct.html + https://developers.hubspot.com/docs/api/crm/companies
Contact-account hierarchy maintenance — Salesforce Account Hierarchy + HubSpot Company Hierarchy + D&B Direct+ (June 2026 SOTA).
-->
# Contact-Account Hierarchy Maintenance — SKILL

Maintain parent-child-sibling account structures (multi-divisional enterprise, M&A, divestitures, subsidiary mapping). **Salesforce Account Hierarchy** native + **HubSpot Company Hierarchy** + **D&B Direct+** for DUNS-based parent-child refresh + **LeanData BookBuilder** for ABM hierarchy enforcement. Bulk re-parent via Composite API. Detect drift between CRM hierarchy and external truth (D&B). Reconcile when M&A activity hits.

## When to use

- **Re-parent an account after M&A** — acquirer became new global ultimate; reroute child accounts.
- **Detect hierarchy drift** — CRM `ParentId` chain disagrees with D&B DUNS structure.
- **Bulk hierarchy refresh** — quarterly D&B Direct+ pull → reconcile against Salesforce.
- **Subsidiary mapping** — a new account is a division of an existing customer; merge or link.
- **HubSpot company hierarchy** — set `parent` association on a child company.
- **ABM account family rollup** — show total opps + ARR across the parent tree.
- **Trigger phrases**: "account hierarchy", "parent account", "D&B refresh", "DUNS", "subsidiary mapping", "company tree", "global ultimate", "M&A reparent".

Do NOT use this skill for: **dedup** (use `duplicate-mgmt-leandata-dedupe`); **enrichment of individual contact records** (use `data-enrichment-zoominfo-apollo-clay`); **territory assignment after re-parent** (use `territory-planning-assignment`).

## Setup

```bash
# Salesforce SFDX (for bulk re-parent)
npm install -g @salesforce/cli
sf org login web --alias prod --instance-url https://login.salesforce.com

# D&B Direct+ — OAuth client credentials
# Get from https://directplus.documentation.dnb.com/
export DNB_CLIENT_ID="<id>"
export DNB_CLIENT_SECRET="<secret>"

# HubSpot — private app token (Settings → Integrations → Private Apps)
export HUBSPOT_TOKEN="<token>"

# api-gateway fallback (Maton-onboarded)
export MATON_API_KEY="<key>"

# Test connectivity
sf org display --target-org prod
curl -s -u "$DNB_CLIENT_ID:$DNB_CLIENT_SECRET" \
  -X POST "https://plus.dnb.com/v2/token" \
  -d "grant_type=client_credentials" | jq .access_token
```

Required:
- Salesforce admin role + API Enabled permission
- D&B Direct+ subscription (paid; enterprise tier for hierarchy data)
- HubSpot Sales/Service Hub Pro+ (company associations API)
- Optional: LeanData BookBuilder admin (ABM hierarchy enforcement)

## Common recipes

### Recipe 1: Salesforce — pull current Account hierarchy

```bash
# All accounts with parent chain (recursive helper SOQL not supported — pull flat + join)
sf data query --target-org prod \
  --query "SELECT Id, Name, ParentId, Parent.Name, DUNS_Number__c, BillingCountry, AnnualRevenue, Type FROM Account WHERE Type IN ('Customer','Prospect') ORDER BY Name" \
  --bulk --wait 30 --result-format csv > sf_accounts.csv
```

### Recipe 2: Salesforce — bulk re-parent via Composite API

```bash
# Build reparent.csv with Id + ParentId columns
# Id,ParentId
# 001XX0000ABCXYZ,001XX0000DEFUVW
# ...

sf data upsert bulk \
  --target-org prod \
  --sobject Account \
  --external-id Id \
  --file reparent.csv \
  --wait 30
```

Use this when M&A hits and 50+ child accounts need a new global ultimate. Always sandbox-first.

### Recipe 3: Apex — hierarchy roll-up of ARR

```apex
// force-app/main/default/classes/AccountHierarchyRollup.cls
public with sharing class AccountHierarchyRollup {
    public static Decimal totalARR(Id rootAccountId) {
        Set<Id> tree = new Set<Id>{ rootAccountId };
        // BFS down the tree (5 levels max in practice)
        for (Integer depth = 0; depth < 5; depth++) {
            List<Account> children = [
                SELECT Id FROM Account WHERE ParentId IN :tree
            ];
            if (children.isEmpty()) break;
            for (Account c : children) tree.add(c.Id);
        }
        AggregateResult ar = [
            SELECT SUM(ARR__c) total FROM Account WHERE Id IN :tree
        ];
        return (Decimal) ar.get('total');
    }
}
```

Salesforce native `Account.IsParent` field exists but only flags "has children" — no recursive SUM is supported declaratively. Apex BFS is the standard pattern (capped at 5 levels for governor limits).

### Recipe 4: Hierarchy report (Lightning) via SOQL recursion helper

```python
# Run via cli-anything — build a hierarchy tree from flat export
import pandas as pd

df = pd.read_csv("sf_accounts.csv")
children = df.groupby("ParentId")["Id"].apply(list).to_dict()

def descend(node, depth=0, out=None):
    if out is None: out = []
    out.append({"depth": depth, "Id": node, "Name": df[df["Id"] == node]["Name"].iloc[0]})
    for child in children.get(node, []):
        descend(child, depth + 1, out)
    return out

# Roots: accounts with no parent
roots = df[df["ParentId"].isna()]["Id"].tolist()
for root in roots:
    tree = descend(root)
    for n in tree:
        print("  " * n["depth"], n["Name"])
```

### Recipe 5: D&B Direct+ — fetch company family by DUNS

```bash
# 1. Get OAuth token
TOKEN=$(curl -s -u "$DNB_CLIENT_ID:$DNB_CLIENT_SECRET" \
  -X POST "https://plus.dnb.com/v2/token" \
  -d "grant_type=client_credentials" | jq -r .access_token)

# 2. Fetch full corporate linkage for a DUNS
curl -s "https://plus.dnb.com/v1/familyTree?duns=804735132" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .

# Returns:
# - globalUltimate (top of tree)
# - domesticUltimate (top of the in-country branch)
# - parent
# - branches[] / subsidiaries[]
```

### Recipe 6: D&B Direct+ — bulk DUNS refresh

```python
# Run via cli-anything — refresh DUNS-linked accounts
import requests, time, pandas as pd

token = requests.post("https://plus.dnb.com/v2/token",
    auth=("$DNB_CLIENT_ID", "$DNB_CLIENT_SECRET"),
    data={"grant_type": "client_credentials"}).json()["access_token"]

accounts = pd.read_csv("sf_accounts.csv")
refreshed = []
for _, row in accounts.dropna(subset=["DUNS_Number__c"]).iterrows():
    r = requests.get(
        f"https://plus.dnb.com/v1/familyTree?duns={row['DUNS_Number__c']}",
        headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        data = r.json()
        refreshed.append({
            "Id": row["Id"],
            "dnb_global_ultimate_duns": data.get("globalUltimate", {}).get("duns"),
            "dnb_global_ultimate_name": data.get("globalUltimate", {}).get("name"),
            "dnb_parent_duns": data.get("parent", {}).get("duns"),
        })
    time.sleep(0.2)  # ~5 calls/s polite

pd.DataFrame(refreshed).to_csv("dnb_refresh.csv", index=False)
```

### Recipe 7: Drift detection — CRM vs D&B truth

```python
# Compare CRM ParentId chain to D&B parent DUNS
sf = pd.read_csv("sf_accounts.csv")
dnb = pd.read_csv("dnb_refresh.csv")

# Map DUNS → SF Account Id
duns_to_sfid = sf.set_index("DUNS_Number__c")["Id"].to_dict()

merged = sf.merge(dnb, on="Id", how="left")
merged["expected_parent_id"] = merged["dnb_parent_duns"].map(duns_to_sfid)
merged["drift"] = (merged["ParentId"] != merged["expected_parent_id"]) & merged["expected_parent_id"].notna()

drift_log = merged[merged["drift"]][["Id", "Name", "ParentId", "expected_parent_id"]]
drift_log.to_csv("hierarchy_drift.csv", index=False)
print(f"{len(drift_log)} accounts drift from D&B truth")
```

### Recipe 8: HubSpot — set company parent association

```bash
# v4 associations API — child to parent (categoryId 13 = parent/child)
curl -X PUT \
  "https://api.hubapi.com/crm/v4/objects/companies/$CHILD_ID/associations/companies/$PARENT_ID" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":13}]'
```

Association type IDs:
- `13` = Parent company → Child company (forward)
- `14` = Child company → Parent company (reverse, auto-created)

### Recipe 9: HubSpot — get full company tree

```bash
# Get all children of a parent company
curl -s \
  "https://api.hubapi.com/crm/v4/objects/companies/$PARENT_ID/associations/companies" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" | jq '.results[] | select(.associationTypes[].typeId == 14)'
```

### Recipe 10: Hierarchy normalization Apex trigger (prevent cycles)

```apex
// force-app/main/default/triggers/AccountParentCycleCheck.trigger
trigger AccountParentCycleCheck on Account (before update) {
    for (Account a : Trigger.new) {
        if (a.ParentId == null) continue;
        if (a.ParentId == a.Id) {
            a.addError('Account cannot be its own parent.');
            continue;
        }
        // Walk up the chain — must terminate, no cycles
        Set<Id> seen = new Set<Id>{ a.Id };
        Id cursor = a.ParentId;
        Integer hops = 0;
        while (cursor != null && hops < 10) {
            if (seen.contains(cursor)) {
                a.addError('Parent assignment creates a cycle.');
                break;
            }
            seen.add(cursor);
            Account parent = [SELECT ParentId FROM Account WHERE Id = :cursor LIMIT 1];
            cursor = parent.ParentId;
            hops++;
        }
    }
}
```

### Recipe 11: LeanData BookBuilder — ABM hierarchy enforcement

```bash
# LeanData runs in-Salesforce. Configure via Salesforce admin UI:
# 1. LeanData → BookBuilder → New Book
# 2. Add hierarchy roll-up: "Group accounts by Global Ultimate Account"
# 3. Set ownership rule: "Named AE owns full tree if account is Tier-1 ABM"
# 4. Run preview against 100 sample accounts
# 5. Activate → LeanData auto-assigns ownership across the tree
```

Reference doc the rule set in `notion` so the routing logic is reviewable outside the LeanData UI.

### Recipe 12: api-gateway fallback (proxy to Salesforce + D&B)

```bash
# When local SFDX/D&B keys unavailable
curl "https://gateway.maton.ai/salesforce/services/data/v60.0/query?q=SELECT+Id,Name,ParentId+FROM+Account+WHERE+ParentId+!=+NULL" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl "https://gateway.maton.ai/dnb/v1/familyTree?duns=804735132" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

## Examples

### Example 1: Microsoft acquires Activision — re-parent the tree

**Goal:** After M&A, re-route Activision + Blizzard + King child accounts under Microsoft as global ultimate.

**Steps:**
1. Pull current Activision tree from Salesforce (Recipe 1).
2. Hit D&B Direct+ for Activision DUNS → confirm globalUltimate is now Microsoft (Recipe 5).
3. Find Microsoft's `Account.Id` in Salesforce (`sf data query`).
4. Build `reparent.csv`: every Activision-tree leaf gets `ParentId = <Microsoft Id>`, intermediate nodes get `ParentId = Activision (still alive as division)`.
5. Sandbox dry-run via Recipe 2.
6. Roll up ARR via Recipe 3 — confirm Microsoft tree now shows combined ARR.
7. Production deploy + Slack alert to AEs on affected accounts.

**Result:** Hierarchy reflects post-M&A reality; ABM tier-1 named AE coverage rolls up correctly.

### Example 2: Quarterly D&B drift reconciliation

**Goal:** Identify and resolve all accounts whose CRM parent chain disagrees with D&B's corporate linkage.

**Steps:**
1. Recipe 1 — export all Salesforce accounts with DUNS populated.
2. Recipe 6 — bulk D&B refresh (typically 5K-20K accounts).
3. Recipe 7 — drift detection report.
4. Triage by deal volume: drift on accounts with open opps gets manual SalesOps review first.
5. For low-risk drift, bulk apply D&B truth via Recipe 2.
6. Log delta to `notion` quarterly hierarchy audit doc.

**Result:** Drift held below 5% account base; named-account routing stays accurate.

### Example 3: ABM tier-1 family tree for executive QBR

**Goal:** CRO QBR needs total ARR + open pipeline across the GE Healthcare family (subsidiary of GE).

**Steps:**
1. Identify GE Holdings root `Account.Id`.
2. Run Apex `AccountHierarchyRollup.totalARR()` (Recipe 3).
3. Run pipeline rollup variant (same BFS, SUM `Amount` on Opportunity).
4. Render to `notion` QBR page + Slack thread to CRO.

**Result:** One-number ARR + pipeline visibility across a 30-division enterprise customer.

## Edge cases / gotchas

- **Salesforce 500-level hierarchy limit** — Salesforce supports unlimited depth in theory, but Lightning UI's "View Hierarchy" component caps at 500 levels. Real customers rarely exceed 5-7.
- **Apex governor limits on tree walks** — SOQL queries inside loops hit limits fast. BFS in batches; cap depth at 5 unless customer is conglomerate-scale.
- **DUNS isn't always populated** — Salesforce auto-DUNS via D&B Optimizer is opt-in. ~30-40% of accounts will lack DUNS; fall back to fuzzy name + country matching for those.
- **D&B Direct+ rate limit** — 100 calls/min default; 1000/min on enterprise. For bulk refresh > 5K accounts, paginate and sleep.
- **D&B "globalUltimate" vs "domesticUltimate"** — globalUltimate is the worldwide parent. Sometimes you want domesticUltimate (e.g., GE Healthcare USA, not GE worldwide) for tax/legal entity tracking. Pick deliberately.
- **HubSpot company hierarchy is single-parent only** — no multi-parent (matrix org) support. Salesforce native is also single-parent. Workarounds via custom junction objects.
- **Re-parenting triggers ownership changes if LeanData BookBuilder is on** — every re-parent fires the ABM routing rule. Pause the rule during bulk re-parent or stand back for 1000s of ownership change emails.
- **ParentId cycles silently corrupt rollups** — Salesforce doesn't enforce acyclic. Apex trigger (Recipe 10) is the only safeguard.
- **Account merge ≠ re-parent** — merge collapses two accounts into one (data loss risk). Re-parent leaves both intact with hierarchy link. Use merge only after dedup determination, not for hierarchy correction.
- **Currency mismatch on rolled-up ARR** — multi-currency orgs need `convertCurrency()` in SOQL or the rollup mixes USD + EUR + GBP. Standard miss.
- **CRMA / Tableau CRM dashboards need flat hierarchy table** — they can't recursively traverse. Build a `dim_account_hierarchy` flat table via dbt or Apex schedule (level1, level2, level3, ... globalUltimate columns).
- **HubSpot company sync from Salesforce won't sync hierarchy** — HubSpot's Salesforce connector skips ParentId. Use a custom Operations Hub workflow + the v4 associations API to mirror.
- **D&B contract size** — Direct+ family-tree API is in the higher-tier package, not basic enrichment. Confirm before promising hierarchy refresh.
- **Soft-deleted accounts can leave orphan children** — `IsDeleted = FALSE` filter is critical when building trees; orphan branches break rollups.

## Sources

- [Salesforce Account Hierarchy — Help](https://help.salesforce.com/s/articleView?id=sf.account_hierarchy.htm)
- [Salesforce — IsParent + Parent Account](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_account.htm)
- [Salesforce Composite + Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/)
- [D&B Direct+ Family Tree API](https://directplus.documentation.dnb.com/openAPI.html?apiID=familyTree)
- [D&B Direct+ Overview](https://www.dnb.com/business-credit/dun-and-bradstreet-direct.html)
- [HubSpot CRM v4 Associations API](https://developers.hubspot.com/docs/api/crm/associations/v4)
- [HubSpot Companies Object](https://developers.hubspot.com/docs/api/crm/companies)
- [LeanData BookBuilder Docs](https://docs.leandata.com/bookbuilder)
- [Apex Trigger Best Practices](https://developer.salesforce.com/wiki/apex_code_best_practices)
