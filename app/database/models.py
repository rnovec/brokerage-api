from datetime import datetime

import sqlalchemy as _sql

from .config import Base


class Account(Base):
    __tablename__ = "accounts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    cash = _sql.Column(_sql.Float, nullable=False, default=0)
    created_at = _sql.Column(_sql.DateTime, default=datetime.utcnow)
