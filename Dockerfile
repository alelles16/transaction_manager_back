FROM python:3.11-alpine

# Variables
ENV VIRTUAL_ENV=/py
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system and libraries needed for psycopg2
RUN apk update && apk add --no-cache \
    postgresql-client \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    build-base \
    && python -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy code
COPY . /app
WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]