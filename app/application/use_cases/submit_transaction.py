import uuid
import shutil
from datetime import datetime
from fastapi import UploadFile
from pathlib import Path

from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.workers.tasks.transaction_tasks import process_transaction_file_async
from app.domain.models.transaction import Transaction
from app.domain.models.transaction_status import TransactionStatus


def submit_transaction_file(file: UploadFile, repo: TransactionRepository) -> Transaction:
    """
    Submit a transaction file to the system.

    Args:
        file: The uploaded file containing the transaction data.
        repo: The repository for storing the transaction data.

    Returns:
        The created transaction.
    """

    transaction_id = uuid.uuid4()

    temp_dir = Path("/tmp/transactions")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file_path = temp_dir / f"{transaction_id}.csv"

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transaction = Transaction(
        id=transaction_id,
        created_at=datetime.now(),
        status=TransactionStatus.PENDING
    )
    repo.create_transaction(transaction)

    process_transaction_file_async.delay(str(transaction_id), str(temp_file_path))

    return transaction
