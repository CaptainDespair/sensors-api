from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class Sensor(db.Model):

    __tablename__ = 'sensors'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
   
    name = db.Column(
        db.String(128),
    )

    type = db.Column(
        db.Enum("1", "2", "3", name='limited_types')
    )

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f'<Sensor {self.name}>'


class Event(db.Model):

    __tablename__ ='events'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    
    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey('sensors.id', ondelete='CASCADE'),
        nullable=False,
    )

    name = db.Column(
        db.String(128),
    )

    temperature = db.Column(
        db.Integer,
    )

    humidity = db.Column(
        db.Integer,
    )

    def __init__(self, sensor_id, name, temperature, humidity):
        self.sensor_id = sensor_id
        self.name = name
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return f'<Event {self.name}>'