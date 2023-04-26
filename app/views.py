from flask import request
from flask import render_template

from app import app
from app.models import Event, Sensor

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/all_events')
def show_all_events():
    try:
        events = Event.query.all()
        return render_template('all_events.html', 
                               events=events)
    except:
        return render_template('index.html')
    

@app.route('/all_events/<int:id>')
def events_pagination(id):
    try:
        event = Event.query.get(id)
        return render_template('event_info.html', 
                            event=event)
    except:
        error = 'Ошибка базы данных'
        return render_template('event_info.html',
                               error=error)


@app.route('/all_sensors')
def show_all_sensors():
    try:
        sensors = Sensor.query.all()
        return render_template('all_sensors.html', 
                               sensors=sensors)
    except:
        return render_template('index.html')


@app.route('/all_sensors/<int:id>')
def get_events_from_sensor(id):
    try:
        sensor = Sensor.query.get(id)
        events = Event.query.\
                    filter_by\
                    (sensor_id = id)\
                    .all()
        return render_template('get_sensor_events.html', 
                            events=events, 
                            sensor=sensor)
    except:
        error = 'Ошибка базы данных'
        return render_template('get_sensor_events.html',
                               error=error)


@app.route('/filter', methods=["GET", "POST"])
def filter():
    try:
        if request.method == 'POST':
            temperature = request.form.get('temperature')
            humidity = request.form.get('humidity')
            if temperature and humidity:
                filtered_events = Event\
                                .query\
                                .filter(Event.temperature == temperature or\
                                        Event.humidity == humidity)\
                                .all()
                return render_template('filtered_events.html',\
                                        events=filtered_events,\
                                        temperature=temperature,\
                                        humidity=humidity)
            if temperature:
                filtered_events = Event\
                                .query\
                                .filter(Event.temperature == temperature)\
                                .all()
                return render_template('filtered_events.html',\
                                        events=filtered_events,\
                                        temperature=temperature,\
                                        humidity=humidity)
            if humidity:
                filtered_events = Event\
                                .query\
                                .filter(Event.humidity == humidity)\
                                .all()
                return render_template('filtered_events.html',\
                                        events=filtered_events,\
                                        temperature=temperature,\
                                        humidity=humidity)
    except:
        error = 'Вы неправильно ввели значения. Введите значения типа INT'
        return render_template('filter.html', error=error)
    else:
        return render_template('filter.html')