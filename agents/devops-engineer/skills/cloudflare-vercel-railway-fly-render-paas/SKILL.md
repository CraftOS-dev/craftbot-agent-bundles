<!--
Source: https://developers.cloudflare.com/ · https://vercel.com/docs · https://docs.railway.com/ · https://fly.io/docs/ · https://render.com/docs
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Cloudflare / Vercel / Railway / Fly.io / Render — Modern PaaS

DNS + CDN + serverless + container PaaS deployment patterns. Choose by
workload: **Cloudflare** (DNS+CDN+WAF+Workers+Pages+R2+D1+Zero-Trust;
default for edge), **Vercel** (Next.js + frontend), **Railway** (monorepo +
DB-included), **Fly.io** (global edge + Fly Machines), **Render** (low-config
containerized). Skip when K8s is the right tool.

## When to use

- Frontend / SSG / Next.js → Vercel.
- Static site + edge functions → Cloudflare Pages + Workers.
- Monorepo full-stack (app + Postgres + Redis) → Railway.
- Global multi-region containers → Fly.io.
- Low-config container PaaS → Render.
- DNS + CDN + WAF + DDoS protection → Cloudflare (no matter where the
  origin is).

Skip when: workload needs StatefulSet/PVC/complex networking → K8s; needs
multi-cloud orchestration → Terraform + K8s; has compliance constraints
PaaS providers don't meet.

## Setup

```bash
# Cloudflare
brew install cloudflare/cloudflare/wrangler           # Workers + Pages
brew install cloudflare/cloudflare/cloudflared        # tunnels
wrangler login                                          # OAuth

# Vercel
npm install -g vercel
vercel login

# Railway
npm install -g @railway/cli
railway login

# Fly.io
brew install flyctl
flyctl auth login

# Render
brew install render/render/render
render login

# Cloudflare Terraform provider
# Add to versions.tf:
# cloudflare = { source = "cloudflare/cloudflare", version = "~> 4.40" }
```

API tokens:
- Cloudflare: My Profile → API Tokens → "Edit Cloudflare Workers" template
- Vercel: Settings → Tokens
- Railway: `railway login` opens browser, generates token in `~/.config/railway/`
- Fly.io: `flyctl auth token`
- Render: Account → API Keys

## Common recipes

### Recipe 1 — Cloudflare DNS + CDN (via Terraform)

```hcl
provider "cloudflare" { api_token = var.cf_api_token }

data "cloudflare_zone" "myorg" { name = "myorg.com" }

resource "cloudflare_record" "api" {
  zone_id = data.cloudflare_zone.myorg.id
  name    = "api"
  type    = "CNAME"
  value   = "api.myorg.eks.aws"          # origin
  proxied = true                           # orange-cloud = CDN + WAF
  ttl     = 1
}

resource "cloudflare_ruleset" "rate_limit" {
  zone_id = data.cloudflare_zone.myorg.id
  name    = "API rate limit"
  kind    = "zone"
  phase   = "http_ratelimit"
  rules {
    action      = "block"
    description = "Block over 100 req/min per IP to /api/*"
    expression  = "(http.request.uri.path matches \"^/api/\")"
    ratelimit {
      characteristics = ["ip.src"]
      period          = 60
      requests_per_period = 100
      mitigation_timeout  = 600
    }
  }
}
```

### Recipe 2 — Cloudflare Workers (edge functions)

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/api/health") {
      return new Response(JSON.stringify({ ok: true }), {
        headers: { "Content-Type": "application/json" },
      });
    }
    return new Response("Not found", { status: 404 });
  },
} satisfies ExportedHandler<Env>;
```

```toml
# wrangler.toml
name = "api-edge"
main = "src/index.ts"
compatibility_date = "2025-01-01"
workers_dev = true

[[routes]]
pattern = "api.myorg.com/*"
zone_name = "myorg.com"

