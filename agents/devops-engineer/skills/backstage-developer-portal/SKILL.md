<!--
Source: https://backstage.io/docs · https://www.cncf.io/projects/backstage/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Backstage Developer Portal

Spotify Backstage (CNCF incubating) — the dominant 2026 internal developer
platform (IDP). Software Catalog (entities-as-code), TechDocs (Markdown +
MkDocs), Software Templates (cookiecutter-style scaffolding), Scaffolder,
and a plugin ecosystem (GitHub, ArgoCD, K8s, Sentry, PagerDuty, ...).
Replaces "spreadsheet of services owned by who".

## When to use

- "Who owns this service?" — search Catalog.
- "How do I create a new service that follows our patterns?" — Software
  Template.
- "Where are the docs for this service?" — TechDocs.
- "What's the health of all my team's services?" — plugins surface ArgoCD
  sync, Sentry errors, PagerDuty incidents in one view.
- Onboarding new engineers: portal is the front door.

Skip when: team < 10 engineers (process > tooling); zero services to
catalog. Use Port / Cortex / OpsLevel as hosted alternatives.

## Setup

```bash
# Scaffold a new Backstage app
npx @backstage/create-app@latest
# Choose project name + DB (sqlite for dev; postgres for prod)
cd my-backstage
yarn install
yarn dev          # http://localhost:3000

# Add plugins
yarn --cwd packages/app add @backstage/plugin-kubernetes
yarn --cwd packages/app add @roadiehq/backstage-plugin-argo-cd
yarn --cwd packages/app add @backstage/plugin-pagerduty

# Production: Deploy to K8s
docker build -f packages/backend/Dockerfile -t myorg/backstage:1.0.0 .
helm repo add backstage https://backstage.github.io/charts
helm upgrade --install backstage backstage/backstage -n backstage --create-namespace -f values.yaml
```

Auth: GitHub OAuth (Recipe 7) or Okta / Google / Microsoft SSO.

## Common recipes

### Recipe 1 — `catalog-info.yaml` (entity registration)

```yaml
# Living next to the service code, in repo root
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: api
  description: Customer-facing API service.
  annotations:
    github.com/project-slug: myorg/api
    argocd/app-name: api
    pagerduty.com/integration-key: ${PD_INT_KEY}
    sentry.io/project-slug: api-prod
    backstage.io/kubernetes-id: api
    backstage.io/techdocs-ref: dir:.
  tags: [python, fastapi, public-api]
  links:
    - { url: "https://api.myorg.com", title: "Production", icon: web }
    - { url: "https://grafana.myorg.com/d/api-overview", title: "Dashboard", icon: dashboard }
spec:
  type: service
  lifecycle: production
  owner: team-platform
  system: customer-experience
  dependsOn: [resource:postgres-prod, component:auth]
  providesApis: [api-rest]
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: api-rest
  description: REST API for customer dashboard.
spec:
  type: openapi
  lifecycle: production
  owner: team-platform
  system: customer-experience
  definition:
    $text: ./openapi.yaml
```

### Recipe 2 — Locations (where to find catalog entities)

```yaml
# app-config.yaml
catalog:
  locations:
    - type: url
      target: https://github.com/myorg/.github/blob/main/all-entities.yaml
    - type: github-discovery
      target: https://github.com/myorg/*/blob/-/catalog-info.yaml
  rules:
    - allow: [Component, System, API, Resource, Domain, User, Group]
```

GitHub Discovery auto-discovers `catalog-info.yaml` across all repos in
the org.

### Recipe 3 — User + Group from GitHub Teams

```yaml
catalog:
  providers:
    githubOrg:
      - id: myorg
        githubUrl: https://github.com
        orgs: [myorg]
        schedule:
          frequency: { hours: 1 }
          timeout: { minutes: 50 }
```

Auto-imports GitHub orgs → Backstage Group + User entities. Ownership
queries (`owner: team-platform`) then resolve.

### Recipe 4 — Software Template (Scaffolder)

