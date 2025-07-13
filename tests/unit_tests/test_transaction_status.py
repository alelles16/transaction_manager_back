from app.domain.models.transaction_status import TransactionStatus


class TestTransactionStatus:
    """Test cases for the TransactionStatus enum."""

    def test_transaction_status_values(self):
        """Test that TransactionStatus has the expected values."""
        assert TransactionStatus.PENDING == "pending"
        assert TransactionStatus.PROCESSING == "processing"
        assert TransactionStatus.DONE == "done"

    def test_transaction_status_membership(self):
        """Test that TransactionStatus values are valid enum members."""
        assert "pending" in [status.value for status in TransactionStatus]
        assert "processing" in [status.value for status in TransactionStatus]
        assert "done" in [status.value for status in TransactionStatus]

    def test_transaction_status_iteration(self):
        """Test that we can iterate over TransactionStatus values."""
        statuses = list(status.value for status in TransactionStatus)
        expected_statuses = ["pending", "processing", "done"]

        assert len(statuses) == len(expected_statuses)
        for status in expected_statuses:
            assert status in statuses

    def test_transaction_status_string_representation(self):
        """Test string representation of TransactionStatus values."""
        assert str(TransactionStatus.PENDING.value) == "pending"
        assert str(TransactionStatus.PROCESSING.value) == "processing"
        assert str(TransactionStatus.DONE.value) == "done"

    def test_transaction_status_equality(self):
        """Test equality comparison of TransactionStatus values."""
        assert TransactionStatus.PENDING == TransactionStatus.PENDING
        assert TransactionStatus.PENDING != TransactionStatus.DONE
