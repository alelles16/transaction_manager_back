from app.infrastructure.workers.celery_app import celery_app
from app.infrastructure.database.repository_impl import TransactionRepositoryImpl
from app.domain.models.transaction_status import TransactionStatus
import csv


def process_csv_file(file_path: str):
    """
    Process a CSV file and return the number of records, total debit, and total credit.
    """
    num_records = 0
    total_debit = 0
    total_credit = 0
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        expected_fields = {"id", "date", "type", "amount"}

        if set(reader.fieldnames or []) != expected_fields:
            raise ValueError("Invalid file format")

        for row in reader:
            try:
                amount = float(row["amount"])
                if row["type"] == "debit":
                    total_debit += amount
                elif row["type"] == "credit":
                    total_credit += amount
                else:
                    continue
                num_records += 1
            except (ValueError, KeyError):
                continue

    return num_records, total_debit, total_credit


@celery_app.task
def process_transaction_file_async(transaction_id: str, file_path: str):
    """
    Process a transaction file asynchronously.
    """
    repo = TransactionRepositoryImpl()
    try:
        transaction = repo.get_transaction(id=transaction_id)
        transaction.status = TransactionStatus.PROCESSING
        repo.update_transaction(transaction)

        num_records, total_debit, total_credit = process_csv_file(file_path)
        transaction.num_records = num_records
        transaction.total_debit = total_debit
        transaction.total_credit = total_credit
        transaction.status = TransactionStatus.DONE
        repo.update_transaction(transaction)
    except Exception as e:
        return f"Error processing transaction {transaction_id}: {e}"

    return f"Transaction {transaction_id} processed successfully!"
