## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Nikita-Legostaev/warehouse.git   
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   poetry install
   poetry shell
   ```

3. Создайте файл `.env` на основе `.env.example` и настройте параметры:
   ```bash
   cp .env.example .env
   ```

4. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Откройте документацию API:
   ```
   http://localhost:8000/docs
   ```

### Запуск через Docker

1. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Сборка Docker-образа и контейнеров:
   ```bash
   docker build -t warehouse .
   docker-compose build
   ```

2. Запустите контейнеры:
   ```bash
   docker-compose up 
   ```

3. Откройте документацию API:
   ```
   http://localhost:8000/docs
   ```

## Тестирование

Запуск тестов:

```bash
pytest
```

Запуск с отчетом о покрытии:

```bash
pytest --cov=app 
```
