import unittest
from app import app, db, User, Post

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        self.ctx = app.app_context()
        self.ctx.push()


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
    
    def test_new_post(self):
        # This creates a new user
        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()

        # Then, send a POST request to the new post page with form data
        # and check if the response status code is 302 (redirect).
        response = self.client.post(f'/users/{user.id}/posts/new', data={'title': 'Test Post', 'content': 'Test Content'})
        self.assertEqual(response.status_code, 302)

    def test_post_detail(self):
        # This creates a new user and post
        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='Test Content', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # Then, send a GET request to the post detail page
        # and check if the response status code is 200 (success).
        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.ctx.pop()
if __name__ == '__main__':
    # Runs the unit tests.
    unittest.main()