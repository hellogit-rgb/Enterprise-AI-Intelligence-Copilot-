FROM python:3.11-slim

WORKDIR /app
COPY ai-service/requirements-docker.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ai-service/app ./app
COPY evaluation ./evaluation

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
