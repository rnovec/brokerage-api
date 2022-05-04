from datetime import datetime

from sqlalchemy.orm import Session

from app.api.constants import (
    BUY_ORDER_OPERATION,
    SELL_ORDER_OPERATION,
    SUPPORTED_ORDER_OPERATIONS,
)
from app.api.exceptions import (
    ClosedMarketException,
    InsufficentFundsException,
    InsufficentStocksException,
    InvalidOperationException,
)
from app.api.utils import is_time_between
from app.database.models import Account, Order

from .schemas import AccountSchema, OrderSchema


def create_account(db: Session, payload: AccountSchema):
    """Create a new investment account."""
    account = Account(cash=payload.cash)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account_balance(
    db: Session, operation: Order.Operations, account: Account, amount: float
):
    """Update the balance of an investment account."""
    if operation == Order.Operations.BUY:
        account.cash -= amount
    elif operation == Order.Operations.SELL:
        account.cash += amount
    db.commit()
    db.refresh(account)
    return account


def create_order(db: Session, payload: OrderSchema, account: Account):
    """Create a new buy/sell order."""
    order = None
    timestamp = datetime.fromtimestamp(payload.timestamp)
    if not is_time_between(timestamp.time()):
        raise ClosedMarketException()

    order_amount = payload.total_shares * payload.shared_price
    if payload.operation == BUY_ORDER_OPERATION and order_amount > account.cash:
        raise InsufficentFundsException(f"Account {account.id} has insufficient funds.")

    elif payload.operation == SELL_ORDER_OPERATION:
        stocks = db.query(Order).filter(
            Order.account_id == account.id,
            Order.operation == Order.Operations.BUY,
            Order.issuer_name == payload.issuer_name,
        )
        if stocks.count() == 0:
            raise InsufficentStocksException(f"Account {account.id} has no orders.")

    if payload.operation in SUPPORTED_ORDER_OPERATIONS:
        order = Order(
            account_id=account.id,
            timestamp=payload.timestamp,
            operation=payload.operation,
            issuer_name=payload.issuer_name,
            total_shares=payload.total_shares,
            shared_price=payload.shared_price,
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Update the account balance
        update_account_balance(db, order.operation, account, order_amount)
    else:
        raise InvalidOperationException(
            f"Operation {payload.operation} is not supported."
        )

    return order
