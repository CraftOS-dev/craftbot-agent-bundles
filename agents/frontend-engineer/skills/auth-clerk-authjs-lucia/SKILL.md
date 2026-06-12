<!--
Source: https://clerk.com/docs · https://authjs.dev/ · https://lucia-auth.com/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Auth — Clerk, Auth.js v5, Lucia v3

Three viable auth paths in 2026: **Clerk** (paid SaaS, drop-in components,
fastest), **Auth.js v5** (OSS, framework-agnostic, edge-ready), **Lucia v3**
(lightweight library + your DB). This skill picks the right one per situation
and documents the canonical setup.

## When to use

- Greenfield Next 15 app with auth requirements
- Adding auth to an existing app
- Migrating off NextAuth v4 (must move to Auth.js v5)
- Need MFA / org / RBAC out of the box → Clerk
- Trigger phrases: "auth", "authentication", "login", "OAuth", "session",
  "Clerk", "Auth.js", "NextAuth", "Lucia", "MFA", "passkey"

## Decision tree

| Need | Pick |
|---|---|
| Fastest TTV; budget for SaaS | **Clerk** ($25/mo+, drop-in UI, MFA, orgs) |
| OSS, framework-agnostic, edge | **Auth.js v5** |
| OSS, lightweight, fully custom | **Lucia v3** |
| Enterprise SSO/SCIM | WorkOS |
| Already on Supabase | Supabase Auth |

## Setup — Clerk

```bash
pnpm add @clerk/nextjs
```

```ts
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function Layout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en"><body>{children}</body></html>
    </ClerkProvider>
  );
}
```

```ts
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtected = createRouteMatcher(["/dashboard(.*)", "/settings(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtected(req)) await auth.protect();
});

export const config = { matcher: ["/((?!_next|.*\\..*).*)"] };
```

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

Auth / API keys:
- Sign up at https://clerk.com — free tier: 10,000 MAUs, basic features.
- Paid: from $25/mo for MFA, orgs, branding.

## Setup — Auth.js v5

```bash
pnpm add next-auth@beta @auth/prisma-adapter   # or @auth/drizzle-adapter
pnpm dlx auth secret                            # generates AUTH_SECRET
```

```ts
// auth.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHub({ clientId: process.env.GITHUB_ID, clientSecret: process.env.GITHUB_SECRET }),
    Google({ clientId: process.env.GOOGLE_ID, clientSecret: process.env.GOOGLE_SECRET }),
  ],
  session: { strategy: "database" },
  callbacks: {
    async session({ session, user }) {
      session.user.id = user.id;
      return session;
    },
  },
});
```

```ts
// app/api/auth/[...nextauth]/route.ts
export { GET, POST } from "@/auth";
```

```ts
// middleware.ts
export { auth as middleware } from "@/auth";
export const config = { matcher: ["/((?!api|_next|.*\\..*).*)"] };
```

```bash
# .env
AUTH_SECRET=...                              # `pnpm dlx auth secret`
GITHUB_ID=...
GITHUB_SECRET=...
DATABASE_URL=postgres://...
```

Free / OSS — keys are from each OAuth provider.

## Setup — Lucia v3

```bash
pnpm add lucia @lucia-auth/adapter-prisma oslo
```

```ts
// src/lib/auth.ts
import { Lucia } from "lucia";
import { PrismaAdapter } from "@lucia-auth/adapter-prisma";
import { prisma } from "./prisma";

const adapter = new PrismaAdapter(prisma.session, prisma.user);

export const lucia = new Lucia(adapter, {
  sessionCookie: {
    expires: false,
    attributes: { secure: process.env.NODE_ENV === "production" },
  },
  getUserAttributes: (data) => ({ email: data.email, name: data.name }),
});

declare module "lucia" {
  interface Register {
    Lucia: typeof lucia;
    DatabaseUserAttributes: { email: string; name: string | null };
  }
}
```

Free / OSS.

## Common recipes — Clerk

### Recipe 1 — Drop-in components

```tsx
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
  return <SignIn appearance={{ elements: { card: "shadow-xl" } }} />;
}
```

```tsx
// Any header
import { SignedIn, SignedOut, UserButton, SignInButton } from "@clerk/nextjs";

<header>
  <SignedIn><UserButton /></SignedIn>
  <SignedOut><SignInButton mode="modal" /></SignedOut>
</header>
```

### Recipe 2 — Server-side user

```ts
// app/dashboard/page.tsx
import { auth, currentUser } from "@clerk/nextjs/server";

export default async function Dashboard() {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");
  const user = await currentUser();
  return <h1>Hello, {user?.firstName}</h1>;
}
```

### Recipe 3 — Org-based access control

```ts
const { has } = await auth();
if (!has({ permission: "org:billing:manage" })) {
  return new Response("Forbidden", { status: 403 });
}
```

### Recipe 4 — Webhook to sync user → app DB

```ts
// app/api/clerk-webhook/route.ts
import { Webhook } from "svix";

export async function POST(req: Request) {
  const payload = await req.text();
  const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!);
  let evt: any;
  try {
    evt = wh.verify(payload, Object.fromEntries(req.headers));
  } catch {
    return new Response("Bad signature", { status: 400 });
  }

  if (evt.type === "user.created") {
    await db.user.create({ data: { clerkId: evt.data.id, email: evt.data.email_addresses[0].email_address } });
  }
  return new Response("ok");
}
```

## Common recipes — Auth.js v5

### Recipe 5 — Sign-in page

