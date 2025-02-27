from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# The app package is defined by the app directory and the __init__.py script, and it is also defined as the instance of the Flask class.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

login = LoginManager(app)
login.login_view = 'login'  # The 'login' view function name (not the URL) for the login page

from app import routes, models, errors