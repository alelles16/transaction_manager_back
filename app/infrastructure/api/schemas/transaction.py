from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.domain.models.transaction_status import TransactionStatus


class TransactionResponse(BaseModel):
    id: UUID
    created_at: datetime
    status: TransactionStatus

    class Config:
        orm_mode = True
