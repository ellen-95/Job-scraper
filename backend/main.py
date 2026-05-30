from collections import Counter
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from sqlalchemy import select

from backend.database import SessionLocal, init_db, save_jobs
from backend.models import Job
from backend.scraper import fetch_remoteok_jobs


app = FastAPI(title="Job-scraper")

FRONTEND_INDEX = Path(__file__).resolve().parent.parent / "frontend" / "index.html"


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(FRONTEND_INDEX)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/scrape")
def scrape() -> dict[str, int]:
    jobs = fetch_remoteok_jobs()
    inserted = save_jobs(jobs)
    return {"fetched": len(jobs), "inserted": inserted}


@app.get("/jobs")
def list_jobs(
    keyword: str | None = Query(default=None),
    company: str | None = Query(default=None),
) -> list[dict]:
    with SessionLocal() as session:
        jobs = (
            session.execute(select(Job).order_by(Job.created_at.desc()))
            .scalars()
            .all()
        )

    filtered_jobs = [
        job
        for job in jobs
        if _matches_keyword(job, keyword) and _matches_company(job, company)
    ]
    return [_job_to_dict(job) for job in filtered_jobs]


@app.get("/stats")
def stats() -> dict:
    with SessionLocal() as session:
        jobs = session.execute(select(Job)).scalars().all()

    tag_counts = Counter(tag for job in jobs for tag in (job.tags or []))
    day_counts = Counter(job.date_posted for job in jobs if job.date_posted)

    return {
        "total_jobs": len(jobs),
        "top_5_tags": [
            {"tag": tag, "count": count} for tag, count in tag_counts.most_common(5)
        ],
        "jobs_per_day": [
            {"date": date, "count": count} for date, count in sorted(day_counts.items())
        ],
    }


def _matches_keyword(job: Job, keyword: str | None) -> bool:
    if not keyword:
        return True

    normalized_keyword = keyword.lower()
    title = (job.title or "").lower()
    tags = " ".join(job.tags or []).lower()
    return normalized_keyword in title or normalized_keyword in tags


def _matches_company(job: Job, company: str | None) -> bool:
    if not company:
        return True

    return company.lower() in (job.company or "").lower()


def _job_to_dict(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "tags": job.tags or [],
        "location": job.location,
        "date_posted": job.date_posted,
        "url": job.url,
        "created_at": job.created_at.isoformat() if job.created_at else "",
    }
