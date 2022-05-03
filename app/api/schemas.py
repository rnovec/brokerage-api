from typing import List

from pydantic import BaseModel


class AccountSchema(BaseModel):
    cash: float


class AccountSchemaRead(BaseModel):
    id: int
    cash: float
    issuers: List[str] = []

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    timestamp: float
    operation: str
    issuer_name: str
    total_shares: int
    shared_price: float


class OrderSchemaItem(BaseModel):
    issuer_name: str
    total_shares: int
    shared_price: float

    class Config:
        orm_mode = True


class BalanceSchema(BaseModel):
    cash: float
    issuers: List[OrderSchemaItem] = []


class OperationSchemaResponse(BaseModel):
    current_balance: BalanceSchema
    business_errors: List[str] = []
