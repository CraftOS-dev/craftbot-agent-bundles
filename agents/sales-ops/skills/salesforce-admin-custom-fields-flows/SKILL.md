<!--
Source: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/ + https://developer.salesforce.com/tools/salesforcecli
Salesforce Admin — custom fields, validation rules, Lightning Flows, Apex (June 2026 SOTA).
-->
# Salesforce Admin — Custom Fields, Validation Rules, Flows — SKILL

Salesforce CRM administration via Metadata API + Tooling API + SFDX CLI. Deploys CustomField, ValidationRule, Flow (Lightning Flow), ApexClass, RecordType, PageLayout from a source-controlled `force-app/` project. Sandbox-first, RunLocalTests, then promote. Tooling API for runtime metadata reads (field-usage audits, schema hygiene).

## When to use

- **Deploy a custom field** — add a new field to Opportunity / Account / Lead / Contact / custom object.
- **Build a validation rule** — block save on stage advance without required fields (MEDDIC enforcement).
- **Build a Lightning Flow** — record-triggered, scheduled, or screen flow.
- **Schema audit** — find unused custom fields, nullity scan, deprecation queue.
- **Apex deploy** — light Apex (triggers, classes) with RunLocalTests.
- **Trigger phrases**: "deploy a Salesforce field", "validation rule on stage", "build a flow", "Tooling API field usage", "unused fields audit", "sandbox to production", "sf project deploy".

Do NOT use this skill for: **CPQ rules** (use `salesforce-cpq-conga-dealhub`); **approval routing** (use `deal-desk-discount-approval`); **CRMA dashboards** (use `rep-performance-dashboards`); **lead routing** (use `lead-routing-leandata-chili-piper`).

## Setup

```bash
# Install SFDX CLI
npm install -g @salesforce/cli
sf --version    # confirm >= 2.0
sf plugins install @salesforce/plugin-data
sf plugins install @salesforce/plugin-source

# Auth to sandbox + production
sf org login web --alias sandbox --instance-url https://test.salesforce.com
sf org login web --alias prod --instance-url https://login.salesforce.com

# Or via JWT (for CI/CD)
sf org login jwt --client-id $SF_CLIENT_ID --jwt-key-file server.key \
                 --username $SF_USERNAME --alias prod

# Confirm orgs
sf org list

# Env for api-gateway access
export MATON_API_KEY="<key>"   # for Tooling API via gateway
```

Required:
- `SF_CLIENT_ID` — Connected App consumer key (one-time setup in Salesforce Setup → App Manager)
- Connected App with `api` + `refresh_token` + `web` OAuth scopes
- Sandbox + production org access

## Common recipes

### Recipe 1: Pull current metadata to local project

```bash
# Initialize project
sf project generate --name my-org-source

# Pull all metadata (large org — use selective)
sf project retrieve start --target-org sandbox \
  --metadata CustomObject:Opportunity,CustomField:Opportunity.MEDDIC_Score__c

# Or by manifest (package.xml)
sf project retrieve start --target-org sandbox --manifest manifest/package.xml
```

### Recipe 2: Deploy a custom field (source XML)

```xml
<!-- force-app/main/default/objects/Opportunity/fields/Champion__c.field-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Champion__c</fullName>
    <label>Champion</label>
    <type>Lookup</type>
    <referenceTo>Contact</referenceTo>
    <relationshipName>Champion_Opportunities</relationshipName>
    <relationshipLabel>Champion Opportunities</relationshipLabel>
    <required>false</required>
    <description>MEDDIC champion contact reference</description>
</CustomField>
```

```bash
# Validate-only first
sf project deploy start --target-org sandbox \
  --source-dir force-app/main/default/objects/Opportunity/fields/Champion__c.field-meta.xml \
  --test-level RunLocalTests --check-only

# Real deploy
sf project deploy start --target-org sandbox \
  --source-dir force-app/main/default/objects/Opportunity/fields/Champion__c.field-meta.xml \
  --test-level RunLocalTests --wait 30
```

### Recipe 3: Validation rule — stage criteria enforcement

