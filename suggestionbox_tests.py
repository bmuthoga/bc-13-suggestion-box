# Unit tests cases for the functions
import os
import unittest
import app
import tempfile

class SuggestionBoxTestCase(unittest.TestCase):

    # This method creates a new test client and initializes a new database.
    # This function is called before each individual test function is run.
    def setUp(self):
        self.db_fd, suggestionbox.app.config['DATABASE'] = tempfile.mkstemp()
        # TESTING config flag activated during setup. It disables error
        # catching during request handling to get better error reports when
        # performing test requests against application.
        suggestionbox.app.config['TESTING'] = True
        # Test client gives us simple interface to the application
        self.app = suggestionbox.app.test_client()
        with suggestionbox.app.app_context():
            suggestionbox.init_db()

    # Deleting database after test by closing file and removing it from
    # filesystem.
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(suggestionbox.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assertEqual(rv, render_template('signin.html'))

    def login(self, username, password):
        return self.app.post('/login', data=dict(
        username=username,
        password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('bmuthoga@gmail.com', '1234')
        assertEqual(rv, render_template('landingpage.html'))
        rv = self.logout()
        assertEqual(rv, render_template('index.html'))
        rv = self.login('bmuthoga@gmail.com', 'default')
        assertEqual(rv, render_template('signin.html'))
        rv = self.login('admin', '1234')
        assertEqual(rv, render_template('signin.html'))

    def test_add_suggestion(self):
        self.login('bmuthoga@gmail.com', '1234')
        rv = self.app.post('/viewSuggestion', data=dict(
            title='<Hello>',
            content='<strong>HTML</strong> allowed here'
            ), follow_redirects=True)
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()
