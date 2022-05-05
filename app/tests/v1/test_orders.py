from fastapi.testclient import TestClient

from app.common.constants import (
    CLOSED_MARKET_ERROR_KEY,
    DUPLICATED_OPERATION_ERROR_KEY,
    INSUFFICIENT_FUNDS_ERROR_KEY,
    INSUFFICIENT_STOCKS_ERROR_KEY,
)
from app.main import app

from .mocks import (
    BUY_ORDER_TEST_PAYLOAD,
    CLOSED_MARKET_ORDER_TEST_PAYLOAD,
    SELL_ORDER_TEST_PAYLOAD,
)

client = TestClient(app)


def test_create_buy_order():
    """Test creating a buy order."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a buy order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert isinstance(order["business_errors"], list)
    assert isinstance(order["current_balance"]["issuers"], list)
    assert order["current_balance"]["cash"] == 900
    assert order["business_errors"] == []


def test_create_sell_order_failed():
    """Test creating a sell order with insufficient stocks."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a sell order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=SELL_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert INSUFFICIENT_STOCKS_ERROR_KEY in order["business_errors"]


def test_create_sell_order_success():
    """Test creating a sell order."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a buy order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200

    # Create a sell order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=SELL_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert order["business_errors"] == []


def test_insufficient_balance():
    """Test creating a buy order on and account with insufficient cash balance."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 0})
    account = response.json()
    account_id = account["id"]

    # Create a sell order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "business_errors" in order
    assert order["business_errors"] != []
    assert INSUFFICIENT_FUNDS_ERROR_KEY in order["business_errors"]


def test_closed_market():
    """Test creating a buy order on and account out of time."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 100})
    account = response.json()
    account_id = account["id"]

    # Create a sell order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=CLOSED_MARKET_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "business_errors" in order
    assert order["business_errors"] != []
    assert CLOSED_MARKET_ERROR_KEY in order["business_errors"]


def test_create_duplicated_operation():
    """Test creating a sell order."""
    # Create an account
    response = client.post("/v1/accounts", json={"cash": 1000})
    account = response.json()
    account_id = account["id"]

    # Create a buy order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert order["business_errors"] == []

    # Create a sell order
    response = client.post(
        f"/v1/accounts/{account_id}/orders", json=BUY_ORDER_TEST_PAYLOAD
    )
    order = response.json()
    assert response.status_code == 200
    assert "current_balance" in order
    assert "business_errors" in order
    assert DUPLICATED_OPERATION_ERROR_KEY in order["business_errors"]