```xml
<!-- force-app/main/default/objects/Opportunity/validationRules/Evaluation_Requires_Champion.validationRule-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Evaluation_Requires_Champion</fullName>
    <active>true</active>
    <description>Champion must be set to advance to Evaluation stage</description>
    <errorConditionFormula>AND(
  ISCHANGED(StageName),
  TEXT(StageName) = "Evaluation",
  OR(
    ISBLANK(Champion__c),
    ISBLANK(Champion_Advocacy_Note__c)
  )
)</errorConditionFormula>
    <errorMessage>Identify a Champion (with advocacy note) before advancing to Evaluation.</errorMessage>
    <errorDisplayField>Champion__c</errorDisplayField>
</ValidationRule>
```

```bash
sf project deploy start --target-org sandbox \
  --source-dir force-app/main/default/objects/Opportunity/validationRules/ \
  --test-level RunLocalTests
```

### Recipe 4: Record-triggered Lightning Flow (stale-deal scan)

```xml
<!-- force-app/main/default/flows/Daily_Stale_Deal_Scan.flow-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <label>Daily Stale Deal Scan</label>
    <processType>AutoLaunchedFlow</processType>
    <runInMode>SystemModeWithSharing</runInMode>
    <start>
        <object>Opportunity</object>
        <recordTriggerType>None</recordTriggerType>
        <scheduledPaths>
            <name>DailyScan</name>
            <connector><targetReference>FilterStaleDeals</targetReference></connector>
            <pathType>AsyncAfterCommit</pathType>
            <maxBatchSize>200</maxBatchSize>
            <runAsync>true</runAsync>
        </scheduledPaths>
        <triggerType>Scheduled</triggerType>
        <schedule>
            <frequency>Daily</frequency>
            <startDate>2026-06-15</startDate>
            <startTime>09:00:00Z</startTime>
        </schedule>
        <filterFormula>AND(
  NOT(IsClosed),
  Last_Activity_Date__c &lt; TODAY() - 14
)</filterFormula>
    </start>
    <status>Active</status>
</Flow>
```

```bash
sf project deploy start --target-org sandbox \
  --source-dir force-app/main/default/flows/Daily_Stale_Deal_Scan.flow-meta.xml \
  --test-level RunLocalTests
```

### Recipe 5: Tooling API — unused field audit

```bash
# Step 1: list all unmanaged custom fields
sf data query --target-org prod \
  --query "SELECT EntityDefinition.QualifiedApiName, DeveloperName, DataType, CreatedDate FROM CustomField WHERE ManageableState = 'unmanaged' ORDER BY EntityDefinition.QualifiedApiName" \
  --use-tooling-api --result-format csv > custom_fields.csv

# Step 2: per field, run nullity check
sf data query --target-org prod \
  --query "SELECT COUNT(Id) total, COUNT(Champion__c) populated FROM Opportunity" \
  --result-format json
# nullity = populated / total; flag < 20% as deprecation candidate

# Step 3: cross-check report usage (Tooling API)
sf data query --target-org prod \
  --query "SELECT Id, DeveloperName, FolderName FROM Report" \
  --use-tooling-api --result-format csv > all_reports.csv

# Step 4: flow usage scan
sf data query --target-org prod \
  --query "SELECT Id, MasterLabel, ProcessType FROM FlowDefinition" \
  --use-tooling-api
```

### Recipe 6: Python nullity scan helper

```python
import subprocess, json, csv

def field_nullity(org, sobject, field):
    q = f"SELECT COUNT(Id) total, COUNT({field}) populated FROM {sobject}"
    r = subprocess.run(["sf","data","query","--target-org",org,"--query",q,"--json"],
                       capture_output=True, text=True, check=True)
    rec = json.loads(r.stdout)["result"]["records"][0]
    total = rec["total"] or 0
    pop = rec["populated"] or 0
    return (pop / total) if total else 0.0

with open("custom_fields.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sobj = row["EntityDefinition.QualifiedApiName"]
        fld  = row["DeveloperName"] + "__c"
        try:
            ratio = field_nullity("prod", sobj, fld)
            status = "deprecation_candidate" if ratio < 0.20 else "keep"
            print(f"{sobj}.{fld}: {ratio:.1%} {status}")
        except Exception as e:
            print(f"{sobj}.{fld}: ERROR {e}")
```

### Recipe 7: Apex class deploy with test coverage

