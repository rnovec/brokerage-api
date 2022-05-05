import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

from app.core.settings import settings

engine = _sql.create_engine(settings.database_uri)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base(engine)


def get_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
