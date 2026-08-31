from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..models import (
    Ride,
    RideStatus,
    DriverProfile,
)


class RideService:

    # =========================================================
    # ACCEPT RIDE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def accept_ride(
        ride_id,
        user,
    ):

        # -----------------------------------------------------
        # GET RIDE
        # -----------------------------------------------------

        try:
            ride = Ride.objects.select_for_update(of=("self",)).get(id=ride_id)

        except Ride.DoesNotExist:
            raise

        # -----------------------------------------------------
        # DRIVER CHECK
        # -----------------------------------------------------

        try:
            driver = DriverProfile.objects.select_related("user").get(user=user)

        except DriverProfile.DoesNotExist:
            raise PermissionError("You are not registered as a driver.")

        # -----------------------------------------------------
        # DRIVER ACTIVE CHECK
        # -----------------------------------------------------

        if driver.status != DriverProfile.DriverStatus.ACTIVE:
            raise PermissionError("Your driver account is not active.")

        # -----------------------------------------------------
        # RIDE STATUS CHECK
        # -----------------------------------------------------

        if ride.status.name != RideStatus.Status.REQUESTED:
            raise ValueError(
                f"Ride cannot be accepted from " f"'{ride.status.name}' status."
            )

        # -----------------------------------------------------
        # ASSIGN DRIVER
        # -----------------------------------------------------

        ride.driver = driver

        # -----------------------------------------------------
        # GET ACCEPTED STATUS
        # -----------------------------------------------------

        try:
            accepted_status = RideStatus.objects.get(name=RideStatus.Status.ACCEPTED)

        except RideStatus.DoesNotExist:
            raise ValueError("Accepted ride status is not configured.")

        # -----------------------------------------------------
        # UPDATE RIDE
        # -----------------------------------------------------

        ride.status = accepted_status

        ride.save(
            update_fields=[
                "driver",
                "status",
                "updated_at",
            ]
        )

        return ride

    # =========================================================
    # UPDATE RIDE STATUS
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_status(
        ride_id,
        driver,
        new_status_name,
    ):

        # -----------------------------------------------------
        # GET RIDE
        # -----------------------------------------------------
        # Do NOT use select_related("driver") here because
        # Ride.driver is nullable.

        try:
            ride = (
                Ride.objects.select_for_update()
                .select_related("status")
                .get(id=ride_id)
            )

        except Ride.DoesNotExist:
            raise

        # -----------------------------------------------------
        # DRIVER CHECK
        # -----------------------------------------------------

        try:
            driver_profile = DriverProfile.objects.get(user=driver)

        except DriverProfile.DoesNotExist:
            raise PermissionError("You are not registered as a driver.")

        # -----------------------------------------------------
        # RIDE DRIVER OWNERSHIP
        # -----------------------------------------------------

        if ride.driver_id != driver_profile.id:
            raise PermissionError("You are not assigned to this ride.")

        # -----------------------------------------------------
        # CURRENT STATUS
        # -----------------------------------------------------

        current_status = ride.status.name

        # -----------------------------------------------------
        # ALLOWED TRANSITIONS
        # -----------------------------------------------------

        allowed_transitions = {
            RideStatus.Status.REQUESTED: [
                RideStatus.Status.ACCEPTED,
                RideStatus.Status.CANCELLED,
            ],
            RideStatus.Status.ACCEPTED: [
                RideStatus.Status.DRIVER_ARRIVING,
                RideStatus.Status.STARTED,
                RideStatus.Status.COMPLETED,
                RideStatus.Status.CANCELLED,
            ],
            RideStatus.Status.DRIVER_ARRIVING: [
                RideStatus.Status.STARTED,
                RideStatus.Status.CANCELLED,
            ],
            RideStatus.Status.STARTED: [
                RideStatus.Status.COMPLETED,
            ],
            RideStatus.Status.COMPLETED: [],
            RideStatus.Status.CANCELLED: [],
        }

        allowed_statuses = allowed_transitions.get(current_status, [])

        # -----------------------------------------------------
        # VALIDATE TRANSITION
        # -----------------------------------------------------

        if new_status_name not in allowed_statuses:
            raise ValueError(
                f"Cannot change ride status "
                f"from '{current_status}' "
                f"to '{new_status_name}'."
            )

        # -----------------------------------------------------
        # GET NEW STATUS
        # -----------------------------------------------------

        try:
            new_status = RideStatus.objects.get(name=new_status_name)

        except RideStatus.DoesNotExist:
            raise ValueError(f"Ride status '{new_status_name}' " f"is not configured.")

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        ride.status = new_status

        ride.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        # -----------------------------------------------------
        # BROADCAST RIDE STATUS
        # -----------------------------------------------------

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"ride_{ride.id}",
            {
                "type": "ride_status_update",
                "ride_id": str(ride.id),
                "status": ride.status.name,
                "message": f"Ride status changed to {ride.status.name}",
            },
        )

        return ride

    # =========================================================
    # CANCEL RIDE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def cancel_ride(
        ride_id,
        rider,
    ):

        # -----------------------------------------------------
        # GET RIDE
        # -----------------------------------------------------
        # Do NOT use select_related("driver") here because
        # Ride.driver is nullable.

        try:
            ride = (
                Ride.objects.select_for_update()
                .select_related("status")
                .get(id=ride_id)
            )

        except Ride.DoesNotExist:
            raise

        # -----------------------------------------------------
        # RIDER OWNERSHIP
        # -----------------------------------------------------

        if ride.rider_id != rider.id:
            raise PermissionError("You are not allowed to cancel this ride.")

        # -----------------------------------------------------
        # CURRENT STATUS
        # -----------------------------------------------------

        current_status = ride.status.name

        # -----------------------------------------------------
        # CANCELLABLE STATUSES
        # -----------------------------------------------------

        cancellable_statuses = [
            RideStatus.Status.REQUESTED,
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
        ]

        if current_status not in cancellable_statuses:
            raise ValueError(
                f"Ride cannot be cancelled from " f"'{current_status}' status."
            )

        # -----------------------------------------------------
        # GET CANCELLED STATUS
        # -----------------------------------------------------

        try:
            cancelled_status = RideStatus.objects.get(name=RideStatus.Status.CANCELLED)

        except RideStatus.DoesNotExist:
            raise ValueError("Cancelled ride status is not configured.")

        # -----------------------------------------------------
        # CANCEL RIDE
        # -----------------------------------------------------

        ride.status = cancelled_status

        ride.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return ride
