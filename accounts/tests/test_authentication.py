from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@example.com",
            password="Test@12345"
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
            {
                "email": "test@example.com",
                "password": "WrongPassword123",
            },
            format="json",
        )

        print("INVALID LOGIN STATUS:", response.status_code)
        print("INVALID LOGIN RESPONSE:", response.data)

        self.assertNotEqual(response.status_code, 200)

    def test_user_registration(self):
        url = reverse("register")

        response = self.client.post(
            url,
            {
                "email": "newuser@example.com",
                "password": "Test@12345",
            },
            format="json",
        )

        print("REGISTER STATUS:", response.status_code)
        print("REGISTER RESPONSE:", response.data)

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            User.objects.filter(
                email="newuser@example.com"
            ).exists()
        )

    def test_token_refresh(self):
        login_url = reverse("login")

        login_response = self.client.post(
            login_url,
            {
                "email": "test@example.com",
                "password": "Test@12345",
            },
            format="json",
        )

        print("TOKEN LOGIN STATUS:", login_response.status_code)
        print("TOKEN LOGIN RESPONSE:", login_response.data)

        refresh_token = login_response.data["data"]["refresh"]

        url = reverse("token_refresh")

        response = self.client.post(
            url,
            {
                "refresh": refresh_token,
            },
            format="json"
        )

        print("TOKEN REFRESH STATUS:", response.status_code)
        print("TOKEN REFRESH RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)