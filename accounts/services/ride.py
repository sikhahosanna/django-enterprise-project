from django.db import transaction

from ..models import (
    Ride,
    RideStatus,
    DriverProfile,
)


class RideService:

    # =========================================================
    # TASK 5 + TASK 6
    # ACCEPT RIDE
    # =========================================================

    @classmethod
    @transaction.atomic
    def accept_ride(cls, ride_id, user):

        # -----------------------------------------------------
        # 1. LOCK ONLY RIDE ROW
        # -----------------------------------------------------

        ride = (
            Ride.objects
            .select_for_update()
            .get(id=ride_id)
        )

        # -----------------------------------------------------
        # 2. CHECK DRIVER
        # -----------------------------------------------------

        try:

            driver = user.driver_profile

        except DriverProfile.DoesNotExist:

            raise PermissionError(
                "You are not registered as a driver."
            )

        # -----------------------------------------------------
        # 3. CHECK DRIVER STATUS
        # -----------------------------------------------------

        if driver.status != "active":

            raise PermissionError(
                "Driver is not active."
            )

        # -----------------------------------------------------
        # 4. CHECK RIDE STATUS
        # -----------------------------------------------------

        if not ride.status:

            raise ValueError(
                "Ride status is not available."
            )

        if ride.status.name.lower() != "requested":

            raise ValueError(
                "Ride cannot be accepted in its current status."
            )

        # -----------------------------------------------------
        # 5. CHECK ALREADY ASSIGNED DRIVER
        # -----------------------------------------------------

        if ride.driver_id is not None:

            raise ValueError(
                "Ride has already been accepted."
            )

        # -----------------------------------------------------
        # 6. GET ACCEPTED STATUS
        # -----------------------------------------------------

        accepted_status = (
            RideStatus.objects
            .get(
                name__iexact="accepted"
            )
        )

        # -----------------------------------------------------
        # 7. ASSIGN DRIVER
        # -----------------------------------------------------

        ride.driver = driver

        # -----------------------------------------------------
        # 8. UPDATE STATUS
        # -----------------------------------------------------

        ride.status = accepted_status

        # -----------------------------------------------------
        # 9. SAVE
        # -----------------------------------------------------

        ride.save(
            update_fields=[
                "driver",
                "status",
                "updated_at",
            ]
        )

        # -----------------------------------------------------
        # 10. RETURN
        # -----------------------------------------------------

        return ride
    # =========================================================
    # TASK 7 - CANCEL RIDE
    # =========================================================

    @classmethod
    @transaction.atomic
    def cancel_ride(cls, ride_id, rider):

        # Lock ONLY the ride row
        ride = (
            Ride.objects
            .select_for_update()
            .get(id=ride_id)
        )

        # -----------------------------------------------------
        # CHECK RIDER
        # -----------------------------------------------------

        if ride.rider_id != rider.id:
            raise PermissionError(
                "You can cancel only your own ride."
            )

        # -----------------------------------------------------
        # CHECK CURRENT STATUS
        # -----------------------------------------------------

        if not ride.status:
            raise ValueError(
                "Ride status is not configured."
            )

        current_status = ride.status.name.lower()

        # -----------------------------------------------------
        # ALREADY CANCELLED
        # -----------------------------------------------------

        if current_status == "cancelled":
            raise ValueError(
                "Ride is already cancelled."
            )

        # -----------------------------------------------------
        # INVALID STATES
        # -----------------------------------------------------

        if current_status not in [
            "requested",
            "accepted",
        ]:
            raise ValueError(
                "Ride cannot be cancelled in its current status."
            )

        # -----------------------------------------------------
        # GET CANCELLED STATUS
        # -----------------------------------------------------

        cancelled_status = (
            RideStatus.objects
            .get(name__iexact="cancelled")
        )

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        ride.status = cancelled_status

        ride.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return ride