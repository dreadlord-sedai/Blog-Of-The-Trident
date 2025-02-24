from flask import Flask

app = Flask(__name__)

from app import routes # Import routes after creating `app` to avoid circular import issues.