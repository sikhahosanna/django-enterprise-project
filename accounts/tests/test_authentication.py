from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@example.com", password="Test@12345"
        )

    def test_login_with_valid_credentials(self):
        url = reverse("login")

        response = self.client.post(
            url,
            {
                "email": "test@example.com",
                "password": "Test@12345",
            },
            format="json",
        )

        print("LOGIN STATUS:", response.status_code)
        print("LOGIN RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_password(self):
        url = reverse("login")
        response = self.client.post(
            url,
            {"email": "test@example.com", "password": "WrongPassword123"},
            format="json",
        )

        print("INVALID LOGIN STATUS:", response.status_code)
        print("INVALID LOGIN RESPONSE:", response.data)

        self.assertNotEqual(response.status_code, 200)
