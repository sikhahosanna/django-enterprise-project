from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    VehicleType,
    RideStatus,
)


class RideCreationTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        # -------------------------------------------------
        # USER
        # -------------------------------------------------

        self.user = User.objects.create_user(
            email="rider_test@example.com",
            password="TestPassword123",
        )

        # -------------------------------------------------
        # VEHICLE TYPE
        # -------------------------------------------------

        self.vehicle_type = VehicleType.objects.create(
            name="car",
        )

        # -------------------------------------------------
        # RIDE STATUS
        # -------------------------------------------------

        self.requested_status = RideStatus.objects.create(
            name="requested",
        )

        # -------------------------------------------------
        # AUTHENTICATION
        # -------------------------------------------------

        self.client.force_authenticate(
            user=self.user,
        )

    # =====================================================
    # RIDE CREATION
    # =====================================================

    def test_ride_creation(self):

        response = self.client.post(
            "/api/rides/",
            {
                "vehicle_type": str(
                    self.vehicle_type.id
                ),

                "pickup_address": "Guntur",
                "pickup_latitude": 16.3067,
                "pickup_longitude": 80.4365,

                "dropoff_address": "Vijayawada",
                "dropoff_latitude": 16.3200,
                "dropoff_longitude": 80.4500,
            },
            format="json",
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.data)

        if response.status_code == 500:
            print(
                "CONTENT:",
                response.content.decode()
            )

        self.assertEqual(
            response.status_code,
            201,
        )