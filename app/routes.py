from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from datetime import datetime, timezone
import sqlalchemy as sa
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db # Import the `app` instance from `__init__.py`
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
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
    form = EmptyForm()
    return render_template("user.html", user=user, posts=posts, form=form)

# The before_request decorator registers a function to run before the view function, no matter what URL is requested.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # if the form is submitted and valid, the code updates the current_user object with the new values,
    # and commits the changes to the database
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You unfollowed {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

    