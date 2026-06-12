<!--
Sources: https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/
         https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026
         https://www.siit.io/tools/comparison/jumpcloud-vs-okta
Stage-based: Stytch+SSOJet (pre-PMF), Auth0 (Series A-B), WorkOS (B2B SaaS), Okta (enterprise), JumpCloud (open dir + MDM).
-->
# SSO / IAM Setup — Okta / JumpCloud / WorkOS / Stytch / Auth0 — SKILL

Stand up SSO + SCIM provisioning for workforce IAM. Stage-based platform selection, SAML config, SCIM 2.0 user lifecycle automation, group-based app assignment, MFA enforcement. Includes Just-In-Time (JIT) provisioning recipes and conditional access policy templates.

## When to use

- SOC 2 / ISO 27001 audit forces SSO.
- Customer asks for "SSO for enterprise tier" (B2B SaaS).
- Tool count > 25 → IAM consolidation cuts seat costs + audit time.
- Off-boarding takes > 1 hour → SCIM-based deprovisioning solves it.
- Trigger phrases: "SSO", "SAML", "SCIM", "MFA", "Okta", "WorkOS", "JumpCloud", "Stytch", "Auth0", "Just-in-time provisioning", "identity provider".

## Setup

```bash
export OKTA_API_TOKEN="xxx"      # https://<org>.okta.com/admin/access/api/tokens
export OKTA_ORG="<org>"          # e.g., acme.okta.com → "acme"
export JUMPCLOUD_KEY="xxx"       # https://console.jumpcloud.com — API settings
export WORKOS_API_KEY="xxx"      # https://dashboard.workos.com
export STYTCH_PROJECT_ID="xxx"
export STYTCH_SECRET="xxx"
export AUTH0_DOMAIN="<tenant>.auth0.com"
export AUTH0_MGMT_TOKEN="xxx"    # Management API token
```

Tier notes:
- **Okta** Workforce Identity ~$2-15/user/mo by feature; richest catalog.
- **JumpCloud** ~$8-23/user/mo; bundles IAM + MDM + infra.
- **WorkOS** usage-based for B2B SaaS; SSO ~$125/connection/mo.
- **Stytch** B2B ~free <1k MAU.
- **Auth0** Free <7.5k MAU; B2C+B2B unified.

## Common recipes

### Recipe 1: Stage-based platform selection
```yaml
choose:
  pre_pmf_seed_under_1M_ARR:
    primary: Stytch + SSOJet
    why: Stytch B2B Orgs free <1k MAU; SSOJet handles enterprise IdPs cheaply
  series_a_b_b2c_or_mixed:
    primary: Auth0
    why: Decade leader; B2C+B2B unified; broadest IdP catalog
  series_a_plus_b2b_saas_enterprise_deals:
    primary: WorkOS
    why: 4-week SAML → 4-day; Directory Sync (SCIM) productised; AdminPortal
  enterprise_workforce_plus_customer:
    primary: Okta
    why: Workforce + Customer Identity in one contract; broadest integration catalog
  open_directory_iam_mdm_infra_in_one:
    primary: JumpCloud
    why: Mac/Win/Linux MDM bundled; LDAP + RADIUS; SSO; one contract
  saml_oidc_across_all_idps:
    primary: Scalekit
    why: Cross-IdP normalization (Okta + Entra + Google + JumpCloud + OneLogin + ADFS + Ping + Shibboleth)
```

### Recipe 2: Create Okta SAML app
```bash
curl -s -X POST "https://$OKTA_ORG.okta.com/api/v1/apps" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"template_saml_2_0",
    "label":"Internal — Production Console",
    "signOnMode":"SAML_2_0",
    "settings":{
      "signOn":{
        "ssoAcsUrl":"https://console.example.com/saml/acs",
        "audience":"https://console.example.com",
        "subjectNameIdTemplate":"${user.email}",
        "subjectNameIdFormat":"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
        "responseSigned":true,
        "assertionSigned":true,
        "signatureAlgorithm":"RSA_SHA256",
        "honorForceAuthn":true
      }
    }
  }'
```

