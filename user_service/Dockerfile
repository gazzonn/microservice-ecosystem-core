FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY user_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "user_service.app.main:app", "--host", "0.0.0.0", "--port", "8003"]
