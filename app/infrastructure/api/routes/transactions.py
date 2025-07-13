from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.infrastructure.api.schemas.transaction import (
    TransactionResponse,
    TransactionAllResponse,
)
from app.infrastructure.database.repository_impl import TransactionRepositoryImpl
from app.application.use_cases.submit_transaction import submit_transaction_file
from app.application.use_cases.get_transaction import get_transaction
from app.application.use_cases.list_transactions import list_transactions
from typing import List

router = APIRouter()


def get_transaction_repository():
    return TransactionRepositoryImpl()


@router.post("/transactions/upload")
def upload_transaction_file(
    file: UploadFile,
    repo: TransactionRepositoryImpl = Depends(get_transaction_repository),
) -> TransactionResponse:
    transaction = submit_transaction_file(file, repo)
    return TransactionResponse(
        id=transaction.id, created_at=transaction.created_at, status=transaction.status
    )


@router.get("/transactions/{transaction_id}")
def get_transaction_by_id(
    transaction_id: str,
    repo: TransactionRepositoryImpl = Depends(get_transaction_repository),
) -> TransactionAllResponse:
    transaction = get_transaction(transaction_id, repo)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionAllResponse(
        id=transaction.id,
        created_at=transaction.created_at,
        status=transaction.status,
        num_records=transaction.num_records,
        total_debit=transaction.total_debit,
        total_credit=transaction.total_credit,
    )


@router.get("/transactions")
def get_all_transactions(
    repo: TransactionRepositoryImpl = Depends(get_transaction_repository),
) -> List[TransactionAllResponse]:
    transactions = list_transactions(repo)
    return [
        TransactionAllResponse(
            id=transaction.id,
            created_at=transaction.created_at,
            status=transaction.status,
            num_records=transaction.num_records,
            total_debit=transaction.total_debit,
            total_credit=transaction.total_credit,
        )
        for transaction in transactions
    ]