```yaml
# template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: python-fastapi-service
  title: Python FastAPI Service
  description: Bootstrap a new prod-grade Python service.
spec:
  owner: team-platform
  type: service
  parameters:
    - title: Service info
      required: [name, owner]
      properties:
        name: { title: Name, type: string, pattern: '^[a-z0-9-]+$' }
        description: { title: Description, type: string }
        owner:
          title: Owner
          type: string
          ui:field: OwnerPicker
          ui:options: { allowedKinds: [Group] }
  steps:
    - id: fetch
      name: Fetch template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}
        defaultBranch: main
        repoVisibility: private
    - id: register
      name: Register in catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'
  output:
    links:
      - { title: Repository, url: ${{ steps.publish.output.remoteUrl }} }
      - { title: Catalog entry, icon: catalog, entityRef: ${{ steps.register.output.entityRef }} }
```

User clicks "Create"; portal scaffolds repo + registers entity in one
flow.

### Recipe 5 — TechDocs (MkDocs + Backstage)

```yaml
# In each repo: docs/index.md, docs/architecture.md, etc.
# mkdocs.yml:
site_name: api
plugins:
  - techdocs-core
nav:
  - Home: index.md
  - Architecture: architecture.md
  - Runbook: runbook.md
```

```yaml
# In catalog-info.yaml metadata:
annotations:
  backstage.io/techdocs-ref: dir:.    # docs live in this repo
```

Backstage renders MkDocs in the portal. Mode: local (dev), recommended
(generate in CI + serve from S3).

### Recipe 6 — Kubernetes plugin (per-service K8s view)

```yaml
# app-config.yaml
kubernetes:
  serviceLocatorMethod: { type: multiTenant }
  clusterLocatorMethods:
    - type: config
      clusters:
        - url: https://prod-eks.myorg.com
          name: prod
          authProvider: serviceAccount
          serviceAccountToken: ${PROD_K8S_TOKEN}
          caData: ${PROD_K8S_CA}
        - url: https://staging-eks.myorg.com
          name: staging
          authProvider: serviceAccount
```

```yaml
# In catalog-info.yaml:
annotations:
  backstage.io/kubernetes-id: api      # or kubernetes-label-selector
```

Component detail page shows pods, deployments, ingresses, events for
matching workloads across clusters.

### Recipe 7 — GitHub OAuth

```yaml
# app-config.yaml
auth:
  providers:
    github:
      production:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
        signIn:
          resolvers:
            - resolver: usernameMatchingUserEntityName
```

Create OAuth App in GitHub: Settings → Developer settings → OAuth Apps →
callback `https://backstage.myorg.com/api/auth/github/handler/frame`.

### Recipe 8 — Production deploy (Helm chart)

```yaml
# values.yaml
backstage:
  image:
    repository: myorg/backstage
    tag: 1.0.0
  replicas: 2
  appConfig:
    app: { baseUrl: https://backstage.myorg.com }
    backend: { baseUrl: https://backstage.myorg.com, listen: { port: 7007 } }
    catalog: { ... }  # paste from app-config.yaml
postgresql:
  enabled: true
  auth:
    database: backstage
    username: backstage
ingress:
  enabled: true
  className: nginx
  host: backstage.myorg.com
  tls: { enabled: true, secretName: backstage-tls }
```

```bash
helm upgrade --install backstage backstage/backstage -f values.yaml -n backstage --create-namespace
```

### Recipe 9 — Useful plugins

| Plugin | Purpose |
|---|---|
| `@roadiehq/backstage-plugin-argo-cd` | ArgoCD sync status per Component |
| `@backstage/plugin-kubernetes` | K8s resources per Component |
| `@backstage/plugin-pagerduty` | active incidents + on-call |
| `@backstage/plugin-sentry` | Sentry errors per Component |
| `@backstage/plugin-github-actions` | Workflows + runs per Component |
| `@backstage/plugin-tech-radar` | Tech radar (adopted/trial/assess/hold) |
| `@backstage/plugin-catalog-graph` | Visualize dependency graph |
| `@backstage/plugin-search` | Cross-portal full-text search |

### Recipe 10 — Backstage CLI

