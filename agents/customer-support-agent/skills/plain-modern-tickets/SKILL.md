<!--
Source: https://www.plain.com/docs/graphql/introduction
Plain GraphQL API: https://www.plain.com/docs/api
-->
# Plain Modern Tickets — SKILL

Plain is the modern, dev-first SaaS ticket platform with a GraphQL-only API. Best fit for technical SaaS supporting developer customers. This skill covers the ticket lifecycle (Threads in Plain terminology): create, search, reply, assign, label, snippet management, customer lookup.

## When to use

- **Recipient runs Plain** — common for B2B dev-tool startups (Posthog, Vercel, Linear-style shops).
- **Programmatic ticket creation** from email / webhook / Slack-relayed customer events.
- **Snippets (Plain's macro equivalent)** authoring and rollout.
- **Thread assignment + status transitions** (DONE / TODO / SNOOZED).
- **Customer enrichment** — Plain's customer cards expose external metadata you can drive from CRM.
- **Reply-as-customer impersonation** for migrating tickets from another platform.

Trigger phrases: "create Plain thread", "reply to Plain ticket", "Plain snippet", "assign Plain thread", "Plain customer card".

## Setup

```bash
# Plain has SDKs for JS/TS, Python. CLI via curl always works.
# Endpoint: https://core-api.uk.plain.com/graphql/v1 (UK region)
#           https://core-api.eu.plain.com/graphql/v1 (EU region, request-only)
curl -sS https://core-api.uk.plain.com/graphql/v1 \
  -H "Authorization: Bearer $PLAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ workspace { id name } }"}'
```

Auth + env:
- `PLAIN_API_KEY` — at `Plain Settings > API Keys > Create key`. Scoped to roles (read-only / write / admin). Use write scope for the support agent.
- All requests are POST to the single GraphQL endpoint with the query in the body. Use Apollo / `graphql-request` SDK for non-trivial schemas.

## Common recipes

### Recipe 1: Search customers by email

```graphql
query SearchCustomer {
  customers(filters: { emails: ["user@example.com"] }, first: 1) {
    edges {
      node {
        id
        email { email isVerified }
        fullName
        externalId
        company { name }
      }
    }
  }
}
```

```bash
curl -sS https://core-api.uk.plain.com/graphql/v1 \
  -H "Authorization: Bearer $PLAIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{ customers(filters:{emails:[\"user@example.com\"]},first:1){ edges{ node{ id email{ email } fullName } } } }"}'
```

Use the returned `id` (a Plain customer ID, NOT the email) for thread creation.

### Recipe 2: Create a thread (Plain's "ticket")

```graphql
mutation CreateThread {
  createThread(input: {
    customerIdentifier: { customerId: "c_01HW..." }
    title: "Cannot complete checkout"
    components: [
      { componentText: { text: "Customer reports checkout failing with error code E422." } }
    ]
    labelTypeIds: ["lt_billing"]
  }) {
    thread {
      id
      title
      status
    }
    error { message }
  }
}
```

The `components` array is Plain's rich-content model. Use `componentText`, `componentDivider`, `componentLinkButton`, `componentSpacer` per docs. Threads start in `TODO` by default.

### Recipe 3: Reply to a thread

```graphql
mutation ReplyToThread {
  replyToThread(input: {
    threadId: "th_01HW..."
    textContent: "Hi — clearing browser cache usually fixes this. Steps: ..."
    markdownContent: "Hi — clearing browser cache usually fixes this. Steps:\n\n1. ...\n2. ..."
  }) {
    error { message }
  }
}
```

Communication channel inferred from the thread (API / CHAT / EMAIL / SLACK / MS_TEAMS). Markdown content rendered platform-native; text content is the fallback.

### Recipe 4: Reply impersonating a customer (migration / proxy use)

```graphql
mutation ReplyAsCustomer {
  replyToThread(input: {
    threadId: "th_01HW..."
    textContent: "From customer: thanks for the workaround."
    impersonation: { asCustomer: { customerIdentifier: { emailAddress: "user@example.com" } } }
  }) { error { message } }
}
```

Used when migrating tickets from another platform or proxying customer-Slack-DM messages into Plain.

### Recipe 5: Assign thread

```graphql
mutation AssignThread {
  assignThread(input: {
    threadId: "th_01HW..."
    assignee: { userId: "u_01HW..." }
  }) {
    thread { id assignedAt assignee { name } }
    error { message }
  }
}
```

`assignee` can be `{ userId }` or `{ machineUserId }` (for bot assignment). Pass `null` to unassign.

### Recipe 6: Change thread status

```graphql
mutation ChangeStatus {
  changeThreadStatus(input: {
    threadId: "th_01HW..."
    status: DONE
    statusDetail: { changeNote: "Resolved via workaround." }
  }) {
    thread { id status }
    error { message }
  }
}
```

Statuses: `TODO`, `IN_PROGRESS`, `SNOOZED`, `DONE`. `SNOOZED` requires a `snoozeUntil` timestamp.

### Recipe 7: Apply labels (tags equivalent)

```graphql
mutation ApplyLabels {
  applyLabels(input: {
    threadId: "th_01HW..."
    labelTypeIds: ["lt_billing","lt_enterprise","lt_high_priority"]
  }) { error { message } }
}
```

Label types are defined workspace-wide. Cache `labels` query results to map name → labelTypeId.

### Recipe 8: Create a snippet (Plain's macro / saved reply)

```graphql
mutation CreateSnippet {
  createSnippet(input: {
    name: "[topic-billing] Plan downgrade walkthrough"
    body: "Hi {{customer.first_name}},\n\nHere are the exact steps to downgrade your plan: ..."
    visibility: WORKSPACE
  }) {
    snippet { id name }
    error { message }
  }
}
```

`visibility` is `WORKSPACE` (shared) or `PERSONAL`. Use mustache for customer fields — Plain expands at insertion time.

### Recipe 9: List recent threads (cursor-paginated)

```graphql
query RecentThreads {
  threads(
    filters: { statuses: [TODO, IN_PROGRESS] }
    first: 25
    sortBy: { field: CREATED_AT, direction: DESC }
  ) {
    edges {
      cursor
      node {
        id
        title
        status
        assignee { id name }
        customer { fullName email { email } }
        labels { labelType { name } }
        createdAt { iso8601 }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
```

Paginate by passing `after: $endCursor`. Plain uses Relay-style connections.

### Recipe 10: Read full thread including timeline events

```graphql
query ThreadDetail {
  thread(threadId: "th_01HW...") {
    id
    title
    status
    customer { fullName email { email } externalId }
    timelineEntries(first: 50) {
      edges {
        node {
          id
          entry {
            __typename
            ... on CustomerEventEntry { event { title } }
            ... on EmailEntry { from { email } textContent }
            ... on ChatEntry { text }
            ... on NoteEntry { markdown }
          }
        }
      }
    }
  }
}
```

Use the `timelineEntries` union to pull the conversation transcript across channel types.

### Recipe 11: Upsert customer (sync from CRM)

```graphql
mutation UpsertCustomer {
  upsertCustomer(input: {
    identifier: { emailAddress: "user@example.com" }
    onCreate: {
      fullName: "Jane Doe"
      email: { email: "user@example.com", isVerified: true }
      externalId: "stripe_cus_abc"
    }
    onUpdate: {
      fullName: { value: "Jane Doe" }
      externalId: { value: "stripe_cus_abc" }
    }
  }) {
    customer { id }
    result    # CREATED | UPDATED | NOOP
    error { message }
  }
}
```

Atomic upsert by email — idempotent if you key on `externalId` or email.

### Recipe 12: Customer Card config (push CRM data into Plain UI)

Customer cards are read-time webhook fetches. Configure at `Settings > Customer Cards > New Card`. The agent's server returns JSON like:

```json
{
  "cards": [{
    "key": "subscription",
    "timeToLiveSeconds": 60,
    "components": [
      { "componentText": { "text": "Plan: Enterprise ($120k ARR)" } },
      { "componentDivider": { "spacingSize": "M" } },
      { "componentText": { "text": "MRR: $10,000" } }
    ]
  }]
}
```

Plain GETs your endpoint with `customer.email` query param when an agent opens the thread.

## Examples

### Example 1: Webhook-driven ticket creation from product event

**Goal:** When a user hits a critical error in-product, auto-create a Plain thread.

**Steps:**
1. Product emits `error.critical` webhook to the agent server.
2. Agent calls `upsertCustomer` with email + externalId.
3. Agent calls `createThread` with the error context as a `componentText`.
4. Agent applies labels: `auto-created`, `error-critical`, `<feature-area>`.
5. Agent posts internal note tagging the on-call developer.

**Result:** Customer has a thread before they even open a chat; developer sees it in their assignments.

### Example 2: Migrate tickets from Zendesk → Plain

**Goal:** Backfill 1000 historical Zendesk tickets into Plain for unified search.

**Steps:**
1. Export Zendesk via `/incremental/tickets/cursor.json`.
2. For each ticket: `upsertCustomer` (by email).
3. `createThread` with the original subject as `title`, full body as components.
4. For each customer reply in the Zendesk thread: `replyToThread` with `impersonation.asCustomer`.
5. For each agent reply: `replyToThread` without impersonation (records as the agent user).
6. `changeThreadStatus(status: DONE)` on closed tickets.

**Result:** Plain workspace mirrors Zendesk history; searchable / labeled / linkable.

## Edge cases / gotchas

- **GraphQL only** — no REST surface. Tooling: Apollo, `graphql-request`, or `curl` with stringified query. For complex mutations, generate types with `graphql-codegen` against Plain's schema.
- **Regional endpoints** — UK (`core-api.uk.plain.com`) is default. EU (`core-api.eu.plain.com`) is data-residency option. Confirm region in workspace settings; calling the wrong region returns 401.
- **All errors live in the mutation's `error` field, not GraphQL `errors`** — Plain returns 200 with `error: { message }` for business logic failures. Always check `data.<mutation>.error`.
- **Customer identifiers are nuanced** — `customerId` (Plain's), `externalId` (your CRM's), or `emailAddress`. Always pick one and stay consistent within a flow.
- **Components-based content** — text replies use `textContent`/`markdownContent`; structured replies use the `components` array. Mixing is allowed but order matters.
- **Snippet variables use mustache** — `{{customer.firstName}}`, `{{customer.fullName}}`, `{{thread.title}}`. Undefined variables render literally — test before pushing.
- **Rate limits** — 100 req/min per workspace by default; contact Plain for higher tier. Cursor-paginate, don't repeat full queries.
- **No SLA / Macros API** — Plain has no SLA-policy primitive yet (June 2026). Implement SLAs via your warehouse + scheduled queries. "Macros" are called "Snippets" — different feature surface from Zendesk.
- **Webhook signature** — HMAC-SHA256 with `PLAIN_WEBHOOK_SECRET`; verify `X-Plain-Signature`.
- **`changeThreadStatus` with SNOOZED requires `snoozeUntil`** — easy 400 if you forget.
- **Label types vs labels** — `labelTypeIds` defines what a label is workspace-wide; applying it creates the label instance on the thread. Don't confuse the two.

## Sources

- [Plain GraphQL introduction](https://www.plain.com/docs/graphql/introduction)
- [Plain API docs (llms-full)](https://www.plain.com/docs/llms-full.txt)
- [Plain customer cards](https://www.plain.com/docs/customer-cards)
- [Plain blog — API-first support 2026](https://www.plain.com/blog/api-first-support-platforms)
