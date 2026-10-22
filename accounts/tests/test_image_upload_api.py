from io import BytesIO
from tempfile import TemporaryDirectory

from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image

from accounts.models import User, Profile


class ProfileImageUploadAPITests(APITestCase):

    def setUp(self):
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)

        settings_override = override_settings(
            MEDIA_ROOT=self.media_dir.name
        )
        settings_override.enable()
        self.addCleanup(settings_override.disable)

        self.user = User.objects.create_user(
            email="image_upload_test@example.com",
            password="TestPass123!",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone="9876543210",
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/api/v1/profile/image/"

    def make_png(self):
        buffer = BytesIO()
        Image.new("RGB", (2, 2), color="red").save(
            buffer, format="PNG"
        )
        return SimpleUploadedFile(
            "profile.png",
            buffer.getvalue(),
            content_type="image/png",
        )

    def test_valid_profile_image_upload_succeeds(self):
        response = self.client.post(
            self.url,
            {"profile_image": self.make_png()},
            format="multipart",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            response.data,
        )
        self.assertTrue(response.data["success"])
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_image)

    def test_corrupted_profile_image_is_rejected(self):
        upload = SimpleUploadedFile(
            "broken.png",
            b"not a real image",
            content_type="image/png",
        )
        response = self.client.post(
            self.url,
            {"profile_image": upload},
            format="multipart",
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            response.data,
        )
