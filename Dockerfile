FROM python:3.10-slim

# Встановлення системних бібліотек
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt /app/

# Встановлення Python-залежностей
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копіюємо проект
COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]