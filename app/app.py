from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config.Config')
# app.config['SECRET_KEY'] = 'C&Q7dWjosuKSPTKhLEo&6Q828N^QQD'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db' # mysql://username:password@server/databasename
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress warning
# app.config['LANGUAGES'] = ['en', 'nl']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)

import views, models, cli

@login_manager.user_loader
def load_user(user_id):
	return models.User(id=user_id)

@babel.localeselector
def get_locale():
	return 'nl'