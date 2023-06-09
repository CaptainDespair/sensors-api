import os
import json
from flask import request, render_template
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Event, Sensor


#menu
@app.route('/')
def index():
    return render_template('index.html')
       

#show all events with pagination by 5 objects
@app.route('/all_events')
def show_all_events():
    try:
        page = request.args.get('page', type=int, default=1)
        events = Event.query.paginate(page=page, per_page=5)
        return render_template('all_events.html', 
                               events=events)
    except:
        return render_template('index.html')
    
    
#show event details with method Delete 
@app.route('/all_events/<int:id>', methods=["GET", "POST"])
def get_event_info(id):
    try:
        if request.method == "GET":
            event = Event.query.get(id)
            return render_template('event_info.html', 
                                    event=event)
        elif request.method == 'POST':
            event_id = request.form.get('delete_event')
            event = Event.query.get(event_id)
            db.session.delete(event)
            db.session.commit()
            return render_template('all_events.html',
                                   event=event)
        else:
            return render_template('all_events.html')
    except:
        error = 'Событие удалено'
        return render_template('event_info.html',
                               error=error,
                               event=event)


#show all sensors on the page
@app.route('/all_sensors')
def show_all_sensors():
    try:
        sensors = Sensor.query.all()
        return render_template('all_sensors.html', 
                               sensors=sensors)
    except:
        return render_template('index.html')


#show sensor's events, with method Delete
@app.route('/all_sensors/<int:id>', methods=["GET", "POST"])
def get_events_from_sensor(id):
    try:
        if request.method == 'GET':
            sensor = Sensor.query.get(id)
            events = Event.query\
                        .filter_by\
                        (sensor_id = id)\
                        .all()
            return render_template('get_sensor_events.html', 
                                events=events, 
                                sensor=sensor)
        elif request.method == 'POST':
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
        return render_template('all_sensors.html')


#filter with temperature and humidity parametres   
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
            elif temperature:
                filtered_events = Event\
                                .query\
                                .filter(Event.temperature == temperature)\
                                .all()
                return render_template('filtered_events.html',\
                                        events=filtered_events,\
                                        temperature=temperature,\
                                        humidity=humidity)
            elif humidity:
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
    

#create method for sensors
@app.route('/create_sensor', methods=["GET", "POST"])
def create_sensor():
        try:
            if request.method == 'POST':
                name = request.form.get('name')
                type = request.form.get('type')
                new_sensor = Sensor(name=name, type=type)
                db.session.add(new_sensor)
                db.session.commit()
                success_message = f'Успешно добавлен датчик {name}'
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
        

#create method for event
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
    except(IntegrityError, Exception) as error:
        if error == IntegrityError:
            get_max_id = Event\
                            .query\
                            .order_by(Event.id.desc())\
                            .first()
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
    

#Update method for events
@app.route('/all_events/<int:id>/update', methods=["GET", "POST"])
def update_event_info(id):
    try:
        if request.method == 'POST': 
            event = Event.query.get(id)
            event.sensor_id = request.form.get('sensor_id')
            event.name = request.form.get('name')
            event.temperature = request.form.get('temperature')
            event.humidity = request.form.get('humidity')
            if event.sensor_id and event.name and event.temperature and event.humidity:
                db.session.commit()
                done_message = 'Событие обновлено'
                return render_template('event_info.html',\
                                event=event,
                                done_message=done_message)
            else:
                db.session.rollback()
                annotation = 'Заполните все поля и введите валидные данные.'
                return render_template('event_info.html',
                                       annotation=annotation) 
        else:
            return render_template('all_events.html')
    except:
        error = 'Ошибка базы данных'
        return render_template('event_info.html', 
                               error=error)
    

#Update method for sensors
@app.route('/all_sensors/<int:id>/update', methods=["GET", "POST"])
def update_sensor(id):
    try:
        if request.method == 'POST': 
            events = Event.query.\
                        filter_by\
                        (sensor_id = id)\
                        .all()
            sensor = Sensor.query.get(id)
            sensor.name = request.form.get('name')
            sensor.type = request.form.get('type')
            if sensor.name and sensor.type:
                db.session.commit()
                done_message = 'Датчик обновлен'
                return render_template('get_sensor_events.html',
                                        sensor=sensor,
                                        done_message=done_message,
                                        events=events)
            else:
                db.session.rollback()
                annotation = 'Заполните все поля и введите валидные данные.'
                return render_template('get_sensor_events.html',
                                        sensor=sensor,
                                        annotation=annotation,
                                        events=events) 
        else:
            return render_template('get_sensor_events.html')
    except:
        return render_template('get_sensor_events.html')


#upload *.json files from /json
@app.route('/json_load', methods=["GET", "POST"])
def load_events():
    try:
        if request.method == 'POST':
            #uploading files from UPLOAD_FOLDER
            files = request.files.getlist("file") 
            
            for file in files:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       file.filename))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       file.filename), 
                                       'r', 
                                       encoding='utf-8') as f:
                    #json reading, get sensors_id
                    json_data = json.load(f)
                    sensors_ids = [sensor.id for sensor\
                                   in Sensor.query.all()] 
                    #parsing for values
                    for data in json_data:
                        sensor_id = data['sensor_id']
                        name = data['name']
                        temperature = data['temperature']\
                                      if 'temperature' in data.keys()\
                                      else None
                        humidity = data['humidity']\
                                   if 'humidity' in data.keys()\
                                   else None
                        #checking for validation (if sensor_id not exist)
                        if sensor_id not in sensors_ids:
                            print(f'sensor_id={sensor_id} не существует.\
                                  \nЗапись не будет добавлена в БД')
                            continue
                        event = Event(sensor_id, 
                                      name,
                                      temperature,
                                      humidity)
                        #inserting data into the database
                        db.session.add(event)
                        db.session.commit()
            return render_template('success_json_load.html',
                                files=files)
        else:
            return render_template('json_load.html')
    except:
        return render_template('json_load.html')