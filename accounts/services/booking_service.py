from datetime import date, time

from django.db import transaction

from ..models import Booking


class BookingService:

    ALLOWED_TRANSITIONS = {
        "pending": [
            "confirmed",
            "cancelled",
            "payment_failed",
        ],
        "confirmed": [
            "in_progress",
            "cancelled",
        ],
        "in_progress": [
            "completed",
        ],
        "completed": [],
        "cancelled": [],
        "payment_failed": [],
    }

    @staticmethod
    def get_booking(booking_id, customer=None):
        queryset = Booking.objects.select_related(
            "customer",
            "provider",
            "service",
        )

        if customer is not None:
            queryset = queryset.filter(customer=customer)

        return queryset.get(id=booking_id)

    @staticmethod
    def get_bookings_for_customer(customer):
        return (
            Booking.objects
            .select_related(
                "provider",
                "service",
            )
            .filter(customer=customer)
            .order_by("-created_at")
        )

    @staticmethod
    def create_booking(
        customer,
        service,
        provider,
        booking_date=None,
        booking_time=None,
    ):
        booking = Booking.objects.create(
            customer=customer,
            provider=provider,
            service=service,
            booking_date=booking_date or date.today(),
            booking_time=booking_time or time(10, 0),
            amount=service.price,
        )

        return booking

    @classmethod
    def update_status(cls, booking_id, customer, new_status):
        valid_statuses = [
            choice[0]
            for choice in Booking.BookingStatus.choices
        ]

        if new_status not in valid_statuses:
            raise ValueError("Invalid booking status.")

        with transaction.atomic():
            booking = (
                Booking.objects
                .select_for_update()
                .get(
                    id=booking_id,
                    customer=customer,
                )
            )

            current_status = booking.status

            if new_status not in cls.ALLOWED_TRANSITIONS.get(
                current_status,
                [],
            ):
                raise ValueError(
                    f"Invalid transition: "
                    f"{current_status} -> {new_status}"
                )

            booking.status = new_status

            booking.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return booking