### Recipe 3: Okta SCIM 2.0 provisioning to a downstream app
```bash
# Enable SCIM provisioning on an existing Okta app
curl -s -X PUT "https://$OKTA_ORG.okta.com/api/v1/apps/<app_id>/features/USER_PROVISIONING" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"USER_PROVISIONING",
    "status":"ENABLED",
    "capabilities":{
      "create":{"lifecycleCreate":{"status":"ENABLED"}},
      "update":{
        "profile":{"status":"ENABLED"},
        "lifecycleDeactivate":{"status":"ENABLED"}
      }
    }
  }'
```

### Recipe 4: WorkOS Directory Sync setup
```bash
# Create a directory connection (HR-driven SCIM provisioning)
curl -s -X POST "https://api.workos.com/directories" \
  -H "Authorization: Bearer $WORKOS_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"acme-prod",
    "type":"okta scim v2.0"
  }'
# returns a tenant URL + bearer token; configure on Okta side
```

### Recipe 5: Group-based app assignment (Okta)
```bash
# Assign group "Engineering" to the "GitHub Enterprise" app
curl -s -X PUT "https://$OKTA_ORG.okta.com/api/v1/apps/<app_id>/groups/<group_id>" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"priority":0}'
```

### Recipe 6: Conditional access policy (Okta)
```bash
# Require MFA, deny risky logins
curl -s -X POST "https://$OKTA_ORG.okta.com/api/v1/policies" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "type":"ACCESS_POLICY",
    "name":"Production-app access — MFA required",
    "settings":{
      "factorMode":"2FA",
      "factorRequiredAuthenticator":["okta_verify","webauthn"]
    },
    "conditions":{
      "network":{"connection":"ANYWHERE"},
      "riskScore":{"level":"MEDIUM_OR_HIGHER","action":"DENY"},
      "userType":{"include":["EMPLOYEE","CONTRACTOR"]}
    }
  }'
```

### Recipe 7: WorkOS SSO via SAML for a customer-facing app
```javascript
// Authenticate a user via WorkOS SSO (B2B SaaS pattern)
import { WorkOS } from '@workos-inc/node';
const workos = new WorkOS(process.env.WORKOS_API_KEY);

// Step 1: Get auth URL
const url = workos.sso.getAuthorizationUrl({
  organization: 'org_XXX',
  redirectUri: 'https://app.example.com/callback',
  clientId: process.env.WORKOS_CLIENT_ID,
});

// Step 2: On callback, exchange code for profile
const { profile, accessToken } = await workos.sso.getProfileAndToken({
  code: req.query.code,
  clientId: process.env.WORKOS_CLIENT_ID,
});
```

### Recipe 8: Stytch B2B Organizations + Members
```bash
# Create org
curl -s -X POST https://test.stytch.com/v1/b2b/organizations \
  -u "$STYTCH_PROJECT_ID:$STYTCH_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"organization_name":"Acme Inc","email_jit_provisioning":"NOT_ALLOWED","mfa_methods":"ENFORCED"}'

# Create SCIM connection
curl -s -X POST https://test.stytch.com/v1/b2b/scim/connections \
  -u "$STYTCH_PROJECT_ID:$STYTCH_SECRET" \
  -d '{"organization_id":"<org>","display_name":"Acme SCIM"}'
```

### Recipe 9: JumpCloud user lifecycle (REST)
```bash
# Create user
curl -s "https://console.jumpcloud.com/api/systemusers" \
  -X POST -H "x-api-key: $JUMPCLOUD_KEY" -H "Content-Type: application/json" \
  -d '{
    "email":"avery@co.com",
    "username":"avery",
    "firstname":"Avery",
    "lastname":"Lee",
    "groups":["<ops-group>","<all-staff>"]
  }'

# Suspend
curl -s "https://console.jumpcloud.com/api/systemusers/<id>" \
  -X PUT -H "x-api-key: $JUMPCLOUD_KEY" -H "Content-Type: application/json" \
  -d '{"suspended":true}'
```

### Recipe 10: Audit log pull for SOC 2
```bash
# Okta system log
curl -s "https://$OKTA_ORG.okta.com/api/v1/logs?since=2026-06-01&filter=eventType+sw+%22user.account%22" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" | jq '[.[] | {ts: .published, actor: .actor.alternateId, event: .eventType, target: .target[0].displayName}]'
```

