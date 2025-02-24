from flask import render_template
from app import app  # Import the `app` instance from `__init__.py`
from app.forms import LoginForm



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Fabio'}
    posts=[
        {
            'author': {'username': 'Robb Stark'},
            'body': 'I am the Young Wolf.'
        },
        {
            'author': {'username': 'Greatjon Umber'},
            'body': 'The King in the North!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)