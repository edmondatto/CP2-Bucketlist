from flask import request
from flask_restplus import Resource, fields
from .restplus import api
from app.models import User, db

auth = api.namespace('auth', description='Authentication Endpoints')

user_input = api.model('user_input', {
    'email': fields.String(required=True, description='Email address of new or registered user'),
    'password': fields.String(required=True, description='Password of the new user'),
})

user_output = api.model('user_output', {
    'id': fields.Integer(required=True, readOnly=True, description='The user\'s unique identifier.'),
    'email': fields.String(require=True, descritpion='User\'s email address'),
    'password': fields.String(required=True, description='User\'s password'),
    'registered_on': fields.DateTime,
})


@auth.route('/register')
class Register(Resource):
    @api.expect(user_input)
    @api.marshal_with(user_output)
    def post(self):
        """Creates a new user when passed an email and a password"""
        new_user_email = request.json['email']
        new_user_password = request.json['password']
        new_user = User(new_user_email, new_user_password)
        new_user.save()
        return new_user, 201


@auth.route('/login')
class Login(Resource):
    @api.expect(user_input)
    @api.marshal_with(user_output)
    def post(self):
        """Logs in an existing user when passed an email and the correct password"""
        user_email = request.json['email']
        user_password = request.json['password']
        try:
            user = User.query.filter_by(email=user_email).first()
            if user.is_valid_password(user_password):
                return user
        except AttributeError:
            return 'User does not exist!'