### Recipe 11: SCIM provisioning rules per group
```yaml
# Group → app fanout matrix
all-staff:
  apps: [Google Workspace, Slack, Notion, Zoom, Loom, 1Password]
engineering:
  apps: [GitHub Enterprise, Linear, Sentry, Vercel, Datadog, AWS SSO]
sales:
  apps: [HubSpot, Gong, Apollo, Outreach, ZoomInfo]
support:
  apps: [Intercom, Zendesk, Statuspage]
ops:
  apps: [Ramp, Vendr, Notion-Ops-Wiki, Linear-Triage]
founders:
  apps: [all]
contractor:
  apps: [Google Workspace, Slack-guest, Notion-guest]
  conditional_access: MFA_required + restricted_to_VPN
```

## Examples

### Example 1: Stand up SSO + SCIM for 50-person team
**Goal:** Replace email/password sprawl with Okta SSO + SCIM-managed provisioning.
**Steps:**
1. Recipe 1: select Okta (workforce IAM).
2. For each SaaS app: Recipe 2 (SAML config) + Recipe 3 (SCIM).
3. Recipe 11: groups + app assignment matrix in Notion.
4. Recipe 5 apply assignments.
5. Recipe 6 conditional access for prod-tier apps.
6. Recipe 10: validate logs flowing to Datadog/Splunk for audit.

**Result:** One sign-on; auto-provisioning; SCIM deprovisioning on termination; SOC 2 IDM controls covered.

### Example 2: B2B SaaS "enterprise SSO" feature
**Goal:** Customer asks for SSO into your app.
**Steps:**
1. Recipe 1: pick WorkOS (4-week → 4-day SAML).
2. Recipe 7: integrate SDK in app.
3. WorkOS Admin Portal: customer self-configures their IdP (Okta/Entra/Google/Auth0/Ping).
4. Recipe 4: enable Directory Sync for SCIM provisioning of their users into your org.
5. Bill enterprise tier on signed contract.

**Result:** Enterprise-ready SSO in days, not weeks; SCIM provisioning across customer IdPs.

## Edge cases / gotchas

- **SAML attribute mismatch.** `NameID` format mismatch between IdP and SP is the #1 SAML pain. Always check both ends emit/expect `emailAddress` (or persistent ID, consistently).
- **SCIM not the same as SAML.** SCIM = user lifecycle (create/update/disable). SAML = auth. Need both.
- **JIT provisioning on first sign-in.** Allows account creation when user first SAML-auths. Pair with SCIM for full lifecycle; otherwise create-only, no deprovision.
- **MFA fatigue / push bombing.** Default Okta Verify push is push-bomb-susceptible. Use number-matching / webauthn / passkeys for prod.
- **Group sprawl.** Don't model every fine-grained access in groups; nest groups (all-staff + role groups + team groups). Quarterly review.
- **Auth0 free tier MAU cap (7.5k).** Easy to exceed; plan tier transition before hitting cap.
- **WorkOS per-connection pricing.** ~$125/customer-connection/mo. Profitable on enterprise tiers, not on small customers.
- **Service accounts.** Don't put service accounts under your SSO; keep separate vaulted-credential model.
- **Federated breakup risk.** When you change IdP vendor, every downstream SCIM connection re-configures. Plan 4-6 weeks.
- **Stytch B2B JIT toggle.** Recipe 8 sets `email_jit_provisioning:NOT_ALLOWED`; flip to ALLOWED for self-serve SaaS.
- **Conditional access edge.** Geo-block US-OFAC countries (CU, IR, KP, SY, +Russia/Belarus depending on policy); see Recipe 6 conditions. **Defer to `legal-counsel` for binding sanctions-compliance review.**
- **SOC 2 evidence trail.** Recipe 10 logs must retain ≥ 1 year for SOC 2 + ≥ 7 years for SOX.

## Sources

- Security Boulevard — Auth0 vs Okta vs Stytch vs WorkOS vs SSOJet 2026: https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/
- WorkOS — Best SCIM Providers 2026: https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026
- SIIT — JumpCloud vs Okta 2026: https://www.siit.io/tools/comparison/jumpcloud-vs-okta
- Okta dev docs: https://developer.okta.com/
- JumpCloud API: https://docs.jumpcloud.com/api/
- WorkOS docs: https://workos.com/docs
- Stytch B2B docs: https://stytch.com/docs/b2b
- Auth0 Management API: https://auth0.com/docs/api/management/v2
- Scalekit: https://www.scalekit.com/
