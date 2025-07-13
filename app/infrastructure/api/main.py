from fastapi import FastAPI
from app.infrastructure.api.routes import transactions

app = FastAPI()
app.include_router(transactions.router)
