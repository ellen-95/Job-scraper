# Job-scraper

## Overview

Job-scraper is a small FastAPI application that fetches remote job listings from the RemoteOK public API, stores them in MySQL, and displays the results in a simple browser dashboard.

## Features

- Job scraping from RemoteOK
- MySQL storage
- Duplicate prevention by job URL
- REST API for scraping, listing, filtering, and statistics
- Dashboard built with plain HTML, CSS, JavaScript, and Chart.js
- Docker support with Docker Compose
- Automated testing and CI with pytest, Ruff, and GitHub Actions

## Architecture

The data flow is:

```text
RemoteOK API -> Scraper -> MySQL -> FastAPI -> Dashboard
```

The scraper normalizes RemoteOK job data, the database layer stores only new jobs, FastAPI exposes API endpoints, and the dashboard consumes those endpoints.

## Setup

Run the application with Docker Compose:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

## API Endpoints

Trigger a scrape:

```http
POST /scrape
```

List stored jobs:

```http
GET /jobs
```

Filter jobs by keyword:

```http
GET /jobs?keyword=python
```

Filter jobs by company:

```http
GET /jobs?company=stripe
```

Return aggregate statistics:

```http
GET /stats
```

## Testing

Run linting:

```bash
ruff check backend
```

Run tests:

```bash
pytest backend
```

## AI Usage

AI tools, including Codex/ChatGPT, were used as coding assistants for project scaffolding, implementation suggestions, debugging, and documentation. All generated code was reviewed, tested, and adapted before submission.

## Limitations

- The scraper uses the public RemoteOK API and depends on its availability and response format.
- Filtering is intentionally simple.
- There is no authentication or background job scheduler.
