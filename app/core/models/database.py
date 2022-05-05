import enum
from datetime import datetime

import sqlalchemy as _sql
from sqlalchemy.orm import relationship

from .config import Base


class Account(Base):
    __tablename__ = "accounts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    cash = _sql.Column(_sql.Float, nullable=False, default=0)
    created_at = _sql.Column(_sql.DateTime, default=datetime.utcnow)
    orders = relationship("Order")


class Order(Base):
    __tablename__ = "orders"

    class Operations(enum.Enum):
        BUY = 1
        SELL = 2

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    account_id = _sql.Column(_sql.Integer, _sql.ForeignKey("accounts.id"))
    _timestamp = _sql.Column(_sql.DateTime)
    operation = _sql.Column(_sql.Enum(Operations))
    issuer_name = _sql.Column(_sql.String(10))
    total_shares = _sql.Column(_sql.SmallInteger)
    shared_price = _sql.Column(_sql.Float)
    created_at = _sql.Column(_sql.DateTime, default=datetime.utcnow)

    @property
    def timestamp(self):
        return datetime.timestamp(self._timestamp)

    @timestamp.setter
    def timestamp(self, ts):
        self._timestamp = datetime.fromtimestamp(ts)
