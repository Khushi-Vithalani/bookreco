# BookReco

Backend service for a book recommendation system.

## Tech Stack
- FastAPI
- PostgreSQL (Docker)
- SQLAlchemy
- Open Library API

## Features (current)
- Book catalog ingestion from Open Library
- REST APIs to browse and search books
- Fiction / Non-fiction classification

## Setup
```bash
docker compose up -d
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload