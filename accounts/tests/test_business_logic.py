from rest_framework.test import APITestCase
from accounts.models import User, DriverProfile, DriverLocation
from django.core.cache import cache


class DriverAvailabilityTest(APITestCase):

    def setUp(self):
        self.driver_user = User.objects.create_user(
            email="driver@test.com",
            password="Test@12345"
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user
        )

        self.location = DriverLocation.objects.create(
            driver=self.driver,
            latitude=17.3850,
            longitude=78.4867,
            availability_status="offline"
        )

    def test_driver_can_go_online(self):
        self.client.force_authenticate(user=self.driver_user)

        response = self.client.patch(
            "/api/v1/drivers/availability/",
            {"availability_status": "online"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.location.refresh_from_db()

        self.assertEqual(
            self.location.availability_status,
            "online"
        )

    def test_invalid_availability_status(self):
        self.client.force_authenticate(user=self.driver_user)

        response = self.client.patch(
            "/api/v1/drivers/availability/",
            {"availability_status": "invalid"},
            format="json"
        )

        self.assertEqual(response.status_code, 400)
class NearbyDriverSelectionTest(APITestCase):

    def setUp(self):
        cache.clear()
        # Passenger
        self.passenger = User.objects.create_user(
            email="passenger@test.com",
            password="Test@12345"
        )

        # Nearby active driver
        self.driver_user = User.objects.create_user(
            email="driver@test.com",
            password="Test@12345"
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            license_number="LIC-001",
            status=DriverProfile.DriverStatus.ACTIVE
        )

        self.location = DriverLocation.objects.create(
            driver=self.driver,
            latitude=17.3850,
            longitude=78.4867,
            availability_status="online"
        )

    def test_nearby_online_active_driver_selected(self):
        self.client.force_authenticate(user=self.passenger)

        response = self.client.get(
            "/api/v1/drivers/nearby/",
            {
                "latitude": 17.3850,
                "longitude": 78.4867,
                "radius": 5
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.data["data"]

        self.assertEqual(data["count"], 1)
        self.assertEqual(
            data["drivers"][0]["driver_id"],
            str(self.driver.id)
        )

    def test_nearby_driver_requires_online_status(self):
        self.location.availability_status = "offline"
        self.location.save()

        self.client.force_authenticate(user=self.passenger)

        response = self.client.get(
            "/api/v1/drivers/nearby/",
            {
                "latitude": 17.3850,
                "longitude": 78.4867,
                "radius": 5
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.data["data"]

        self.assertEqual(data["count"], 0)
class RideValidationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="ridevalidation@test.com",
            password="Test@12345"
        )

        self.client.force_authenticate(user=self.user)

    def test_missing_required_field(self):
        response = self.client.post(
            "/api/v1/rides/fare/",
            {
                "vehicle_type": "car",
                "pickup_latitude": 17.3850,
                "pickup_longitude": 78.4867,
                "dropoff_latitude": 17.4399,
                # dropoff_longitude missing
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_vehicle_type(self):
        response = self.client.post(
            "/api/v1/rides/fare/",
            {
                "vehicle_type": "invalid-id",
                "pickup_latitude": 17.3850,
                "pickup_longitude": 78.4867,
                "dropoff_latitude": 17.4399,
                "dropoff_longitude": 78.4983,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 404)