import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path):
    database_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")

    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    for module_name in ["backend.main", "backend.models", "backend.database"]:
        sys.modules.pop(module_name, None)

    main = importlib.import_module("backend.main")
    with TestClient(main.app) as test_client:
        yield test_client


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_stats_returns_expected_keys(client: TestClient) -> None:
    response = client.get("/stats")

    assert response.status_code == 200
    assert set(response.json()) == {"total_jobs", "top_5_tags", "jobs_per_day"}
