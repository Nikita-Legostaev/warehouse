FROM python:3.12-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-interaction --no-root

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]