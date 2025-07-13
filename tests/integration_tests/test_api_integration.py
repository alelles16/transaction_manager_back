import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from app.infrastructure.api.main import app
from app.infrastructure.api.routes import transactions
import uuid


class TestAPIIntegration:
    """Integration tests for the API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository for testing."""
        return Mock()

    def test_get_transaction_endpoint_success(
        self, client, mock_repository, sample_transaction
    ):
        """Test successful GET /transactions/{transaction_id} endpoint."""
        # Arrange
        mock_repository.get_transaction.return_value = sample_transaction
        app.dependency_overrides[transactions.get_transaction_repository] = (
            lambda: mock_repository
        )

        # Act
        response = client.get(f"/transactions/{sample_transaction.id}")
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_transaction.id)
        assert data["status"] == sample_transaction.status
        assert data["num_records"] == sample_transaction.num_records
        assert data["total_debit"] == sample_transaction.total_debit
        assert data["total_credit"] == sample_transaction.total_credit

    def test_get_transaction_endpoint_not_found(self, client, mock_repository):
        """Test GET /transactions/{transaction_id} endpoint when transaction not found."""
        # Arrange
        transaction_id = uuid.uuid4()
        mock_repository.get_transaction.return_value = None
        app.dependency_overrides[transactions.get_transaction_repository] = (
            lambda: mock_repository
        )

        # Act
        response = client.get(f"/transactions/{transaction_id}")
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_list_transactions_endpoint_success(
        self, client, mock_repository, sample_transactions
    ):
        """Test successful GET /transactions endpoint."""
        # Arrange
        mock_repository.list_transactions.return_value = sample_transactions
        app.dependency_overrides[transactions.get_transaction_repository] = (
            lambda: mock_repository
        )

        # Act
        response = client.get("/transactions")
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(sample_transactions)

        # Verify first transaction
        first_transaction = data[0]
        assert "id" in first_transaction
        assert "status" in first_transaction
        assert "num_records" in first_transaction
        assert "total_debit" in first_transaction
        assert "total_credit" in first_transaction

    def test_list_transactions_endpoint_empty(self, client, mock_repository):
        """Test GET /transactions endpoint when no transactions exist."""
        # Arrange
        mock_repository.list_transactions.return_value = []
        app.dependency_overrides[transactions.get_transaction_repository] = (
            lambda: mock_repository
        )

        # Act
        response = client.get("/transactions")
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch(
        "app.application.use_cases.submit_transaction.process_transaction_file_async"
    )
    @patch("app.application.use_cases.submit_transaction.Path")
    @patch("app.application.use_cases.submit_transaction.shutil")
    def test_submit_transaction_endpoint_success(
        self, mock_shutil, mock_path, mock_celery_task, client, mock_repository
    ):
        """Test successful POST /transactions endpoint."""
        # Arrange
        mock_file = Mock()
        mock_file.file = Mock()

        mock_temp_dir = MagicMock()
        mock_path.return_value = mock_temp_dir
        mock_temp_file_path = MagicMock()
        mock_temp_dir.__truediv__.return_value = mock_temp_file_path

        # Create a mock file content
        file_content = b"test,data,here"
        app.dependency_overrides[transactions.get_transaction_repository] = (
            lambda: mock_repository
        )

        # Act
        response = client.post(
            "/transactions/upload",
            files={"file": ("test.csv", file_content, "text/csv")},
        )
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        assert "id" in data
        assert (
            data["status"] == mock_repository.create_transaction.call_args[0][0].status
        )

        # Verify repository was called
        mock_repository.create_transaction.assert_called_once()

        # Verify celery task was called
        mock_celery_task.delay.assert_called_once()

    def test_submit_transaction_endpoint_no_file(self, client):
        """Test POST /transactions endpoint without file."""
        # Act
        response = client.post("/transactions/upload")
        app.dependency_overrides = {}

        # Assert
        assert response.status_code == 422  # Validation error
