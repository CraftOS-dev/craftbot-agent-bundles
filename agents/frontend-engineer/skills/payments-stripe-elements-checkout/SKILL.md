<!--
Source: https://docs.stripe.com/payments/checkout · https://docs.stripe.com/payments/payment-element
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Payments — Stripe Elements + Checkout + Connect

Stripe is the standard for web payments in 2026. **Checkout** is the hosted
flow (simplest, PCI-DSS off your plate). **Elements + Payment Intents** give
you inline custom UX. **Connect** is for marketplaces. Webhooks must be
signature-verified. Always use Stripe test mode for development.

## When to use

- Need to accept payments (subscriptions, one-time, marketplace)
- Migrating off Paddle / Lemon Squeezy
- Adding subscription billing to a Next 15 app
- Webhook signature verification
- Trigger phrases: "Stripe", "payment", "checkout", "subscription", "Elements",
  "Payment Intents", "webhook", "Connect"

## Setup

```bash
pnpm add stripe @stripe/stripe-js @stripe/react-stripe-js

# Stripe CLI for webhook forwarding in dev
brew install stripe/stripe-cli/stripe        # macOS
# or scoop install stripe                    # Windows
# or pnpm dlx stripe-cli@latest              # one-off
```

```bash
stripe login                                 # opens browser
```

Auth / API key requirements:
- `STRIPE_SECRET_KEY` — `sk_test_...` for test mode (free); `sk_live_...` for
  production. Get from https://dashboard.stripe.com/apikeys.
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` — `pk_test_...` / `pk_live_...`.
- `STRIPE_WEBHOOK_SECRET` — `whsec_...` per webhook endpoint.

Free for test mode; live mode requires verified business account + processing
fees (2.9% + $0.30 typical).

## Common recipes

### Recipe 1 — Stripe Checkout (hosted, simplest)

```ts
// app/api/checkout/route.ts
import Stripe from "stripe";
import { NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { priceId } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",                    // or "payment" for one-time
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.APP_URL}/cancel`,
    automatic_tax: { enabled: true },
    customer_email: req.headers.get("x-user-email") ?? undefined,
    allow_promotion_codes: true,
  });

  return NextResponse.json({ url: session.url });
}
```

```tsx
"use client";
async function subscribe(priceId: string) {
  const { url } = await fetch("/api/checkout", {
    method: "POST",
    body: JSON.stringify({ priceId }),
  }).then((r) => r.json());
  window.location.assign(url);
}

<button onClick={() => subscribe("price_1Pxxx")}>Subscribe — $29/mo</button>
```

### Recipe 2 — Inline Payment Element (custom UX)

```tsx
// app/checkout/page.tsx
"use client";
import { useEffect, useState } from "react";
import { Elements, PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export default function CheckoutPage() {
  const [clientSecret, setClientSecret] = useState<string>();

  useEffect(() => {
    fetch("/api/payment-intent", { method: "POST" })
      .then((r) => r.json())
      .then((d) => setClientSecret(d.clientSecret));
  }, []);

  if (!clientSecret) return <p>Loading...</p>;

  return (
    <Elements stripe={stripePromise} options={{ clientSecret, appearance: { theme: "stripe" } }}>
      <CheckoutForm />
    </Elements>
  );
}

function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string>();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!stripe || !elements) return;
    setSubmitting(true);

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: { return_url: `${window.location.origin}/order-complete` },
    });

    if (error) setError(error.message);
    setSubmitting(false);
  }

  return (
    <form onSubmit={onSubmit}>
      <PaymentElement />
      <button type="submit" disabled={!stripe || submitting}>
        {submitting ? "Processing..." : "Pay"}
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
```

```ts
// app/api/payment-intent/route.ts
export async function POST() {
  const intent = await stripe.paymentIntents.create({
    amount: 2999,
    currency: "usd",
    automatic_payment_methods: { enabled: true },
  });
  return NextResponse.json({ clientSecret: intent.client_secret });
}
```

### Recipe 3 — Webhook signature verification

```ts
// app/api/webhook/route.ts
import Stripe from "stripe";
import { NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const sig = req.headers.get("stripe-signature");
  if (!sig) return new Response("No signature", { status: 400 });

  let event: Stripe.Event;
  try {
    const body = await req.text();
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return new Response(`Webhook error: ${(err as Error).message}`, { status: 400 });
  }

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object;
      await db.subscription.upsert({
        where: { userId: session.client_reference_id! },
        create: { userId: session.client_reference_id!, status: "active", stripeId: session.id },
        update: { status: "active" },
      });
      break;
    }
    case "customer.subscription.deleted":
    case "customer.subscription.updated": {
      const sub = event.data.object;
      await db.subscription.update({
        where: { stripeId: sub.id },
        data: { status: sub.status },
      });
      break;
    }
    case "invoice.payment_failed":
      // notify user
      break;
  }

  return NextResponse.json({ received: true });
}
```

**Important:** in App Router, you cannot use `req.json()` for the webhook —
the raw body must be passed to `constructEvent`. Use `req.text()`.

### Recipe 4 — Local webhook forwarding

```bash
stripe listen --forward-to http://localhost:3000/api/webhook
# Prints a webhook signing secret — set STRIPE_WEBHOOK_SECRET to that value in .env.local
```

Trigger a test event:

```bash
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
```

### Recipe 5 — Customer Portal (self-service billing)

