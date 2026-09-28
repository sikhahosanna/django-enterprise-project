from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User, Provider, Service, Booking, Payment
from accounts.views import BookingStatusUpdateView, PaymentInitiateView


class BookingWorkflowTests(TestCase):

    def setUp(self):

        self.customer = User.objects.create_user(
            email="workflow_customer@test.com",
            password="Test@12345",
        )

        provider_user = User.objects.create_user(
            email="workflow_provider@test.com",
            password="Test@12345",
        )

        self.provider = Provider.objects.create(
            user=provider_user,
            name="Workflow Provider",
        )

        self.service = Service.objects.create(
            name="Workflow Service",
            description="Workflow test service",
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

        self.factory = APIRequestFactory()

    def update_status(self, status_value):

        request = self.factory.patch(
            f"/api/v1/bookings/{self.booking.id}/status/",
            {"status": status_value},
            format="json",
        )

        force_authenticate(
            request,
            user=self.customer,
        )

        return BookingStatusUpdateView.as_view()(
            request,
            booking_id=self.booking.id,
        )

    def test_create_booking(self):

        self.assertIsNotNone(self.booking.id)

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.PENDING,
        )

    def test_confirm_booking(self):

        response = self.update_status("confirmed")

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.CONFIRMED,
        )

    def test_start_booking(self):

        self.booking.status = Booking.BookingStatus.CONFIRMED
        self.booking.save(update_fields=["status"])

        response = self.update_status("in_progress")

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.IN_PROGRESS,
        )

    def test_complete_booking(self):

        self.booking.status = Booking.BookingStatus.IN_PROGRESS
        self.booking.save(update_fields=["status"])

        response = self.update_status("completed")

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.COMPLETED,
        )

    def test_cancel_booking(self):

        response = self.update_status("cancelled")

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.CANCELLED,
        )

    def test_payment_failure(self):

        response = self.update_status("payment_failed")

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.PAYMENT_FAILED,
        )

    def test_invalid_transition_rejected(self):

        response = self.update_status("completed")

        self.assertEqual(response.status_code, 400)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.PENDING,
        )

    def test_duplicate_request_rejected(self):

        first_response = self.update_status("confirmed")

        self.assertEqual(
            first_response.status_code,
            200,
        )

        second_response = self.update_status("confirmed")

        self.assertEqual(
            second_response.status_code,
            400,
        )

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.CONFIRMED,
        )

    def test_payment_duplicate_request_is_idempotent(self):

        request_data = {
            "booking_id": str(self.booking.id),
            "amount": "750.00",
        }

        request_one = self.factory.post(
            "/api/v1/payments/initiate/",
            request_data,
            format="json",
            HTTP_IDEMPOTENCY_KEY="workflow-payment-001",
        )

        force_authenticate(
            request_one,
            user=self.customer,
        )

        response_one = PaymentInitiateView.as_view()(
            request_one
        )

        self.assertEqual(
            response_one.status_code,
            201,
        )

        request_two = self.factory.post(
            "/api/v1/payments/initiate/",
            request_data,
            format="json",
            HTTP_IDEMPOTENCY_KEY="workflow-payment-001",
        )

        force_authenticate(
            request_two,
            user=self.customer,
        )

        response_two = PaymentInitiateView.as_view()(
            request_two
        )

        self.assertEqual(
            response_two.status_code,
            200,
        )

        self.assertEqual(
            Payment.objects.filter(
                booking=self.booking,
                idempotency_key="workflow-payment-001",
            ).count(),
            1,
        )