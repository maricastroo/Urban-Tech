#users.py
from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin ):
    __tablename__= "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column( db.Integer, db.ForeignKey(Role.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    password= db.Column(db.String(256) , nullable=False)

    def save_user(role_type, username, email,password):
        role = Role.get_single_role(role_type)
        user = User(role_id = role.id, username = username, email = email, 
                    password = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()


    

    def get_users():
        user = User.query.join(Role, Role.id == User.role_id)\
                    .add_columns(User.username, User.email, User.password, Role.name).all()
        return user
    
    def delete_user(email):
        user = User.query.filter(User.email == email).first()
        db.session.delete(user)
        db.session.commit()

    def get_single_user(email):
        user = User.query.filter(User.email == email)\
            .add_columns(User.username, User.email, User.password, Role.name).first()
        
        if user is not None:
            return [user]
        
    def get_user_id(user_id):
        id = User.query.filter_by(id = user_id).first()
        if id is not None:
            return id


    def upadte_user(username, email, password, role_name):
        user = User.query.filter(User.email == email).first()
        role = Role.get_single_role(role_name)
        if user is not None:
            user.username = username
            user.password = password
            user.role_id = role.id
            db.session.commit()
            return User.get_users()
        
    def validate_user(email,password):
        user = User.query.filter(User.email == email).first()
        if(user==None or not check_password_hash(user.password,password)):
            return None
        else:
            return user