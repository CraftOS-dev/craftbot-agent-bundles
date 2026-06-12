<!--
Source: https://hypothesis.readthedocs.io/ · https://github.com/HypothesisWorks/hypothesis
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# hypothesis — Property-Based Testing

`hypothesis` (David MacIver, HypothesisWorks) is the de facto property-based
testing library for Python. Instead of writing specific examples, you write
PROPERTIES (invariants) and let hypothesis generate inputs to disprove them.
When it finds a failure, it SHRINKS the input to a minimal counterexample.

This is the 2026 SOTA approach for testing pure functions, encoders/decoders,
state machines, and serialization round-trips.

## When to use this skill

- Encoding/decoding round-trips (JSON, MessagePack, Protobuf, custom)
- Pure-math functions with mathematical invariants
- Parser correctness (validate that valid input always parses)
- Stateful object behaviour (state machines)
- Edge cases you'd never think of (empty list, single char, NaN, surrogate
  pairs, leap-day, EPOCH boundary)
- Refactoring confidence — same property before and after
- Snapshot escape hatch — when "snapshot equality" misses semantic equality

Do NOT use hypothesis for: I/O-heavy tests (slow); checking specific business
rules ("user X gets discount Y" needs an example); stochastic tests where
"close enough" is the contract (use `pytest.approx`).

## Setup

```bash
uv add --dev hypothesis
# Optional integrations
uv add --dev hypothesis[django]               # django strategies
uv add --dev hypothesis[pandas,numpy]         # pandas + numpy strategies
```

## Common recipes

### Recipe 1 — Round-trip property

```python
import json
from hypothesis import given, strategies as st

@given(data=st.recursive(
    st.one_of(st.none(), st.booleans(), st.integers(), st.floats(allow_nan=False), st.text()),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=20,
))
def test_json_roundtrip(data):
    assert json.loads(json.dumps(data)) == data
```

`@given` decorator runs the test many times with generated inputs. Failures
are SHRUNK to the minimal counterexample (e.g., from `{"a": [1, NaN, 3]}`
down to `[NaN]`).

### Recipe 2 — Encoding invariants

```python
from hypothesis import given, strategies as st
from my_app.crypto import encrypt, decrypt, KEY_BYTES

@given(
    plaintext=st.binary(max_size=4096),
    key=st.binary(min_size=KEY_BYTES, max_size=KEY_BYTES),
)
def test_decrypt_inverts_encrypt(plaintext, key):
    assert decrypt(encrypt(plaintext, key), key) == plaintext
```

### Recipe 3 — Numerical invariants

```python
from hypothesis import given, strategies as st
import math

@given(x=st.floats(allow_nan=False, allow_infinity=False))
def test_sqrt_squared_is_x_for_non_negative(x):
    if x < 0:
        return  # skip; sqrt(-1) is complex
    assert math.isclose(math.sqrt(x) ** 2, x, rel_tol=1e-9)
```

### Recipe 4 — Composite strategy (build a domain object)

```python
from hypothesis import given, strategies as st
from my_app.models import User

@st.composite
def user_strategy(draw):
    return User(
        id=draw(st.uuids()),
        email=draw(st.emails()),
        age=draw(st.integers(min_value=0, max_value=150)),
        roles=draw(st.lists(st.sampled_from(["admin", "user", "guest"]),
                            min_size=1, unique=True)),
    )

@given(user=user_strategy())
def test_user_serialization_roundtrip(user):
    assert User.from_json(user.to_json()) == user
```

### Recipe 5 — Stateful testing (RuleBasedStateMachine)

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis import strategies as st
from my_app.cart import Cart

class CartStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cart = Cart()
        self.expected_total = 0

    @rule(item=st.text(min_size=1), price=st.integers(min_value=0, max_value=1000))
    def add_item(self, item, price):
        self.cart.add(item, price)
        self.expected_total += price

    @rule()
    def empty(self):
        self.cart.empty()
        self.expected_total = 0

    @invariant()
    def total_matches(self):
        assert self.cart.total == self.expected_total

TestCart = CartStateMachine.TestCase
```

Hypothesis generates sequences of rules, executes them, and asserts
invariants. This catches state-dependent bugs (forgotten-empty, double-add,
order-dependent failures).

### Recipe 6 — Settings

```python
from hypothesis import given, settings, Verbosity, strategies as st

@given(x=st.integers())
@settings(
    max_examples=500,                 # default 100
    deadline=1000,                    # per-example ms cap
    verbosity=Verbosity.verbose,
)
def test_heavy_property(x):
    ...
