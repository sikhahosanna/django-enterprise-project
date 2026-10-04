import logging

from ..models import (
    DriverProfile,
    DriverLocation,
    Ride,
    RideStatus,
)


database_logger = logging.getLogger("database")


class DriverService:

    @classmethod
    def get_driver_for_user(cls, user):

        try:
            return DriverProfile.objects.get(user=user)

        except DriverProfile.DoesNotExist:
            database_logger.warning(
                "Driver profile not found for user"
            )
            raise PermissionError(
                "You are not registered as a driver."
            )

    @classmethod
    def validate_active_driver(cls, driver):

        if driver.status != DriverProfile.DriverStatus.ACTIVE:
            raise PermissionError(
                "Driver is not active."
            )

        return driver

    @classmethod
    def has_active_ride(cls, driver):

        active_statuses = {
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
            RideStatus.Status.STARTED,
        }

        return Ride.objects.filter(
            driver=driver,
            status__name__in=active_statuses,
        ).exists()

    @classmethod
    def update_location(
        cls,
        driver,
        latitude,
        longitude,
        availability_status,
    ):
        return DriverLocation.objects.update_or_create(
            driver=driver,
            defaults={
                "latitude": latitude,
                "longitude": longitude,
                "availability_status": availability_status,
            },
        )

    @classmethod
    def get_location(cls, driver):

        return DriverLocation.objects.get(
            driver=driver,
        )

    @classmethod
    def update_availability(
        cls,
        driver,
        availability_status,
    ):

        location = cls.get_location(driver)

        location.availability_status = availability_status

        location.save(
            update_fields=[
                "availability_status",
                "last_updated",
            ]
        )

        return location