```apex
// force-app/main/default/classes/MeddicScorer.cls
public with sharing class MeddicScorer {
    public static Integer score(Opportunity o) {
        Integer s = 0;
        if (o.Metrics__c != null) s += 2;
        if (o.Economic_Buyer__c != null) s += 3;
        if (o.Decision_Criteria__c != null) s += 2;
        if (o.Champion__c != null) s += 3;
        return s;
    }
}
```

```apex
// force-app/main/default/classes/MeddicScorerTest.cls — required for prod deploy
@isTest
private class MeddicScorerTest {
    @isTest static void scoresFully() {
        Opportunity o = new Opportunity(Name='t', StageName='Discovery',
            CloseDate=Date.today().addDays(30), Champion__c='001000000000001',
            Economic_Buyer__c='001000000000002', Metrics__c='ROI doc',
            Decision_Criteria__c='3 criteria');
        System.assertEquals(10, MeddicScorer.score(o));
    }
}
```

```bash
sf project deploy start --target-org prod \
  --source-dir force-app/main/default/classes/ \
  --test-level RunSpecifiedTests --tests MeddicScorerTest --wait 30
```

### Recipe 8: Sandbox-to-prod promotion checklist

```bash
# 1. Validate against production (no commit)
sf project deploy start --target-org prod \
  --source-dir force-app \
  --test-level RunLocalTests --check-only --wait 60 \
  --json > validate.json

# 2. Smoke-test in sandbox UI
# - Create record, trigger validation
# - Verify flow fires (Debug Logs)
# - Confirm dashboard renders new field

# 3. Promote
sf project deploy start --target-org prod \
  --source-dir force-app \
  --test-level RunLocalTests --wait 60

# 4. Post-deploy: quick query to confirm new field exists
sf data query --target-org prod \
  --query "SELECT Id, Champion__c FROM Opportunity LIMIT 1"
```

### Recipe 9: Destructive changes (delete field safely)

```xml
<!-- destructiveChanges.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Opportunity.Old_Field__c</members>
        <name>CustomField</name>
    </types>
    <version>60.0</version>
</Package>
```

```bash
# Pre-flight: confirm 0 reports, 0 flows, 0 Apex references
# (use Recipe 5 audit before destructive)

sf project deploy start --target-org sandbox \
  --manifest manifest/destructiveChanges.xml \
  --pre-destructive-changes manifest/destructiveChangesPre.xml \
  --check-only
```

### Recipe 10: Permission set deploy (replace Profile customization)

```xml
<!-- force-app/main/default/permissionsets/MEDDIC_Power_User.permissionset-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>MEDDIC Power User</label>
    <fieldPermissions>
        <editable>true</editable>
        <field>Opportunity.Champion__c</field>
        <readable>true</readable>
    </fieldPermissions>
    <fieldPermissions>
        <editable>true</editable>
        <field>Opportunity.Economic_Buyer__c</field>
        <readable>true</readable>
    </fieldPermissions>
</PermissionSet>
```

### Recipe 11: api-gateway fallback (Tooling API via REST)

```bash
# When SFDX isn't available — hit Tooling API via api-gateway
curl -X POST "https://gateway.maton.ai/salesforce/services/data/v60.0/tooling/query/?q=SELECT+Id,DeveloperName+FROM+CustomField+WHERE+ManageableState='unmanaged'" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Recipe 12: Bulk SOQL data export

```bash
# Export all Opportunity records (Bulk API 2.0 — fast for > 50K records)
sf data query --target-org prod \
  --query "SELECT Id, Name, StageName, Amount, CloseDate, Owner.Name FROM Opportunity WHERE IsClosed = FALSE" \
  --bulk --wait 30 \
  --result-format csv > open_opps.csv
