import uuid
import shutil
from datetime import datetime
from fastapi import UploadFile
from pathlib import Path

from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.workers.tasks import process_transaction_async


def submit_transaction_file(file: UploadFile, repo: TransactionRepository) -> uuid.UUID:
    """
    Submit a transaction file to the system.

    Args:
        file: The uploaded file containing the transaction data.
        repo: The repository for storing the transaction data.

    Returns:
        The ID of the created transaction.
    """

    transaction_id = uuid.uuid4()

    temp_dir = Path("/tmp/transactions")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file_path = temp_dir / f"{transaction_id}.csv"

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    repo.create_transaction(
        id=transaction_id,
        created_at=datetime.utcnow(),
        status="pending"
    )

    process_transaction_async.delay(str(transaction_id), str(temp_file_path))

    return transaction_id
