<!--
Source: https://fakerjs.dev/ · https://faker.readthedocs.io/ · https://mockaroo.com/ · https://www.tonic.ai/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Test Data Management — Synthetic + GDPR-Safe

The 2026 SOTA: **Faker.js / Faker (Python)** for column-level synthetic data
in code; **Mockaroo** for schema-based mock datasets; **Tonic.ai** /
**DBmask** for production-like masked synthetic when realistic distributions
matter. Store fixtures in Git alongside test code. Never copy production PII
to test environments.

## When to use

- New test needs realistic-looking data (names, emails, addresses)
- Database fixtures for integration tests
- Load-test populations (10k users with varied profiles)
- GDPR / HIPAA / PCI mandates no prod PII in lower environments
- Cross-environment seed data for staging / preview deploys
- Trigger phrases: "test data", "fixtures", "Faker", "Mockaroo", "Tonic",
  "GDPR", "PII", "seed data", "synthetic data", "mock data"

## Setup

```bash
# Faker (Python)
uv add --dev faker

# Faker.js (JS/TS)
npm i -D @faker-js/faker

# Mockaroo CLI (community)
npm i -g mockaroo-cli

# Factory libraries
uv add --dev factory-boy            # Python (Django/SQLAlchemy)
npm i -D fishery                    # JS/TS factory

# Tonic.ai — SaaS; via API
# https://docs.tonic.ai/
```

Auth: `MOCKAROO_API_KEY` (Mockaroo API); `TONIC_API_KEY` (Tonic Cloud).

## Common recipes

### Recipe 1 — Faker Python basics

```python
from faker import Faker

fake = Faker()
Faker.seed(42)  # deterministic for tests

user = {
    "id": fake.uuid4(),
    "name": fake.name(),
    "email": fake.email(),
    "phone": fake.phone_number(),
    "address": fake.address(),
    "company": fake.company(),
    "created_at": fake.iso8601(),
}

# Localized
fake_jp = Faker("ja_JP")
print(fake_jp.name(), fake_jp.address())

# Multiple locales
fake = Faker(["en_US", "es_ES", "ja_JP"])
```

### Recipe 2 — Faker.js basics

```ts
import { faker } from "@faker-js/faker";
faker.seed(42);

const user = {
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email().toLowerCase(),
  phone: faker.phone.number(),
  address: faker.location.streetAddress({ useFullAddress: true }),
  company: faker.company.name(),
  createdAt: faker.date.past({ years: 2 }).toISOString(),
};
```

### Recipe 3 — factory-boy (Python — Django / SQLAlchemy)

```python
# tests/factories.py
import factory
from faker import Faker
from myapp.models import User, Order

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("uuid4")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    role = factory.Iterator(["admin", "user", "guest"])

class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total = factory.Faker("pyfloat", positive=True, max_value=1000)
    status = "pending"
    items = factory.RelatedFactoryList("tests.factories.OrderItemFactory",
                                       factory_related_name="order", size=3)
```

```python
def test_user_has_orders(db_session):
    user = UserFactory(role="admin")
    OrderFactory.create_batch(5, user=user)
    assert db_session.query(Order).filter_by(user_id=user.id).count() == 5
```

### Recipe 4 — fishery (TS factories)

```ts
import { Factory } from "fishery";
import { faker } from "@faker-js/faker";

type User = { id: string; email: string; role: "admin" | "user" };

const userFactory = Factory.define<User>(({ sequence }) => ({
  id: faker.string.uuid(),
  email: `user${sequence}@example.com`,
  role: "user",
}));

const admin = userFactory.build({ role: "admin" });
const team = userFactory.buildList(20);
```

### Recipe 5 — Mockaroo schema-based dataset

```yaml
# mockaroo-schema.yml — describe schema, fetch 1000 rows
fields:
  - name: id
    type: Row Number
  - name: email
    type: Email Address
  - name: signup
    type: Date
    min: 2024-01-01
    max: 2026-06-01
  - name: country
    type: Country
  - name: subscription
    type: Custom List
    values: [free, pro, enterprise]
    selection_style: weighted
    weights: [70, 25, 5]
```

```bash
curl "https://api.mockaroo.com/api/generate.json?key=$MOCKAROO_API_KEY&count=1000" \
  -d @mockaroo-schema.json -o fixtures/users.json
```

### Recipe 6 — Tonic.ai masked snapshot (CLI)

```bash
# Sync masked snapshot from prod-like source
tonic workspace create --name=staging --source-id=prod-readonly
tonic job run --workspace=staging --target=staging-db

# Mask rules: PII columns → faker; structural columns kept
# Generated DB has production-like distribution, no real PII
```

Verify masking:

```sql
SELECT email FROM users LIMIT 5;
-- alice.real@yahoo.com  → fake.4892@maskeddomain.com
```

### Recipe 7 — pytest fixtures pattern

```python
# tests/conftest.py
import pytest
from tests.factories import UserFactory, OrderFactory

@pytest.fixture
def alice(db_session):
    user = UserFactory(email="alice@example.com")
    yield user
    db_session.delete(user); db_session.commit()

@pytest.fixture
def alice_with_orders(db_session, alice):
    orders = OrderFactory.create_batch(3, user=alice)
    yield alice, orders
    for o in orders:
        db_session.delete(o)
    db_session.commit()
```

### Recipe 8 — Playwright fixture for fresh user

