import unittest
from api import create_app, db
import json


class BucketlistsTestCase(unittest.TestCase):
    """Bucketlist test cases"""

    def setUp(self):
        """Setup test app, user and registration/login"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.bucketlist = {'name': 'Go skydiving in Diani'}
        self.bucketlist_item = {
            'name': 'Buy skydiving gear and take lessons'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_test_user(self, test_email='johndoe@example.com', test_password='password'):
        """Utility function that registers a test user"""
        test_user_data = {
            'email': test_email,
            'password': test_password
        }
        return self.client.post('/auth/register', data=json.dumps(test_user_data),
                                headers={'content': 'application/json'})

    def login_test_user(self, test_email='johndoe@example.com', test_password='password'):
        """Utility function that logs a test user in"""
        test_user_data = {
            'email': test_email,
            'password': test_password
        }
        return self.client.post('/auth/login', data=json.dumps(test_user_data), headers={'content': 'application/json'})

    def test_creates_bucketlist_successfully(self):
        """Test that a new user can be registered successfully"""
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        response = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                                    headers={'content': 'application/json', 'Authorization': access_token})
        self.assertIn('Go skydiving in Diani', str(response.data), msg='Bucketlist creation failed')
        self.assertEqual(response.status_code, 201)

    def test_cannot_create_bucketlist_without_authorization(self):
        """Test that a user cannot create a bucketlist without logging in"""
        response = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                                    headers={'content': 'application/json'})
        result = json.loads(response.data.decode())
        self.assertIn('Failed! You must be logged in to create a bucketlist.', result['message'],
                      'Bucketlist created without authorization')
        self.assertEqual(response.status_code, 401)

    def test_deletes_bucketlist_successfully(self):
        """Test that a user can delete a bucketlist"""
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                         headers={'content': 'application/json', 'Authorization': access_token})
        response = self.client.delete('/bucketlists/1',
                                      headers={'content': 'application/json', 'Authorization': access_token})
        self.assertEqual(response.status_code, 204)

        # Try retrieving deleted bucketlist using GET operation
        response_2 = self.client.get('/bucketlists/1',
                                     headers={'content': 'application/json', 'Authorization': access_token})
        result_2 = json.loads(response_2.data.decode())
        self.assertIn('Bucketlist 1 does not exist', result_2['message'], msg='Bucketlist 1 was not deleted!')
        self.assertRaises(AttributeError)
        self.assertEqual(response_2.status_code, 404)

    def test_updates_bucketlist_successfully(self):
        """Test that a user can update a bucketlist"""
        bucketlist_update_data = {
            'name': 'Go wind-sailing and skydiving in Diani'
        }
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                         headers={'content': 'application/json', 'Authorization': access_token})
        response = self.client.put('/bucketlists/1', data=json.dumps(bucketlist_update_data),
                                   headers={'content': 'application/json', 'Authorization': access_token})
        self.assertEqual(response.status_code, 200)

        # Retrieve Bucketlist 1 and check for updated name
        response_2 = self.client.get('/bucketlists/1',
                                     headers={'content': 'application/json', 'Authorization': access_token})
        self.assertIn('Go wind-sailing and skydiving in Diani', str(response_2.data))

    def test_retrieves_bucketlist_with_id(self):
        """Test that a user can access a bucketlist using its ID"""
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                         headers={'content': 'application/json', 'Authorization': access_token})
        response = self.client.get('/bucketlists/1',
                                   headers={'content': 'application/json', 'Authorization': access_token})
        self.assertIn('Go skydiving in Diani', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_search_bucketlist_with_query_string(self):
        """Test that a user can retrieve a bucketlist by searching using its name"""
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                         headers={'content': 'application/json', 'Authorization': access_token})
        response = self.client.get('/bucketlists/?per_page=20&q=Diani',
                                   headers={'content': 'application/json', 'Authorization': access_token})
        self.assertIn('Go skydiving in Diani', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_creates_a_bucketlist_item_successfully(self):
        """Test that a user can create a new bucketlist item belonging to a bucketlist"""
        self.register_test_user()
        result = self.login_test_user()
        access_token = json.loads(result.data)['access_token']
        self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                         headers={'content': 'application/json', 'Authorization': access_token})
        response = self.client.get('/bucketlists/1/items/', data=json.dumps(self.bucketlist_item),
                                   headers={'content': 'application/json', 'Authorization': access_token})
        self.assertEqual(response.status_code, 404)

    def test_unregistered_user_cannot_perform_bucketlist_operations(self):
        """Tests to verify that unauthorized users cannot perform CRUD operations"""
        fake_access_token = 'This-Is-An-Inaccurate-Token'

        # create a new bucketlist
        response_1 = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                                      headers={'content': 'application/json', 'Authorization': fake_access_token})
        self.assertIn('Failed! You must be logged in to create a bucketlist.', str(response_1.data))
        self.assertEqual(response_1.status_code, 401)

        # fetch a bucketlist using it's ID
        response_2 = self.client.get('/bucketlists/1',
                                     headers={'content': 'application/json', 'Authorization': fake_access_token})
        self.assertIn('Invalid user. Please log in to view a bucketlist.', str(response_2.data))
        self.assertEqual(response_2.status_code, 401)

        # fetch all bucketlists owned by another user
        response_3 = self.client.get('/bucketlists/',
                                     headers={'content': 'application/json', 'Authorization': fake_access_token})
        self.assertIn('Invalid user. Please log in to view these bucketlists.', str(response_3.data))
        self.assertEqual(response_3.status_code, 401)

        # update a bucketlist owned by another user
        bucketlist_update_data = {
            'name': 'Go wind-sailing and skydiving in Diani'
        }
        response_4 = self.client.put('/bucketlists/1', data=json.dumps(bucketlist_update_data),
                                     headers={'content': 'application/json', 'Authorization': fake_access_token})
        self.assertIn('Invalid user. Please log in to update a bucketlist.', str(response_4.data))
        self.assertEqual(response_4.status_code, 401)

        # delete a bucketlist owned by another user
        response_4 = self.client.delete('/bucketlists/1',
                                        headers={'content': 'application/json', 'Authorization': fake_access_token})
        self.assertIn('Invalid user. Please log in to delete a bucketlist.', str(response_4.data))
        self.assertEqual(response_4.status_code, 401)