[[d1_databases]]
binding = "DB"
database_name = "prod"
database_id = "abc-123"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "myorg-assets"
```

```bash
wrangler dev                       # local
wrangler deploy                    # to prod
wrangler tail                       # live log
wrangler d1 execute prod --command "CREATE TABLE users (id INTEGER PRIMARY KEY)"
wrangler r2 object put myorg-assets/img.png --file=./img.png
```

### Recipe 3 — Cloudflare Pages (static + SSR)

```bash
# Connect via git: Cloudflare Dashboard → Pages → Create → Git
# OR CLI deploy:
cd my-app/
npm run build
wrangler pages deploy dist --project-name=my-app --branch=main
```

```bash
wrangler pages project list
wrangler pages project create my-app --production-branch=main
wrangler pages deployment list --project-name=my-app
```

### Recipe 4 — Cloudflare Zero-Trust tunnel

```bash
cloudflared tunnel create my-app
cloudflared tunnel route dns my-app app.internal.myorg.com
cloudflared tunnel run my-app           # forwards to localhost:8080 by default
```

No inbound port; tunnel registers outbound to Cloudflare edge. ZeroTrust
policies gate access.

### Recipe 5 — Vercel deploy (Next.js)

```bash
vercel link              # link local dir to a Vercel project
vercel env add DATABASE_URL production
vercel build              # local build matching Vercel env
vercel deploy --prod      # promote build to prod
vercel logs <deployment-url>
vercel rollback           # to previous prod deployment
```

```json
// vercel.json
{
  "buildCommand": "next build",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1", "fra1"],
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://api.myorg.com/$1" }
  ]
}
```

### Recipe 6 — Railway (monorepo + DB)

```bash
railway login
railway init                     # creates project
railway link                      # link cwd to project
railway add                       # add service (Postgres, Redis, etc.)
railway up                        # deploy from local
railway logs --service api
railway run "python migrate.py"   # exec in service env
railway variables                  # show env vars
railway domain                     # generate myproject.up.railway.app
```

```toml
# railway.toml (in repo root)
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 10
restartPolicyType = "ON_FAILURE"
numReplicas = 2
```

### Recipe 7 — Fly.io (global containers)

```bash
flyctl launch                     # creates fly.toml + app
flyctl deploy
flyctl scale count 3 --region iad,sfo,fra
flyctl logs
flyctl ssh console -a my-app
flyctl postgres create -n my-db   # managed PG
flyctl postgres attach my-db --app my-app
flyctl secrets set DATABASE_URL=$DB_URL
```

```toml
# fly.toml
app = "my-app"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"
  [[services.ports]]
    handlers = ["http", "tls"]
    port = 443
  [services.concurrency]
    type = "connections"
    hard_limit = 200
    soft_limit = 100

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Recipe 8 — Render (low-config)

```bash
render services list
render deploys list --service-id srv-abc
render env get --service-id srv-abc
render shell --service-id srv-abc
```

```yaml
# render.yaml (Blueprint — IaC for Render)
services:
  - type: web
    name: api
    runtime: docker
    repo: https://github.com/myorg/api
    branch: main
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
    autoDeploy: true
    plan: standard
    envVars:
      - { key: DATABASE_URL, fromDatabase: { name: prod-db, property: connectionString } }
    scaling:
      minInstances: 2
      maxInstances: 10
      targetCPUPercent: 70

databases:
  - name: prod-db
    plan: standard
    postgresMajorVersion: 16
    region: ohio
```

### Recipe 9 — Choose by workload

| Workload | Best PaaS | Why |
|---|---|---|
| Next.js / React frontend | Vercel | First-class framework support; ISR; image opt |
| Static site + edge code | Cloudflare Pages | $0 for huge traffic; Workers free tier |
| Monorepo full-stack (Python/Go + Postgres) | Railway | Good monorepo support; DB plug-in |
| Global multi-region container | Fly.io | Anycast TCP; Fly Machines fast cold start |
| Low-config Docker container | Render | Simpler than K8s; managed Postgres/Redis |
| API + heavy WAF/DDoS | Cloudflare in front of any of above | Best-in-class L7 protection |

### Recipe 10 — Multi-PaaS pattern

Front-of-stack: Cloudflare DNS + WAF + CDN.
Origin: Vercel (frontend) + Fly.io (API) + Railway (background jobs).

```hcl
# Cloudflare DNS pointing to multi-origin
resource "cloudflare_record" "web" {
  zone_id = data.cloudflare_zone.myorg.id
  name    = "@"
  type    = "CNAME"
  value   = "cname.vercel-dns.com"
  proxied = true
}

resource "cloudflare_record" "api" {
  zone_id = data.cloudflare_zone.myorg.id
  name    = "api"
  type    = "CNAME"
  value   = "my-app.fly.dev"
  proxied = true
}
```

