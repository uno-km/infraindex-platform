# System Architecture

## Overall Architecture
The system follows a domain-neutral data platform approach, layered as follows:
- **Layer 1:** Source Layer (API, Bulk Files, Webpages)
- **Layer 2:** Raw Ingestion Layer (Immutable source snapshots)
- **Layer 3:** Canonical Domain Layer (Compute, Storage, Semiconductor, Market)
- **Layer 4:** Observation Layer (Prices, Availability, Capacity)
- **Layer 5:** Derived Metric Layer (Normalized pricing, Index values)
- **Layer 6:** Product/API Layer (Search API, GraphQL/REST, Frontend)
- **Layer 7:** Governance Layer (License tracking, Audit logs)

## Technology Stack
- **Monorepo:** pnpm workspace with Turborepo
- **Frontend:** Next.js (App Router, Tailwind CSS, TanStack Query)
- **Backend API:** FastAPI (Python 3.13), SQLAlchemy, Alembic, Pydantic
- **Worker:** Celery + Redis for ingestion and data normalization
- **Database:** PostgreSQL
- **Object Storage:** For raw JSON/HTML snapshots
- **Infrastructure:** Docker, Docker Compose (for local development)
