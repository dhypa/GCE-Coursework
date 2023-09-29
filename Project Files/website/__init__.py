from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()            #CREATES DATABASE
DB_NAME = "database.db"

def create_database(app):                             #Function checks if database DOES NOT EXIST, then creates database if so
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)c
        print('Created Database!')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    from .views import views                            #imports views from both auth and views files
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')       #sets the default url prefix for views in both files as '/'
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Users, product                  #imports table models from database
   
    with app.app_context():                             #initializes database with tables
        db.create_all()
              


    
    login_manager= LoginManager(app)                    
    login_manager.login_view = 'auth.login'   #if a user is not logged in, they are automatically directed to the view 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader              #This callback is used to reload the user object from the user ID stored
    def load_user(id):
        return Users.query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')








    
