from tests.base_test_case import BaseTestCase
import json


class TestAuth(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "username": "user1",
            "email": "test1@a.com",
            "password": "pass1"
        }

    def test_login_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        response = self.app.post('/users/login', content_type='application/json',
                             data=json.dumps({"username": self.user_data["username"],
                                              "password": self.user_data["password"]}))
        self.assertEqual(200, response.status_code)

    def test_login_invalid(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        response1 = self.app.post('/users/login', content_type='application/json',
                                  data=json.dumps({"username": self.user_data["username"],
                                                  "password": "test"}))
        self.assertEqual(401, response1.status_code)
        response2 = self.app.post('/users/login', content_type='application/json',
                                  data=json.dumps({"password": "test"}))
        self.assertEqual(401, response2.status_code)