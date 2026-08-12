from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    Ride,
    RideStatus,
    VehicleType,
    DriverProfile,
)


class DuplicateRideAcceptanceTest(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # CLIENTS
        # -------------------------------------------------

        self.client_a = APIClient()
        self.client_b = APIClient()

        # -------------------------------------------------
        # RIDER
        # -------------------------------------------------

        self.rider = User.objects.create_user(
            email="duplicate_rider@example.com",
            password="TestPassword123",
        )

        # -------------------------------------------------
        # DRIVER A
        # -------------------------------------------------

        self.driver_user_a = User.objects.create_user(
            email="driver_a@example.com",
            password="TestPassword123",
        )

        self.driver_a = DriverProfile.objects.create(
            user=self.driver_user_a,
            license_number="DRIVER-A-123",
            status="active",
        )

        # -------------------------------------------------
        # DRIVER B
        # -------------------------------------------------

        self.driver_user_b = User.objects.create_user(
            email="driver_b@example.com",
            password="TestPassword123",
        )

        self.driver_b = DriverProfile.objects.create(
            user=self.driver_user_b,
            license_number="DRIVER-B-123",
            status="active",
        )

        # -------------------------------------------------
        # AUTHENTICATION
        # -------------------------------------------------

        self.client_a.force_authenticate(
            user=self.driver_user_a
        )

        self.client_b.force_authenticate(
            user=self.driver_user_b
        )

        # -------------------------------------------------
        # VEHICLE TYPE
        # -------------------------------------------------

        self.vehicle_type = VehicleType.objects.create(
            name="car"
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.requested_status = RideStatus.objects.create(
            name="requested"
        )

        self.accepted_status = RideStatus.objects.create(
            name="accepted"
        )

        # -------------------------------------------------
        # RIDE
        # -------------------------------------------------

        self.ride = Ride.objects.create(
            rider=self.rider,
            driver=None,
            vehicle_type=self.vehicle_type,
            status=self.requested_status,

            pickup_address="Guntur",
            pickup_latitude=16.3067,
            pickup_longitude=80.4365,

            dropoff_address="Vijayawada",
            dropoff_latitude=16.3200,
            dropoff_longitude=80.4500,

            fare=100,
        )

    # =====================================================
    # DUPLICATE RIDE ACCEPTANCE
    # =====================================================

    def test_duplicate_ride_acceptance(self):

        # -------------------------------------------------
        # DRIVER A ACCEPTS
        # -------------------------------------------------

        response_a = self.client_a.post(
            f"/api/rides/{self.ride.id}/accept/",
            format="json",
        )

        print("DRIVER A STATUS:", response_a.status_code)
        print("DRIVER A RESPONSE:", response_a.data)

        self.assertEqual(
            response_a.status_code,
            200,
        )

        # -------------------------------------------------
        # DRIVER B TRIES SAME RIDE
        # -------------------------------------------------

        response_b = self.client_b.post(
            f"/api/rides/{self.ride.id}/accept/",
            format="json",
        )

        print("DRIVER B STATUS:", response_b.status_code)
        print("DRIVER B RESPONSE:", response_b.data)

        self.assertNotEqual(
            response_b.status_code,
            200,
        )

        # -------------------------------------------------
        # VERIFY RIDE STILL BELONGS TO DRIVER A
        # -------------------------------------------------

        self.ride.refresh_from_db()

        self.assertEqual(
            self.ride.driver_id,
            self.driver_a.id,
        )

        self.assertEqual(
            self.ride.status.name.lower(),
            "accepted",
        )