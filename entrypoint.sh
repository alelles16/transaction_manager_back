#!/bin/sh

# Inicializar la base de datos
python -c "from app.infrastructure.database.init_db import init_db; init_db()"

# Ejecutar el servidor uvicorn
exec uvicorn app.infrastructure.api.main:app --host 0.0.0.0 --port 8000 --reload
