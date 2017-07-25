from flask import request
from flask_restplus import Resource, fields
from .restplus import api
from app.models import User, db
import re
from .serializers import user_input, user_output

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

auth = api.namespace('auth', description='Authentication Endpoints')


@auth.route('/register')
@api.response(201, 'User successfully created')
@api.response(409, 'User already exists')
@api.response(401, 'An error occurred during user registration, try again later')
@api.response(400, 'Invalid email format')
class Register(Resource):
    @api.expect(user_input)
    def post(self):
        """Creates a new user when passed an email and a password"""
        new_user_email = request.json['email'].strip()
        new_user_password = request.json['password'].strip()
        if not EMAIL_REGEX.match(new_user_email):
            response = {
                'message': 'Invalid email format! Please enter a valid email',
            }
            return response, 400
        if not User.query.filter_by(email=new_user_email).first():
            try:
                new_user = User(new_user_email, new_user_password)
                new_user.save()
                response = {
                    'message': 'User created successfully!'
                }
                return response, 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return response, 401
        response = {
            'message': 'User already registered. Log in.'
        }
        return response, 409


@auth.route('/login')
@api.response(400, 'Invalid email format')
@api.response(401, 'Invalid log in credentials')
@api.response(200, 'User logged in successfully')
@api.response(500, 'An error occurred during user registration, try again later')
class Login(Resource):
    @api.expect(user_input)
    def post(self):
        """Logs in an existing user when passed an email and the correct password"""
        try:
            user_email = request.json['email'].strip()
            user_password = request.json['password'].strip()
            if not EMAIL_REGEX.match(user_email):
                response = {
                    'message': 'Invalid email format! Please enter a valid email',
                }
                return response, 400
            user = User.query.filter_by(email=user_email).first()
            if user and user.is_valid_password(user_password):
                auth_token = user.create_token(user.id)
                if auth_token:
                    response = {
                        'message': 'User logged in successfully',
                        'access_token': auth_token.decode('utf-8'),
                    }
                    return response, 200
            else:
                response = {
                    'message': 'Invalid username or password'
                }
                return response, 401
        except Exception as e:
            response = {
                'message': str(e)
            }
            return response, 500
