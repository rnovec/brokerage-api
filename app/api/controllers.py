from sqlalchemy.orm import Session

from app.api.constants import SUPPORTED_ORDER_OPERATIONS
from app.database.models import Account, Order

from .schemas import AccountSchema, OrderSchema


def create_account(db: Session, payload: AccountSchema):
    """Create a new investment account."""
    account = Account(cash=payload.cash)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account_balance(db: Session, order: OrderSchema, account: Account):
    """Update the balance of an investment account."""
    print(account.cash, order.operation)
    if order.operation == Order.Operations.BUY:
        account.cash -= order.total_shares * order.shared_price
    elif order.operation == Order.Operations.SELL:
        account.cash += order.total_shares * order.shared_price
    db.commit()
    db.refresh(account)
    return account


def create_order(db: Session, payload: OrderSchema, account_id: int):
    """Create a new buy/sell order."""
    order = None
    account = db.query(Account).get(account_id)
    if account is None:
        raise ValueError("Account not found.")

    if payload.operation in SUPPORTED_ORDER_OPERATIONS:
        order = Order(
            account_id=account_id,
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
        account = update_account_balance(db, order, account)

    return order, account
