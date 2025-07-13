from datetime import datetime
from app.domain.models.transaction import Transaction
from app.domain.models.transaction_status import TransactionStatus
import uuid


class TestTransactionModel:
    """Test cases for the Transaction domain model."""

    def test_create_transaction_with_defaults(self):
        """Test creating a transaction with default values."""
        transaction_id = uuid.uuid4()
        created_at = datetime.now()

        transaction = Transaction(id=transaction_id, created_at=created_at)

        assert transaction.id == transaction_id
        assert transaction.created_at == created_at
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.num_records == 0
        assert transaction.total_debit == 0.0
        assert transaction.total_credit == 0.0

    def test_create_transaction_with_all_values(self):
        """Test creating a transaction with all values specified."""
        transaction_id = uuid.uuid4()
        created_at = datetime.now()
        status = TransactionStatus.DONE
        num_records = 10
        total_debit = 150.50
        total_credit = 100.25

        transaction = Transaction(
            id=transaction_id,
            created_at=created_at,
            status=status,
            num_records=num_records,
            total_debit=total_debit,
            total_credit=total_credit,
        )

        assert transaction.id == transaction_id
        assert transaction.created_at == created_at
        assert transaction.status == status
        assert transaction.num_records == num_records
        assert transaction.total_debit == total_debit
        assert transaction.total_credit == total_credit

    def test_transaction_equality(self):
        """Test that two transactions with same values are equal."""
        transaction_id = uuid.uuid4()
        created_at = datetime.now()

        transaction1 = Transaction(
            id=transaction_id, created_at=created_at, status=TransactionStatus.PENDING
        )

        transaction2 = Transaction(
            id=transaction_id, created_at=created_at, status=TransactionStatus.PENDING
        )

        assert transaction1 == transaction2

    def test_transaction_inequality(self):
        """Test that two transactions with different values are not equal."""
        transaction_id1 = uuid.uuid4()
        transaction_id2 = uuid.uuid4()
        created_at = datetime.now()

        transaction1 = Transaction(
            id=transaction_id1, created_at=created_at, status=TransactionStatus.PENDING
        )

        transaction2 = Transaction(
            id=transaction_id2, created_at=created_at, status=TransactionStatus.PENDING
        )

        assert transaction1 != transaction2

    def test_transaction_string_representation(self):
        """Test the string representation of a transaction."""
        transaction_id = uuid.uuid4()
        created_at = datetime.now()

        transaction = Transaction(
            id=transaction_id, created_at=created_at, status=TransactionStatus.PENDING
        )

        str_repr = str(transaction)
        assert str(transaction_id) in str_repr
        assert "PENDING" in str_repr
