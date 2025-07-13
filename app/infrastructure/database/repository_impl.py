from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.database.models import TransactionORM
from app.infrastructure.database.session import SessionLocal
from app.domain.models.transaction import Transaction
from app.domain.models.transaction_status import TransactionStatus
from typing import List, Optional
from uuid import UUID


class TransactionRepositoryImpl(TransactionRepository):

    def create_transaction(self, transaction: Transaction) -> None:
        db = SessionLocal()
        try:
            transaction_orm = TransactionORM(
                id=transaction.id,
                created_at=transaction.created_at,
                status=transaction.status,
            )
            db.add(transaction_orm)
            db.commit()
        finally:
            db.close()

    def update_transaction(self, transaction: Transaction) -> None:
        db = SessionLocal()
        try:
            transaction_orm = (
                db.query(TransactionORM)
                .filter(TransactionORM.id == transaction.id)
                .first()
            )
            if transaction_orm:
                transaction_orm.status = transaction.status
                transaction_orm.num_records = transaction.num_records
                transaction_orm.total_debit = transaction.total_debit
                transaction_orm.total_credit = transaction.total_credit
                db.commit()
        finally:
            db.close()

    def get_transaction(self, id: UUID) -> Optional[Transaction]:
        db = SessionLocal()
        try:
            transaction_orm = (
                db.query(TransactionORM).filter(TransactionORM.id == id).first()
            )
            if transaction_orm is None:
                return None
            return Transaction(
                id=transaction_orm.id,
                created_at=transaction_orm.created_at,
                status=transaction_orm.status,
                num_records=transaction_orm.num_records,
                total_debit=transaction_orm.total_debit,
                total_credit=transaction_orm.total_credit,
            )
        finally:
            db.close()

    def list_transactions(self) -> List[Transaction]:
        db = SessionLocal()
        try:
            return [
                Transaction(
                    id=tx.id,
                    created_at=tx.created_at,
                    status=TransactionStatus(tx.status),
                    num_records=tx.num_records,
                    total_debit=tx.total_debit,
                    total_credit=tx.total_credit,
                )
                for tx in db.query(TransactionORM).all()
            ]
        finally:
            db.close()
