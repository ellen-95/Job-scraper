# Job-scraper

Minimal FastAPI scaffold for a take-home task.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Open http://localhost:8000.

## Run with Docker Compose

```bash
docker compose up
```

## Endpoints

- `GET /` serves `frontend/index.html`
- `GET /health` returns `{"status": "ok"}`

The scraper is intentionally not implemented yet.
