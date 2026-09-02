from django.test import TestCase

from rest_framework.test import APIClient

from accounts.models import User


class PermissionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Admin
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="Admin@12345",
        )

        # Driver
        self.driver = User.objects.create_user(
            email="driver@example.com",
            password="Driver@12345",
        )

        # Passenger
        self.passenger = User.objects.create_user(
            email="passenger@example.com",
            password="Passenger@12345",
        )

        self.url = "/api/v1/profiles/"

    def test_admin_permission(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.url)

        print("ADMIN STATUS:", response.status_code)
        print("ADMIN RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

    def test_driver_permission(self):
        self.client.force_authenticate(user=self.driver)

        response = self.client.get(self.url)

        print("DRIVER STATUS:", response.status_code)
        print("DRIVER RESPONSE:", response.data)

        self.assertEqual(response.status_code, 403)

    def test_passenger_permission(self):
        self.client.force_authenticate(user=self.passenger)

        response = self.client.get(self.url)

        print("PASSENGER STATUS:", response.status_code)
        print("PASSENGER RESPONSE:", response.data)

        self.assertEqual(response.status_code, 403)

    def test_anonymous_permission(self):
        response = self.client.get(self.url)

        print("ANONYMOUS STATUS:", response.status_code)
        print("ANONYMOUS RESPONSE:", response.data)

        self.assertEqual(response.status_code, 401)