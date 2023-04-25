1) Сначала вы должны создать в PostgreSQL базу данных с именем sensors_db или любое, в таком случае изменив PG_DATABASE_NAME в /app/config.py
2) Создайте файл /app/keys.py , туда занесите SECRET_KEY = "flask key", PG_PASSWORD = "your postgres password"
2) pip install -r requirements
3) Config.py поставить свои настройки 
4) python ./create_tables.py - создание таблиц в БД
5) flask db init, flask db migrate, flask db upgrade - миграции 
6) python ./run.py
