
import uuid

from django.db import IntegrityError, transaction

from ..models import Payment


class PaymentService:

    @staticmethod
    def get_payment(payment_id):
        return (
            Payment.objects
            .select_related("booking")
            .get(id=payment_id)
        )

    @staticmethod
    def get_payment_for_booking(booking):
        return Payment.objects.filter(
            booking=booking
        ).first()

    @staticmethod
    def initiate_payment(booking, idempotency_key):
        existing_payment = Payment.objects.filter(
            booking=booking,
            idempotency_key=idempotency_key,
        ).first()

        if existing_payment:
            return existing_payment, False

        try:
            with transaction.atomic():
                payment = Payment.objects.create(
                    booking=booking,
                    amount=booking.amount,
                    transaction_id=str(uuid.uuid4()),
                    payment_status=Payment.PaymentStatus.PENDING,
                    payment_method="upi",
                    idempotency_key=idempotency_key,
                )

        except IntegrityError:
            payment = Payment.objects.get(
                booking=booking,
                idempotency_key=idempotency_key,
            )

            return payment, False

        return payment, True

    @staticmethod
    def process_mock_payment(payment, result):
        if payment.payment_status != Payment.PaymentStatus.PENDING:
            raise ValueError("Payment is already processed.")

        payment.payment_status = (
            Payment.PaymentStatus.SUCCESS
            if result == "success"
            else Payment.PaymentStatus.FAILED
        )

        payment.save(
            update_fields=["payment_status"]
        )

        return payment

    @staticmethod
    def process_webhook(payment_id, event):
        if event not in ["success", "failed"]:
            raise ValueError("Invalid payment event.")

        with transaction.atomic():
            payment = (
                Payment.objects
                .select_for_update()
                .select_related("booking")
                .get(id=payment_id)
            )

            if payment.payment_status != Payment.PaymentStatus.PENDING:
                return payment, False

            payment.payment_status = (
                Payment.PaymentStatus.SUCCESS
                if event == "success"
                else Payment.PaymentStatus.FAILED
            )

            payment.save(
                update_fields=["payment_status"]
            )

            booking = payment.booking

            if event == "success":
                booking.status = "confirmed"
                booking.save(
                    update_fields=["status"]
                )

        return payment, True
