# Cloud Cost Estimation (Staging Environment)

This document provides a monthly cost estimation for running the InfraIndex staging environment on AWS (`ap-northeast-2`, Seoul region). Prices are estimates as of 2026.

## Compute (Amazon ECS - Fargate)
We deploy three lightweight containers (API, Worker, Web) using ECS Fargate to minimize operational overhead.
- **API Task**: 0.5 vCPU, 1 GB RAM -> ~$15.00/month
- **Worker Task**: 0.5 vCPU, 1 GB RAM -> ~$15.00/month
- **Web Task**: 0.5 vCPU, 1 GB RAM -> ~$15.00/month
- **Compute Subtotal**: ~$45.00/month

## Database (Amazon RDS for PostgreSQL)
For staging, we use a single-AZ burstable instance.
- **Instance Type**: `db.t4g.micro` (2 vCPU, 1GB RAM) -> ~$13.50/month
- **Storage**: 20GB gp3 -> ~$2.40/month
- **DB Subtotal**: ~$15.90/month

## Cache & Broker (Amazon ElastiCache for Redis)
For Celery queueing and basic caching.
- **Instance Type**: `cache.t4g.micro` -> ~$11.00/month
- **Cache Subtotal**: ~$11.00/month

## Networking & Miscellaneous
- **NAT Gateway / VPC Endpoints / Data Transfer**: ~$15.00/month (Estimated based on low staging traffic)

## **Total Estimated Monthly Cost (Staging)**
**~$86.90 / month**

> **Note**: This is a staging environment. Production will require Multi-AZ deployments, larger instance types (e.g., `db.m7g.large`), ClickHouse clustering, and load balancers, pushing the expected cost closer to ~$500 - $1,500/month depending on traffic and data volume.
