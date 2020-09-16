import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email": "xyz@xyz.com", 'first_name': "xyz", "last_name": "qwe", "password1": "xyzxyzxyz", "password2": "xyzxyzxyz"}
        resp = self.client.post("/api/v1/rest-auth/registration/", data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)