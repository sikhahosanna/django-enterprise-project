from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..models import (
    Ride,
    RideStatus,
    DriverProfile,
)

from .fare_service import FareService


class RideService:

    # Create ride
    @staticmethod
    @transaction.atomic
    def create_ride(rider, validated_data):
        validated_data.pop("rider", None)

        # Get requested status
        try:
            requested_status = RideStatus.objects.get(
                name=RideStatus.Status.REQUESTED
            )
        except RideStatus.DoesNotExist:
            raise ValueError(
                "Requested ride status is not configured."
            )

        # Calculate fare
        fare_details = FareService.calculate_fare(
            vehicle_type=validated_data["vehicle_type"],
            pickup_latitude=validated_data["pickup_latitude"],
            pickup_longitude=validated_data["pickup_longitude"],
            dropoff_latitude=validated_data["dropoff_latitude"],
            dropoff_longitude=validated_data["dropoff_longitude"],
            duration_minutes=0,
        )

        final_fare = fare_details["total"]

        # Create ride
        return Ride.objects.create(
            rider=rider,
            driver=None,
            status=requested_status,
            fare=final_fare,
            **validated_data,
        )

    # Accept ride
    @staticmethod
    @transaction.atomic
    def accept_ride(ride_id, user):

        # Get ride
        try:
            ride = Ride.objects.select_for_update(
                of=("self",)
            ).get(id=ride_id)
        except Ride.DoesNotExist:
            raise

        # Driver check
        try:
            driver = DriverProfile.objects.select_related(
                "user"
            ).get(user=user)
        except DriverProfile.DoesNotExist:
            raise PermissionError(
                "You are not registered as a driver."
            )

        # Driver active check
        if driver.status != DriverProfile.DriverStatus.ACTIVE:
            raise PermissionError(
                "Your driver account is not active."
            )

        # Ride status check
        if ride.status.name != RideStatus.Status.REQUESTED:
            raise ValueError(
                f"Ride cannot be accepted from "
                f"'{ride.status.name}' status."
            )

        # Assign driver
        ride.driver = driver

        # Get accepted status
        try:
            accepted_status = RideStatus.objects.get(
                name=RideStatus.Status.ACCEPTED
            )
        except RideStatus.DoesNotExist:
            raise ValueError(
                "Accepted ride status is not configured."
            )

        # Update ride
        ride.status = accepted_status

        ride.save(
            update_fields=[
                "driver",
                "status",
                "updated_at",
            ]
        )

        # Broadcast ride accepted
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"ride_{ride.id}",
            {
                "type": "ride_status_update",
                "ride_id": str(ride.id),
                "status": ride.status.name,
                "message": "Ride accepted successfully",
            },
        )

        return ride

    # Update ride status
    @staticmethod
    @transaction.atomic
    def update_status(
        ride_id,
        driver,
        new_status_name,
    ):

        # Get ride
        try:
            ride = (
                Ride.objects.select_for_update()
                .select_related("status")
                .get(id=ride_id)
            )
        except Ride.DoesNotExist:
            raise

        # Driver check
        try:
            driver_profile = DriverProfile.objects.get(
                user=driver
            )
        except DriverProfile.DoesNotExist:
            raise PermissionError(
                "You are not registered as a driver."
            )

        # Driver ownership check
        if ride.driver_id != driver_profile.id:
            raise PermissionError(
                "You are not assigned to this ride."
            )

        # Current status
        current_status = ride.status.name

        # Allowed status transitions
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

        allowed_statuses = allowed_transitions.get(
            current_status,
            []
        )

        # Validate transition
        if new_status_name not in allowed_statuses:
            raise ValueError(
                f"Cannot change ride status "
                f"from '{current_status}' "
                f"to '{new_status_name}'."
            )

        # Get new status
        try:
            new_status = RideStatus.objects.get(
                name=new_status_name
            )
        except RideStatus.DoesNotExist:
            raise ValueError(
                f"Ride status '{new_status_name}' "
                f"is not configured."
            )

        # Update status
        ride.status = new_status

        ride.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # Broadcast status
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

    # Cancel ride
    @staticmethod
    @transaction.atomic
    def cancel_ride(ride_id, rider):

        # Get ride
        try:
            ride = (
                Ride.objects.select_for_update()
                .select_related("status")
                .get(id=ride_id)
            )
        except Ride.DoesNotExist:
            raise

        # Rider ownership check
        if ride.rider_id != rider.id:
            raise PermissionError(
                "You are not allowed to cancel this ride."
            )

        # Current status
        current_status = ride.status.name

        # Cancellable statuses
        cancellable_statuses = [
            RideStatus.Status.REQUESTED,
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
        ]

        if current_status not in cancellable_statuses:
            raise ValueError(
                f"Ride cannot be cancelled from "
                f"'{current_status}' status."
            )

        # Get cancelled status
        try:
            cancelled_status = RideStatus.objects.get(
                name=RideStatus.Status.CANCELLED
            )
        except RideStatus.DoesNotExist:
            raise ValueError(
                "Cancelled ride status is not configured."
            )

        # Cancel ride
        ride.status = cancelled_status

        ride.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return ride