FROM python:3.12-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY src/ /app/src/

# Segurança: Cria usuário não-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PYTHONPATH=/app/src