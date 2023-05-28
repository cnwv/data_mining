FROM alpine:latest

# Установка зависимостей
RUN apk update && apk add --no-cache python3 py3-pip

# Копирование скрипта парсинга в контейнер
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Запуск скрипта при старте контейнера
CMD ["python3", "/app/main.py"]

