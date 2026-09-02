from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import (
    User,
    DriverProfile,
    VehicleType,
)


class VehicleTests(APITestCase):

    def setUp(self):

        self.admin = User.objects.create_superuser(
            email="admin_vehicle@example.com", password="AdminPass123!"
        )

        self.user = User.objects.create_user(
            email="normal_vehicle@example.com", password="UserPass123!"
        )

        self.driver_user = User.objects.create_user(
            email="driver_vehicle@example.com", password="DriverPass123!"
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            license_number="TEST-LICENSE-001",
            status=DriverProfile.DriverStatus.ACTIVE,
        )

        self.vehicle_type = VehicleType.objects.create(name=VehicleType.Type.CAR)

        self.url = "/api/v1/vehicles/"


    # POSITIVE TEST
    

    def test_admin_can_list_vehicles(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.url)

        print("ADMIN VEHICLE STATUS:", response.status_code)

        print("ADMIN VEHICLE RESPONSE:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

   
    # NEGATIVE TEST
    

    def test_normal_user_cannot_create_vehicle(self):

        self.client.force_authenticate(user=self.user)

        data = {
            "vehicle_type": str(self.vehicle_type.id),
            "registration_number": "TEST-1234",
            "model": "Test Car",
        }

        response = self.client.post(self.url, data, format="json")

        print("NORMAL USER VEHICLE STATUS:", response.status_code)

        print("NORMAL USER VEHICLE RESPONSE:", response.data)

        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
