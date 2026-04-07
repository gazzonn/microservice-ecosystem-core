FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY api_gateway/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "api_gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
