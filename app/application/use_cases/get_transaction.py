from uuid import UUID
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.models.transaction import Transaction


def get_transaction(transaction_id: UUID, repo: TransactionRepository) -> Transaction:
    return repo.get_transaction(transaction_id)
