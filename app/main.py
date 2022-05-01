import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.database.config import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Brokerage API", version="1.0.0", openapi_prefix="")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
