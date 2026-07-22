# Storage Strategy (PostgreSQL vs TimescaleDB vs ClickHouse)

## 1. Storage Boundaries
As per Requirement 70, dual writing in application logic is strictly forbidden. 

### PostgreSQL (System of Record)
- **Usage**: Provider catalog, Users, Configuration, Scheduled Jobs, Outbox Events.
- **Role**: Source of truth for relational state.

### TimescaleDB
- **Usage**: GPU & Cloud price observations.
- **Role**: Time-series extension built on top of Postgres, useful when data grows to require continuous aggregates and hypertable partitioning.

### ClickHouse
- **Usage**: Ultra-high frequency market ticks (quotes, order books, trades).
- **Role**: Analytical columnar store designed for analyzing billions of financial ticks rapidly for chart rendering.

## 2. Data Propagation (CQRS / Outbox)
To move data reliably from the relational store (Postgres) to analytical stores without dual-writing from the application domain:
1. Application updates PostgreSQL and atomically writes an `OutboxEvent`.
2. A separate background process (Change Data Capture or Outbox Publisher) reads the `OutboxEvent` and publishes it to the Event Bus (Kafka/Redis).
3. Analytics Consumers (Go/Python) subscribe to the Bus and write to ClickHouse/TimescaleDB.
