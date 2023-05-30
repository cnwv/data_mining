FROM python3.9:latest

# Установка зависимостей
# RUN python3:latest

# Копирование скрипта парсинга в контейнер
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Запуск скрипта при старте контейнера
CMD ["python3", "/app/main.py"]
# или RUN python3 main.py