```ts
// app/api/portal/route.ts
export async function POST(req: Request) {
  const userId = await getUserId(req);
  const user = await db.user.findUnique({ where: { id: userId }, select: { stripeCustomerId: true } });
  if (!user?.stripeCustomerId) return new Response("No customer", { status: 404 });

  const session = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.APP_URL}/settings/billing`,
  });
  return NextResponse.json({ url: session.url });
}
```

Customer Portal handles plan changes, cancellation, invoice download, payment
method updates — for free, no UI to build.

### Recipe 6 — Create Customer + attach to Checkout

```ts
const customer = await stripe.customers.create({
  email: user.email,
  metadata: { userId: user.id },
});
await db.user.update({ where: { id: user.id }, data: { stripeCustomerId: customer.id } });

// Later, in checkout:
const session = await stripe.checkout.sessions.create({
  customer: customer.id,
  client_reference_id: user.id,
  // ...
});
```

### Recipe 7 — Stripe Connect (marketplace)

```ts
const account = await stripe.accounts.create({
  type: "express",                           // or "standard" / "custom"
  email: seller.email,
  business_type: "individual",
});

const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: `${process.env.APP_URL}/connect/refresh`,
  return_url: `${process.env.APP_URL}/connect/complete`,
  type: "account_onboarding",
});

// Redirect user to accountLink.url
```

When checking out for a Connected account product:

```ts
const session = await stripe.checkout.sessions.create({
  payment_intent_data: {
    application_fee_amount: Math.round(total * 0.05),   // 5% platform fee
    transfer_data: { destination: sellerStripeAccountId },
  },
  // ...
});
```

### Recipe 8 — Subscription with trial

```ts
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  line_items: [{ price: "price_1Pxxx", quantity: 1 }],
  subscription_data: {
    trial_period_days: 14,
    trial_settings: { end_behavior: { missing_payment_method: "pause" } },
  },
  payment_method_collection: "if_required",
  // ...
});
```

### Recipe 9 — Stripe Tax (automatic VAT/GST)

```ts
const session = await stripe.checkout.sessions.create({
  automatic_tax: { enabled: true },          // Stripe calculates tax based on customer location
  customer_update: { address: "auto" },      // Update saved address from Checkout
  tax_id_collection: { enabled: true },      // Collect B2B VAT ID
  // ...
});
```

Requires Stripe Tax enabled in dashboard.

## Examples

### Example 1: $29/mo SaaS with Checkout + webhook

```bash
# 1. Create product + price in Stripe dashboard
# 2. Implement Checkout route (Recipe 1)
# 3. Implement webhook + verification (Recipe 3)
# 4. Forward locally: stripe listen --forward-to localhost:3000/api/webhook
# 5. Trigger flow: stripe trigger checkout.session.completed
```

### Example 2: Inline custom checkout with Payment Element

1. Create PaymentIntent server-side (Recipe 2)
2. Render `<Elements>` + `<PaymentElement>` client-side
3. Call `stripe.confirmPayment` on submit
4. Handle webhook for `payment_intent.succeeded` to fulfill order

## Edge cases / gotchas

- **NEVER trust client-side amounts** — always create PaymentIntent / Checkout
  Session server-side with prices fetched from your DB or Stripe.
- **Webhook must verify signature** — without it, attackers can forge events.
- **Webhook handlers must be idempotent** — Stripe retries on 5xx for 3 days.
  Use the event `id` as a dedup key.
- **App Router webhooks need `req.text()`** for the raw body — `req.json()` is
  parsed already and signature verification fails.
- **Test mode keys (`sk_test_...`)** can do everything live keys can — except
  charge real cards. Use freely.
- **PCI-DSS scope** — using Elements/Checkout keeps card data off your servers.
  Custom card forms (rolling your own) put you in PCI scope.
- **3D Secure / SCA** — required in EU. `automatic_payment_methods: { enabled:
  true }` handles it.
- **Stripe Connect Express** requires onboarding (KYC) — sellers can't accept
  payments until they complete it.
- **`application_fee_amount` only works** with Connect Standard/Custom. Express
  + direct charges, fee deducted from seller.
- **Trial periods + no payment method** — `payment_method_collection: "if_
  required"` skips the card prompt. Risky for fraud — pair with email
  verification.
- **Refunds happen via `refunds.create`** — not via webhook. Implement a
  refund endpoint or use the Stripe dashboard.
- **Stripe.js is loaded async** (`loadStripe`) — never call `useStripe` outside
  `<Elements>`.

## Sources

- [Stripe docs](https://docs.stripe.com/)
- [Stripe Checkout](https://docs.stripe.com/payments/checkout)
- [Payment Element](https://docs.stripe.com/payments/payment-element)
- [Webhooks](https://docs.stripe.com/webhooks)
- [Customer Portal](https://docs.stripe.com/customer-management)
- [Stripe Connect](https://docs.stripe.com/connect)
- [Stripe Tax](https://docs.stripe.com/tax)
- [Stripe.js reference](https://docs.stripe.com/js)
- [@stripe/react-stripe-js](https://github.com/stripe/react-stripe-js)
- [Stripe CLI](https://docs.stripe.com/stripe-cli)
- [Stripe sample apps](https://github.com/stripe-samples) — official examples
- [Lee Robinson — Stripe + Next 15 (2025)](https://leerob.com/) — recent integration walkthroughs
