from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

app = Flask(__name__)
app.config.from_object(Config())

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
	return User(id=user_id)

@babel.localeselector
def get_locale():
	return 'nl'

import views, models, cli