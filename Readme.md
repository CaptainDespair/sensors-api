# sensors-api

Данное Flask web-приложение представляет собой API для CRUD-методов датчиков и зависимых событий. 

Взаимодействие моделей происходит соответствующим образом: 
![image](https://user-images.githubusercontent.com/105984453/234718178-114d5126-2a88-4fb3-83fd-c19b9637f384.png)

Реализованы следующие задачи: 
- CRUD операции для событий;
- CRUD операции для датчиков;
- Пагинация для событий;
- Получение всех событий для конкретного датчика;
- Фильтрацию событий по ***temperature*** и ***humidity***;
- Выгрузка данных событий из JSON-файла в базу данных (если файл не *.JSON, либо поля не соответствуют, либо sensor_id не существует, запись события не произойдет);

# Структура проекта
- /app - папка приложения, где находятся 
  - /templates (html+jinja)
  - config для настроек БД и Flask
  - models(таблицы sensors и events)
  - views - логика и url's API 
- /json - папка, в которой будут находиться загруженные events.json
- create_tables.py - скрипт, который создает таблицы в базе данных, если все корректно в подключено к Postgres в config
- в /app/__init__.py реализованы Migrate функции, которые можно вызвать посрдеством комманд, если структура моделей поменяется:
  - flask db init
  - flask db migrate
  - flask db upgrade
  
# Скрытая структура проекта:
- В /app.py лежит файл keys.py, его необходимо создать, чтобы внести следующие переменные:
  - SECRET_KEY = "flask key"
  - PG_PASSWORD = "your postgres password"

# Запуск приложения
1) Сначала вы должны создать в PostgreSQL базу данных с именем sensors_db или любое, в таком случае изменив PG_DATABASE_NAME в /app/config.py
2) Создайте файл /app/keys.py , туда занесите SECRET_KEY = "flask key", PG_PASSWORD = "your postgres password"
3) >pip install -r requirements
4) в /app/config.py поставить свои настройки 
5) >python ./create_tables.py - создание таблиц в БД
6)  >python ./run.py

# Стек
- Python3.9
  - Flask
  - jinja2
  - SQLAlchemy
  - psycopg2
  - json
- Postgres

