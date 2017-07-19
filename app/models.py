from flask_bcrypt import Bcrypt

from app import db


class User(db.Model):
    """A Model that represents the users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """A function that initalises a User with an email and a password"""
        self.email = email
        self.password = Bcrypt.generate_password_hash(password)

    def is_valid_password(self, password_to_check):
        """A password that validates the provided password by comparing it to the hashed version"""
        Bcrypt.check_password_hash(self.password, password_to_check)


class Bucketlist(db.Model):
    """A Model that represents the bucketlists table"""

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    items = db.relationship('BucketlistItem', order_by='BucketlistItem.id', cascade='all, delete-orphan')
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """A function that initialises a bucketlist with its name and creator"""
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        """A function that returns a representation of a bucketlist object"""
        return '<Bucketlist {}>'.format(self.name)

    def __str__(self):
        """A function that returns a human-readable representation of a bucketlist object"""
        return 'A bucketlist called {}, created by {}'.format(self.name, self.created_by)


class BucketlistItem(db.Model):
    """A Model to represent items in a bucketlist"""

    __tablename__ = "bucketlist items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self, name):
        """A function that initialises a bucketlist item with a name"""
        self.name = name
