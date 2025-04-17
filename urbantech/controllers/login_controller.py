# login_controller.py
from flask import Blueprint, request, render_template, flash
from models.user.users import User
from models.user.roles import Role
import flask_login
from flask_login import LoginManager, logout_user


login = Blueprint("login",__name__, template_folder="views")

@login.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.validate_user(email, password)
        if(user == None):
            flash('usuário e/ou senha incorreta!', category='danger')
            return render_template('login.html')
        else:
            flask_login.login_required
            flask_login.login_user(user)
            if user.role_id == 1:  # Acessando o nome da role via relacionamento
                return render_template('home.html')
            elif user.role_id == 2:
                return render_template('home2.html')
    else:
        return render_template('login.html')
    

@login.route('/logoff')
@flask_login.login_required
def logoff():
    logout_user()
    return render_template("login.html")
    