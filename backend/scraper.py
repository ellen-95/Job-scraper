from typing import Any

from ftfy import fix_text
import requests


REMOTEOK_API_URL = "https://remoteok.com/api"
REQUEST_TIMEOUT_SECONDS = 10


def fetch_remoteok_jobs(limit: int = 100) -> list[dict]:
    """Fetch and normalize job listings from the RemoteOK public API."""
    if limit <= 0:
        return []

    try:
        response = requests.get(
            REMOTEOK_API_URL,
            headers={"User-Agent": "Job-scraper/0.1"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return []

    if not isinstance(payload, list):
        return []

    jobs: list[dict] = []
    for entry in payload:
        if len(jobs) >= limit:
            break

        if not _is_job_entry(entry):
            continue

        jobs.append(_normalize_job(entry))

    return jobs


def _is_job_entry(entry: Any) -> bool:
    """RemoteOK can include metadata in the response; only keep real jobs."""
    if not isinstance(entry, dict):
        return False

    has_title = bool(entry.get("position") or entry.get("title"))
    has_source = bool(entry.get("company") or entry.get("url"))
    return has_title and has_source


def _normalize_job(entry: dict) -> dict:
    return {
        "title": _clean_string(entry.get("position") or entry.get("title")),
        "company": _clean_string(entry.get("company")),
        "tags": _clean_tags(entry.get("tags")),
        "location": _clean_location(entry.get("location")),
        "date_posted": _clean_string(entry.get("date")),
        "url": _clean_string(entry.get("url")),
    }


def _clean_string(value: Any) -> str:
    if value is None:
        return ""

    return fix_text(str(value)).strip()


def _clean_location(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        locations = [_clean_string(item) for item in value]
        return ", ".join(location for location in locations if location)

    return _clean_string(value)


def _clean_tags(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    tags = []
    seen_tags = set()
    for tag in value:
        cleaned_tag = _clean_string(tag)
        if cleaned_tag and cleaned_tag not in seen_tags:
            seen_tags.add(cleaned_tag)
            tags.append(cleaned_tag)

    return tags
