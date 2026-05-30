from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI(title="Job-scraper")

FRONTEND_INDEX = Path(__file__).resolve().parent.parent / "frontend" / "index.html"


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(FRONTEND_INDEX)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
