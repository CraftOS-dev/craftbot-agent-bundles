<!--
Source: https://developers.cloudflare.com/workers/ · https://hono.dev/ · https://docs.partykit.io/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Cloudflare Workers — Edge functions, Pages, Hono, PartyKit

Cloudflare Workers (V8 isolates) are the SOTA edge runtime in 2026 — sub-50ms
cold starts globally, generous free tier, KV/D1/R2/Durable Objects bundled.
Hono is the modern lightweight web framework that runs on Workers (and Vercel,
Bun, Deno, Node). PartyKit layers multiplayer/real-time on top of Durable Objects.

## When to use

- Edge API for a frontend (geolocation, A/B, request rewrites)
- Hosting a Next.js / Astro / Remix app on Cloudflare Pages
- Stateful edge (auth sessions in KV, SQLite via D1, blobs in R2)
- Multiplayer / WebSockets (PartyKit on Durable Objects)
- Trigger phrases: "Cloudflare Workers", "edge", "wrangler", "Hono",
  "PartyKit", "KV", "D1", "R2", "Durable Objects", "Cloudflare Pages"

## Setup

```bash
# Wrangler (Cloudflare CLI) — global or per-project
pnpm add -D wrangler

# Authenticate (opens browser)
pnpm dlx wrangler login

# New Worker
pnpm dlx wrangler init my-worker --type=ts

# Hono Workers template
pnpm create hono@latest my-api -- --template=cloudflare-workers

# PartyKit template
pnpm dlx partykit@latest init my-party
```

Verify: `pnpm dlx wrangler --version` → 3.x.

Auth / API key requirements:
- `CLOUDFLARE_API_TOKEN` — at https://dash.cloudflare.com/profile/api-tokens
  (free Workers tier: 100k req/day, no card required)

## Common recipes

### Recipe 1 — Minimal Worker

```ts
// src/index.ts
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/health") return new Response("ok");
    return new Response("Hello from the edge", { headers: { "content-type": "text/plain" } });
  },
} satisfies ExportedHandler<Env>;
```

```toml
# wrangler.toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2026-06-01"
compatibility_flags = ["nodejs_compat"]   # only if you need Node API shims

[observability]
enabled = true
```

```bash
pnpm dlx wrangler dev               # local dev on :8787 (Miniflare V3)
pnpm dlx wrangler deploy            # publish to *.workers.dev
```

### Recipe 2 — Hono router with bindings

```ts
// src/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

type Bindings = {
  DB: D1Database;
  CACHE: KVNamespace;
  BUCKET: R2Bucket;
};

const app = new Hono<{ Bindings: Bindings }>();
app.use("*", logger());
app.use("/api/*", cors({ origin: "https://example.com", credentials: true }));

app.get("/api/posts/:id", async (c) => {
  const id = c.req.param("id");
  const cached = await c.env.CACHE.get(`post:${id}`, "json");
  if (cached) return c.json(cached);

  const post = await c.env.DB.prepare("SELECT * FROM posts WHERE id = ?").bind(id).first();
  if (!post) return c.notFound();

  await c.env.CACHE.put(`post:${id}`, JSON.stringify(post), { expirationTtl: 300 });
  return c.json(post);
});

app.post("/api/posts", async (c) => {
  const body = await c.req.json<{ title: string; body: string }>();
  const result = await c.env.DB.prepare("INSERT INTO posts (title, body) VALUES (?, ?) RETURNING *")
    .bind(body.title, body.body)
    .first();
  return c.json(result, 201);
});

export default app;
```

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-app"
database_id = "abc-123-..."           # from `wrangler d1 create my-app`

[[kv_namespaces]]
binding = "CACHE"
id = "..."                            # from `wrangler kv namespace create CACHE`

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-blobs"
```

### Recipe 3 — D1 (SQLite at the edge)

```bash
pnpm dlx wrangler d1 create my-app
# Add the returned binding to wrangler.toml

# Apply schema
pnpm dlx wrangler d1 execute my-app --file=./schema.sql

# Local dev DB
pnpm dlx wrangler d1 execute my-app --local --file=./schema.sql

# Query
pnpm dlx wrangler d1 execute my-app --command="SELECT * FROM posts LIMIT 5"
```

```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
```

### Recipe 4 — KV (key-value cache)

```bash
pnpm dlx wrangler kv namespace create CACHE
pnpm dlx wrangler kv namespace create CACHE --preview   # for `wrangler dev`
```

```ts
await c.env.CACHE.put("user:123", JSON.stringify(user), { expirationTtl: 3600 });
const cached = await c.env.CACHE.get("user:123", "json");
await c.env.CACHE.delete("user:123");
```

### Recipe 5 — R2 (S3-compatible blob)

```bash
pnpm dlx wrangler r2 bucket create my-uploads
```

```ts
app.put("/api/upload/:key", async (c) => {
  const key = c.req.param("key");
  await c.env.BUCKET.put(key, c.req.raw.body!, {
    httpMetadata: { contentType: c.req.header("content-type") ?? "application/octet-stream" },
  });
  return c.json({ key });
});

app.get("/api/files/:key", async (c) => {
  const obj = await c.env.BUCKET.get(c.req.param("key"));
  if (!obj) return c.notFound();
  return new Response(obj.body, {
    headers: { "content-type": obj.httpMetadata?.contentType ?? "application/octet-stream" },
  });
});
```

### Recipe 6 — Durable Object (single-instance, strongly consistent)

```ts
// src/counter.ts
export class Counter {
  state: DurableObjectState;
  constructor(state: DurableObjectState) { this.state = state; }

