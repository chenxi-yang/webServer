from flask_testing import TestCase
from webServer import db, app

TEST_SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"

class MyTest(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()