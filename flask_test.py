from mainApp import app
import unittest
app.config.update(
    DEBUG=True,
    SECRET_KEY='super_secret_key'
)

class FlaskTestCase(unittest.TestCase):

    # Ensure flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertIn(b'login', response.data)

    # Ensure register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertIn(b'register', response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'You are logged in', response.data)

    # Ensure login fails given incorrect username
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(username="wrong", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'Username does not exist.', response.data)

    # Ensure login fails given incorrect password
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(username="Incorrect password", password="paword"),
            follow_redirects=True
        )
        self.assertIn(b'login', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        response = tester.get('/logout/', follow_redirects=True)
        self.assertIn(b'You are logged out.', response.data)

    # Ensure content shows on user logged in homepage
    def test_logged_in_homepage(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        self.assertIn(b'Price', response.data)
        self.assertIn(b'Date', response.data)
        self.assertIn(b'Description', response.data)
        self.assertIn(b'Action', response.data)

    # Ensure add page loads correctly
    def test_add_new_expense_page_loads(self):
        tester = app.test_client(self)
        tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        response = tester.get('/user/1/add', follow_redirects=True)
        self.assertIn(b'Add new expense', response.data)

    # Ensure edit page loads correctly
    def test_edit_expense_page_loads(self):
        tester = app.test_client(self)
        tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        response = tester.get('/user/1/3/edit', follow_redirects=True)
        self.assertIn(b'Edit an expense', response.data)

    # Ensure delete page loads correctly
    def test_delete_expense_page_loads(self):
        tester = app.test_client(self)
        tester.post(
            '/login/',
            data=dict(username="user", password="password"),
            follow_redirects=True
        )
        response = tester.get('/user/1/3/delete', follow_redirects=True)
        self.assertIn(b'Delete an expense', response.data)


if __name__ == '__main__':
    unittest.main()