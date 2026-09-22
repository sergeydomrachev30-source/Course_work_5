FROM python:3.12-slim

# Базовые настройки Python и отключение виртуальных окружений внутри Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Устанавливаем Poetry напрямую через pip
RUN pip install --no-cache-dir poetry==1.8.2

# Копируем файл описания проекта
COPY pyproject.toml ./

# Устанавливаем чистые зависимости проекта без лишних флагов групп
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем весь остальной код проекта
COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
