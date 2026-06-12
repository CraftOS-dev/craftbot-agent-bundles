---
name: sso-gated-kb-okta-auth0
description: SSO-gated KB — SAML 2.0 / OIDC via Okta, Auth0, Azure AD; SCIM 2.0 provisioning; group-based ACL at section level. Confluence / Notion / Guru / Document360 all SCIM-capable in 2026. Use when KB must be employee-only or partner-restricted.
---

# SSO-gated KB — Okta / Auth0 / Azure AD + SCIM

## When to use

User says "gate KB behind SSO", "Okta integration", "SCIM provisioning", "internal-only docs", "partner KB with restricted access". Reach BEFORE any sensitive content lands on the wiki.

Defer the IdP configuration depth (multi-factor flows, conditional access) to `security-agent`. This skill covers KB-side wiring.

## Setup

```bash
# Okta admin
# CLI optional: pipx install okta-cli
export OKTA_DOMAIN=acme.okta.com
export OKTA_API_TOKEN=...      # API → tokens

# Auth0
export AUTH0_DOMAIN=acme.us.auth0.com
export AUTH0_MGMT_TOKEN=...    # Management API token

# Azure AD via Microsoft Graph
export AZURE_TENANT_ID=...
export AZURE_CLIENT_ID=...
export AZURE_CLIENT_SECRET=...
```

Auth / API key requirements:
- `OKTA_API_TOKEN` — Okta admin → API → Tokens
- `AUTH0_MGMT_TOKEN` — Auth0 Management API
- Azure: client cred app with Directory.ReadWrite.All

## Common recipes

### Recipe 1: Create Okta SAML 2.0 app for KB

```bash
curl -X POST "https://${OKTA_DOMAIN}/api/v1/apps" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"template_saml_2_0",
    "label":"Acme KB (Confluence)",
    "signOnMode":"SAML_2_0",
    "settings":{
      "signOn":{
        "ssoAcsUrl":"https://acme.atlassian.net/login/saml/callback",
        "audience":"https://acme.atlassian.net",
        "recipient":"https://acme.atlassian.net/login/saml/callback",
        "destination":"https://acme.atlassian.net/login/saml/callback",
        "subjectNameIdTemplate":"${user.email}",
        "subjectNameIdFormat":"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
      }
    }
  }'
```

### Recipe 2: OIDC app on Auth0

```bash
curl -X POST "https://${AUTH0_DOMAIN}/api/v2/clients" \
  -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Acme KB (GitBook)",
    "app_type":"regular_web",
    "callbacks":["https://docs.acme.com/auth/callback"],
    "allowed_logout_urls":["https://docs.acme.com"],
    "grant_types":["authorization_code","refresh_token"],
    "jwt_configuration":{"alg":"RS256"}
  }'
```

### Recipe 3: SCIM provisioning — Notion Enterprise

```bash
# Create user
curl -X POST "https://api.notion.com/scim/v2/Users" \
  -H "Authorization: Bearer $NOTION_SCIM_TOKEN" \
  -H "Content-Type: application/scim+json" \
  -d '{
    "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName":"alice@example.com",
    "active":true,
    "emails":[{"value":"alice@example.com","primary":true}],
    "name":{"givenName":"Alice","familyName":"Chen"}
  }'

# Deactivate
curl -X PATCH "https://api.notion.com/scim/v2/Users/$USER_ID" \
  -H "Authorization: Bearer $NOTION_SCIM_TOKEN" \
  -H "Content-Type: application/scim+json" \
  -d '{"schemas":["urn:ietf:params:scim:api:messages:2.0:PatchOp"],"Operations":[{"op":"replace","path":"active","value":false}]}'
```

### Recipe 4: SCIM provisioning — Confluence (Atlassian Guard)

```bash
# Atlassian uses Atlassian Guard (formerly Atlassian Access) for SCIM
curl -X POST "https://api.atlassian.com/scim/directory/${DIRECTORY_ID}/Users" \
  -H "Authorization: Bearer $ATLASSIAN_SCIM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName":"alice@example.com",
    "name":{"givenName":"Alice","familyName":"Chen"},
    "emails":[{"value":"alice@example.com","primary":true}],
    "active":true
  }'
```

### Recipe 5: SCIM groups — push from Okta

In Okta admin: Applications → your KB app → Provisioning → Integration → enable Push Groups. Configure the SCIM connector base URL + token.

### Recipe 6: Confluence space-level access (group)

```bash
# Add a group with VIEW permission to a Space
curl -X POST "https://${SITE}.atlassian.net/wiki/rest/api/space/${SPACE_KEY}/permission" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject":{"type":"group","identifier":"docs-readers"},
    "operation":{"key":"read","target":"space"}
  }'
```

### Recipe 7: Notion teamspace permissions

