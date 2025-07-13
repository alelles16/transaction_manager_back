from datetime import datetime
from app.domain.models.transaction_status import TransactionStatus
from app.application.use_cases.get_transaction import get_transaction
from app.application.use_cases.list_transactions import list_transactions
import uuid


class TestTransactionRepositoryIntegration:
    """Integration tests for the TransactionRepository with SQLite database."""

    def test_create_and_get_transaction(
        self, transaction_repository, sample_transaction
    ):
        """Test creating a transaction and then retrieving it."""
        # Arrange
        transaction_id = sample_transaction.id

        # Act - Create transaction
        transaction_repository.create_transaction(sample_transaction)

        # Act - Get transaction
        retrieved_transaction = transaction_repository.get_transaction(transaction_id)

        # Assert
        assert retrieved_transaction is not None
        assert retrieved_transaction.id == sample_transaction.id
        assert retrieved_transaction.created_at == sample_transaction.created_at
        assert retrieved_transaction.status == sample_transaction.status
        assert retrieved_transaction.num_records == sample_transaction.num_records
        assert retrieved_transaction.total_debit == sample_transaction.total_debit
        assert retrieved_transaction.total_credit == sample_transaction.total_credit

    def test_get_nonexistent_transaction(self, transaction_repository):
        """Test getting a transaction that doesn't exist."""
        # Arrange
        nonexistent_id = uuid.uuid4()

        # Act
        result = transaction_repository.get_transaction(nonexistent_id)

        # Assert
        assert result is None

    def test_update_transaction(self, transaction_repository, sample_transaction):
        """Test updating a transaction."""
        # Arrange
        transaction_repository.create_transaction(sample_transaction)

        # Update the transaction
        updated_transaction = sample_transaction
        updated_transaction.status = TransactionStatus.DONE
        updated_transaction.num_records = 15
        updated_transaction.total_debit = 300.0
        updated_transaction.total_credit = 250.0

        # Act
        transaction_repository.update_transaction(updated_transaction)

        # Assert
        retrieved_transaction = transaction_repository.get_transaction(
            sample_transaction.id
        )
        assert retrieved_transaction.status == TransactionStatus.DONE
        assert retrieved_transaction.num_records == 15
        assert retrieved_transaction.total_debit == 300.0
        assert retrieved_transaction.total_credit == 250.0

    def test_list_transactions_empty(self, transaction_repository):
        """Test listing transactions when database is empty."""
        # Act
        transactions = transaction_repository.list_transactions()

        # Assert
        assert transactions == []

    def test_list_transactions_multiple(
        self, transaction_repository, sample_transactions
    ):
        """Test listing multiple transactions."""
        # Arrange
        for transaction in sample_transactions:
            transaction_repository.create_transaction(transaction)

        # Act
        transactions = transaction_repository.list_transactions()

        # Assert
        assert len(transactions) == len(sample_transactions)

        # Verify all transactions are present
        transaction_ids = {t.id for t in transactions}
        expected_ids = {t.id for t in sample_transactions}
        assert transaction_ids == expected_ids

    def test_transaction_lifecycle(self, transaction_repository):
        """Test complete transaction lifecycle: create, update, retrieve."""
        # Arrange
        transaction_id = uuid.uuid4()
        created_at = datetime.now()

        # Create initial transaction
        initial_transaction = type(
            "Transaction",
            (),
            {
                "id": transaction_id,
                "created_at": created_at,
                "status": TransactionStatus.PENDING,
                "num_records": 0,
                "total_debit": 0.0,
                "total_credit": 0.0,
            },
        )()

        # Act & Assert - Create
        transaction_repository.create_transaction(initial_transaction)
        retrieved = transaction_repository.get_transaction(transaction_id)
        assert retrieved.status == TransactionStatus.PENDING
        assert retrieved.num_records == 0

        # Act & Assert - Update to processing
        processing_transaction = type(
            "Transaction",
            (),
            {
                "id": transaction_id,
                "created_at": created_at,
                "status": TransactionStatus.PROCESSING,
                "num_records": 5,
                "total_debit": 100.0,
                "total_credit": 50.0,
            },
        )()

        transaction_repository.update_transaction(processing_transaction)
        retrieved = transaction_repository.get_transaction(transaction_id)
        assert retrieved.status == TransactionStatus.PROCESSING
        assert retrieved.num_records == 5
        assert retrieved.total_debit == 100.0
        assert retrieved.total_credit == 50.0

        # Act & Assert - Update to done
        done_transaction = type(
            "Transaction",
            (),
            {
                "id": transaction_id,
                "created_at": created_at,
                "status": TransactionStatus.DONE,
                "num_records": 10,
                "total_debit": 200.0,
                "total_credit": 150.0,
            },
        )()

        transaction_repository.update_transaction(done_transaction)
        retrieved = transaction_repository.get_transaction(transaction_id)
        assert retrieved.status == TransactionStatus.DONE
        assert retrieved.num_records == 10
        assert retrieved.total_debit == 200.0
        assert retrieved.total_credit == 150.0


class TestUseCasesWithRepositoryIntegration:
    """Integration tests for use cases with the actual repository."""

    def test_get_transaction_use_case_integration(
        self, transaction_repository, sample_transaction
    ):
        """Test get_transaction use case with real repository."""
        # Arrange
        transaction_repository.create_transaction(sample_transaction)

        # Act
        result = get_transaction(sample_transaction.id, transaction_repository)

        # Assert
        assert result is not None
        assert result.id == sample_transaction.id
        assert result.status == sample_transaction.status

    def test_list_transactions_use_case_integration(
        self, transaction_repository, sample_transactions
    ):
        """Test list_transactions use case with real repository."""
        # Arrange
        for transaction in sample_transactions:
            transaction_repository.create_transaction(transaction)

        # Act
        result = list_transactions(transaction_repository)

        # Assert
        assert len(result) == len(sample_transactions)
        result_ids = {t.id for t in result}
        expected_ids = {t.id for t in sample_transactions}
        assert result_ids == expected_ids