```

## Examples

### Example 1: Deploy "Champion required for Evaluation" enforcement

**Goal:** Block stage advance to Evaluation unless Champion + Champion advocacy note present.

**Steps:**
1. Retrieve current Opportunity object metadata (Recipe 1).
2. Add Champion__c lookup + Champion_Advocacy_Note__c long-text via field-meta XML (Recipe 2).
3. Add validation rule from Recipe 3.
4. Validate against sandbox + RunLocalTests (`--check-only`).
5. Deploy to sandbox. Manually try to advance an opp → confirm error message.
6. Deploy to production using Recipe 8 promotion sequence.

**Result:** Reps can no longer move to Evaluation without naming a Champion; pipeline data quality lifts.

### Example 2: Quarterly schema audit (deprecation queue)

**Goal:** Identify custom fields with < 20% nullity, no reports, no flows; mark for deprecation.

**Steps:**
1. Recipe 5 step 1 — list all unmanaged CustomField records → `custom_fields.csv`.
2. Recipe 6 Python script — compute nullity for each.
3. Recipe 5 step 3 — pull all reports + flows + Apex references.
4. Join in pandas: field has nullity < 20% AND 0 reports AND 0 flows → deprecation candidate.
5. Render audit table → notion page with reviewer sign-off column.
6. After reviewer approval: Recipe 9 destructive deploy in sandbox first.

**Result:** ~15-30% of legacy custom fields retired per quarter; schema stays clean.

### Example 3: Stale-deal Scheduled Flow rollout

**Goal:** Daily 9am UTC scan of stale opportunities (> 14 days no activity in non-closed stage), surface to a Salesforce report owned by sales managers.

**Steps:**
1. Add Last_Activity_Date__c rollup or formula field (Recipe 2).
2. Deploy Scheduled Flow from Recipe 4 to sandbox.
3. Set Flow to populate a custom Is_Stale__c boolean.
4. Build report on Opportunity with filter `Is_Stale__c = TRUE`.
5. Validate one day's run in sandbox via Setup → Process Automation → Paused/Failed Flow Interviews → run history.
6. Promote to production. Verify report populates next morning.

**Result:** Managers have a single dashboard for stale-deal triage; pairs with `stalled-deal-alerts-engagement-signals` Slack pings.

## Edge cases / gotchas

- **RunLocalTests is mandatory for production** — Salesforce enforces ≥75% Apex coverage. Without tests, deploy fails. Even non-Apex deploys to production require running existing local tests.
- **Field-Level Security (FLS)** — new custom fields default to NOT visible. Add Permission Set in same deploy (Recipe 10) or new field is invisible to users.
- **Validation rule formula limits** — 4,000 character limit on errorConditionFormula. Hit it on complex rules: refactor to record-triggered Flow.
- **ISCHANGED() in validation rules requires stage advance** — won't fire on insert of new record at that stage. Pair with workflow rule or formula.
- **Deploy locks** — only one deploy at a time per org. Production locks during 30-min deploys. CI/CD: serialize.
- **Inactive flows aren't deleted** — old draft / inactive flows accumulate. Quarterly cleanup via Tooling API.
- **Object names in `<field>` permission references** — must be fully qualified (`Opportunity.Champion__c` not `Champion__c`). Common deploy error.
- **Refresh sandboxes after major prod changes** — staleness causes deploy drift. Refresh full sandbox quarterly.
- **API version mismatch** — `<apiVersion>` in meta XML must match org. Bump to 60.0+ for 2026. Old version (< 50) deprecation looming.
- **Destructive changes lockstep** — deleting field while it's referenced in a Report breaks the deploy mid-flight. Pre-flight Recipe 5 step 3 always.
- **Profile vs Permission Set** — Salesforce is deprecating Profile-based permissions in favor of Permission Sets. New work: Permission Sets only.
- **Tooling API rate limits** — 100 calls/min per user. Bulk Tooling API (separate endpoint) for large audits.
- **Lookup deletion behavior** — `<deleteConstraint>SetNull</deleteConstraint>` vs `Restrict` vs `Cascade`. Wrong choice silently nulls or blocks deletes.
- **Org-default flow user** — Scheduled Flows run as a system user; permission errors silent. Test with Debug Logs.
- **Manifest size limits** — `package.xml` > 10K members times out. Split into smaller deploys.
- **2GP managed package fields can't be deployed via Metadata API** — use the package upgrade flow instead.

## Sources

- [Salesforce Metadata API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/)
- [Salesforce Tooling API Reference](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/)
- [Salesforce CLI (sf) Command Reference](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/)
- [Salesforce DX Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/)
- [Validation Rules — Salesforce Help](https://help.salesforce.com/s/articleView?id=sf.validation_rules.htm)
- [Lightning Flow — Trailhead](https://trailhead.salesforce.com/content/learn/modules/flow-fundamentals)
- [Apex Test Coverage Requirements](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_qs_apexruntests.htm)
- [Field-Level Security Best Practices](https://help.salesforce.com/s/articleView?id=sf.admin_fls.htm)
