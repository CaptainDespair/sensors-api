from flask import Flask
from flask_migrate import Migrate

from app.models import db, Event, Sensor
from app.config import ProductiontConfig, DevelopementConfig

app = Flask(__name__)
app.config.from_object(DevelopementConfig)

db.init_app(app)
migrate = Migrate(app, db)

from app import views