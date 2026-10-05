# HelaCare Architecture

## Principles

- **Safety before generation** — red-flag detection executes before knowledge retrieval.
- **Grounding before fluency** — only verified records can support user-facing claims.
- **Visible provenance** — the API returns the sources used.
- **Auditable behavior** — chat decisions are persisted for review.
- **Separation of concerns** — UI, API, persistence, retrieval, safety, and future LLM
  synthesis are isolated.
- **Progressive sophistication** — lexical retrieval works first; vector retrieval and
  LLM synthesis can be introduced without breaking the public API.

## Components

### Next.js web
TypeScript App Router application. It is intentionally a thin client over the API.

### FastAPI
Routes, schemas, services, models, and persistence are separated into modules.

### PostgreSQL + pgvector
Canonical knowledge and audit store. pgvector is enabled for semantic retrieval in
the next milestone.

### Redis
Reserved for rate limits, cache, background jobs, and idempotency.

## Future production topology

```text
CDN/WAF
  |
Load Balancer / Ingress
  |
  +--- Next.js replicas
  |
  +--- FastAPI replicas
          |
          +--- PostgreSQL/pgvector
          +--- Redis
          +--- OpenTelemetry collector
```
