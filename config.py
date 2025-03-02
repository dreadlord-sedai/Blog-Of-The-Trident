import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # The SECRET_KEY configuration variable is an important part in most Flask applications.
    # It is used by Flask and many of its extensions to encrypt data, including cookies, request data, and the CSRF token.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # This configuration option is used to signal the application every time a change is about to be made in the database.
    # Email Server Details
    MAIL_SERVER = os.environ.get('MAIL_SERVER') # or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) 
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['dahamifabbio@gmail.com']

    # The POSTS_PER_PAGE configuration variable is used to set the number of blog posts to display per page.
    POSTS_PER_PAGE = 25

    # The LANGUAGES configuration variable is used to specify the languages supported by the application.
    LANGUAGES = ['en', 'es']

    # The MS_TRANSLATOR_KEY configuration variable is used to store the Microsoft Translator API key.
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    