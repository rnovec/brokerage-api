import os

import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from app.api import api_router
from app.database.config import Base, engine

from .settings import settings

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Brokerage API",
    version="1.0.0",
    openapi_prefix=settings.openapi_prefix,
    openapi_url=settings.openapi_url,
)

app.include_router(api_router)

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
