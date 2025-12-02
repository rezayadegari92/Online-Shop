FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=1 PIP_DEFAULT_TIMEOUT=120 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Minimal runtime/build libs for Pillow (jpeg,zlib) and stable networking
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libjpeg62-turbo zlib1g ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --default-timeout=120 -r requirements.txt

COPY . .

# Create media directory if it doesn't exist
RUN mkdir -p /app/media

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]