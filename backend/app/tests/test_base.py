from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_list_sensor() -> None:
    response = client.get("/api/sensors")
    assert response.status_code == 200
