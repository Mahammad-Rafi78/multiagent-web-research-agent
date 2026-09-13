FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY providers ./providers
COPY frontend ./frontend
COPY ui_server.py .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn ui_server:app --host 0.0.0.0 --port ${PORT}"]