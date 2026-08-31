from ..tasks import (
    ride_accepted_notification,
    driver_arriving_notification,
    ride_started_notification,
    ride_completed_event_notification,
    ride_cancelled_notification,
)


class NotificationService:

    @staticmethod
    def ride_accepted(ride):
        ride_accepted_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def driver_arriving(ride):
        driver_arriving_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_started(ride):
        ride_started_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_completed(ride):
        ride_completed_event_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_cancelled(ride):
        ride_cancelled_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )
