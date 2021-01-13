from tests.base_test_case import BaseTestCase
import json


class TestEvents(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "username": "user1",
            "email": "test1@a.com",
            "password": "pass1"
        }
        self.user2_data = {
            "username": "user2",
            "email": "test2@a.com",
            "password": "pass2"
        }
        self.event_data = {
            "name": "Event1",
            "description": "Description1",
            "event_date": "2020-12-11",
            "users": []
        }
        self.event2_data = {
            "name": "Event2",
            "description": "Description2",
            "event_date": "2020-12-12",
            "users": []
        }
        self.invalid_event_data = {
            "name": "Event1",
            "description": "Description1",
            "event_date": "2020.12.11",
            "users": []
        }
        self.edited_event_data = {
            "id": 1,
            "name": "Event2",
            "description": "Description2",
            "event_date": "2020-12-12",
            "users": []
        }

    def test_create_event_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                              "password": self.user_data["password"]})).get_json()["access_token"]

        response = self.app.post('/events', content_type='application/json',
                                 headers={"Authorization": f"JWT {token}"}, data=json.dumps(self.event_data))
        self.assertEqual(201, response.status_code)

    def test_create_event_invalid(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        response = self.app.post('/events', content_type='application/json',
                                 headers={"Authorization": f"JWT {token}"}, data=json.dumps(self.invalid_event_data))
        self.assertEqual(400, response.status_code)

    def test_create_event_unauthorized(self):
        response = self.app.post('/events', content_type='application/json', data=json.dumps(self.event_data))
        self.assertEqual(401, response.status_code)

    def test_get_events_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event2_data))
        response = self.app.get('/events', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_change_event_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        response = self.app.put('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                                data=json.dumps(self.edited_event_data))
        self.assertEqual(201, response.status_code)
        self.assertEqual({'description': 'Description2',
                          'event_date': '2020-12-12',
                          'id': 1,
                          'name': 'Event2',
                          'organizer_id': 1,
                          'users': []}, response.json)

    def test_change_event_invalid_id(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        new_data = self.edited_event_data
        new_data["id"] = "abc"
        response = self.app.put('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                                data=json.dumps(new_data))
        self.assertEqual(400, response.status_code)

    def test_change_event_not_found(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        new_data = self.edited_event_data
        new_data["id"] = 2
        response = self.app.put('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                                data=json.dumps(new_data))
        self.assertEqual(404, response.status_code)

    def test_change_event_not_authorized(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))

        response = self.app.put('/events', content_type='application/json', data=json.dumps(self.edited_event_data))
        self.assertEqual(401, response.status_code)

    def test_change_event_no_access(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user2_data))
        token1 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event_data))
        token2 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user2_data["username"],
                                               "password": self.user2_data["password"]})).get_json()["access_token"]

        response = self.app.put('/events', content_type='application/json', headers={"Authorization": f"JWT {token2}"},
                                data=json.dumps(self.edited_event_data))
        self.assertEqual(403, response.status_code)

    def test_delete_event_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        response1 = self.app.delete('/events/1', headers={"Authorization": f"JWT {token}"})
        self.assertEqual(200, response1.status_code)
        response2 = self.app.get('/events', content_type='application/json')
        self.assertEqual([], response2.json)

    def test_delete_event_not_found(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        response = self.app.delete('/events/1', headers={"Authorization": f"JWT {token}"})
        self.assertEqual(404, response.status_code)

    def test_delete_event_invalid_id(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        response1 = self.app.delete('/events/abs', headers={"Authorization": f"JWT {token}"})
        self.assertEqual(400, response1.status_code)

    def test_delete_event_not_authorized(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token}"},
                      data=json.dumps(self.event_data))
        response1 = self.app.delete('/events/1')
        self.assertEqual(401, response1.status_code)

    def test_delete_event_no_access(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        token1 = self.app.post('/users/login', content_type='application/json',
                              data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event_data))
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user2_data))
        token2 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user2_data["username"],
                                                "password": self.user2_data["password"]})).get_json()["access_token"]
        response1 = self.app.delete('/events/1', headers={"Authorization": f"JWT {token2}"})
        self.assertEqual(403, response1.status_code)

    def test_connected_users_successful(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user2_data))
        token1 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.event_data["users"].append(2)
        self.event2_data["users"].append(2)

        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event_data))
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event2_data))
        response = self.app.get("/events/connected/2", content_type='application/json',
                                headers={"Authorization": f"JWT {token1}"})
        self.assertEqual(200, response.status_code)

    def test_connected_users_invalid_id(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user2_data))
        token1 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user_data["username"],
                                                "password": self.user_data["password"]})).get_json()["access_token"]
        self.event_data["users"].append(2)
        self.event2_data["users"].append(2)
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event_data))
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event2_data))
        response = self.app.get("/events/connected/abc", content_type='application/json',
                                headers={"Authorization": f"JWT {token1}"})
        self.assertEqual(404, response.status_code)

    def test_connected_users_not_authorized(self):
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user_data))
        self.app.post('/users', content_type='application/json', data=json.dumps(self.user2_data))
        token1 = self.app.post('/users/login', content_type='application/json',
                               data=json.dumps({"username": self.user_data["username"],
                                               "password": self.user_data["password"]})).get_json()["access_token"]
        self.event_data["users"].append(2)
        self.event2_data["users"].append(2)
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event_data))
        self.app.post('/events', content_type='application/json', headers={"Authorization": f"JWT {token1}"},
                      data=json.dumps(self.event2_data))
        response = self.app.get("/events/connected/2", content_type='application/json')
        self.assertEqual(401, response.status_code)