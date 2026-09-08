import logging
import time

from celery import shared_task

from .models import Notification


logger = logging.getLogger(__name__)


@shared_task(queue="notifications")
def ride_notification(ride_id, user_id, message):
    start_time = time.perf_counter()

    try:
        notification, created = Notification.objects.get_or_create(
            user_id=user_id,
            ride_id=ride_id,
            notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            defaults={
                "message": message,
            },
        )

        execution_time = time.perf_counter() - start_time

        logger.info(
            "Ride notification processed for ride_id=%s, created=%s, execution_time=%.4f seconds",
            ride_id,
            created,
            execution_time,
        )

        return {
            "notification_id": str(notification.id),
            "created": created,
            "execution_time": execution_time,
        }

    except Exception:
        execution_time = time.perf_counter() - start_time

        logger.error(
            "Background task failed: ride notification, execution_time=%.4f seconds",
            execution_time,
            exc_info=True,
        )
        raise

@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(queue="notifications")
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


@shared_task(
    queue="notifications",
    bind=True,
    max_retries=2,
)
def retry_test_task(self):
    attempt = self.request.retries + 1

    logger.info(
        "Retry test task started: attempt=%s",
        attempt,
    )

    try:
        # Simulate failure for first 2 attempts
        if attempt < 3:
            raise Exception(
                f"Simulated failure on attempt {attempt}"
            )

        logger.info(
            "Retry test task succeeded: attempt=%s",
            attempt,
        )

        return "Retry test successful"

    except Exception as exc:
        logger.error(
            "Retry test task failed: attempt=%s",
            attempt,
            exc_info=True,
        )

        if self.request.retries < self.max_retries:
            logger.warning(
                "Retrying task: attempt=%s",
                attempt,
            )
            raise self.retry(
                exc=exc,
                countdown=2,
            )

        logger.error(
            "Retry test task failed permanently after %s attempts",
            attempt,
        )
        raise

@shared_task(queue="reports")
def generate_ride_report():
    try:
        logger.info("Ride report generation started")

        # Report generation logic will be added here

        logger.info("Ride report generated successfully")

        return "Ride report generated successfully"

    except Exception:
        logger.error(
            "Background task failed: ride report generation",
            exc_info=True,
        )
        raise

@shared_task(queue="maintenance")
def clean_expired_data():
    try:
        logger.info("Expired data cleanup started")

        # Expired data cleanup logic will be added here

        logger.info("Expired data cleaned successfully")

        return "Expired data cleaned successfully"

    except Exception:
        logger.error(
            "Background task failed: expired data cleanup",
            exc_info=True,
        )
        raise


@shared_task(queue="maintenance")
def process_background_records():
    try:
        logger.info("Background record processing started")

        # Background processing logic will be added here

        logger.info("Background records processed successfully")

        return "Background records processed successfully"

    except Exception:
        logger.error(
            "Background task failed: background record processing",
            exc_info=True,
        )
        raise