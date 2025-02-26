from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login


# The User class represents users who write blog posts.
# User class is a subclass of db.Model, which declares the class as a model for a database table.
# The db.Model is a base class for all models in Flask-SQLAlchemy. (See __init__.py)
# Each class variable represents a database field in the table.
# The id field is the primary key, which is used to uniquely identify each user in the table.
# The username and email fields are indexed and must be unique.
# The password_hash field is not a plain text password, but a secure hash.
# The posts field is a one-to-many relationship to the Post class, which means that for each user, there can be multiple blog posts.
# The back_populates argument defines the name of a field that will be added to the related class that will point back to this class.
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                 unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                              unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # The set_password method takes a password, hashes it, and stores it in the password_hash field
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # The check_password method checks the password against the hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# The Post class represents blog posts written by users.
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                                index=True)
        
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# The UserMixin class provides default implementations for the methods that Flask-Login expects user objects to have.
class User(UserMixin, db.Model):
    #...

# The user_loader callback is used to reload the user object from the user ID stored in the session.
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


