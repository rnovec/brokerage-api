from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_account():
    """Test endpoint to create a new investment account."""
    payload = {"cash": 1000}
    response = client.post("/accounts", json=payload)
    account = response.json()
    assert response.status_code == 201
    assert "id" in account
    assert "cash" in account
    assert "issuers" in account
    assert account["cash"] == payload["cash"]
    assert account["issuers"] == []
