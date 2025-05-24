# Installation
#create environment
python3 -m venv venv

#activate environment
source venv/bin/activate

#install dependencies
pip install -r requirements.txt

#run the app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

---

# FastAPI + Redis + Kafka (Cloud-Based)

This project is a lightweight FastAPI application built for interview-ready demos and real-world prototyping. It connects to **Upstash Redis** and **Confluent Cloud Kafka**, providing REST endpoints to:

- Set and Get key-value pairs in Redis
- Produce and Consume Kafka messages
- Run entirely in GitHub Codespaces or any Python environment

---

## Tech Stack

- **FastAPI** — Lightweight async API framework
- **Redis (Upstash)** — Cloud-hosted key-value store
- **Kafka (Confluent Cloud)** — Managed Kafka broker
- **Uvicorn** — ASGI server
- **Python-dotenv** — Secure config loading
- **Confluent-Kafka** — Python client for Kafka

---
# Environment Variables
# Create a `.env` file in the root directory with the following variables:
# Redis (Upstash)
REDIS_HOST=your-upstash-host.upstash.io
REDIS_PORT=your-port
REDIS_PASSWORD=your-password

# Kafka (Confluent Cloud)
KAFKA_BOOTSTRAP=pkc-xxxxx.gcp.confluent.cloud:9092
KAFKA_API_KEY=your-api-key
KAFKA_API_SECRET=your-api-secret
KAFKA_TOPIC=test-events
