import os
from collections.abc import Iterable
from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://appuser:apppassword@db:3306/jobsdb",
)


Base = declarative_base()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create database tables if they do not already exist."""
    from backend import models

    Base.metadata.create_all(bind=engine)


def save_jobs(jobs: Iterable[dict]) -> int:
    """Insert new jobs and skip rows whose URL is already stored."""
    from backend.models import Job

    prepared_jobs = list(jobs)
    urls = {_clean_string(job.get("url")) for job in prepared_jobs}

    with SessionLocal() as session:
        existing_urls = set()
        if urls:
            existing_urls = set(
                session.execute(select(Job.url).where(Job.url.in_(urls))).scalars()
            )

        new_jobs = []
        seen_urls = set(existing_urls)
        for job in prepared_jobs:
            url = _clean_string(job.get("url"))
            if url in seen_urls:
                continue

            seen_urls.add(url)
            new_jobs.append(
                Job(
                    title=_clean_string(job.get("title")),
                    company=_clean_string(job.get("company")),
                    tags=_clean_tags(job.get("tags")),
                    location=_clean_string(job.get("location")),
                    date_posted=_clean_string(job.get("date_posted")),
                    url=url,
                )
            )

        if not new_jobs:
            return 0

        session.add_all(new_jobs)
        session.commit()
        return len(new_jobs)


def _clean_string(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _clean_tags(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    return [_clean_string(tag) for tag in value if _clean_string(tag)]
