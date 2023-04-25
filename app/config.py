import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = 'secret'
    DB_NAME = 'postgresql'
    PG_USER = 'postgres'
    PG_PASSWORD = '1234'
    PG_HOST = 'localhost'
    PG_DATABASE_NAME = 'sensors_db'
    SQLALCHEMY_DATABASE_URI = f'{DB_NAME}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE_NAME}'


class DevelopementConfig(BaseConfig):
    DEBUG = True


class ProductiontConfig(BaseConfig):
    DEBUG = False