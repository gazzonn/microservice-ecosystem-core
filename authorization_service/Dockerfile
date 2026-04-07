FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY authorization_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "authorization_service.app.main:app", "--host", "0.0.0.0", "--port", "8002"]
