#reads_controller.py
from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator

import flask_login

write= Blueprint("write",__name__, template_folder="views")


@write.route("/history_write")
@flask_login.login_required
def history_write():
    actuators = Actuator.get_actuators()
    write = {}
    return render_template("history_write.html", actuators = actuators, write = write)


@write.route("/get_write", methods=['POST'])
@flask_login.login_required
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        
        write = Write.get_write(id, start, end)
        print(write)
        actuators = Actuator.get_actuators()
        return render_template("history_write.html", actuators = actuators, write = write)