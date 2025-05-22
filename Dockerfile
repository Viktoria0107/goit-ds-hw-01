# 1. Базовий образ
FROM python:3.12-slim

# 2. Робоча директорія всередині контейнера
WORKDIR /app

# 3. Копіюємо файли, необхідні для встановлення залежностей
COPY pyproject.toml poetry.lock ./

# 4. Встановлюємо Poetry
RUN pip install poetry

# 5. Інсталюємо залежності (без створення додаткового venv)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# 6. Копіюємо весь проєкт
COPY . .

# 7. Точка входу — запускаємо твій CLI-скрипт
ENTRYPOINT ["python", "bot.py"]
