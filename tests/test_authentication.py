import unittest
from api import create_app, db
import json


class AuthenticationTestCase(unittest.TestCase):
    """Authentication test cases"""

    def setUp(self):
        """Sets up test app and user data"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.user_data = {
            'email': 'johndoe@example.com',
            'password': 'password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registers_user_successfully(self):
        """Test that new users are registered successfully"""
        response = self.client.post('/auth/register', data=json.dumps(self.user_data),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User created successfully! Please log in.')
        self.assertEqual(response.status_code, 201)

    def test_registered_users_login_successfully(self):
        self.client.post('/auth/register', data=json.dumps(self.user_data))
        response = self.client.post('/auth/login', data=json.dumps(self.user_data),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User logged in successfully', msg='User login failed!')
        self.assertEqual(response.status_code, 200)

    def test_rejects_duplicate_registration(self):
        """Test that already registered users cannot be re-registered"""
        self.client.post('/auth/register', data=json.dumps(self.user_data))
        response = self.client.post('/auth/register', data=json.dumps(self.user_data),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User already registered. Log in.')
        self.assertEqual(response.status_code, 409)

    def test_rejects_invalid_email_format(self):
        user_data_1 = {
            'email': 'luke skywalker',
            'password': 'password'
        }

        user_data_2 = {
            'email': 'johndoe.com',
            'password': 'password'
        }

        user_data_3 = {
            'email': 'johndoe@example',
            'password': 'password'
        }

        # Attempt user registration with data-set 1
        response_1 = self.client.post('/auth/register', data=json.dumps(user_data_1),
                                      headers={'content': 'application/json'})
        result_1 = json.loads(response_1.data.decode())
        self.assertEqual(result_1['message'], 'Invalid email format! Please enter a valid email',
                         msg='Failed to detect invalid password format')
        self.assertEqual(response_1.status_code, 400)

        # Attempt user registration with data-set 2
        response_2 = self.client.post('/auth/register', data=json.dumps(user_data_2),
                                      headers={'content': 'application/json'})
        result_2 = json.loads(response_2.data.decode())
        self.assertEqual(result_2['message'], 'Invalid email format! Please enter a valid email',
                         msg='Failed to detect invalid password format')
        self.assertEqual(response_2.status_code, 400)

        # Attempt user registration with data-set 3
        response_3 = self.client.post('/auth/register', data=json.dumps(user_data_3),
                                      headers={'content': 'application/json'})
        result_3 = json.loads(response_3.data.decode())
        self.assertEqual(result_3['message'], 'Invalid email format! Please enter a valid email',
                         msg='Failed to detect invalid password format')
        self.assertEqual(response_3.status_code, 400)

    def test_rejects_incomplete_data_input(self):
        incomplete_user_data = {
            'email': 'johndoe@example.com'
        }
        self.client.post('/auth/register', data=json.dumps(self.user_data))
        response = self.client.post('/auth/login', data=json.dumps(incomplete_user_data),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Both email and password are required! Try again.',
                         msg='Failed to detect incomplete payload')
        self.assertEqual(response.status_code, 401)

    def test_non_registered_users_cannot_login(self):
        response = self.client.post('/auth/login', data=json.dumps(self.user_data),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid username or password',
                         msg='Non registered users should not be able to log in')
        self.assertEqual(response.status_code, 401)
