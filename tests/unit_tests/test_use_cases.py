import pytest
from unittest.mock import Mock, patch, MagicMock
from app.application.use_cases.get_transaction import get_transaction
from app.application.use_cases.list_transactions import list_transactions
from app.application.use_cases.submit_transaction import submit_transaction_file
from app.domain.models.transaction_status import TransactionStatus
import uuid


class TestGetTransactionUseCase:
    """Test cases for the get_transaction use case."""

    def test_get_transaction_success(self, sample_transaction):
        """Test successfully getting a transaction."""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_transaction.return_value = sample_transaction

        # Act
        result = get_transaction(sample_transaction.id, mock_repo)

        # Assert
        assert result == sample_transaction
        mock_repo.get_transaction.assert_called_once_with(sample_transaction.id)

    def test_get_transaction_not_found(self):
        """Test getting a transaction that doesn't exist."""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_transaction.return_value = None
        transaction_id = uuid.uuid4()

        # Act
        result = get_transaction(transaction_id, mock_repo)

        # Assert
        assert result is None
        mock_repo.get_transaction.assert_called_once_with(transaction_id)


class TestListTransactionsUseCase:
    """Test cases for the list_transactions use case."""

    def test_list_transactions_success(self, sample_transactions):
        """Test successfully listing transactions."""
        # Arrange
        mock_repo = Mock()
        mock_repo.list_transactions.return_value = sample_transactions

        # Act
        result = list_transactions(mock_repo)

        # Assert
        assert result == sample_transactions
        mock_repo.list_transactions.assert_called_once()

    def test_list_transactions_empty(self):
        """Test listing transactions when there are none."""
        # Arrange
        mock_repo = Mock()
        mock_repo.list_transactions.return_value = []

        # Act
        result = list_transactions(mock_repo)

        # Assert
        assert result == []
        mock_repo.list_transactions.assert_called_once()


class TestSubmitTransactionUseCase:
    """Test cases for the submit_transaction_file use case."""

    @patch(
        "app.application.use_cases.submit_transaction.process_transaction_file_async"
    )
    @patch("app.application.use_cases.submit_transaction.Path")
    @patch("app.application.use_cases.submit_transaction.shutil")
    def test_submit_transaction_success(
        self, mock_shutil, mock_path, mock_celery_task, sample_transaction
    ):
        """Test successfully submitting a transaction file."""
        # Arrange
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.file = Mock()

        # Mock Path and __truediv__
        mock_temp_dir = MagicMock()
        mock_path.return_value = mock_temp_dir
        mock_temp_file_path = MagicMock()
        mock_temp_dir.__truediv__.return_value = mock_temp_file_path

        # Act
        result = submit_transaction_file(mock_file, mock_repo)

        # Assert
        assert result.id is not None
        assert result.created_at is not None
        assert result.status == TransactionStatus.PENDING

        # Verify repository was called
        mock_repo.create_transaction.assert_called_once()

        # Verify file operations
        mock_shutil.copyfileobj.assert_called_once()

        # Verify celery task was called
        mock_celery_task.delay.assert_called_once()

    @patch(
        "app.application.use_cases.submit_transaction.process_transaction_file_async"
    )
    @patch("app.application.use_cases.submit_transaction.Path")
    @patch("app.application.use_cases.submit_transaction.shutil")
    def test_submit_transaction_repository_error(
        self, mock_shutil, mock_path, mock_celery_task
    ):
        """Test submitting a transaction when repository fails."""
        # Arrange
        mock_repo = Mock()
        mock_repo.create_transaction.side_effect = Exception("Database error")
        mock_file = Mock()
        mock_file.file = Mock()

        # Mock Path and __truediv__
        mock_temp_dir = MagicMock()
        mock_path.return_value = mock_temp_dir
        mock_temp_file_path = MagicMock()
        mock_temp_dir.__truediv__.return_value = mock_temp_file_path

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            submit_transaction_file(mock_file, mock_repo)

        # Verify celery task was not called
        mock_celery_task.delay.assert_not_called()
