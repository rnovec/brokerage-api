from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.config import get_session

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
    order, account = controllers.create_order(db=db, payload=data, account_id=id)
    return schemas.OperationSchemaResponse(
        current_balance=schemas.BalanceSchema(
            cash=account.cash, issuers=account.orders
        ),
        business_errors=[],
    )
