from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.constants import (
    CLOSED_MARKET_ERROR_KEY,
    DUPLICATED_OPERATION_ERROR_KEY,
    INSUFFICIENT_FUNDS_ERROR_KEY,
    INSUFFICIENT_STOCKS_ERROR_KEY,
    INVALID_OPERATION_ERROR_KEY,
)
from app.common.exceptions import (
    ClosedMarketException,
    DuplicatedOperationException,
    InsufficentFundsException,
    InsufficentStocksException,
    InvalidOperationException,
)
from app.core import schemas
from app.core.models import Account, get_session

from . import controllers

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
    issuers = []
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

    if not business_errors:
        issuers = controllers.get_issuers(db=db, account_id=account.id)
    return schemas.OperationSchemaResponse(
        current_balance=schemas.BalanceSchema(
            cash=account.cash,
            issuers=issuers,
        ),
        business_errors=business_errors,
    )
