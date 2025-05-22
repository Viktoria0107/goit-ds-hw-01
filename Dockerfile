
# Базовий образ
FROM python:3.13-slim

# Робоча директорія в контейнері
WORKDIR /app

# Копіюємо файли проєкту
COPY . /app

# Встановлюємо залежності (poetry + залежності з pyproject.toml)
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Команда запуску
CMD ["python", "bot.py"]