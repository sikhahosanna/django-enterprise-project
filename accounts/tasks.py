import logging
import time
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Notification, Ride, RideStatus

logger = logging.getLogger(__name__)


# Notifications

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
                "title": "Ride Completed",
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


# Retry

@shared_task(bind=True, max_retries=2)
def retry_test_task(self):
    logger.info(f"Retry test started. Attempt: {self.request.retries + 1}")

    try:
        if self.request.retries < 2:
            raise Exception("Simulated task failure")

        logger.info("Retry test completed successfully")
        return "Task completed successfully"

    except Exception as exc:
        logger.error(
            f"Task failed on attempt {self.request.retries + 1}: {exc}"
        )
        raise self.retry(exc=exc, countdown=2)
# Ride Report

@shared_task(queue="reports")
def generate_ride_report():
    start_time = time.time()
    logger.info("Ride report generation started")
    try:
        

        total_rides = Ride.objects.count()

        completed_rides = Ride.objects.filter(
            status__name=RideStatus.Status.COMPLETED
        ).count()

        cancelled_rides = Ride.objects.filter(
            status__name=RideStatus.Status.CANCELLED
        ).count()

        requested_rides = Ride.objects.filter(
            status__name=RideStatus.Status.REQUESTED
        ).count()

        accepted_rides = Ride.objects.filter(
            status__name=RideStatus.Status.ACCEPTED
        ).count()

        started_rides = Ride.objects.filter(
            status__name=RideStatus.Status.STARTED
        ).count()

        completed_fare = sum(
            ride.fare
            for ride in Ride.objects.filter(
                status__name=RideStatus.Status.COMPLETED
            )
        )

        report = {
            "total_rides": total_rides,
            "requested_rides": requested_rides,
            "accepted_rides": accepted_rides,
            "started_rides": started_rides,
            "completed_rides": completed_rides,
            "cancelled_rides": cancelled_rides,
            "total_completed_fare": float(completed_fare),
        }

        logger.info(
            "Ride report generated successfully: %s",
            report,
        )

        return report

    except Exception:
        logger.error(
            "Background task failed: ride report generation",
            exc_info=True,
        )
        raise


# Clean Expired Data

@shared_task(queue="maintenance")
def clean_expired_data():
    try:
        logger.info("Expired data cleanup started")

        cutoff_date = timezone.now() - timedelta(days=30)

        deleted_count, _ = Notification.objects.filter(
            is_read=True,
            created_at__lt=cutoff_date,
        ).delete()

        logger.info(
            "Expired data cleaned successfully: deleted_notifications=%s",
            deleted_count,
        )

        return {
            "deleted_notifications": deleted_count,
        }

    except Exception:
        logger.error(
            "Background task failed: expired data cleanup",
            exc_info=True,
        )
        raise


# Background Records

@shared_task(queue="maintenance")
def process_background_records():
    try:
        logger.info("Background record processing started")

        requested_rides = Ride.objects.filter(
            status__name=RideStatus.Status.REQUESTED
        ).count()

        accepted_rides = Ride.objects.filter(
            status__name=RideStatus.Status.ACCEPTED
        ).count()

        started_rides = Ride.objects.filter(
            status__name=RideStatus.Status.STARTED
        ).count()

        completed_rides = Ride.objects.filter(
            status__name=RideStatus.Status.COMPLETED
        ).count()

        cancelled_rides = Ride.objects.filter(
            status__name=RideStatus.Status.CANCELLED
        ).count()

        result = {
            "requested_rides": requested_rides,
            "accepted_rides": accepted_rides,
            "started_rides": started_rides,
            "completed_rides": completed_rides,
            "cancelled_rides": cancelled_rides,
        }

        logger.info(
            "Background records processed successfully: %s",
            result,
        )

        return result

    except Exception:
        logger.error(
            "Background task failed: background record processing",
            exc_info=True,
        )
        raise