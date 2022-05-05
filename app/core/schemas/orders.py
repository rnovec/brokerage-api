from typing import List

from pydantic import BaseModel, validator


class OrderSchema(BaseModel):
    timestamp: float
    operation: str
    issuer_name: str
    total_shares: int
    shared_price: float

    @validator("total_shares")
    def total_shares_must_be_gt_zero(cls, value, values, **kwargs):
        if value <= 0:
            raise ValueError("Shares must be greater than zero")
        return value

    @validator("shared_price")
    def shared_price_must_be_gt_zero(cls, value, values, **kwargs):
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        return value


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
