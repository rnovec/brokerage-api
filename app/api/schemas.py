from typing import List, Optional

from pydantic import BaseModel


class AccountSchema(BaseModel):
    cash: float


class AccountSchemaRead(BaseModel):
    id: int
    cash: float
    issuers: List[str] = []

    class Config:
        orm_mode = True
