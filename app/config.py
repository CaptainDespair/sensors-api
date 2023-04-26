import os
from app.keys import PG_PASSWORD, SECRET_KEY

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DB_NAME = 'postgresql'
    PG_USER = 'postgres'
    PG_PASSWORD = PG_PASSWORD
    PG_HOST = 'localhost'
    PG_DATABASE_NAME = 'sensors_db'
    SECRET_KEY = SECRET_KEY
    ALLOWED_EXTENSIONS = {'json'}
    UPLOAD_FOLDER = os.path.join('json')
    SQLALCHEMY_DATABASE_URI = f'{DB_NAME}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE_NAME}'


class DevelopementConfig(BaseConfig):
    DEBUG = True


class ProductiontConfig(BaseConfig):
    DEBUG = False