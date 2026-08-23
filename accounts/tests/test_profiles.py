from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User, Profile


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="profile_test@example.com",
            password="TestPass123!"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone="9876543210"
        )

        self.url = "/api/profile/"

    def test_authenticated_user_can_get_profile(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            self.url
        )

        print("PROFILE STATUS:", response.status_code)
        print("PROFILE RESPONSE:", response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["success"],
            True
        )

    def test_unauthenticated_user_cannot_get_profile(self):
        response = self.client.get(
            self.url
        )

        print(
            "UNAUTHENTICATED PROFILE STATUS:",
            response.status_code
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )