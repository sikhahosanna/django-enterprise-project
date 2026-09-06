import logging

from celery import shared_task

from .models import Notification


logger = logging.getLogger(__name__)


@shared_task
def ride_notification(ride_id, user_id, message):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=user_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            defaults={
                "message": message,
            },
        )

        logger.info(
            "Ride notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: ride notification",
            exc_info=True,
        )
        raise


@shared_task
def driver_assignment_notification(ride_id, user_id, driver_id):
    try:
        logger.info(
            "Driver assignment notification processed for ride_id=%s",
            ride_id,
        )

        return "Driver assignment notification sent"

    except Exception:
        logger.error(
            "Background task failed: driver assignment notification",
            exc_info=True,
        )
        raise


@shared_task
def ride_completion_notification(ride_id, user_id):
    try:
        logger.info(
            "Ride completion notification processed for ride_id=%s",
            ride_id,
        )

        return "Ride completion notification sent"

    except Exception:
        logger.error(
            "Background task failed: ride completion notification",
            exc_info=True,
        )
        raise


@shared_task
def reminder_notification(ride_id, user_id, message):
    try:
        logger.info(
            "Reminder notification processed for ride_id=%s",
            ride_id,
        )

        return "Reminder notification sent"

    except Exception:
        logger.error(
            "Background task failed: reminder notification",
            exc_info=True,
        )
        raise


@shared_task
def ride_accepted_notification(ride_id, passenger_id):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=passenger_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            defaults={
                "title": "Ride Accepted",
                "message": "Your driver has accepted the ride.",
            },
        )

        logger.info(
            "Ride accepted notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: ride accepted notification",
            exc_info=True,
        )
        raise


@shared_task
def ride_completed_event_notification(ride_id, passenger_id):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=passenger_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_COMPLETED,
            defaults={
                "message": "Your ride has been completed.",
            },
        )

        logger.info(
            "Ride completed notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: ride completed notification",
            exc_info=True,
        )
        raise


@shared_task
def driver_arriving_notification(ride_id, passenger_id):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=passenger_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.DRIVER_ARRIVING,
            defaults={
                "title": "Driver Arriving",
                "message": "Your driver is arriving.",
            },
        )

        logger.info(
            "Driver arriving notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: driver arriving notification",
            exc_info=True,
        )
        raise


@shared_task
def ride_started_notification(ride_id, passenger_id):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=passenger_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_STARTED,
            defaults={
                "title": "Ride Started",
                "message": "Your ride has started.",
            },
        )

        logger.info(
            "Ride started notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: ride started notification",
            exc_info=True,
        )
        raise


@shared_task
def ride_cancelled_notification(ride_id, passenger_id):
    try:
        notification, created = Notification.objects.get_or_create(
            user_id=passenger_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_CANCELLED,
            defaults={
                "title": "Ride Cancelled",
                "message": "Your ride has been cancelled.",
            },
        )

        logger.info(
            "Ride cancelled notification processed for ride_id=%s",
            ride_id,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
        }

    except Exception:
        logger.error(
            "Background task failed: ride cancelled notification",
            exc_info=True,
        )
        raise


@shared_task(bind=True, max_retries=2)
def retry_test_task(self):
    attempt = self.request.retries + 1

    logger.info(
        "Retry test task started: attempt=%s",
        attempt,
    )

    if attempt < 3:
        logger.warning(
            "Retry test task failed, retrying: attempt=%s",
            attempt,
        )

        raise self.retry(countdown=2)

    logger.info(
        "Retry test task succeeded: attempt=%s",
        attempt,
    )

    return "Retry test successful"