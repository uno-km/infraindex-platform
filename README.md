# 🚀 infraindex-platform

> **An enterprise-grade intelligence platform that tracks, analyzes, and compares global GPU rental prices and compute availability across major cloud providers.**

## 📖 Overview

**infraindex-platform** is a scalable, monorepo-based data platform designed to monitor and aggregate pricing and availability metrics for high-performance compute instances (like NVIDIA H100, A100, L40S) from various neo-cloud providers such as AWS, RunPod, Vast.ai, CoreWeave, and more. 

By utilizing robust background workers and an intuitive API, infraindex-platform empowers AI researchers, DevOps teams, and ML engineers to find the most cost-effective GPU resources for their training and inference workloads without vendor lock-in.

## ✨ Features
- **Real-time Price Scraping:** Automated daily data collection from various cloud provider APIs and web endpoints.
- **Time-Series Analysis:** Track historical price trends to identify the best time to spin up instances.
- **Enterprise-Grade Architecture:** Built with Python (FastAPI + Celery/Redis) for the backend and Turborepo for strict monorepo modularity.
- **Provider Agnostic:** Easily extensible Factory Pattern to integrate new cloud providers seamlessly.

## 🏗️ Architecture Stack
- **API:** FastAPI, Pydantic, SQLAlchemy, PostgreSQL
- **Worker:** Celery, Redis (Asynchronous scraping and retry queues)
- **Monorepo Management:** Turborepo, pnpm
