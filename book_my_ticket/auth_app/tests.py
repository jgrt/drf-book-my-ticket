from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "email": "xyz@xyz.com",
            "first_name": "xyz",
            "last_name": "qwe",
            "date_of_birth": "2020-09-21",
            "password1": "xyzxyzxyz",
            "password2": "xyzxyzxyz",
            "city": "Auckland",
        }
        url = "/sign-up/rest-auth/registration/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserTestCase(TestCase):
    def test_create_user(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="test@xyz.com",
            first_name="xyz",
            last_name="qwe",
            date_of_birth="2020-09-21",
            city="Pune",
            password="xyzxyzxyz",
        )
        self.assertIsNotNone(self.user.email)
        self.assertEqual(self.user.email, "test@xyz.com")

    def test_create_superuser(self):
        self.superuser = CustomUser.objects.create_superuser(
            email="superuser@test.com", password="superduper"
        )
        self.assertTrue(
            self.superuser.is_superuser, "Superuser must have is_superuser=True."
        )
        self.assertTrue(self.superuser.is_staff, "Superuser must have is_staff=True.")
