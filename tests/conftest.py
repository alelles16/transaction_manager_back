import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.models import Base


@pytest.fixture(scope="function")
def sqlite_db():
    """Create a temporary SQLite database for testing."""
    # Create a temporary file for the database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()

    # Create SQLite engine
    database_url = f"sqlite:///{temp_db.name}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield {
        "engine": engine,
        "session_factory": TestingSessionLocal,
        "db_path": temp_db.name,
    }

    # Cleanup: remove the temporary database file
    engine.dispose()
    os.unlink(temp_db.name)


@pytest.fixture(scope="function")
def transaction_repository(sqlite_db):
    """Create a transaction repository with SQLite database."""
    from app.infrastructure.database.repository_impl import TransactionRepositoryImpl

    repo = TransactionRepositoryImpl(session_factory=sqlite_db["session_factory"])
    yield repo


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing."""
    from app.domain.models.transaction import Transaction
    from app.domain.models.transaction_status import TransactionStatus
    from datetime import datetime
    import uuid

    return Transaction(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        status=TransactionStatus.PENDING,
        num_records=0,
        total_debit=0.0,
        total_credit=0.0,
    )


@pytest.fixture
def sample_transactions():
    """Create multiple sample transactions for testing."""
    from app.domain.models.transaction import Transaction
    from app.domain.models.transaction_status import TransactionStatus
    from datetime import datetime
    import uuid

    return [
        Transaction(
            id=uuid.uuid4(),
            created_at=datetime.now(),
            status=TransactionStatus.PENDING,
            num_records=5,
            total_debit=100.0,
            total_credit=50.0,
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at=datetime.now(),
            status=TransactionStatus.DONE,
            num_records=10,
            total_debit=200.0,
            total_credit=150.0,
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at=datetime.now(),
            status=TransactionStatus.PROCESSING,
            num_records=0,
            total_debit=0.0,
            total_credit=0.0,
        ),
    ]
