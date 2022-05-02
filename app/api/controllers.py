from sqlalchemy.orm import Session

from app.database.models import Account

from .schemas import AccountSchema


def create_account(db: Session, payload: AccountSchema):
    """Create a new investment account."""
    account = Account(cash=payload.cash)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
