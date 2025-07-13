from fastapi import APIRouter, UploadFile, Depends
from app.infrastructure.api.schemas.transaction import TransactionResponse
from app.infrastructure.database.repository_impl import TransactionRepositoryImpl
from app.application.use_cases.submit_transaction import submit_transaction_file

router = APIRouter()

@router.post("/transactions/upload")
def upload_transaction_file(
    file: UploadFile,
    repo: TransactionRepositoryImpl = Depends(TransactionRepositoryImpl)
) -> TransactionResponse:
    transaction = submit_transaction_file(file, repo)
    return TransactionResponse(
        id=transaction.id,
        created_at=transaction.created_at,
        status=transaction.status
    )