  async fetch(req: Request): Promise<Response> {
    let value = (await this.state.storage.get<number>("count")) ?? 0;
    const url = new URL(req.url);
    if (url.pathname === "/increment") value++;
    await this.state.storage.put("count", value);
    return new Response(JSON.stringify({ value }), { headers: { "content-type": "application/json" } });
  }
}
```

```toml
# wrangler.toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

```ts
// In main worker
const id = env.COUNTER.idFromName(c.req.param("room"));
const stub = env.COUNTER.get(id);
return stub.fetch(new Request("https://internal/increment"));
```

### Recipe 7 — Cloudflare Pages (deploy a static site)

```bash
pnpm build                            # produces ./dist or ./out
pnpm dlx wrangler pages deploy ./dist
```

Or wire to git:

```bash
pnpm dlx wrangler pages project create my-site
# Then connect via dash.cloudflare.com → Pages → connect to git
```

### Recipe 8 — Next.js on Cloudflare Pages

```bash
pnpm add -D @cloudflare/next-on-pages
# Add to package.json scripts:
#   "build:cf": "next build && npx @cloudflare/next-on-pages"
pnpm build:cf
pnpm dlx wrangler pages deploy .vercel/output/static
```

Or for full SSR support: use `@opennextjs/cloudflare`.

### Recipe 9 — PartyKit (multiplayer)

```ts
// src/server.ts
import type * as Party from "partykit/server";

export default class Chat implements Party.Server {
  constructor(readonly room: Party.Room) {}

  onConnect(conn: Party.Connection) {
    this.room.broadcast(JSON.stringify({ type: "joined", id: conn.id }), [conn.id]);
  }

  onMessage(message: string, sender: Party.Connection) {
    this.room.broadcast(JSON.stringify({ from: sender.id, text: message }));
  }
}
```

```ts
// In a React client
import usePartySocket from "partysocket/react";

const ws = usePartySocket({
  host: "my-party.alice.partykit.dev",
  room: "lobby",
  onMessage: (e) => setMessages((m) => [...m, JSON.parse(e.data)]),
});

ws.send("Hello!");
```

```bash
pnpm dlx partykit dev
pnpm dlx partykit deploy
```

### Recipe 10 — Cron triggers

```ts
export default {
  async scheduled(event: ScheduledEvent, env: Env) {
    await env.CACHE.delete("homepage-data");
    // ... regenerate
  },
  async fetch(req, env) { /* ... */ },
} satisfies ExportedHandler<Env>;
```

```toml
# wrangler.toml
[triggers]
crons = ["0 * * * *"]                # every hour
```

### Recipe 11 — Local dev with real bindings

```bash
pnpm dlx wrangler dev --local --persist-to=.wrangler/state
```

`--local` runs Miniflare locally with real KV/D1/R2 emulation; `--persist-to`
keeps state between restarts.

## Examples

### Example 1: API at the edge, frontend on Vercel

1. `pnpm create hono@latest my-api --template cloudflare-workers`
2. Add D1 binding (Recipe 3)
3. `pnpm dlx wrangler deploy` → `https://my-api.alice.workers.dev`
4. Set `NEXT_PUBLIC_API_URL=https://my-api.alice.workers.dev` on Vercel
5. Frontend fetches the edge API; sub-50ms p50 globally

### Example 2: Multiplayer game with PartyKit

1. `pnpm dlx partykit init game` → scaffolds server + client
2. Implement `onMessage` (Recipe 9)
3. React client uses `usePartySocket` hook
4. `pnpm dlx partykit deploy` — provisions a Durable Object globally

## Edge cases / gotchas

- **Workers have no filesystem** — `fs` doesn't exist. Bundle assets or use R2.
- **CPU time limit** — Free tier: 10ms; Paid: 30s. Long-running work belongs in
  a Durable Object alarm or a queue.
- **Memory cap is 128 MB** — fine for HTTP but tight for image processing.
- **`nodejs_compat`** flag enables `node:buffer`, `node:crypto`, etc. — add to
  `wrangler.toml` if libraries depend on Node APIs.
- **D1 is SQLite** — no FOR UPDATE locks; use `BEGIN IMMEDIATE` for write
  transactions. Plan for eventual consistency on replicas.
- **KV writes are eventually consistent** (~60s globally). Reads from the
  region that wrote are immediate; other regions may lag.
- **Durable Objects** are single-instance — perfect for a chat room, bad for
  shared global counter (use D1 + atomic update instead).
- **`wrangler.toml` env vars are public** — never commit secrets there. Use
  `wrangler secret put SECRET_NAME` for secrets.
- **Hot reload in dev** is fast but doesn't restart Durable Objects state —
  set `--persist-to` or test with fresh runs.
- **PartyKit uses Cloudflare Durable Objects** under the hood — same limits.
- **Cloudflare Pages adapter** for Next.js has incomplete feature parity —
  some Server Actions / middleware quirks. Test thoroughly before committing.
- **WebSocket connections** count against the free 100k req/day limit per
  message — Durable Objects bill separately.

## Sources

- [Cloudflare Workers docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [D1 docs](https://developers.cloudflare.com/d1/)
- [KV docs](https://developers.cloudflare.com/kv/)
- [R2 docs](https://developers.cloudflare.com/r2/)
- [Durable Objects](https://developers.cloudflare.com/durable-objects/)
- [Hono docs](https://hono.dev/)
- [PartyKit docs](https://docs.partykit.io/)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [@cloudflare/next-on-pages](https://github.com/cloudflare/next-on-pages)
- [Cloudflare Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing) — free tier limits
