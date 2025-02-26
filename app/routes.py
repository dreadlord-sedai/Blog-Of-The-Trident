from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db # Import the `app` instance from `__init__.py`
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()

    """ 
    This code checks if the form has been submitted and is valid. If so,
    it queries the database for a user with a username matching the one entered in the form.
    The result is stored in the user variable. 
    """
    if form.validate_on_submit():

        user = db.session.scalar(  # The db.session.scalar method is used to execute a scalar query, which returns a single value
            sa.select(User).where(User.username == form.username.data)
        )

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        
        # login_user() function, comes from Flask-Login
        login_user(user, remember=form.remember_me.data)

        # The next_page variable is used to determine where the user should be redirected after they log in.
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(url_for("index"))

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    # logout_user() function, comes from Flask-Login
    logout_user()
    return redirect(url_for("index"))