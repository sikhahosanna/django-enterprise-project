from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    VehicleType,
    Ride,
    RideStatus,
)


class RideCancellationTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        # RIDER

        self.rider = User.objects.create_user(
            email="rider_cancel@example.com",
            password="TestPassword123",
        )

        # VEHICLE TYPE

        self.vehicle_type = VehicleType.objects.create(
            name="car",
        )
        # RIDE STATUS

        self.requested_status = RideStatus.objects.create(
            name="requested",
        )

        self.cancelled_status = RideStatus.objects.create(
            name="cancelled",
        )

        # CREATE RIDE

        self.ride = Ride.objects.create(
            rider=self.rider,
            vehicle_type=self.vehicle_type,
            status=self.requested_status,
            pickup_address="Guntur",
            pickup_latitude=16.3067,
            pickup_longitude=80.4365,
            dropoff_address="Vijayawada",
            dropoff_latitude=16.3200,
            dropoff_longitude=80.4500,
            fare=Decimal("141.29"),
        )

        # AUTHENTICATE RIDER

        self.client.force_authenticate(
            user=self.rider,
        )
    # TEST RIDE CANCELLATION

    def test_ride_cancellation(self):

        response = self.client.post(
            f"/api/v1/rides/{self.ride.id}/cancel/",
            {},
            format="json",
        )

        print(
            "STATUS:",
            response.status_code,
        )

        print(
            "RESPONSE:",
            response.data,
        )

        # SUCCESS RESPONSE

        self.assertEqual(
            response.status_code,
            200,
        )

        # REFRESH RIDE

        self.ride.refresh_from_db()

        # STATUS MUST BE CANCELLED

        self.assertEqual(
            self.ride.status.name.lower(),
            "cancelled",
        )
