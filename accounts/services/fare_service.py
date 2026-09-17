import logging

from decimal import Decimal, ROUND_HALF_UP
from math import radians, sin, cos, sqrt, atan2

from ..models import VehicleType
from django.core.exceptions import ValidationError

database_logger = logging.getLogger("database")


class FareService:

    @staticmethod
    def get_vehicle_type(vehicle_type_id):
        try:
            return VehicleType.objects.get(id=vehicle_type_id)

        except (
            VehicleType.DoesNotExist,
            ValidationError,
            ValueError,
            TypeError,
        ):
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

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        )

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

        # Convert all fare values to Decimal
        base_fare = Decimal(str(vehicle_type.base_fare))
        cost_per_km = Decimal(str(vehicle_type.cost_per_km))
        cost_per_minute = Decimal(str(vehicle_type.cost_per_minute))
        distance_km = Decimal(str(distance_km))
        duration_minutes = Decimal(str(duration_minutes))

        # Calculate individual fare components
        distance_fare = cost_per_km * distance_km
        time_fare = cost_per_minute * duration_minutes

        # Default surge multiplier
        surge = Decimal("1.00")

        if surge_multiplier is not None:
            surge = Decimal(str(surge_multiplier))

        # Calculate total fare
        total = (
            base_fare
            + distance_fare
            + time_fare
        ) * surge

        # Return detailed fare breakdown
        return {
            "base_fare": base_fare.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
            "distance_fare": distance_fare.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
            "time_fare": time_fare.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
            "surge": surge,
            "total": total.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
        }