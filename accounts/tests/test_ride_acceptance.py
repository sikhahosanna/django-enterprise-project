from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    VehicleType,
    Ride,
    RideStatus,
    DriverProfile,
)


class RideAcceptanceTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        # =================================================
        # RIDER
        # =================================================

        self.rider = User.objects.create_user(
            email="rider_accept@example.com",
            password="TestPassword123",
        )

        # =================================================
        # DRIVER
        # =================================================

        self.driver_user = User.objects.create_user(
            email="driver_accept@example.com",
            password="TestPassword123",
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            license_number="TEST123456",
            status="active",
        )

        # =================================================
        # VEHICLE TYPE
        # =================================================

        self.vehicle_type = VehicleType.objects.create(
            name="car",
        )

        # =================================================
        # RIDE STATUS
        # =================================================

        self.requested_status = RideStatus.objects.create(
            name="requested",
        )

        self.accepted_status = RideStatus.objects.create(
            name="accepted",
        )

        # =================================================
        # CREATE RIDE
        # =================================================

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
            # REQUIRED FIELD
            fare=Decimal("141.29"),
        )

        # =================================================
        # AUTHENTICATE DRIVER
        # =================================================

        self.client.force_authenticate(
            user=self.driver_user,
        )

    # =====================================================
    # TEST RIDE ACCEPTANCE
    # =====================================================

    def test_ride_acceptance(self):

        response = self.client.post(
            f"/api/v1/rides/{self.ride.id}/accept/",
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

        # =================================================
        # RESPONSE SHOULD BE SUCCESS
        # =================================================

        self.assertEqual(
            response.status_code,
            200,
        )

        # =================================================
        # REFRESH FROM DATABASE
        # =================================================

        self.ride.refresh_from_db()

        # =================================================
        # DRIVER MUST BE ASSIGNED
        # =================================================

        self.assertEqual(
            self.ride.driver_id,
            self.driver.id,
        )

        # =================================================
        # STATUS MUST BE ACCEPTED
        # =================================================

        self.assertEqual(
            self.ride.status.name.lower(),
            "accepted",
        )