### Recipe 11 — Workers KV / D1 / R2 (Cloudflare data plane)

```bash
# KV (key-value store)
wrangler kv:namespace create SESSIONS
wrangler kv:key put --binding=SESSIONS "user:123" "session-data"

# D1 (SQLite at edge)
wrangler d1 create prod
wrangler d1 execute prod --command "SELECT * FROM users LIMIT 5"
wrangler d1 backup create prod
wrangler d1 backup restore prod <backup-id>

# R2 (S3-compatible object storage; egress-free)
wrangler r2 bucket create assets
wrangler r2 object put assets/banner.png --file=banner.png
aws s3 ls --endpoint-url=https://<accountid>.r2.cloudflarestorage.com s3://assets/
```

### Recipe 12 — Vercel env per branch (preview deploys)

```bash
vercel env add SENTRY_DSN preview         # only on preview deployments
vercel env add DATABASE_URL production    # prod only
vercel env add STAGE preview production development
```

PR opens → Vercel deploys to a preview URL with the preview env vars.

## Examples

### Example 1 — Stand up landing page on Cloudflare Pages

**Goal:** Static site at `marketing.myorg.com`, free tier.

1. `cd landing/ && npm run build`.
2. `wrangler pages project create marketing --production-branch=main`.
3. `wrangler pages deploy dist --project-name=marketing --branch=main`.
4. In Cloudflare DNS: CNAME `marketing` → `marketing.pages.dev`, proxied.
5. Custom domain in Pages settings.

**Result:** SSL + CDN + DDoS protection; $0 cost.

### Example 2 — Add Cloudflare WAF to existing AWS-hosted API

**Goal:** Add L7 protection without moving origin.

1. NS records: `dig myorg.com NS` should point to Cloudflare.
2. Create CNAME `api.myorg.com` → `api.myorg.eks.aws`, proxied = ON.
3. Page Rule: `api.myorg.com/*` → Cache Level Bypass (don't cache APIs).
4. WAF Custom Rule: block `(http.request.method == "POST") and not (cf.bot_management.score gt 30)`.
5. Rate limit: 100 req/min/IP on `/api/login` (Recipe 1).

**Result:** AWS origin still serves; Cloudflare filters bots + abuse.

## Edge cases / gotchas

- **Cloudflare proxy (orange cloud) breaks SSH / non-HTTP**. Use gray
  cloud (unproxied) for SSH/SMTP/etc. records.
- **Cloudflare 100-second timeout** on Free/Pro plans for long-running
  requests through proxy. Use Enterprise or WebSocket workaround.
- **Vercel function 10s timeout** on Hobby tier; 60s on Pro; 900s on
  Enterprise. Long jobs need queue + worker.
- **Railway 100 GB egress free** then $0.10/GB. Watch high-bandwidth
  workloads.
- **Fly Machines cold start**: ~2-5s for image pull on first boot.
  Use `min_machines_running = 1` in `fly.toml` to keep warm.
- **Render's free tier sleeps after 15 min** of inactivity. Paid plan for
  always-on.
- **Workers free tier**: 100k req/day, 10ms CPU each. Paid: $5/mo for 10M.
  KV reads 100k/day free.
- **D1 is per-region**: writes go to primary region; reads from any.
  Latency for non-primary writes.
- **R2 has no egress charges**, but operations (puts/gets) cost.
  Cheaper than S3 for serve-heavy workloads.
- **Vercel Edge vs Node.js runtime**: Edge functions can't use Node APIs
  (fs, child_process). Most npm packages don't work in Edge runtime.
- **Cloudflare Argo Smart Routing** = $5/mo + $0.10/GB; can shave 30%
  latency on long paths.
- **Cloudflared tunnel max throughput** ~1 Gbps per connection; use multiple
  tunnels for bursting.

## Sources

- https://developers.cloudflare.com/ — Cloudflare docs root
- https://developers.cloudflare.com/workers/ — Workers
- https://developers.cloudflare.com/pages/ — Pages
- https://developers.cloudflare.com/r2/ — R2
- https://developers.cloudflare.com/d1/ — D1
- https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ — Tunnels
- https://vercel.com/docs — Vercel
- https://docs.railway.com/ — Railway
- https://fly.io/docs/ — Fly.io
- https://render.com/docs — Render
- https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs — Cloudflare TF provider
- https://blog.cloudflare.com/r2-ga/ — R2 GA post