```

For CI, define a profile:

```python
# conftest.py
from hypothesis import settings, Verbosity
settings.register_profile("ci", max_examples=500, deadline=None)
settings.register_profile("dev", max_examples=50)
settings.load_profile("ci" if os.environ.get("CI") else "dev")
```

### Recipe 7 — Shrinking + reporting

When a test fails, hypothesis prints:

```
Falsifying example: test_json_roundtrip(data=float('nan'))
```

It SHRANK the failing input to the simplest form that still fails. Often
this is the bug in one line — way more useful than a 10MB random example.

To reproduce a shrunken failure:

```python
@given(...)
@example(float("nan"))                 # regression example
def test_json_roundtrip(data):
    ...
```

Or use `hypothesis-pytest` reproduction commands printed in the output.

### Recipe 8 — Stateful HTTP / DB property test

```python
@given(
    requests=st.lists(
        st.tuples(
            st.sampled_from(["GET", "POST", "DELETE"]),
            st.text(min_size=1, max_size=20),
        ),
        max_size=20,
    )
)
def test_api_never_returns_500_on_valid_routes(requests):
    client = TestClient(app)
    for method, path in requests:
        response = client.request(method, f"/{path}")
        assert response.status_code != 500  # only 4xx for bad inputs
```

### Recipe 9 — Reproducibility seed

```bash
HYPOTHESIS_PROFILE=ci uv run pytest --hypothesis-seed=42
```

Locks the seed for deterministic CI runs (useful for debugging a specific
counterexample).

## Strategy cheat-sheet

```python
st.none()
st.booleans()
st.integers(min_value=-100, max_value=100)
st.floats(allow_nan=False, allow_infinity=False)
st.text(min_size=1, max_size=100, alphabet="abc")
st.binary(min_size=0, max_size=1024)
st.lists(st.integers(), min_size=1, max_size=10, unique=True)
st.dictionaries(st.text(), st.integers())
st.tuples(st.integers(), st.text())
st.one_of(st.none(), st.integers())                # sum type
st.sampled_from([1, 2, 3])                          # choose from list
st.uuids()
st.datetimes(min_value=datetime(2000,1,1))
st.emails()
st.ip_addresses()
st.from_regex(r"[a-z]{1,10}")
st.recursive(base, extend, max_leaves=20)           # for recursive data
```

For pandas / numpy:

```python
from hypothesis.extra import pandas as hpd, numpy as hnp
hpd.data_frames(columns=[hpd.column("x", dtype=int), hpd.column("y", dtype=float)])
hnp.arrays(dtype=float, shape=(10, 10))
```

## When property-based catches what example-based misses

Real bugs hypothesis has caught in published case studies:
- JSON encoders crashing on `float("nan")` / `float("inf")`.
- Date parsers off-by-one near year boundaries / leap seconds.
- Base64 round-trips failing on inputs with trailing whitespace.
- String normalisers producing different output on Unicode surrogate pairs.
- Caches with hash collisions on specific input shapes.
- Sort algorithms that didn't actually sort (typo in comparator).

The pattern: any time you have an INVARIANT (round-trip, monotonicity,
idempotence, commutativity, "fast path equals slow path"), property-based
testing is strictly better than examples.

## Edge cases

- **Slow tests**: set `deadline=None` for tests that are intrinsically slow,
  or reduce `max_examples` for CI.
- **Non-deterministic code**: `assume()` to skip examples that hit known
  unreliable paths.
- **Stateful machine deadlocks**: limit `Bundle` size to avoid runaway
  state explosion.
- **Filtering out invalid examples**: use `.filter(...)` sparingly — too
  much filtering and hypothesis gives up. Use `assume()` for late filters.
- **Time-dependent code**: use `freezegun` inside the test body to freeze
  time across examples.
- **Database tests**: each example commits + rolls back; can be slow. Use a
  testcontainers savepoint pattern (see `testcontainers-integration-testing`
  skill).
- **Reproducibility**: set `derandomize=True` for CI determinism;
  alternatively log the `--hypothesis-seed` to reproduce.

## Sources

- https://hypothesis.readthedocs.io/ — full docs
- https://github.com/HypothesisWorks/hypothesis — source
- https://hypothesis.works/articles/ — blog with practical examples
- https://increment.com/testing/in-praise-of-property-based-testing/ — David MacIver essay
- https://github.com/DRMacIver/QuickCheck — historical context (Haskell origin)