```ts
// fixtures.ts
import { test as base } from "@playwright/test";
import { faker } from "@faker-js/faker";
import { api } from "./api";

export const test = base.extend<{ user: any }>({
  user: async ({}, use) => {
    const u = {
      email: faker.internet.email().toLowerCase(),
      password: "Test1234!",
      name: faker.person.fullName(),
    };
    await api.createUser(u);
    await use(u);
    await api.deleteUser(u.email);
  },
});
```

### Recipe 9 — Seed script for staging

```python
# scripts/seed_staging.py
from faker import Faker
from myapp.models import User, Product, Order
from myapp.db import session

fake = Faker()
Faker.seed(2026)

def main():
    print("Seeding staging...")
    users = [User(email=f"user{i}@example.com", name=fake.name()) for i in range(100)]
    session.add_all(users); session.flush()

    products = [Product(name=fake.catch_phrase(), price=fake.pyfloat(positive=True, max_value=500))
                for _ in range(50)]
    session.add_all(products); session.flush()

    orders = [Order(user=fake.random_element(users),
                    product=fake.random_element(products),
                    qty=fake.random_int(1, 5)) for _ in range(500)]
    session.add_all(orders); session.commit()
    print(f"Done — {len(users)} users, {len(products)} products, {len(orders)} orders")

if __name__ == "__main__":
    main()
```

### Recipe 10 — Deterministic random seeds in tests

```python
@pytest.fixture(autouse=True)
def faker_seed(faker):
    faker.seed_instance(42)
    return faker
```

```ts
beforeEach(() => faker.seed(42));
```

Ensures CI failures reproduce locally.

### Recipe 11 — Load-test population generator

```python
# scripts/gen_loadtest_users.py
from faker import Faker
import json

fake = Faker()
users = [{
    "email": fake.email(),
    "password": "LoadTest1234!",
    "country": fake.country_code(),
} for _ in range(10_000)]

with open("loadtest_users.json", "w") as f:
    json.dump(users, f)
```

Locust / k6 reads + chunks for distributed VUs.

### Recipe 12 — GDPR-safe field-level masking

```sql
-- Postgres function for one-shot mask
CREATE OR REPLACE FUNCTION mask_email(email text)
RETURNS text AS $$
SELECT 'user-' || md5(email) || '@masked.example.com'
$$ LANGUAGE sql IMMUTABLE;

UPDATE users SET email = mask_email(email);
UPDATE users SET phone = '+1' || lpad(floor(random() * 10000000000)::text, 10, '0');
UPDATE users SET name = 'User ' || substring(md5(name), 1, 8);
```

Run on a snapshot before letting devs / QA access.

## Examples

### Example 1: New test suite needs realistic data

**Goal:** Integration test for "list users" endpoint.

1. Add `UserFactory` in `tests/factories.py` (Recipe 3).
2. Test creates 20 users via `UserFactory.create_batch(20)`.
3. Assert list endpoint returns 20.
4. Pytest fixtures auto-clean (Recipe 7).
5. Seed deterministic for CI repro (Recipe 10).

### Example 2: Staging needs prod-like data without PII

**Goal:** Sales demo on staging needs "1000 customers" feel.

1. Use Mockaroo schema for 1000 users (Recipe 5) — saved as fixture.
2. Seed script loads fixture on every staging refresh (Recipe 9).
3. Sales demos use seeded data; no risk of real customer leak.
4. For deeper realism: Tonic snapshot of prod schemas with masking (Recipe 6).

## Edge cases / gotchas

- **Faker is not for security tests** — passwords like "P@ssw0rd!" from
  Faker are predictable; use `secrets.token_urlsafe()` for credentials.
- **Locale matters** — Russian / Japanese / Arabic names break English-only
  string-length assumptions; test with localized faker.
- **Duplicate emails on parallel tests** — use `Sequence` (factory-boy) or
  unique per-worker prefix.
- **Faker seeds in CI vs local** — `Faker.seed(int(os.environ.get('CI_RUN_ID', 42)))`
  to vary across CI runs while reproducible per run.
- **Mockaroo free tier — 200 rows / day, 1000 rows / call** — paid for more.
- **Tonic.ai paid only** — free fallback: write your own SQL masking
  (Recipe 12) or `pg_anonymizer` extension.
- **Real PII in fixtures committed to Git** — easy mistake. Pre-commit:
  `gitleaks` + `detect-secrets` to catch.
- **Date fixtures going stale** — `fake.iso8601()` returns current date; tests
  asserting "this year" pass forever then break in Jan. Use anchored dates.
- **Faker pyfloat sometimes returns NaN** — set `positive=True, allow_nan=False`.
- **Cross-database fixtures** — Postgres seeded for staging, MySQL for tests
  diverge. Use migrations + faker-based seeders in both.
- **Order of fixture creation** — foreign key violations if Order created
  before User. Use `SubFactory` (factory-boy) or topological order.
- **Faker locale list** — 50+ available; `fake.locales()` lists. Mixing locales
  per row needs `Faker(["en_US", "es_ES"])`.

## Sources

- [Faker docs (Python)](https://faker.readthedocs.io/)
- [Faker.js docs](https://fakerjs.dev/)
- [factory-boy docs](https://factoryboy.readthedocs.io/)
- [fishery (JS factory)](https://github.com/thoughtbot/fishery)
- [Mockaroo docs](https://mockaroo.com/docs)
- [Tonic.ai docs](https://docs.tonic.ai/)
- [pg_anonymizer extension](https://postgresql-anonymizer.readthedocs.io/)
- [GDPR test data guidance](https://gdpr.eu/data-protection-impact-assessment-template/)
- [Synthetic Data Vault](https://sdv.dev/) — statistical synthetic data
- [DBmask](https://github.com/lwlcom/DBmask) — masking for MySQL / Postgres
