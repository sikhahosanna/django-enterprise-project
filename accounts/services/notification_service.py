import logging

from ..tasks import (
    ride_accepted_notification,
    driver_arriving_notification,
    ride_started_notification,
    ride_completed_event_notification,
    ride_cancelled_notification,
)

celery_logger = logging.getLogger("celery")


class NotificationService:

    @staticmethod
    def ride_accepted(ride):
        celery_logger.info("Ride accepted notification task triggered")
        ride_accepted_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def driver_arriving(ride):
        celery_logger.info("Driver arriving notification task triggered")
        driver_arriving_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_started(ride):
        celery_logger.info("Ride started notification task triggered")
        ride_started_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_completed(ride):
        celery_logger.info("Ride completed notification task triggered")
        ride_completed_event_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )

    @staticmethod
    def ride_cancelled(ride):
        celery_logger.info("Ride cancelled notification task triggered")
        ride_cancelled_notification.delay(
            ride_id=str(ride.id),
            passenger_id=str(ride.rider.id),
        )