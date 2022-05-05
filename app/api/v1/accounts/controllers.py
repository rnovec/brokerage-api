from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.common.constants import (
    BUY_ORDER_OPERATION,
    SELL_ORDER_OPERATION,
    SUPPORTED_ORDER_OPERATIONS,
)
from app.common.exceptions import (
    ClosedMarketException,
    DuplicatedOperationException,
    InsufficentFundsException,
    InsufficentStocksException,
    InvalidOperationException,
)
from app.common.utils import is_time_between
from app.core.models import Account, Order
from app.core.schemas import AccountSchema, OrderSchema


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


def get_account_stocks(db: Session, account_id: int, issuer_name: str = None):
    """Get the latest orders for a given investment account."""
    return db.query(Order).filter(
        Order.account_id == account_id,
        Order.operation == Order.Operations.BUY,
        Order.issuer_name == issuer_name,
    )


def get_latest_orders(db: Session, account_id: int, operation: str, minutes: int = 5):
    """Get the latest orders for a given investment account."""
    if operation == BUY_ORDER_OPERATION:
        operation = Order.Operations.BUY
    elif operation == SELL_ORDER_OPERATION:
        operation = Order.Operations.SELL

    return db.query(Order).filter(
        Order.operation == operation,
        Order.account_id == account_id,
        Order.created_at >= datetime.utcnow() - timedelta(minutes=minutes),
    )


def create_order(db: Session, payload: OrderSchema, account: Account):
    """Create a new buy/sell order."""
    order = None
    timestamp = datetime.fromtimestamp(payload.timestamp)
    if not is_time_between(timestamp.time()):
        raise ClosedMarketException()

    has_recent_orders = get_latest_orders(db, account.id, payload.operation).count() > 0
    if has_recent_orders:
        raise DuplicatedOperationException()

    order_amount = payload.total_shares * payload.shared_price
    if payload.operation == BUY_ORDER_OPERATION and order_amount > account.cash:
        raise InsufficentFundsException(f"Account {account.id} has insufficient funds.")

    elif payload.operation == SELL_ORDER_OPERATION:
        stocks = get_account_stocks(db, account.id, payload.issuer_name)
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
