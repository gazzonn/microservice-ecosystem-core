FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY demo_microservice/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "demo_microservice.app.main:app", "--host", "0.0.0.0", "--port", "8005"]
