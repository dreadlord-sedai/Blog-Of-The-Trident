from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes # Import routes after creating `app` to avoid circular import issues.