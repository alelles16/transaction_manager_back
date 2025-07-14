from pydantic import BaseModel, computed_field, field_serializer
from uuid import UUID
from datetime import datetime
from app.domain.models.transaction_status import TransactionStatus


class TransactionResponse(BaseModel):
    id: UUID
    created_at: datetime
    status: TransactionStatus

    @computed_field
    @property
    def created_at_formatted(self) -> str:
        return self.created_at.strftime("%d/%m/%Y")

    @field_serializer('created_at')
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%d/%m/%Y")

    class Config:
        orm_mode = True


class TransactionAllResponse(BaseModel):
    id: UUID
    created_at: datetime
    status: TransactionStatus
    num_records: int
    total_debit: float
    total_credit: float

    @field_serializer('created_at')
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%d/%m/%Y")

    class Config:
        orm_mode = True
