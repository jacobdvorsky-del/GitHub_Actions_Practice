# Stage 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /app
COPY flask_app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.14-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY flask_app/ .
RUN adduser --disabled-password --no-create-home appuser
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]