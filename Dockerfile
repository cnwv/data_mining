FROM alpine:latest

# Установка зависимостей
RUN apk update && apk add --no-cache python3 py3-pip
RUN pip3 install pymongo

# Копирование скрипта парсинга в контейнер
COPY main.py /app/

# Запуск скрипта при старте контейнера
CMD ["python3", "/app/main.py.py"]

