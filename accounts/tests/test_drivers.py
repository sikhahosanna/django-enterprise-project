from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User


class DriverTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin_test@example.com", password="AdminPass123!"
        )

        self.user = User.objects.create_user(
            email="normal_user@example.com", password="UserPass123!"
        )

        self.url = "/api/v1/drivers/"

    # POSITIVE TEST
   

    def test_admin_can_access_drivers(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.url)

        print("ADMIN DRIVER STATUS:", response.status_code)
        print("ADMIN DRIVER RESPONSE:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # NEGATIVE TEST
 

    def test_normal_user_cannot_access_drivers(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        print("NORMAL USER DRIVER STATUS:", response.status_code)

        print("NORMAL USER DRIVER RESPONSE:", response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