```bash
yarn backstage-cli new --select plugin --option id=my-plugin
yarn backstage-cli versions:bump
yarn backstage-cli config:check
yarn backstage-cli config:print --frontend
yarn backstage-cli repo build               # build all packages
```

### Recipe 11 — Catalog validation in CI

```yaml
# .github/workflows/catalog-validate.yml
- run: |
    npm install -g @backstage/catalog-client
    for f in $(find . -name catalog-info.yaml); do
      backstage-catalog-validate $f
    done
```

OR use Backstage's `entitiesValidator` action.

### Recipe 12 — Plugin development scaffold

```bash
yarn new --select plugin --option id=cost
# Creates plugins/cost/ + integration boilerplate
yarn --cwd plugins/cost start          # standalone dev
```

Custom plugin to surface OpenCost data per Component (link service → cost).

## Examples

### Example 1 — Onboard 50 services in one afternoon

**Goal:** Empty Backstage → 50 cataloged services.

1. Standard `catalog-info.yaml` template (Recipe 1); commit to each repo.
2. Enable GitHub Discovery (Recipe 2) — Backstage auto-pulls every 30 min.
3. Enable GitHub Org provider (Recipe 3) — Users + Groups from teams.
4. Verify in portal → Catalog → ~50 entities + 12 groups.
5. Tag each with `owner`, `system`, `tags` for filtering.

**Result:** Searchable, owned catalog in <4 hours.

### Example 2 — Self-service "new Python service" template

**Goal:** Engineers run a wizard → new repo with prod-grade scaffolding.

1. Author skeleton (`skeleton/` with Dockerfile, manifests, CI, README).
2. Author template.yaml (Recipe 4).
3. Register template in catalog: add `kind: Template` location.
4. Engineer clicks "Create" → Backstage runs steps → repo published.
5. ArgoCD picks up the new manifest in 5 min → service in K8s.

**Result:** From idea to running service in 5 minutes; zero config drift.

## Edge cases / gotchas

- **Backstage upgrade pain**: minor versions change weekly. Use
  `backstage-cli versions:bump`. Pin in `package.json`; test via Renovate.
- **Catalog drift**: entity files diverge from reality if no validation.
  Run Recipe 11 in CI to catch removed annotations.
- **Auth scope**: GitHub OAuth requires `read:org` for group lookups; users
  hit "not authorized" without it.
- **TechDocs builder modes**: `local` builds on portal load (slow); `external`
  generates in CI, serves from S3 (fast). Use `external` in prod.
- **Plugin proxy config**: backstage backend proxies frontend → external
  APIs (Sentry, Datadog). Configure in `app-config.yaml` → `proxy:` block.
- **K8s plugin RBAC**: ServiceAccount must have `get,list,watch` across all
  resources you display. Avoid `cluster-admin` — write a minimal Role.
- **`spec.owner` must reference an existing User or Group entity**.
  Orphaned ownership = compliance violation.
- **Scaffolder template parameters** use react-jsonschema-form syntax;
  custom widgets need plugin work.
- **Database migrations** auto-run on startup with `postgresql` backend;
  pin chart version + back up DB before upgrade.
- **Hosted alternatives**: Port, Cortex, OpsLevel are paid SaaS. Less setup
  but lock-in. Roadie hosts Backstage as a service.
- **Tech radar**: useful but social — define a process for "Adopt" vs "Hold"
  decisions (RFC, ADR), not just plugin clicks.

## Sources

- https://backstage.io/docs — Backstage docs
- https://backstage.io/docs/features/software-catalog/ — Software Catalog
- https://backstage.io/docs/features/software-templates/ — Software Templates
- https://backstage.io/docs/features/techdocs/ — TechDocs
- https://github.com/backstage/community-plugins — Community plugins
- https://github.com/backstage/charts — Helm chart
- https://www.cncf.io/projects/backstage/ — CNCF Backstage page
- https://www.getport.io/ — Port (hosted alt)
- https://www.cortex.io/ — Cortex (hosted alt)
- https://opslevel.com/ — OpsLevel (hosted alt)
- https://roadie.io/ — Roadie (managed Backstage)
- https://backstage.spotify.com/ — Backstage at Spotify
