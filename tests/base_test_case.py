from application.application import app, session
from tables import Base, engine
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        try:
            session.commit()
        except:
            session.rollback()
            raise
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        try:
            session.commit()
        except:
            session.rollback()
            raise
        Base.metadata.drop_all(bind=engine)