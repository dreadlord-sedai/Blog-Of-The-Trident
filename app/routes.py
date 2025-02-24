from app import app  # Import the `app` instance from `__init__.py`

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"