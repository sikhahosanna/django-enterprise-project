

from ..models import (
    DriverProfile,
    Ride,
    RideStatus,
)


class DriverService:

    @classmethod
    def get_driver_for_user(cls, user):

        try:
            return DriverProfile.objects.get(user=user)
        except DriverProfile.DoesNotExist:
            raise PermissionError("You are not registered as a driver.")

    @classmethod
    def validate_active_driver(cls, driver):

        if driver.status != DriverProfile.DriverStatus.ACTIVE:
            raise PermissionError("Driver is not active.")

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
