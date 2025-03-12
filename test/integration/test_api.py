import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone, timedelta

from app.main import app
from app.dependencies import get_roll_service


@pytest.fixture
def test_app(roll_service):
    original_dependencies = app.dependency_overrides.copy()

    async def override_get_roll_service():
        return roll_service

    app.dependency_overrides[get_roll_service] = override_get_roll_service

    client = TestClient(app)

    yield client

    app.dependency_overrides = original_dependencies


def test_create_roll(test_app):
    response = test_app.post(
        "/api/",
        json={"length": 150.0, "weight": 75.0}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["length"] == 150.0
    assert data["weight"] == 75.0
    assert "id" in data
    assert "created_at" in data
    assert data["removed_at"] is None


def test_get_roll_success(test_app):
    response = test_app.get("/api/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_roll_not_found(test_app):
    response = test_app.get("/api/999")

    assert response.status_code == 404
    assert "detail" in response.json()
    error_detail = response.json().get("detail", "").lower()
    assert any(text in error_detail for text in ["not found", "не найден"])


def test_remove_roll(test_app):
    response = test_app.delete("/api/3")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["removed_at"] is not None


def test_get_rolls(test_app):
    response = test_app.get("/api/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_rolls_with_filter(test_app):
    filter_params = {
        "weight_min": 100.0,
        "is_active": True
    }

    response = test_app.get("/api/", params=filter_params)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    for roll in data:
        assert roll["weight"] >= 100.0
        assert roll["removed_at"] is None


def test_get_statistics(test_app):
    now = datetime.now(timezone.utc)
    period = {
        "start_date": (now - timedelta(days=10)).isoformat(),
        "end_date": now.isoformat()
    }

    response = test_app.post(
        "/api/statistics",
        json=period
    )

    assert response.status_code == 200
    data = response.json()

    assert "period_start" in data
    assert "period_end" in data
    assert "added_rolls_count" in data
    assert "removed_rolls_count" in data
    assert "total_weight" in data
