from flask import Flask
from models import*
from werkzeug.security import generate_password_hash, check_password_hash

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        Role.save_role( "Admin", "Usuário full" )
        Role.save_role( "User", "Usuário com limitações")
        User.save_user("Admin","Admin", "admin","admin")

        