```tsx
"use client";
import { signIn } from "next-auth/react";

<button onClick={() => signIn("github", { callbackUrl: "/dashboard" })}>
  Sign in with GitHub
</button>
```

### Recipe 6 — Server-side auth check

```ts
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function Dashboard() {
  const session = await auth();
  if (!session?.user) redirect("/sign-in");
  return <p>Welcome, {session.user.name}</p>;
}
```

### Recipe 7 — Protect a route via middleware

```ts
// middleware.ts
import { auth } from "@/auth";

export default auth((req) => {
  if (!req.auth && req.nextUrl.pathname.startsWith("/dashboard")) {
    return Response.redirect(new URL("/sign-in", req.url));
  }
});
```

### Recipe 8 — Credentials provider (email + password)

```ts
import Credentials from "next-auth/providers/credentials";

providers: [
  Credentials({
    credentials: { email: {}, password: {} },
    authorize: async (creds) => {
      const user = await db.user.findUnique({ where: { email: creds.email as string } });
      if (!user) return null;
      const valid = await bcrypt.compare(creds.password as string, user.passwordHash);
      return valid ? { id: user.id, email: user.email } : null;
    },
  }),
],
session: { strategy: "jwt" },                  // must be JWT for credentials provider
```

## Common recipes — Lucia v3

### Recipe 9 — Sign-up

```ts
// app/api/sign-up/route.ts
import { hash } from "@node-rs/argon2";
import { lucia } from "@/lib/auth";
import { generateId } from "lucia";

export async function POST(req: Request) {
  const { email, password } = await req.json();
  const passwordHash = await hash(password, { memoryCost: 19_456, timeCost: 2, outputLen: 32, parallelism: 1 });
  const userId = generateId(15);
  await db.user.create({ data: { id: userId, email, passwordHash } });
  const session = await lucia.createSession(userId, {});
  const cookie = lucia.createSessionCookie(session.id);
  return new Response(null, { headers: { "Set-Cookie": cookie.serialize() } });
}
```

### Recipe 10 — Auth check

```ts
// src/lib/auth-helpers.ts
import { lucia } from "./auth";
import { cookies } from "next/headers";

export async function getUser() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(lucia.sessionCookieName)?.value;
  if (!sessionId) return null;
  const { session, user } = await lucia.validateSession(sessionId);
  if (session && session.fresh) {
    const cookie = lucia.createSessionCookie(session.id);
    cookieStore.set(cookie.name, cookie.value, cookie.attributes);
  }
  return user;
}
```

## Examples

### Example 1: New Next 15 SaaS → Clerk

```bash
pnpm dlx create-next-app@latest my-saas --typescript --app --tailwind
cd my-saas
pnpm add @clerk/nextjs
# Add .env keys, wrap in ClerkProvider, add middleware.ts (Setup section)
pnpm dev
# /sign-in route works out of the box
```

### Example 2: OSS app → Auth.js v5 + Prisma

```bash
pnpm add next-auth@beta @auth/prisma-adapter
pnpm dlx auth secret > .env  # or copy to .env.local
# Migrate schema:
pnpm dlx prisma migrate dev --name add-auth-tables
# Wire auth.ts (Setup section)
# Add GitHub OAuth app, set GITHUB_ID/SECRET
pnpm dev
```

## Edge cases / gotchas

- **NextAuth v4 → Auth.js v5** is breaking — config moves to `auth.ts`, env
  vars renamed (`NEXTAUTH_*` → `AUTH_*`), middleware signature changed.
- **Clerk needs both keys** — `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (client) AND
  `CLERK_SECRET_KEY` (server). Without both, requests fail silently.
- **Session strategy `"database"` vs `"jwt"`** — JWT is required for the
  credentials provider; database is preferred for OAuth-only setups.
- **Lucia v3** removed `@oslojs/*` integrations — use `@node-rs/argon2` or
  `@oslojs/crypto` directly.
- **Edge runtime** — Clerk supports it; Auth.js requires using the
  `@auth/core` adapter directly, not the Next adapter (some adapters don't
  work in edge). Lucia works on edge with the right adapter.
- **OAuth callback URLs** must match exactly — `https://example.com/api/auth/
  callback/github` (Auth.js) or `/sso-callback` (Clerk).
- **Cookies + cross-domain** — set `domain: ".example.com"` if you need
  subdomain sharing.
- **CSRF** — Auth.js & Clerk handle it; if rolling your own (Lucia), add a
  CSRF token check on mutations.
- **MFA / Passkeys** — Clerk includes both; Auth.js v5 supports WebAuthn via
  the WebAuthn adapter (beta).
- **Banking-grade auth** is out of scope for any of these — use WorkOS / Auth0
  Enterprise / Okta.
- **Local dev** with OAuth — use `ngrok` to expose `localhost:3000` for
  callbacks the OAuth provider can reach.

## Sources

- [Clerk docs](https://clerk.com/docs)
- [Clerk Next.js quickstart](https://clerk.com/docs/quickstarts/nextjs)
- [Auth.js v5 docs](https://authjs.dev/)
- [Auth.js v5 migration](https://authjs.dev/getting-started/migrating-to-v5)
- [Lucia v3 docs](https://lucia-auth.com/)
- [Lucia v3 Next.js guide](https://lucia-auth.com/tutorials/username-and-password/nextjs-app)
- [WorkOS docs](https://workos.com/docs)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Pilcrow — Lucia author guides](https://github.com/pilcrowOnPaper) — Lucia + best practices
- [Auth comparison (Theo, 2025)](https://www.youtube.com/@t3dotgg) — recurring auth videos
