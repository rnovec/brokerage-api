import sqlalchemy as _sql

from .config import Base


class User(Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
