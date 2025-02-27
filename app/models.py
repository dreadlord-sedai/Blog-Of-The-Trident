from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from hashlib import md5
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login

# The followers table is an auxiliary (association) table that is used to represent a many-to-many relationship between users.
# The followers table is not a model, so it does not have a class.
# It is defined as an instance of the Table class from the SQLAlchemy package.
followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
)


# The User class represents users who write blog posts.
# User class is a subclass of db.Model, which declares the class as a model for a database table.
# The db.Model is a base class for all models in Flask-SQLAlchemy. (See __init__.py)
# Each class variable represents a database field in the table.
# The id field is the primary key, which is used to uniquely identify each user in the table.
# The username and email fields are indexed and must be unique.
# The password_hash field is not a plain text password, but a secure hash.
# The posts field is a one-to-many relationship to the Post class, which means that for each user, there can be multiple blog posts.
# The back_populates argument defines the name of a field that will be added to the related class that will point back to this class.
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                 unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                              unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    # The set_password method takes a password, hashes it, and stores it in the password_hash field
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # The check_password method checks the password against the hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # The followers and following fields are used to represent a many-to-many relationship between users.
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')
    
    # The follow and unfollow methods are used to add and remove followers
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    

    
# The user_loader callback is used to reload the user object from the user ID stored in the session.
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


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


