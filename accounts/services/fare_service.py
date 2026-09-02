from decimal import Decimal, ROUND_HALF_UP
from math import radians, sin, cos, sqrt, atan2
from ..models import VehicleType
from django.core.exceptions import ValidationError

from django.conf import settings


class FareService:

    @staticmethod
    def get_vehicle_type(vehicle_type_id):

       try:
          return VehicleType.objects.get(id=vehicle_type_id)

       except (VehicleType.DoesNotExist, ValidationError, ValueError, TypeError):
          return None

    # =========================================================
    # CALCULATE DISTANCE
    # =========================================================

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

    # =========================================================
    # CALCULATE FARE
    # =========================================================

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

        # -----------------------------------------------------
        # DISTANCE
        # -----------------------------------------------------

        distance_km = cls.calculate_distance(
            pickup_latitude,
            pickup_longitude,
            dropoff_latitude,
            dropoff_longitude,
        )

        # -----------------------------------------------------
        # FARE CONFIGURATION
        # -----------------------------------------------------

        pricing = getattr(settings, "RIDE_FARE_CONFIG", {})

        vehicle_name = vehicle_type.name.strip().lower()

        if vehicle_name not in pricing:

            raise ValueError(
                "Fare pricing is not configured "
                f"for vehicle type "
                f"'{vehicle_type.name}'."
            )

        vehicle_pricing = pricing[vehicle_name]

        # -----------------------------------------------------
        # BASE FARE
        # -----------------------------------------------------

        base_fare = Decimal(str(vehicle_pricing["base_fare"]))

        # -----------------------------------------------------
        # PER KM
        # -----------------------------------------------------

        per_km = Decimal(str(vehicle_pricing["per_km"]))

        # -----------------------------------------------------
        # PER MINUTE
        # -----------------------------------------------------

        per_minute = Decimal(str(vehicle_pricing["per_minute"]))

        # -----------------------------------------------------
        # DISTANCE FARE
        # -----------------------------------------------------

        distance_fare = Decimal(str(distance_km)) * per_km

        # -----------------------------------------------------
        # TIME FARE
        # -----------------------------------------------------

        time_fare = Decimal(str(duration_minutes)) * per_minute

        # -----------------------------------------------------
        # SUBTOTAL
        # -----------------------------------------------------

        subtotal = base_fare + distance_fare + time_fare

        # -----------------------------------------------------
        # SURGE MULTIPLIER
        # -----------------------------------------------------

        if surge_multiplier is None:

            surge_multiplier = Decimal(
                str(
                    getattr(
                        settings,
                        "RIDE_SURGE_MULTIPLIER",
                        "1.00",
                    )
                )
            )

        else:

            surge_multiplier = Decimal(str(surge_multiplier))

        if surge_multiplier < Decimal("1.00"):

            raise ValueError("Surge multiplier cannot " "be less than 1.00.")

        # -----------------------------------------------------
        # SURGE
        # -----------------------------------------------------

        surge = subtotal * (surge_multiplier - Decimal("1.00"))

        # -----------------------------------------------------
        # TOTAL
        # -----------------------------------------------------

        total = subtotal + surge

        # -----------------------------------------------------
        # RETURN
        # -----------------------------------------------------

        return {
            "base_fare": cls.round_value(base_fare),
            "distance_fare": cls.round_value(distance_fare),
            "time_fare": cls.round_value(time_fare),
            "surge": cls.round_value(surge),
            "total": cls.round_value(total),
            "distance_km": cls.round_value(distance_km),
            "surge_multiplier": surge_multiplier,
        }

    # =========================================================
    # ROUND VALUE
    # =========================================================

    @staticmethod
    def round_value(value):

        return Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
