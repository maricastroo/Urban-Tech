from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    id= db.Column('id',  db.Integer, nullable = False, primary_key=True)
    write_datetime = db.Column(db.DateTime(),  nullable = False)
    actuators_id= db.Column(  db.Integer, db.ForeignKey(Actuator.id),nullable = False)
    value = db.Column( db.Float, nullable = True)

    def save_write(topic, value):
        print(f"Received topic: '{topic}'")
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        if actuator:
            print(f"Found actuator: {actuator.id}, topic: '{actuator.topic}'")
            device = Device.query.filter(Device.id == actuator.devices_id).first()
            if device and device.is_active:
                write = Write(write_datetime=datetime.now(), actuators_id=actuator.id, value=float(value))
                db.session.add(write)
                db.session.commit()
                print("Write saved successfully")
            else:
                print("Device is not active or not found")
        else:
            print(f"Actuator not found for topic: '{topic}'")


    def get_write(device_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        write = Write.query.filter(Write.actuators_id == Actuator.devices_id, 
                                   Write.write_datetime > start, Write.write_datetime<end).all()
        return write