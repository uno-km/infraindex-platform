# Realtime & Polyglot Architecture

## 1. Core Principle
Do not build the entire system in a single language blindly. The choice of language should be dictated by workload characteristics (Requirement 69).

## 2. Low-Frequency Pricing Pipeline (Python)
- **Scope**: Gathering scheduled API data (Vast.ai, Runpod), normalization, relational consistency, outlier detection, and complex admin queries.
- **Why Python?**: Fast development cycle, excellent data parsing libraries (Pydantic, Pandas), and Celery integration.
- **Components**: FastAPI endpoints (REST), Celery Workers.

## 3. High-Frequency Realtime Pipeline (Go)
- **Scope**: Live WebSocket/SSE streaming of tens of thousands of market ticks (e.g. options, futures, live spot prices).
- **Why Go?**: Extremely high concurrency handling with low memory overhead (Goroutines), built-in robust net/http for long-lived socket connections, backpressure handling.
- **Components**: Go Feed Handler, WebSocket/SSE Gateway.

## 4. Contract between Python and Go
- The two ecosystems must NEVER import each other's modules or directly share state.
- **Integration**: Python and Go communicate via a strongly typed Event Schema (e.g. Protocol Buffers, JSON Schema) over an abstract EventBus (e.g. Kafka, Redis Streams).
