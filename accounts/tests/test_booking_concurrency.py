import threading
from decimal import Decimal

from django.db import close_old_connections
from django.test import TransactionTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import (
    User,
    Provider,
    Service,
    Booking,
)
from accounts.views import BookingStatusUpdateView


class BookingConcurrencyTests(TransactionTestCase):

    def setUp(self):

        self.customer = User.objects.create_user(
            email="concurrency_customer@test.com",
            password="Test@12345",
        )

        provider_user = User.objects.create_user(
            email="concurrency_provider@test.com",
            password="Test@12345",
        )

        self.provider = Provider.objects.create(
            user=provider_user,
            name="Concurrency Provider",
        )

        self.service = Service.objects.create(
            name="Concurrency Service",
            description="Concurrency test service",
            price=Decimal("750.00"),
            duration=60,
            is_active=True,
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date="2026-09-30",
            booking_time="10:00:00",
            amount=Decimal("750.00"),
            status=Booking.BookingStatus.PENDING,
        )

    def update_booking(self, results, index):

        close_old_connections()

        factory = APIRequestFactory()

        request = factory.patch(
            f"/api/v1/bookings/{self.booking.id}/status/",
            {"status": "confirmed"},
            format="json",
        )

        force_authenticate(request, user=self.customer)

        try:
            response = BookingStatusUpdateView.as_view()(
                request,
                booking_id=self.booking.id,
            )

            results[index] = response.status_code

        except Exception as exc:
            results[index] = str(exc)

        finally:
            close_old_connections()

    def test_only_one_concurrent_update_succeeds(self):

        results = [None, None]

        thread_a = threading.Thread(
            target=self.update_booking,
            args=(results, 0),
        )

        thread_b = threading.Thread(
            target=self.update_booking,
            args=(results, 1),
        )

        thread_a.start()
        thread_b.start()

        thread_a.join()
        thread_b.join()

        success_count = results.count(200)
        failure_count = results.count(400)

        print("\nCONCURRENCY RESULTS:", results)

        self.assertEqual(success_count, 1)
        self.assertEqual(failure_count, 1)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.CONFIRMED,
        )