from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
from flask_login import LoginManager

DB_NAME = "lector.db"

#initialise database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #The URI for a SQLite database named "users.db" in a Flask application using SQLAlchemy for database operations.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    #creates a secret key for app
    app.config['SECRET_KEY'] = 'lector'
    db.init_app(app)
    
    from .views import views
    from .forms import forms

    login_manager=LoginManager()
    login_manager.login_view = 'forms.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(forms, url_prefix='/')

    from website.models import User,Manga,Chapters
    from .mangareques import chapter_request



    #creates database with all resources available
    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')

    