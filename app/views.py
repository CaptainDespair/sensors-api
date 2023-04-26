from flask import request, render_template, redirect
from sqlalchemy.exc import IntegrityError, PendingRollbackError


from app import app, db
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
    

@app.route('/all_events/<int:id>', methods=["GET", "POST"])
def get_event_info(id):
    try:
        if request.method == "GET":
            event = Event.query.get(id)
            return render_template('event_info.html', 
                                event=event)
        if request.method == 'POST':
            event_id = request.form.get('delete_event')
            event = Event.query.get(event_id)
            db.session.delete(event)
            db.session.commit()
            done_message = 'Событие удалено'
            return render_template('all_events.html',\
                                   done_message=done_message)
        else:
            return render_template('all_events.html')
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


@app.route('/all_sensors/<int:id>', methods=["GET", "POST"])
def get_events_from_sensor(id):
    try:
        if request.method == 'GET':
            sensor = Sensor.query.get(id)
            events = Event.query.\
                        filter_by\
                        (sensor_id = id)\
                        .all()
            return render_template('get_sensor_events.html', 
                                events=events, 
                                sensor=sensor)
        if request.method == 'POST':
            sensor_id = request.form.get('delete_sensor')
            sensor = Sensor.query.get(sensor_id)
            db.session.delete(sensor)
            db.session.commit()
            done_message = 'Датчик удален'
            return render_template('all_sensors.html',\
                                   done_message=done_message)
        else:
            return render_template('all_sensors.html')
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
    

@app.route('/create_sensor', methods=["GET", "POST"])
def create_sensor():
        try:
            if request.method == 'POST':
                name = request.form.get('name')
                type = request.form.get('type')
                new_sensor = Sensor(name=name, type=type)
                db.session.add(new_sensor)
                db.session.commit()
                success_message = f'Успешно добавлен сенсор {name}'
                return render_template('create_sensor.html',\
                                        success_message=success_message)
        except(IntegrityError, Exception) as error:
            if error == IntegrityError:
                get_max_id = Sensor\
                                .query\
                                .order_by(Sensor.id.desc())\
                                .first()
                max_id = get_max_id.id + 1
                new_sensor = Sensor(id = max_id, name=name, type=type)
                db.session.add(new_sensor)
                db.session.commit()
                success_message = f'Успешно добавлен датчик {name}'
                return render_template('create_sensor.html',\
                                       success_message=success_message)
            else:
                error_message = 'Ошибка базы данных.' 
                annotation = 'Поле "название" должно быть String, поле "тип" принимает 1, 2 или 3'
                return render_template('create_sensor.html',\
                                       error_message=error_message,
                                       annotation=annotation)
        else:
            return render_template('create_sensor.html')
        

@app.route('/create_event', methods=["GET", "POST"])
def create_event():
    try:
        if request.method == 'POST':
            sensor_id = request.form.get('sensor_id')
            name = request.form.get('name')
            temperature = request.form.get('temperature')
            humidity = request.form.get('humidity')
            new_event = Event(sensor_id=sensor_id,\
                                name=name,\
                                temperature=temperature,\
                                humidity=humidity)
            db.session.add(new_event)
            db.session.commit()
            success_message = f'Успешно добавлено событие {name}'
            return render_template('create_event.html',\
                                    success_message=success_message)
    except(IntegrityError, PendingRollbackError, Exception) as error:
        if error == IntegrityError:
            get_max_id = Event\
                            .query\
                            .order_by(Event.id.desc())\
                            .first()
            print('----------------')
            print(get_max_id.id)
            max_id = get_max_id.id + 1
            new_event = Event(id=max_id,\
                                sensor_id=sensor_id,\
                                name=name,\
                                temperature=temperature,\
                                humidity=humidity)
            db.session.add(new_event)
            db.session.commit()
            success_message = f'Успешно добавлено событие {name}'
            return render_template('create_event.html',\
                                    success_message=success_message)
        else:
            error_message = 'Ошибка базы данных.' 
            annotation = f'"sensor id": id существующего датчика,\
                        \n"название": String, "температура": INT, "влажность": INT'
            return render_template('create_event.html',\
                                    error_message=error_message,
                                    annotation=annotation)
    else:
        return render_template('create_event.html')
