from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    Ride,
    RideStatus,
    VehicleType,
)


class InvalidStateChangeTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        # -------------------------------------------------
        # USER
        # -------------------------------------------------

        self.user = User.objects.create_user(
            email="invalid_state_test@example.com",
            password="TestPassword123",
        )

        self.client.force_authenticate(user=self.user)

        # -------------------------------------------------
        # VEHICLE TYPE
        # -------------------------------------------------

        self.vehicle_type = VehicleType.objects.create(name="car")

        # -------------------------------------------------
        # CANCELLED STATUS
        # -------------------------------------------------

        self.cancelled_status = RideStatus.objects.create(name="cancelled")

        # -------------------------------------------------
        # RIDE
        # -------------------------------------------------

        self.ride = Ride.objects.create(
            rider=self.user,
            vehicle_type=self.vehicle_type,
            status=self.cancelled_status,
            pickup_address="Guntur",
            pickup_latitude=16.3067,
            pickup_longitude=80.4365,
            dropoff_address="Vijayawada",
            dropoff_latitude=16.3200,
            dropoff_longitude=80.4500,
            fare=100,
        )

    # =====================================================
    # CANCELLED RIDE CANNOT BE ACCEPTED
    # =====================================================

    def test_cancelled_ride_cannot_be_accepted(self):

        response = self.client.post(
            f"/api/v1/rides/{self.ride.id}/accept/",
            format="json",
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.data)

        self.assertNotEqual(
            response.status_code,
            200,
        )

        self.assertIn(
            response.status_code,
            [400, 403, 404],
        )
