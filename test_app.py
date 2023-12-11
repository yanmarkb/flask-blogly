import unittest
from app import app, db, User

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        # Sends a GET request to the home page and check if the response status code is 302 (redirect).
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_users(self):
        # Sends a GET request to the users page and check if the response status code is 200 (success).
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_new_user_get(self):
        # Sends a GET request to the new user page and check if the response status code is 200 (success).
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)

    def test_new_user_post(self):
        # Sends a POST request to the new user page with form data and check if the response status code is 302 (redirect).
        response = self.client.post('/users/new', data={'first_name': 'Test', 'last_name': 'User', 'image_url': ''})
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    # Runs the unit tests.
    unittest.main()