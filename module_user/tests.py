from django.test import TestCase
from rest_framework.test import APITestCase


class ModuleUserTests(APITestCase):
    def setUp(self) -> None:
        self.request_body = {
            "first_name": "Eren",
            "last_name": "Yeager",
            "username": "attackTitan",
            "primary_email": "eYeager@emailprovider.com",
            "primary_phone": "",
            "password": "Abc123!@",
            "avatar": ""
        }

    def test_signup(self):
        response = self.client.post('/module_user/signup/', self.request_body, format='json')
        assert response.status_code == 200
