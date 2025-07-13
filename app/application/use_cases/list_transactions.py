from typing import List
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.models.transaction import Transaction


def list_transactions(repo: TransactionRepository) -> List[Transaction]:
    return repo.list_transactions()
