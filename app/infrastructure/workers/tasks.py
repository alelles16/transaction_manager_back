from app.infrastructure.workers.celery_app import celery_app

@celery_app.task
def process_transaction_async(transaction_id: str, file_path: str):
    print(f"Procesando transacción {transaction_id} con archivo {file_path}")
