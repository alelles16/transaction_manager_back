from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from app.domain.models.transaction_status import TransactionStatus


@dataclass
class Transaction:
    """
    Represents a transaction in the system.

    Attributes:
        id: The unique identifier for the transaction.
        created_at: The timestamp when the transaction was created.
        status: The current status of the transaction.
    """

    id: UUID
    created_at: datetime
    status: TransactionStatus = TransactionStatus.PENDING
    num_records: int = 0
    total_debit: float = 0.0
    total_credit: float = 0.0
