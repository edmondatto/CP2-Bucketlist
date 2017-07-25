from datetime import datetime, timedelta

import jwt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from instance.config import Config

# from app import db

db = SQLAlchemy()


class User(db.Model):
    """A Model that represents the users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    bucketlists = db.relationship('Bucketlist', backref='owner', lazy='dynamic', order_by='Bucketlist.id',
                                  cascade="all, delete-orphan")
    registered_on = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, email, password):
        """A method that initalises a User with an email and a password"""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def is_valid_password(self, password_to_check):
        """A method that validates the provided password by comparing it to the hashed version"""
        return Bcrypt().check_password_hash(self.password, password_to_check)

    def save(self):
        """A method that saves a new user to the database or changes to an existing one"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_token(user_id):
        """Generates an access token for a user"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            encoded_string = jwt.encode(
                payload,
                Config.SECRET,
                algorithm='HS256'
            )

            return encoded_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(encoded_token):
        """A method that decodes an encoded token and returns a user's id"""
        try:
            payload = jwt.decode(encoded_token, Config.SECRET)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token is expired! Login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token! Login again or register.'


class Bucketlist(db.Model):
    """A Model that represents the bucketlists table"""

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    items = db.relationship('BucketlistItem', backref='owner', lazy='dynamic', order_by='BucketlistItem.id',
                            cascade='all, delete-orphan')
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """A function that initialises a bucketlist with its name and creator"""
        self.name = name
        self.created_by = created_by

    def save(self):
        """A function that saves a new bucketlist to the database or changes to an existing one"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """A function that returns all existing bucketlists"""
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        """A function that deletes a bucketlist"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """A function that returns a representation of a bucketlist object"""
        return '<Bucketlist {}>'.format(self.name)

    def __str__(self):
        """A function that returns a human-readable representation of a bucketlist object"""
        return 'A bucketlist called {}, created by {}'.format(self.name, self.created_by)


class BucketlistItem(db.Model):
    """A Model to represent items in a bucketlist"""

    __tablename__ = "bucketlist_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self, name, bucketlist_id):
        """A function that initialises a bucketlist item with a name"""
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """A function that deletes a bucketlist item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """A function that returns a representation of a bucketlist item object"""
        return '<Bucketlist Item {}>'.format(self.name)
