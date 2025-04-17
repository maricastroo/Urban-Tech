# users_controller.py
from flask import Blueprint, request, render_template
from models.user.users import User
from models.user.roles import Role

import flask_login

user = Blueprint("user",__name__, template_folder="views")

@user.route('/register_user')
@flask_login.login_required
def register_user():
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user.route('/add_user', methods=['POST'])
@flask_login.login_required
def add_user():
    global users
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        User.save_user(role_name, username, email,password)
    
        users = User.get_users()
        return render_template("users.html", devices=users)
    

@user.route('/list_users')
@flask_login.login_required
def list_users():
    users = User.get_users()
    return render_template("users.html", devices=users)

@user.route('/del_user', methods=['GET','POST'])
@flask_login.login_required
def del_user():
    #global users
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
    else:
        email = request.args.get('email', None)
    
    User.delete_user(email)
    user = User.get_users()
    return render_template("users.html", devices=user)

@user.route('/edit_user', methods=['GET','POST'])
@flask_login.login_required
def edit_user():
    if request.method == 'POST':
        email = request.form['email']
    else:
        email = request.args.get('email', None)
    roles = Role.get_role()
    user = User.get_single_user(email)
    return render_template("update_user.html", users=user, roles=roles)
    

@user.route('/update_user', methods=['GET','POST'])
@flask_login.login_required
def update_user():
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
    user = User.upadte_user(username, email, password, role_name)
    return render_template("users.html", devices=user)