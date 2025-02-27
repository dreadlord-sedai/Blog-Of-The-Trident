import logging
from logging.handlers import SMTPHandler
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


# The following code is used to send error logs to the email address specified in the ADMINS configuration variable.
# This is done using the SMTPHandler class from the logging.handlers module.
# The mail server details are read from the configuration.
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        # The SMTPHandler class sends logs via email. The arguments to the class are the mail server,
        #  the from address, the to address, the subject, and the credentials.
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='The Blog of the Trident Failure',
            credentials=auth, secure=secure)
        # The setLevel method is used to set the logging level, and the addHandler method is used to
        # attach the handler to the app.logger object.
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

from app import routes, models, errors