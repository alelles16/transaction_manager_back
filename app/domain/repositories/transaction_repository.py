from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.domain.models.transaction import Transaction


class TransactionRepository(ABC):
    """
    Abstract base class for transaction repositories.
    """

    @abstractmethod
    def create_transaction(self, transaction: Transaction) -> None:
        """
        Create a new transaction.
        """
        pass

    @abstractmethod
    def update_transaction(self, transaction: Transaction) -> None:
        """
        Update an existing transaction.
        """
        pass

    @abstractmethod
    def get_transaction(self, id: UUID) -> Transaction:
        """
        Get a transaction by ID.
        """
        pass

    @abstractmethod
    def list_transactions(self) -> List[Transaction]:
        """
        Get all transactions.
        """
        pass
