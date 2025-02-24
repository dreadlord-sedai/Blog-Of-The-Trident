from flask import render_template
from app import app  # Import the `app` instance from `__init__.py`



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