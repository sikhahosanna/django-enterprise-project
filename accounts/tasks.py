from celery import shared_task

from .models import Notification


@shared_task
def ride_notification(ride_id, user_id, message):

    notification, created = Notification.objects.get_or_create(
        user_id=user_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.RIDE_ACCEPTED,
        defaults={
            "message": message,
        },
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task
def driver_assignment_notification(ride_id, user_id, driver_id):
    print(f"Driver assignment: ride={ride_id}, " f"user={user_id}, driver={driver_id}")
    return "Driver assignment notification sent"


@shared_task
def ride_completion_notification(ride_id, user_id):
    print(f"Ride completion: ride={ride_id}, " f"user={user_id}")
    return "Ride completion notification sent"


@shared_task
def reminder_notification(ride_id, user_id, message):
    print(f"Reminder: ride={ride_id}, " f"user={user_id}, message={message}")
    return "Reminder notification sent"


@shared_task
def ride_accepted_notification(ride_id, passenger_id):
    notification, created = Notification.objects.get_or_create(
        user_id=passenger_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.RIDE_ACCEPTED,
        defaults={
            "title": "Ride Accepted",
            "message": "Your driver has accepted the ride.",
        },
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task
def ride_completed_event_notification(ride_id, passenger_id):
    notification, created = Notification.objects.get_or_create(
        user_id=passenger_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.RIDE_COMPLETED,
        defaults={"message": "Your ride has been completed."},
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task
def driver_arriving_notification(ride_id, passenger_id):
    notification, created = Notification.objects.get_or_create(
        user_id=passenger_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.DRIVER_ARRIVING,
        defaults={
            "title": "Driver Arriving",
            "message": "Your driver is arriving.",
        },
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task
def ride_started_notification(ride_id, passenger_id):
    notification, created = Notification.objects.get_or_create(
        user_id=passenger_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.RIDE_STARTED,
        defaults={
            "title": "Ride Started",
            "message": "Your ride has started.",
        },
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task
def ride_cancelled_notification(ride_id, passenger_id):
    notification, created = Notification.objects.get_or_create(
        user_id=passenger_id,
        ride_id=ride_id,
        notification_type=Notification.NotificationType.RIDE_CANCELLED,
        defaults={
            "title": "Ride Cancelled",
            "message": "Your ride has been cancelled.",
        },
    )

    return {
        "notification_id": str(notification.id),
        "created": created,
    }


@shared_task(bind=True, max_retries=2)
def retry_test_task(self):
    attempt = self.request.retries + 1

    print(f"Retry test: Attempt {attempt}")

    if attempt < 3:
        print(f"Attempt {attempt} failed. Retrying...")
        raise self.retry(countdown=2)

    print("Attempt 3 succeeded.")
    return "Retry test successful"
