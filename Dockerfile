# 1. Базовый образ
FROM python:3.10-slim

# 2. Рабочая папка
WORKDIR /app

# 3. Скопировать и установить зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Скопировать весь код
COPY . .

# 5. Запуск через gunicorn на порту 5000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=1", "--threads=4"]