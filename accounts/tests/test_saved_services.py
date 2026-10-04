from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Service, SavedService


User = get_user_model()


class SavedServiceTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            email="customer@test.com",
            password="Test@12345",
        )

        self.other_customer = User.objects.create_user(
            email="other@test.com",
            password="Test@12345",
        )

        self.service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=750.00,
            duration=60,
            is_active=True,
        )

        self.client.force_authenticate(
            user=self.customer
        )

        self.url = "/api/v1/saved-services/"

    def test_save_service(self):
        response = self.client.post(
            self.url,
            {"service": str(self.service.id)},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            SavedService.objects.filter(
                customer=self.customer,
                service=self.service,
            ).exists()
        )

    def test_duplicate_save(self):
        SavedService.objects.create(
            customer=self.customer,
            service=self.service,
        )

        response = self.client.post(
            self.url,
            {"service": str(self.service.id)},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_saved_services(self):
        SavedService.objects.create(
            customer=self.customer,
            service=self.service,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_remove_saved_service(self):
        saved_service = SavedService.objects.create(
            customer=self.customer,
            service=self.service,
        )

        response = self.client.delete(
            f"{self.url}{saved_service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            SavedService.objects.filter(
                id=saved_service.id
            ).exists()
        )

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_service_not_found(self):
        response = self.client.post(
            self.url,
            {
                "service": (
                    "00000000-0000-0000-0000-000000000000"
                )
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cannot_remove_other_customer_saved_service(self):
        saved_service = SavedService.objects.create(
            customer=self.other_customer,
            service=self.service,
        )

        response = self.client.delete(
            f"{self.url}{saved_service.id}/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            ],
        )

        self.assertTrue(
            SavedService.objects.filter(
                id=saved_service.id
            ).exists()
        )

    @patch(
        "accounts.services.notification_service."
        "saved_service_unavailable_notification.delay"
    )
    def test_saved_service_notification_triggered(
        self,
        mock_task,
    ):
        from accounts.services.notification_service import (
            NotificationService,
        )

        NotificationService.saved_service_unavailable(
            self.service
        )

        mock_task.assert_called_once_with(
            service_id=str(self.service.id)
        )