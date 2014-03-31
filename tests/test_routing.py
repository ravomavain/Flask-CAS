import unittest
import urllib
import flask
import mock
from StringIO import StringIO
from flask_cas import routing

class test_routing(unittest.TestCase):
    
    def setUp(self):

        self.app = flask.Flask(__name__)

        @self.app.route('/')
        def root():
            return ''

        self.app.secret_key = "SECRET_KEY"
        self.app.register_blueprint(routing.blueprint)
        self.app.testing = True

        self.app.config['CAS_SERVER'] = 'http://cas.server.com'
        self.app.config['CAS_TOKEN_SESSION_KEY'] = '_CAS_TOKEN'
        self.app.config['CAS_USERNAME_SESSION_KEY'] = 'CAS_USERNAME'
        self.app.config['CAS_AFTER_LOGIN'] = 'root'

    def test_setUp(self):
        pass

    def test_login_by_logged_out_user(self):
        with self.app.test_client() as client:
            response = client.get('/login/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.headers['Location'],
                'http://cas.server.com/cas?service=http%3A%2F%2Flocalhost%2Flogin%2F')
    
    @mock.patch.object(urllib, 'urlopen',
            return_value=StringIO('yes\nbob\n'))
    def test_login_by_logged_in_user_valid(self, m):
        with self.app.test_client() as client:
            ticket='12345-abcdefg-cas'
            response = client.get('/login/')
            # TODO

    @mock.patch.object(urllib, 'urlopen',
            return_value=StringIO('yes\nbob\n'))
    def test_login_by_logged_in_user_invalid(self, m):
        with self.app.test_client() as client:
            ticket='12345-abcdefg-cas'
            response = client.get('/login/')
            # TODO
    
    @mock.patch.object(routing, 'validate', return_value=True)
    def test_login_by_cas_valid(self, m):
        with self.app.test_client() as client:
            ticket='12345-abcdefg-cas'
            response = client.get('/login/?ticket={}'.format(ticket))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.headers['Location'],
                'http://localhost/')
            self.assertEqual(
                flask.session[self.app.config['CAS_TOKEN_SESSION_KEY']],
                ticket)

    @mock.patch.object(routing, 'validate', return_value=False)
    def test_login_by_cas_invalid(self, m):
        with self.app.test_client() as client:
            ticket='12345-abcdefg-cas'
            response = client.get('/login/?ticket={}'.format(ticket))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.headers['Location'],
                'http://cas.server.com/cas?service=http%3A%2F%2Flocalhost%2Flogin%2F')

    def test_logout(self):
        with self.app.test_client() as client:
            response = client.get('/logout/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.headers['Location'],
                'http://cas.server.com/cas/logout')

    @mock.patch.object(urllib, 'urlopen',
            return_value=StringIO('yes\nbob\n'))
    def test_validate_valid(self, m):
        with self.app.test_client() as client:
            with self.app.test_request_context('/login/'):
                ticket='12345-abcdefg-cas'
                self.assertEqual(routing.validate(ticket), True)
                self.assertEqual(
                    flask.session[self.app.config['CAS_USERNAME_SESSION_KEY']],
                    'bob')
                self.assertEqual(
                    flask.session[self.app.config['CAS_TOKEN_SESSION_KEY']],
                    ticket)

    @mock.patch.object(urllib, 'urlopen',
            return_value=StringIO('no\n\n'))
    def test_validate_valid(self, m):
        with self.app.test_client() as client:
            with self.app.test_request_context('/login/'):
                ticket='12345-abcdefg-cas'
                self.assertEqual(routing.validate(ticket), False)
