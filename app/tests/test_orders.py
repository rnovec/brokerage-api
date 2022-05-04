from fastapi.testclient import TestClient

from app.api.constants import (INSUFFICIENT_FUNDS_ERROR_KEY,
                               INSUFFICIENT_STOCKS_ERROR_KEY)
from app.main import app
from app.tests.mocks import BUY_ORDER_TEST_PAYLOAD, SELL_ORDER_TEST_PAYLOAD

client = TestClient(app)


def test_create_buy_order():
    """Test creating a buy order."""
    # Create an account
    response = client.post("/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a buy order
    response = client.post(
        f"/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
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
    response = client.post(
        f"/accounts/{account_id}/orders", json=SELL_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert INSUFFICIENT_STOCKS_ERROR_KEY in order["business_errors"]


def test_insufficient_balance():
    """Test creating a buy order on and account with insufficient cash balance."""
    # Create an account
    response = client.post("/accounts", json={"cash": 0})
    account = response.json()
    account_id = account["id"]

    # Create a sell order
    payload = BUY_ORDER_TEST_PAYLOAD
    response = client.post(f"/accounts/{account_id}/orders", json=payload)
    order = response.json()
    assert response.status_code == 200
    assert "business_errors" in order
    assert order["business_errors"] != []
    assert INSUFFICIENT_FUNDS_ERROR_KEY in order["business_errors"]
