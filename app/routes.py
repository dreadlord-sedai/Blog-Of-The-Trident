from flask import render_template
from app import app  # Import the `app` instance from `__init__.py`

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Fabio'}
    return render_template('index.html', title='Home', user=user)