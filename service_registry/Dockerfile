FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY service_registry/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "service_registry.app.main:app", "--host", "0.0.0.0", "--port", "8004"]
