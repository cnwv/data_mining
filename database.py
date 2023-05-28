from pymongo import MongoClient


class Database:
    def __init__(self):
        host = 'mongodb'  # или IP-адрес хоста, где запущен Docker
        port = 27017
        username = 'admin'
        password = 'password'
        self.db = MongoClient(host, port, username=username, password=password)["shinyprofi_parse_26_05"]['wheels']

    def insert_data(self, data):
        # проверяем есть ли в базе данные
        existing_data = self.db.find_one({'url': data['url']})
        if existing_data:
            print('Данные уже существуют в базе')
        else:
            self.db.insert_one(data)
            print('запись сохранена')

