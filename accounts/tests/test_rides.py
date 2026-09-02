
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import (
    User,
    Ride,
    RideStatus,
    DriverProfile,
    VehicleType,
)


class RideAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # USERS

        self.rider = User.objects.create_user(
            email="rider@example.com",
            password="Test@12345",
        )

        self.driver_user = User.objects.create_user(
            email="driver@example.com",
            password="Test@12345",
        )

        # DRIVER

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            status=DriverProfile.DriverStatus.ACTIVE,
        )
        # VEHICLE TYPE

        self.vehicle_type = VehicleType.objects.create(
            name="CAR",
        )


        # RIDE STATUSES

        self.requested_status = RideStatus.objects.create(
            name=RideStatus.Status.REQUESTED
        )

        self.accepted_status = RideStatus.objects.create(
            name=RideStatus.Status.ACCEPTED
        )

        self.started_status = RideStatus.objects.create(
            name=RideStatus.Status.STARTED
        )

        self.completed_status = RideStatus.objects.create(
            name=RideStatus.Status.COMPLETED
        )

        self.cancelled_status = RideStatus.objects.create(
            name=RideStatus.Status.CANCELLED
        )

        # CREATE RIDE URL

        self.create_url = "/api/v1/rides/"

    # CREATE RIDE

    def test_create_ride(self):
        self.client.force_authenticate(user=self.rider)

        response = self.client.post(
            self.create_url,
            {
                "pickup_address": "Hyderabad",
                "pickup_latitude": 17.3850,
                "pickup_longitude": 78.4867,
                "dropoff_address": "Secunderabad",
                "dropoff_latitude": 17.4399,
                "dropoff_longitude": 78.4983,
                "vehicle_type": self.vehicle_type.id,
            },
            format="json",
        )

        print("CREATE RIDE STATUS:", response.status_code)
        print("CREATE RIDE RESPONSE:", response.data)

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Ride.objects.filter(
                rider=self.rider
            ).exists()
        )

    # ACCEPT RIDE

    def test_accept_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            vehicle_type=self.vehicle_type,
            status=self.requested_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=184.55,
        )

        self.client.force_authenticate(user=self.driver_user)

        url = f"/api/v1/rides/{ride.id}/accept/"

        response = self.client.post(url)

        print("ACCEPT RIDE STATUS:", response.status_code)
        print("ACCEPT RIDE RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

        ride.refresh_from_db()

        self.assertEqual(
            ride.status.name,
            RideStatus.Status.ACCEPTED,
        )

        self.assertEqual(
            ride.driver_id,
            self.driver.id,
        )

    # START RIDE

    def test_start_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            status=self.accepted_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=184.55,
        )

        self.client.force_authenticate(user=self.driver_user)

        url = f"/api/v1/rides/{ride.id}/status/"

        response = self.client.patch(
            url,
            {
                "status": RideStatus.Status.STARTED,
            },
            format="json",
        )

        print("START RIDE STATUS:", response.status_code)
        print("START RIDE RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

        ride.refresh_from_db()

        self.assertEqual(
            ride.status.name,
            RideStatus.Status.STARTED,
        )
    # COMPLETE RIDE

    def test_complete_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            status=self.started_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=184.55,
        )

        self.client.force_authenticate(user=self.driver_user)

        url = f"/api/v1/rides/{ride.id}/status/"

        response = self.client.patch(
            url,
            {
                "status": RideStatus.Status.COMPLETED,
            },
            format="json",
        )

        print("COMPLETE RIDE STATUS:", response.status_code)
        print("COMPLETE RIDE RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

        ride.refresh_from_db()

        self.assertEqual(
            ride.status.name,
            RideStatus.Status.COMPLETED,
        )

    # CANCEL RIDE

    def test_cancel_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            vehicle_type=self.vehicle_type,
            status=self.requested_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=184.55,
        )

        self.client.force_authenticate(user=self.rider)

        url = f"/api/v1/rides/{ride.id}/cancel/"

        response = self.client.post(url)

        print("CANCEL RIDE STATUS:", response.status_code)
        print("CANCEL RIDE RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

        ride.refresh_from_db()

        self.assertEqual(
            ride.status.name,
            RideStatus.Status.CANCELLED,
        )

    # INVALID STATUS TRANSITION

    def test_invalid_status_transition(self):
        ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            status=self.started_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=184.55,
        )

        self.client.force_authenticate(user=self.driver_user)

        url = f"/api/v1/rides/{ride.id}/status/"

        response = self.client.patch(
            url,
            {
                "status": RideStatus.Status.ACCEPTED,
            },
            format="json",
        )

        print(
            "INVALID TRANSITION STATUS:",
            response.status_code,
        )

        print(
            "INVALID TRANSITION RESPONSE:",
            response.data,
        )

        self.assertEqual(response.status_code, 400)

        ride.refresh_from_db()

        self.assertEqual(
            ride.status.name,
            RideStatus.Status.STARTED,
        )
