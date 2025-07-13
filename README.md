# 💸 Transaction Manager - FastAPI

This project is a **Transaction Manager** built with **FastAPI** and following **Repository pattern** principles. It allows you to process CSV transaction files, store and query transaction data, and execute asynchronous tasks with Celery and Redis.

---

## 📌 Features

- ✅ Process CSV transaction files.
- ✅ Store and query transactions in PostgreSQL.
- ✅ Asynchronous tasks with Celery and Redis.
- ✅ RESTful API documented with Swagger/OpenAPI.
- ✅ Clean architecture: domain, application, infrastructure.
- ✅ Orchestration with Docker and Docker Compose.

---

## ⚙️ Requirements

- Python 3.11+
- Docker + Docker Compose
- PostgreSQL
- Redis

---

## ⚙️ Setup

1. **Clone the repository:**

```bash
git clone https://github.com/alelles16/transaction_manager_back
cd transaction_manager_back
```

2. **Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Copy `.env.example` to `.env` and adjust values if needed.


---

## 🐳 Running with Docker

1. **Build and start the services:**

```bash
docker-compose build
docker-compose up
```

This will start:
- FastAPI backend
- Celery worker
- Flower (Celery task monitor) at [http://localhost:5555](http://localhost:5555)
- PostgreSQL
- Redis

---

## 🧪 Testing the API

Swagger/OpenAPI documentation is available at:

🔗 [http://localhost:8000/docs](http://localhost:8000/docs)

You can interact with all endpoints from the Swagger UI.

---

## 📬 Available Endpoints

### Transactions

| Method | Endpoint                        | Description                        |
|--------|----------------------------------|------------------------------------|
| POST   | `/transactions/upload`          | Upload and process a CSV file      |
| GET    | `/transactions/{id}`            | Get a transaction by ID            |
| GET    | `/transactions/`                | List all transactions              |

---

## 🧹 Code Style & Formatting

### Run flake8 (linting):

```bash
flake8 .
```

### Run black (code formatter):

```bash
black .
```

---

## 📁 Project Structure

```
transaction_manager_back/
├── app/
│   ├── application/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── models/
│   │   └── repositories/
│   └── infrastructure/
│       ├── api/
│       ├── database/
│       ├── workers/
├── entrypoint.sh
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
```

---

## 🚀 Notes

- Make sure PostgreSQL and Redis are running on the default ports if running locally.
- Flower is available at [http://localhost:5555](http://localhost:5555) to monitor Celery tasks.
