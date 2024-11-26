# Використовуємо офіційний образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект
COPY .. /app/

# Відкриваємо порт для Django
EXPOSE 8000

# Запускаємо сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]