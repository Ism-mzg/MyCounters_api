import unittest
from app import create_app, db
from app.models import User, Counter
from app.counters import CounterManager

class TestCounterManager(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.user = User(username="test_user", password="test")
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_counter(self):
        with self.app.app_context():
            value = CounterManager.get_counter(self.user.id)
            self.assertEqual(value, 0)

    def test_increment_counter(self):
        with self.app.app_context():
            value = CounterManager.increment_counter(self.user.id)
            self.assertEqual(value, 1)
            value = CounterManager.increment_counter(self.user.id)
            self.assertEqual(value, 2)

    def test_decrement_counter(self):
        with self.app.app_context():
            value = CounterManager.decrement_counter(self.user.id)
            self.assertEqual(value, -1)
            value = CounterManager.decrement_counter(self.user.id)
            self.assertEqual(value, -2)