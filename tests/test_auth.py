import unittest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed_password = generate_password_hash("test_password", method='sha256')
            self.user = User(username="test_user", password=hashed_password)
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', json={"username": "test_user", "password": "test_password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_failure(self):
        response = self.client.post('/login', json={"username": "test_user", "password": "wrong_password"})
        self.assertEqual(response.status_code, 401)