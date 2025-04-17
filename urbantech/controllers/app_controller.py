#app_controller.py
from flask import Flask, render_template, request, jsonify
from models.db import db, instance
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.writes_controller import write
from controllers.users_controller import user
from controllers.login_controller import login

from models.user.users import User

from flask_socketio import SocketIO
import json
from flask_mqtt import Mqtt

from models.iot.read import Read
from models.iot.write import Write

import flask_login
from flask_login import LoginManager, logout_user

decibel= 10
h = 0
t = 0
q = ""
air = {
            "humidity": h,
            "temperature": t,
            "quality": q 
        }

def create_app():
    app = Flask(__name__, 
                template_folder="./views/", 
                static_folder="./static/",
                root_path="./")
    

    app.secret_key = 'd54gdh543trg@!54gdh'
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')

    @login_manager.user_loader
    def get_user(user_id):
        user_id = User.get_user_id(user_id)
        return user_id
    
    # @login_manager.request_loader
    # def request_loader(user_id):
    #     user_id = User.get_user_id(user_id)
    #     return user_id



    @app.route('/')
    def index():
        return render_template("login.html")
    
    @app.route('/home')
    @flask_login.login_required
    def home():
        return render_template("home.html")
    
    app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe = ["sensordb",'airsensor']

    @app.route('/tempo_real')
    @flask_login.login_required
    def tempo_real():
        global decibel, air
        values = {"decibel":decibel, "air":air}
        return render_template("tr.html", values=values)

    @app.route('/publish')
    @flask_login.login_required
    def publish():
        return render_template('publish.html')

    @app.route('/publish_message', methods=['GET','POST'])
    @flask_login.login_required
    def publish_message():
        request_data = request.get_json()
        publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
        try:
            with app.app_context():
                Write.save_write(request_data['topic'],float(request_data['message']))
        except:
            pass
        return jsonify(publish_result)


    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe[0]) # subscribe topic
            mqtt_client.subscribe(topic_subscribe[1]) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global decibel, air
        for topic in topic_subscribe:
            if(message.topic==topic):
                if(message.topic=="sensordb"):
                    decibel = message.payload.decode()
                elif(message.topic=="airsensor"):
                    air = message.payload.decode()
                try:
                    with app.app_context():
                        Read.save_read(message.topic,message.payload.decode())
                except:
                    pass
    
    return app
