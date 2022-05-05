from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.models import Account, Order


def get_memory_db():
    engine = create_engine("sqlite:///:memory:")
    db_session = sessionmaker(bind=engine)
    Account.metadata.create_all(engine)
    Order.metadata.create_all(engine)
    return db_session()
