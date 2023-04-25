from app import app
from flask import render_template
from app.models import Event, Sensor

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/all_events')
def show_all_events():
    try:
        events = Event.query.all()
        return render_template('all_events.html', events=events)
    except:
        return render_template('index.html')
    

@app.route('/all_events/<int:id>')
def events_pagination(id):
    event = Event.query.get(id)
    return render_template('event_info.html', event=event)


@app.route('/all_sensors')
def show_all_sensors():
    try:
        sensors = Sensor.query.all()
        return render_template('all_sensors.html', sensors=sensors)
    except:
        return render_template('index.html')


@app.route('/all_sensors/<int:id>')
def get_events_from_sensor(id):
    sensor = Sensor.query.get(id)
    events = Event.query.filter_by(sensor_id = id).all()
    return render_template('get_events.html', events=events, sensor=sensor)

