# Scheduler Architecture

## 1. Overview
The scheduling system for InfraIndex goes beyond a simple cron task to provide a highly reliable, distributed, and idempotent job execution framework.

## 2. Core Components
- **Configuration Store**: Schedules (e.g., 09:00, 13:00, 18:00 KST) are managed in the `ScheduleConfig` database table, allowing live updates without redeployments.
- **Orchestrator Task**: A Celery Beat task runs frequently (e.g., every 5 minutes) to check if any configured schedules are due.
- **Distributed Lock & Idempotency**: `IdempotencyKey` table prevents duplicate execution of the same scheduled collection run.

## 3. Execution Flow
1. Celery Beat triggers `orchestrator.tick()`.
2. Orchestrator fetches active `ScheduleConfig` records.
3. If a schedule matches the current time window, it attempts to acquire a distributed lock via the `IdempotencyKey` table.
4. If successful, it dispatches individual `provider_collection_job` tasks.
5. If unsuccessful (already run), it skips.
