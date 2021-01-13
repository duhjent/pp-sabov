from tests.base_test_case import BaseTestCase
import json


class TestUsers(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "username": "user1",
            "email": "test1@a.com",
            "password": "pass1"
        }

        self.invalid_user_data = {
            "username": "user1",
            "email": "test1",
            "password": "pass1"
        }

    def test_create_user_successful(self):
        response = self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.assertEqual(201, response.status_code)

    def test_create_user_invalid(self):
        response = self.app.post('/users', content_type='application/json', data=json.dumps(self.invalid_user_data))
        self.assertEqual(400, response.status_code)

    def test_create_existed_user(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        response = self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.assertEqual(400, response.status_code)

    def test_get_user_by_username_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        response = self.app.get('/users/user1', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_get_user_by_username_not_found(self):
        response = self.app.get('/users/user1', content_type='application/json')
        self.assertEqual(404, response.status_code)