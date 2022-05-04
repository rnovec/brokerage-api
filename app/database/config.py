import os

import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database.db")

engine = _sql.create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()


def get_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
