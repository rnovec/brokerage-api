from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.constants import (
    CLOSED_MARKET_ERROR_KEY,
    DUPLICATED_OPERATION_ERROR_KEY,
    INSUFFICIENT_FUNDS_ERROR_KEY,
    INSUFFICIENT_STOCKS_ERROR_KEY,
    INVALID_OPERATION_ERROR_KEY,
)
from app.api.exceptions import (
    ClosedMarketException,
    DuplicatedOperationException,
    InsufficentFundsException,
    InsufficentStocksException,
    InvalidOperationException,
)
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
    except ClosedMarketException:
        business_errors.append(CLOSED_MARKET_ERROR_KEY)
    except DuplicatedOperationException:
        business_errors.append(DUPLICATED_OPERATION_ERROR_KEY)
    except InsufficentFundsException:
        business_errors.append(INSUFFICIENT_FUNDS_ERROR_KEY)
    except InsufficentStocksException:
        business_errors.append(INSUFFICIENT_STOCKS_ERROR_KEY)
    except InvalidOperationException:
        business_errors.append(INVALID_OPERATION_ERROR_KEY)

    return schemas.OperationSchemaResponse(
        current_balance=schemas.BalanceSchema(
            cash=account.cash, issuers=account.orders
        ),
        business_errors=business_errors,
    )