```bash
# Share teamspace with a SCIM-provisioned group
curl -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"properties":{...}}'   # Permission grants happen via Notion admin UI for SCIM-pushed groups
```

### Recipe 8: Guru collection-level group permission

```bash
curl -X PUT "https://api.getguru.com/api/v1/collections/$COLLECTION_ID/groups/$GROUP_ID" \
  -u "$GURU_USER:$GURU_TOKEN" \
  -d '{"role":"READ_ONLY"}'
```

### Recipe 9: Document360 group / project access

```bash
# Document360 uses "team accounts"; SCIM via Okta/Azure
curl -X POST "https://apihub.document360.io/v2/Teams" \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  -d '{"name":"docs-readers","email":"docs-readers@acme.com"}'
```

### Recipe 10: Static-site KB gated by Cloudflare Access

```bash
# Cloudflare Access policy for docs subdomain
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{
    "name":"Internal docs",
    "domain":"internal-docs.acme.com",
    "type":"self_hosted",
    "session_duration":"24h",
    "policies":[{
      "name":"Employees only",
      "decision":"allow",
      "include":[{"email_domain":{"domain":"acme.com"}}]
    }]
  }'
```

### Recipe 11: Audit log retention

```bash
# Pull Okta system log entries for KB app
curl -G "https://${OKTA_DOMAIN}/api/v1/logs" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  --data-urlencode "filter=eventType eq \"user.session.start\"" \
  --data-urlencode "since=$(date -u -d '90 days ago' +%FT00:00:00Z)" \
  > okta-logs-90d.json
```

### Recipe 12: Just-in-time provisioning fallback

For low-volume SSO without SCIM:

```javascript
// On SAML/OIDC login, create the user if not present
app.post('/auth/callback', async (req, res) => {
  const { email, name } = req.user;
  let user = await db.users.findUnique({ where: { email } });
  if (!user) {
    user = await db.users.create({ data: { email, name, role:'reader' } });
  }
  // ...
});
```

## Examples

### Example 1: Internal Confluence space behind Okta + SCIM

**Goal:** Engineering Space accessible only to Engineering group.

**Steps:**
1. Provision Atlassian Guard.
2. Create Okta SAML app for atlassian.net (Recipe 1).
3. Enable SCIM in Atlassian → Directory (Recipe 4).
4. Push "Engineering" group from Okta.
5. Assign Space permission to "engineering" group (Recipe 6).
6. Audit logs configured for 1-year retention (Recipe 11).

**Result:** Only engineering group sees Engineering Space; deactivation in Okta = revocation in <5 min.

### Example 2: Static MkDocs site gated by Cloudflare Access

**Goal:** Cheap internal-only KB.

**Steps:**
1. Deploy MkDocs to Cloudflare Pages (`internal-docs.acme.com`).
2. Create Access app + policy (Recipe 10).
3. Identity provider: Okta SAML or Google Workspace.
4. Done — no app-side auth code.

**Result:** $0; gated; logs in Cloudflare dashboard.

## Edge cases / gotchas

- **SCIM provisioning ≠ SSO** — both are needed. SSO authenticates; SCIM keeps the user list in sync.
- **Atlassian Guard required** for Atlassian SCIM (paid Standard tier).
- **Notion SCIM** = Enterprise plan only.
- **Guru SCIM** = Standard plan or above.
- **Document360 SAML** = Pro tier+.
- **Group-claim attribute mapping** — Okta sends groups via SAML attribute; receiver must map. Test with a non-admin user.
- **Audit log retention** — 90d Okta default; export to S3 for longer.
- **SP-initiated vs IdP-initiated flow** — many KBs require SP-initiated only; bookmark in IdP dashboard may break.
- **Email format SAML NameID** — most KB platforms expect emailAddress; subjectNameIdTemplate must match.
- **Per-article ACLs** are an antipattern — use SSO groups at section level. Only carve per-article for compliance.
- **JIT vs SCIM** — JIT creates on first login but doesn't deprovision. SCIM both creates and removes.
- **External / contractor access** — usually a separate IdP group; segregate.

## Sources

- Okta SAML: https://developer.okta.com/docs/concepts/saml/
- Okta SCIM: https://developer.okta.com/docs/concepts/scim/
- Auth0 SAML: https://auth0.com/docs/authenticate/protocols/saml
- Microsoft Graph SCIM: https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups
- Atlassian Guard SCIM: https://support.atlassian.com/provisioning-users/docs/configure-user-provisioning-with-scim/
- Notion SCIM: https://www.notion.com/help/provision-users-and-groups-with-scim
- Guru permissions: https://help.getguru.com/en/articles/4951076-collection-and-card-permissions
- Confluence Space permissions: https://support.atlassian.com/confluence-cloud/docs/what-are-confluence-space-permissions/
- Cloudflare Access: https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/
- SCIM 2.0 RFC: https://tools.ietf.org/html/rfc7644
