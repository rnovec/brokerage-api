from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.constants import (INSUFFICIENT_FUNDS_ERROR_KEY,
                               INSUFFICIENT_STOCKS_ERROR_KEY)
from app.api.exceptions import InsufficentFunds, InsufficentStocks
from app.database.config import get_session
from app.database.models import Account

from . import controllers, schemas

router = APIRouter()


@router.post("/accounts", response_model=schemas.AccountSchemaRead, status_code=201)
def create_account(data: schemas.AccountSchema, db: Session = Depends(get_session)):
    return controllers.create_account(db=db, payload=data)


@router.post(
    "/accounts/{id}/orders",
    response_model=schemas.OperationSchemaResponse,
)
def create_order(
    id: int, data: schemas.OrderSchema, db: Session = Depends(get_session)
):
    account = db.query(Account).get(id)
    business_errors = []
    try:
        controllers.create_order(db=db, payload=data, account=account)
    except InsufficentFunds:
        business_errors.append(INSUFFICIENT_FUNDS_ERROR_KEY)
    except InsufficentStocks:
        business_errors.append(INSUFFICIENT_STOCKS_ERROR_KEY)

    return schemas.OperationSchemaResponse(
        current_balance=schemas.BalanceSchema(
            cash=account.cash, issuers=account.orders
        ),
        business_errors=business_errors,
    )
