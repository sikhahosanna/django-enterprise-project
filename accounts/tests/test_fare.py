from decimal import Decimal

from django.test import TestCase

from accounts.models import VehicleType
from accounts.services.fare_service import FareService


class FareCalculationTest(TestCase):

    def setUp(self):

        self.vehicle_type = VehicleType.objects.create(
            name="car"
        )

    def test_fare_calculation(self):

        result = FareService.calculate_fare(

            vehicle_type=self.vehicle_type,

            pickup_latitude=16.3067,
            pickup_longitude=80.4365,

            dropoff_latitude=16.3200,
            dropoff_longitude=80.4500,

            duration_minutes=10,
        )

        self.assertIn(
            "base_fare",
            result
        )

        self.assertIn(
            "distance_fare",
            result
        )

        self.assertIn(
            "time_fare",
            result
        )

        self.assertIn(
            "surge",
            result
        )

        self.assertIn(
            "total",
            result
        )

        self.assertGreater(
            result["total"],
            Decimal("0")
        )