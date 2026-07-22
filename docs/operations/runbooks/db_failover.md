# Database Failover Runbook

## Overview
This runbook describes the procedure to follow when the primary PostgreSQL database for InfraIndex becomes unresponsive or data corruption is detected.

## Symptoms
- API latency > 5000ms consistently on DB operations
- HTTP 500 responses indicating "Connection Refused" to PostgreSQL
- Alerts on Celery worker queues backing up without processing

## Action Plan

### 1. Verification
1. Access the production server via SSH.
2. Check PostgreSQL container status:
   ```bash
   docker ps | grep postgres
   docker logs postgres_container_name --tail 100
   ```

### 2. Triage & Restart
If the process is simply deadlocked or OOM killed:
1. Restart the container:
   ```bash
   docker restart postgres_container_name
   ```
2. Monitor API health endpoint `/api/v1/health`.

### 3. Failover to Replica (If primary is unrecoverable)
1. Stop traffic at the load balancer or stop API containers.
2. Promote the read-replica (RDS / Managed DB workflow):
   - Access cloud console.
   - Promote read-replica to standalone instance.
3. Update `.env` file `POSTGRES_SERVER` to the new endpoint.
4. Restart API and Worker containers.
5. Re-enable traffic.

### 4. Post-Incident
1. Analyze PostgreSQL logs to find root cause (OOM, slow queries, disk full).
2. Write post-mortem and adjust DB resources or query optimization.
