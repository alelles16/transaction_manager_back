from sqlalchemy import Column, Integer, Float, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from app.domain.models.transaction_status import TransactionStatus
import uuid
from datetime import datetime


Base = declarative_base()

class TransactionORM(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now())
    status = Column(SQLAlchemyEnum(TransactionStatus), default=TransactionStatus.PENDING)
    num_records = Column(Integer, default=0)
    total_debit = Column(Float, default=0.0)
    total_credit = Column(Float, default=0.0)
