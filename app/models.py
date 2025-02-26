from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin

# The User class represents users who write blog posts.
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
    

class User(UserMixin, db.Model):
    # ...