from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.config import get_session

from . import controllers, schemas

router = APIRouter()


@router.post("/accounts", response_model=schemas.AccountSchemaRead, status_code=201)
def create_account(data: schemas.AccountSchema, db: Session = Depends(get_session)):
    return controllers.create_account(db=db, payload=data)
