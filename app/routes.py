from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db # Import the `app` instance from `__init__.py`
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Robb Stark'},
            'body': 'I am the Young Wolf!'
        },
        {
            'author': {'username': 'Greatjon Umber'},
            'body': 'The King in the North!'
        }
    ]
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("user.html", user=user, posts=posts)