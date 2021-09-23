from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://doadmin:show-password@volt-onboarding-do-user-9874080-0.b.db.ondigitalocean.com:25060/defaultdb?ssl-mode=REQUIRED'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import User, Project

    create_database(app)

    return app

def create_database(app):
    if not path.exists('db/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
