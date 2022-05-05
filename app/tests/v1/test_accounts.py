from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.v1.accounts.controllers import create_account, update_account_balance
from app.core.models import Account, Order
from app.core.schemas.accounts import AccountSchema
from app.main import app
from app.tests.database import get_memory_db

client = TestClient(app)


def test_create_account_controller():
    """Test controller to create a new investment account."""
    db: Session = get_memory_db()
    payload = AccountSchema(cash=1000)
    account = create_account(db=db, payload=payload)
    assert account.id is not None
    assert account.cash == 1000
    assert isinstance(account, Account)


def test_update_balance_controller():
    """Test controller to update account's balance."""
    db: Session = get_memory_db()
    account = Account(cash=300)
    db.add(account)
    db.commit()
    db.refresh(account)
    account = update_account_balance(
        db=db, account=account, operation=Order.Operations.BUY, amount=100
    )
    assert account.cash == 200
    assert isinstance(account, Account)

    account = update_account_balance(
        db=db, account=account, operation=Order.Operations.SELL, amount=50
    )
    assert account.cash == 250
    assert isinstance(account, Account)


def test_create_account():
    """Test endpoint to create a new investment account."""
    payload = {"cash": 1000}
    response = client.post("/v1/accounts", json=payload)
    account = response.json()
    assert response.status_code == 201
    assert "id" in account
    assert "cash" in account
    assert "issuers" in account
    assert account["cash"] == payload["cash"]
    assert account["issuers"] == []
