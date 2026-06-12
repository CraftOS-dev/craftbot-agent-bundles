<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-resilience/SKILL.md
Repo: wshobson/agents

NOTE: WebFetch returned a summarized view of this file rather than verbatim content.
The summary below captures the SOTA recommendations from the source.
-->

# Python Resilience Patterns

Fault-tolerant Python application design using resilience patterns for handling transient failures.

## When to Use This Skill

- Integrating retry mechanisms into external service calls
- Establishing timeouts for network operations
- Constructing microservices that remain operational despite dependency issues

## Core Principles

- **Distinguish transient from permanent failures.** Temporary failures warrant retries (network blip, rate limit, 503). Permanent ones (4xx auth errors, bugs) do not.
- **Exponential backoff with jitter.** Prevents overwhelming a recovering service. Each retry waits exponentially longer; jitter randomizes the exact delay to avoid synchronized retries from many clients.
- **Bounded retries.** Always cap both the number of attempts and the total elapsed time.
- **Every network call needs a timeout.** No exceptions.

## Implementation

The guidance relies on the `tenacity` library for production-quality retry decoration. Patterns progress from:

1. **Basic retry logic** — `@retry(stop=stop_after_attempt(3))`
2. **Selective error handling** — only retry specific exception classes
3. **HTTP status code evaluation** — retry on 5xx, not on 4xx
4. **Combined exception + status approaches**

## Critical Recommendations

- **Retry only transient errors.** Don't retry bugs or authentication failures.
- **Every network call needs a timeout.**
- **Log retries transparently.** Monitor retry rates as indicators of systemic problems — don't silently mask them.
- **Inject dependencies for testability.** Decoupled retry logic is easier to test than embedded retry loops.
- **Separate resilience from business logic.** Decorators keep retry/timeout/circuit-breaker behavior infrastructure-level, business code clean.

## Detail referenced in source

The original SKILL.md file references additional detail in `references/details.md`. For complete worked examples (`tenacity` decorators, circuit breakers, bulkhead patterns), see the source repo.
