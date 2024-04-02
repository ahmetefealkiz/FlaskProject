from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel


db = SQLAlchemy()
DB_NAME = "database.db"
admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdashdua'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    admin.init_app(app)

    babel = Babel(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User, Message
    
    class MessageView(ModelView):
        can_delete = True
        form_columns = ["name", "text", "user"]
        column_list = ["name", "text", "user"]

    admin.add_view(ModelView(User, db.session))
    admin.add_view(MessageView(Message, db.session))
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
