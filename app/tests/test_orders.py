from fastapi.testclient import TestClient

from app.database.models import Account, Order
from app.main import app

client = TestClient(app)


def test_create_buy_order():
    """Test creating a buy order."""
    # Create an account
    response = client.post("/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a buy order
    payload = {
        "timestamp": 1583362645,
        "operation": "BUY",
        "issuer_name": "AAPL",
        "total_shares": 2,
        "shared_price": 50,
    }
    response = client.post(f"/accounts/{account_id}/orders", json=payload)
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert isinstance(order["business_errors"], list)
    assert isinstance(order["current_balance"]["issuers"], list)
    assert order["current_balance"]["cash"] == 900
    assert order["business_errors"] == []


def test_create_sell_order():
    """Test creating a sell order."""
    # Create an account
    response = client.post("/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a sell order
    payload = {
        "timestamp": 1583362645,
        "operation": "SELL",
        "issuer_name": "AAPL",
        "total_shares": 2,
        "shared_price": 50,
    }
    response = client.post(f"/accounts/{account_id}/orders", json=payload)
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert order["current_balance"]["cash"] == 1100
