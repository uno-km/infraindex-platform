# Function Inventory

## Backend (FastAPI)
- `apps/api/core/database.py:get_db`: Yields AsyncSession generator for dependency injection.
- `apps/api/api/v1/endpoints/providers.py:read_providers`: Returns list of providers with pagination.
- `apps/api/api/v1/endpoints/search.py:search_offers`: Performs filtered search of instance offerings.

## Worker (Celery)
- `apps/worker/core/circuit_breaker.py:CircuitBreaker.allow_request`: Determines if a request should be made.
- `apps/worker/adapters/vast_ai/client.py:VastAiAdapter.fetch_prices`: Fetches live offers from Vast.ai API.
- `apps/worker/adapters/runpod/client.py:RunpodAdapter.fetch_catalog`: Fetches GPU types and prices from Runpod GraphQL.
- `apps/worker/tasks/orchestrator.py:run_all_collections`: Celery beat task to orchestrate scraping.
