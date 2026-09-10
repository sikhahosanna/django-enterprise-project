import logging

from ..models import DriverProfile, Vehicle

database_logger = logging.getLogger("database")


class VehicleService:

    @staticmethod
    def get_driver(user):
        try:
            return user.driver_profile
        except DriverProfile.DoesNotExist:
            database_logger.warning(
                "Driver profile not found while accessing vehicle"
            )
            raise PermissionError("You are not registered as a driver.")

    @staticmethod
    def get_vehicle_queryset(user):
        queryset = Vehicle.objects.select_related(
            "driver",
            "driver__user",
            "vehicle_type",
        )

        if user.is_staff:
            return queryset

        return queryset.filter(driver__user=user)

    @staticmethod
    def save_vehicle(serializer, user):
        if user.is_staff:
            return serializer.save()

        driver = VehicleService.get_driver(user)

        return serializer.save(driver=driver)