import logging

from decimal import Decimal, ROUND_HALF_UP
from math import radians, sin, cos, sqrt, atan2
from ..models import VehicleType
from django.core.exceptions import ValidationError
from django.conf import settings

database_logger = logging.getLogger("database")


class FareService:

    @staticmethod
    def get_vehicle_type(vehicle_type_id):
        try:
            return VehicleType.objects.get(id=vehicle_type_id)

        except (VehicleType.DoesNotExist, ValidationError, ValueError, TypeError):
            database_logger.warning(
                "Vehicle type not found or invalid vehicle type ID"
            )
            return None

    # Calculate distance

    @classmethod
    def calculate_distance(
        cls,
        pickup_latitude,
        pickup_longitude,
        dropoff_latitude,
        dropoff_longitude,
    ):

        earth_radius_km = 6371

        lat1 = radians(float(pickup_latitude))
        lon1 = radians(float(pickup_longitude))

        lat2 = radians(float(dropoff_latitude))
        lon2 = radians(float(dropoff_longitude))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return earth_radius_km * c

    # Calculate fare

    @classmethod
    def calculate_fare(
        cls,
        vehicle_type,
        pickup_latitude,
        pickup_longitude,
        dropoff_latitude,
        dropoff_longitude,
        duration_minutes=0,
        surge_multiplier=None,
    ):

        distance_km = cls.calculate_distance(
            pickup_latitude,
            pickup_longitude,
            dropoff_latitude,
            dropoff_longitude,
        )

        base_fare = vehicle_type.base_fare
        cost_per_km = vehicle_type.cost_per_km
        cost_per_minute = vehicle_type.cost_per_minute

        fare = (
            base_fare
            + (cost_per_km * distance_km)
            + (cost_per_minute * duration_minutes)
        )

        if surge_multiplier is not None:
            fare *= surge_multiplier

        return Decimal(fare).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    