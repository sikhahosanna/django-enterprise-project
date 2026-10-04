import logging

from ..models import Notification

from ..tasks import (
    ride_accepted_notification,
    driver_arriving_notification,
    ride_started_notification,
    ride_completed_event_notification,
    ride_cancelled_notification,
    booking_created_notification,
    payment_successful_notification,
    booking_confirmed_notification,
    provider_started_notification,
    booking_completed_notification,
    booking_cancelled_notification,
    saved_service_unavailable_notification,
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

    @staticmethod
    def booking_created(booking):
        booking_created_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def payment_successful(booking):
        payment_successful_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def booking_confirmed(booking):
        booking_confirmed_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def provider_started(booking):
        provider_started_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def booking_completed(booking):
        booking_completed_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def booking_cancelled(booking):
        booking_cancelled_notification.delay(
            booking_id=str(booking.id),
            user_id=str(booking.customer.id),
        )

    @staticmethod
    def saved_service_unavailable(service):
        celery_logger.info(
            "Saved service unavailable notification task triggered"
        )

        saved_service_unavailable_notification.delay(
            service_id=str(service.id)
        )

    @staticmethod
    def mark_as_read(notification_id, user):
        notification = Notification.objects.get(
            id=notification_id,
            user=user,
        )

        notification.is_read = True
        notification.save(
            update_fields=["is_read"]
        )

        return notification

    @staticmethod
    def mark_all_as_read(user):
        return Notification.objects.filter(
            user=user,
            is_read=False,
        ).update(
            is_read=True
        )