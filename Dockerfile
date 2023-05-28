FROM ubuntu:latest

# Установка зависимостей
RUN apt update && apt install -y python3 python3-pip

# Копирование скрипта парсинга в контейнер
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Запуск скрипта при старте контейнера
CMD ["python3", "/app/main.py"]

