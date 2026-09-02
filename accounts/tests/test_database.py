from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import (
    User,
    DriverProfile,
    VehicleType,
    Vehicle,
    Ride,
    RideStatus,
)


class DatabaseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="database@test.com",
            password="Test@12345",
        )

        self.driver_user = User.objects.create_user(
            email="driver_database@test.com",
            password="Test@12345",
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            license_number="LIC-DB-001",
            status=DriverProfile.DriverStatus.ACTIVE,
        )

        self.vehicle_type = VehicleType.objects.create(
            name=VehicleType.Type.CAR,
        )

        self.ride_status = RideStatus.objects.create(
            name=RideStatus.Status.REQUESTED,
        )

    # 1. UNIQUE FIELDS

    def test_user_email_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    email="database@test.com",
                    password="Another@123",
                )

    def test_driver_license_number_unique(self):
        another_user = User.objects.create_user(
            email="another_driver@test.com",
            password="Test@12345",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DriverProfile.objects.create(
                    user=another_user,
                    license_number="LIC-DB-001",
                    status=DriverProfile.DriverStatus.ACTIVE,
                )

    def test_vehicle_registration_number_unique(self):
        Vehicle.objects.create(
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            registration_number="TS-DB-001",
            model="Test Car",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vehicle.objects.create(
                    driver=self.driver,
                    vehicle_type=self.vehicle_type,
                    registration_number="TS-DB-001",
                    model="Another Car",
                )

    # 2. FOREIGN KEY

    def test_ride_foreign_key_relationship(self):
        ride = Ride.objects.create(
            rider=self.user,
            vehicle_type=self.vehicle_type,
            status=self.ride_status,
            pickup_address="Hyderabad",
            pickup_latitude=Decimal("17.385000"),
            pickup_longitude=Decimal("78.486700"),
            dropoff_address="Secunderabad",
            dropoff_latitude=Decimal("17.439900"),
            dropoff_longitude=Decimal("78.498300"),
            fare=Decimal("100.00"),
        )

        self.assertEqual(ride.rider_id, self.user.id)
        self.assertEqual(ride.vehicle_type_id, self.vehicle_type.id)
        self.assertEqual(ride.status_id, self.ride_status.id)

    def test_vehicle_foreign_key_relationship(self):
        vehicle = Vehicle.objects.create(
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            registration_number="TS-DB-002",
            model="Test Car",
        )

        self.assertEqual(vehicle.driver_id, self.driver.id)
        self.assertEqual(vehicle.vehicle_type_id, self.vehicle_type.id)


    # 3. REQUIRED FIELDS

    def test_vehicle_type_name_required(self):
        vehicle_type = VehicleType(name="")

        with self.assertRaises(ValidationError):
            vehicle_type.full_clean()

    def test_vehicle_model_required(self):
        vehicle = Vehicle(
            driver=self.driver,
            vehicle_type=self.vehicle_type,
            registration_number="TS-DB-003",
            model="",
        )

        with self.assertRaises(ValidationError):
            vehicle.full_clean()

    # 4. ONE-TO-ONE RELATIONSHIP

    def test_driver_profile_user_one_to_one(self):
        another_user = User.objects.create_user(
            email="profile_test@test.com",
            password="Test@12345",
        )

        DriverProfile.objects.create(
            user=another_user,
            license_number="LIC-DB-002",
            status=DriverProfile.DriverStatus.ACTIVE,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DriverProfile.objects.create(
                    user=another_user,
                    license_number="LIC-DB-003",
                    status=DriverProfile.DriverStatus.ACTIVE,
                )

    # 5. MODEL CONSTRAINT

    def test_ride_fare_cannot_be_negative(self):
        ride = Ride(
            rider=self.user,
            vehicle_type=self.vehicle_type,
            status=self.ride_status,
            pickup_address="Hyderabad",
            pickup_latitude=Decimal("17.385000"),
            pickup_longitude=Decimal("78.486700"),
            dropoff_address="Secunderabad",
            dropoff_latitude=Decimal("17.439900"),
            dropoff_longitude=Decimal("78.498300"),
            fare=Decimal("-100.00"),
        )

        with self.assertRaises(ValidationError):
            ride.full_clean()

    # 6. INVALID RELATIONSHIP

    def test_invalid_rider_relationship(self):
        with self.assertRaises(ValueError):
            Ride(rider=self.vehicle_type)