
from datetime import date, time
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from accounts.models import (
    Booking,
    DriverProfile,
    DriverLocation,
    Notification,
    Profile,
    Provider,
    Payment,
    Ride,
    RideStatus,
    SavedService,
    Service,
    ServiceImage,
    User,
    Vehicle,
    VehicleType,
)

from accounts.services.booking_service import BookingService
from accounts.services.driver_service import DriverService
from accounts.services.fare_service import FareService
from accounts.services.notification_service import NotificationService
from accounts.services.payment_service import PaymentService
from accounts.services.profile_service import ProfileService
from accounts.services.ride import RideService
from accounts.services.saved_service import SavedServiceService
from accounts.services.service_service import ServiceService
from accounts.services.user_service import UserService
from accounts.services.vehicle_service import VehicleService


# Service service tests

class ServiceServiceTests(TestCase):

    # Get service

    def test_get_service(self):
        service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=750.00,
            duration=60,
            is_active=True,
        )

        result = ServiceService.get_service(service.id)

        self.assertEqual(result.id, service.id)
        self.assertEqual(result.name, "Home Cleaning")

    def test_get_service_invalid_id(self):
        with self.assertRaises(Service.DoesNotExist):
            ServiceService.get_service(
                "00000000-0000-0000-0000-000000000000"
            )

    # Get service images

    def test_get_service_images(self):
        service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=750.00,
            duration=60,
            is_active=True,
        )

        image1 = SimpleUploadedFile(
            "image1.jpg",
            b"image-content-1",
            content_type="image/jpeg",
        )

        image2 = SimpleUploadedFile(
            "image2.jpg",
            b"image-content-2",
            content_type="image/jpeg",
        )

        ServiceImage.objects.create(
            service=service,
            image=image1,
        )

        ServiceImage.objects.create(
            service=service,
            image=image2,
        )

        result = ServiceService.get_service_images(service)

        self.assertEqual(result.count(), 2)
        self.assertEqual(
            result.first().service_id,
            service.id,
        )

    def test_get_service_images_empty(self):
        service = Service.objects.create(
            name="Plumbing",
            description="Plumbing service",
            price=500.00,
            duration=45,
            is_active=True,
        )

        result = ServiceService.get_service_images(service)

        self.assertEqual(result.count(), 0)

    # Get service image

    def test_get_service_image(self):
        service = Service.objects.create(
            name="Electrician",
            description="Electrical service",
            price=600.00,
            duration=60,
            is_active=True,
        )

        image = SimpleUploadedFile(
            "electrician.jpg",
            b"image-content",
            content_type="image/jpeg",
        )

        service_image = ServiceImage.objects.create(
            service=service,
            image=image,
        )

        result = ServiceService.get_service_image(
            service_image.id
        )

        self.assertEqual(
            result.id,
            service_image.id,
        )

        self.assertEqual(
            result.service_id,
            service.id,
        )

    def test_get_service_image_invalid_id(self):
        with self.assertRaises(ServiceImage.DoesNotExist):
            ServiceService.get_service_image(
                "00000000-0000-0000-0000-000000000000"
            )


# Booking service tests

class BookingServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.customer = User.objects.create_user(
            email="customer@test.com",
            password="TestPass123",
        )

        provider_user = User.objects.create_user(
            email="provider@test.com",
            password="TestPass123",
        )

        self.provider = Provider.objects.create(
            user=provider_user,
            name="Test Provider",
            is_active=True,
        )

        self.service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=Decimal("750.00"),
            duration=60,
            is_active=True,
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date=date.today(),
            booking_time=time(10, 0),
            amount=Decimal("750.00"),
            status=Booking.BookingStatus.PENDING,
        )

    # Create booking

    def test_create_booking(self):
        result = BookingService.create_booking(
            customer=self.customer,
            service=self.service,
            provider=self.provider,
        )

        self.assertIsNotNone(result.id)

        self.assertEqual(
            result.customer,
            self.customer,
        )

        self.assertEqual(
            result.service,
            self.service,
        )

        self.assertEqual(
            result.amount,
            self.service.price,
        )

    # Get booking

    def test_get_booking(self):
        result = BookingService.get_booking(
            self.booking.id,
            customer=self.customer,
        )

        self.assertEqual(
            result.id,
            self.booking.id,
        )

        self.assertEqual(
            result.customer,
            self.customer,
        )

    # Get customer bookings

    def test_get_bookings_for_customer(self):
        result = BookingService.get_bookings_for_customer(
            self.customer
        )

        self.assertEqual(
            result.count(),
            1,
        )

        self.assertEqual(
            result.first().id,
            self.booking.id,
        )

    # Valid status transition

    def test_update_status_valid_transition(self):
        result = BookingService.update_status(
            booking_id=self.booking.id,
            customer=self.customer,
            new_status=Booking.BookingStatus.CONFIRMED,
        )

        self.assertEqual(
            result.status,
            Booking.BookingStatus.CONFIRMED,
        )

    # Invalid status transition

    def test_update_status_invalid_transition(self):
        with self.assertRaises(ValueError):
            BookingService.update_status(
                booking_id=self.booking.id,
                customer=self.customer,
                new_status=Booking.BookingStatus.COMPLETED,
            )

    # Invalid status

    def test_update_status_invalid_status(self):
        with self.assertRaises(ValueError):
            BookingService.update_status(
                booking_id=self.booking.id,
                customer=self.customer,
                new_status="invalid_status",
            )


# Payment service tests

class PaymentServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.customer = User.objects.create_user(
            email="payment_customer@test.com",
            password="TestPass123",
        )

        provider_user = User.objects.create_user(
            email="payment_provider@test.com",
            password="TestPass123",
        )

        self.provider = Provider.objects.create(
            user=provider_user,
            name="Payment Provider",
            is_active=True,
        )

        self.service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=Decimal("750.00"),
            duration=60,
            is_active=True,
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date=date.today(),
            booking_time=time(10, 0),
            amount=Decimal("750.00"),
            status=Booking.BookingStatus.PENDING,
        )

    # Get payment

    def test_get_payment(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-001",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-001",
        )

        result = PaymentService.get_payment(payment.id)

        self.assertEqual(
            result.id,
            payment.id,
        )

        self.assertEqual(
            result.booking.id,
            self.booking.id,
        )

    # Get payment for booking

    def test_get_payment_for_booking(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-002",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-002",
        )

        result = PaymentService.get_payment_for_booking(
            self.booking
        )

        self.assertEqual(
            result.id,
            payment.id,
        )

    # Initiate payment

    def test_initiate_payment(self):
        payment, created = PaymentService.initiate_payment(
            booking=self.booking,
            idempotency_key="IDEMP-003",
        )

        self.assertTrue(created)

        self.assertEqual(
            payment.booking,
            self.booking,
        )

        self.assertEqual(
            payment.amount,
            self.booking.amount,
        )

        self.assertEqual(
            payment.payment_status,
            Payment.PaymentStatus.PENDING,
        )

    # Payment idempotency

    def test_initiate_payment_idempotency(self):
        payment1, created1 = PaymentService.initiate_payment(
            booking=self.booking,
            idempotency_key="IDEMP-004",
        )

        payment2, created2 = PaymentService.initiate_payment(
            booking=self.booking,
            idempotency_key="IDEMP-004",
        )

        self.assertTrue(created1)
        self.assertFalse(created2)

        self.assertEqual(
            payment1.id,
            payment2.id,
        )

    # Process successful payment

    def test_process_mock_payment_success(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-005",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-005",
        )

        result = PaymentService.process_mock_payment(
            payment,
            "success",
        )

        self.assertEqual(
            result.payment_status,
            Payment.PaymentStatus.SUCCESS,
        )

    # Process failed payment

    def test_process_mock_payment_failed(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-006",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-006",
        )

        result = PaymentService.process_mock_payment(
            payment,
            "failed",
        )

        self.assertEqual(
            result.payment_status,
            Payment.PaymentStatus.FAILED,
        )

    # Already processed payment

    def test_process_mock_payment_already_processed(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-007",
            payment_status=Payment.PaymentStatus.SUCCESS,
            payment_method="upi",
            idempotency_key="IDEMP-007",
        )

        with self.assertRaises(ValueError):
            PaymentService.process_mock_payment(
                payment,
                "success",
            )

    # Webhook success

    def test_process_webhook_success(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-008",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-008",
        )

        result, updated = PaymentService.process_webhook(
            payment.id,
            "success",
        )

        self.assertTrue(updated)

        self.assertEqual(
            result.payment_status,
            Payment.PaymentStatus.SUCCESS,
        )

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.status,
            Booking.BookingStatus.CONFIRMED,
        )

    # Webhook failed

    def test_process_webhook_failed(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-009",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-009",
        )

        result, updated = PaymentService.process_webhook(
            payment.id,
            "failed",
        )

        self.assertTrue(updated)

        self.assertEqual(
            result.payment_status,
            Payment.PaymentStatus.FAILED,
        )

    # Invalid webhook

    def test_process_webhook_invalid_event(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=Decimal("750.00"),
            transaction_id="TXN-TEST-010",
            payment_status=Payment.PaymentStatus.PENDING,
            payment_method="upi",
            idempotency_key="IDEMP-010",
        )

        with self.assertRaises(ValueError):
            PaymentService.process_webhook(
                payment.id,
                "invalid",
            )


# Driver service tests

class DriverServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.user = User.objects.create_user(
            email="driver@test.com",
            password="TestPass123",
        )

        self.driver = DriverProfile.objects.create(
            user=self.user,
            status=DriverProfile.DriverStatus.ACTIVE,
            license_number="DL123456789",
        )

    # Get driver

    def test_get_driver_for_user(self):
        result = DriverService.get_driver_for_user(
            self.user
        )

        self.assertEqual(
            result.id,
            self.driver.id,
        )

    # Driver not found

    def test_get_driver_for_user_not_found(self):
        user = User.objects.create_user(
            email="nodriver@test.com",
            password="TestPass123",
        )

        with self.assertRaises(PermissionError):
            DriverService.get_driver_for_user(user)

    # Active driver

    def test_validate_active_driver(self):
        result = DriverService.validate_active_driver(
            self.driver
        )

        self.assertEqual(
            result.id,
            self.driver.id,
        )

    # Inactive driver

    def test_validate_inactive_driver(self):
        self.driver.status = (
            DriverProfile.DriverStatus.INACTIVE
        )

        self.driver.save(
            update_fields=["status"]
        )

        with self.assertRaises(PermissionError):
            DriverService.validate_active_driver(
                self.driver
            )

    # Update location

    def test_update_location(self):
        result, created = DriverService.update_location(
            driver=self.driver,
            latitude=17.3850,
            longitude=78.4867,
            availability_status="available",
        )

        self.assertEqual(
            result.driver,
            self.driver,
        )

        self.assertTrue(created)

        self.assertEqual(
            float(result.latitude),
            17.3850,
        )

        self.assertEqual(
            float(result.longitude),
            78.4867,
        )

    # Get location

    def test_get_location(self):
        DriverService.update_location(
            driver=self.driver,
            latitude=17.3850,
            longitude=78.4867,
            availability_status="available",
        )

        result = DriverService.get_location(
            self.driver
        )

        self.assertEqual(
            result.driver,
            self.driver,
        )

    # Check active ride

    def test_has_active_ride_false(self):
        result = DriverService.has_active_ride(
            self.driver
        )

        self.assertFalse(result)


# Notification service tests

class NotificationServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.user = User.objects.create_user(
            email="notification@test.com",
            password="Test@12345",
        )

    # Mark notification as read

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Test Notification",
            message="Test message",
            notification_type="general",
            is_read=False,
        )

        result = NotificationService.mark_as_read(
            notification.id,
            self.user,
        )

        self.assertTrue(result.is_read)

    # Mark all notifications as read

    def test_mark_all_as_read(self):
        Notification.objects.create(
            user=self.user,
            title="Notification 1",
            message="Message 1",
            notification_type="general",
            is_read=False,
        )

        Notification.objects.create(
            user=self.user,
            title="Notification 2",
            message="Message 2",
            notification_type="general",
            is_read=False,
        )

        count = NotificationService.mark_all_as_read(
            self.user
        )

        self.assertEqual(
            count,
            2,
        )

    # Booking notification

    @patch(
        "accounts.services.notification_service.booking_created_notification.delay"
    )
    def test_booking_created(self, mock_delay):
        booking = MagicMock()
        booking.id = "booking-id"
        booking.customer.id = self.user.id

        NotificationService.booking_created(booking)

        mock_delay.assert_called_once()

    # Payment notification

    @patch(
        "accounts.services.notification_service.payment_successful_notification.delay"
    )
    def test_payment_successful(self, mock_delay):
        booking = MagicMock()
        booking.id = "booking-id"
        booking.customer.id = self.user.id

        NotificationService.payment_successful(booking)

        mock_delay.assert_called_once()


# Profile service tests

class ProfileServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.user = User.objects.create_user(
            email="profile@test.com",
            password="Test@12345",
        )

    # Get profile

    def test_get_profile_not_found(self):
        result = ProfileService.get_profile(
            self.user
        )

        self.assertIsNone(result)


# Fare service tests

class FareServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.vehicle_type = VehicleType.objects.create(
            name="Sedan",
            base_fare=Decimal("50.00"),
            cost_per_km=Decimal("10.00"),
            cost_per_minute=Decimal("2.00"),
        )

    # Get vehicle type

    def test_get_vehicle_type(self):
        result = FareService.get_vehicle_type(
            self.vehicle_type.id
        )

        self.assertEqual(
            result,
            self.vehicle_type,
        )

    # Invalid vehicle type

    def test_get_vehicle_type_invalid(self):
        result = FareService.get_vehicle_type(
            "invalid-id"
        )

        self.assertIsNone(result)

    # Calculate distance

    def test_calculate_distance(self):
        distance = FareService.calculate_distance(
            17.3850,
            78.4867,
            17.4000,
            78.5000,
        )

        self.assertGreater(
            distance,
            0,
        )

    # Same location distance

    def test_same_location_distance(self):
        distance = FareService.calculate_distance(
            17.3850,
            78.4867,
            17.3850,
            78.4867,
        )

        self.assertAlmostEqual(
            distance,
            0,
            places=5,
        )

    # Calculate fare

    def test_calculate_fare(self):
        result = FareService.calculate_fare(
            vehicle_type=self.vehicle_type,
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_latitude=17.4000,
            dropoff_longitude=78.5000,
            duration_minutes=10,
        )

        self.assertIn(
            "base_fare",
            result,
        )

        self.assertIn(
            "distance_fare",
            result,
        )

        self.assertIn(
            "time_fare",
            result,
        )

        self.assertIn(
            "total",
            result,
        )

        self.assertGreater(
            result["total"],
            Decimal("0"),
        )

    # Calculate fare with surge

    def test_calculate_fare_with_surge(self):
        result = FareService.calculate_fare(
            vehicle_type=self.vehicle_type,
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_latitude=17.4000,
            dropoff_longitude=78.5000,
            duration_minutes=10,
            surge_multiplier=Decimal("1.5"),
        )

        self.assertEqual(
            result["surge"],
            Decimal("1.5"),
        )


# User service tests

class UserServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="Test@12345",
        )

    # Get user

    def test_get_user(self):
        result = UserService.get_user(
            self.user.id
        )

        self.assertEqual(
            result,
            self.user,
        )

    # User not found

    def test_get_user_not_found(self):
        result = UserService.get_user(
            "00000000-0000-0000-0000-000000000000"
        )

        self.assertIsNone(result)

    # Get user by email

    def test_get_user_by_email(self):
        result = UserService.get_user_by_email(
            "user@test.com"
        )

        self.assertEqual(
            result,
            self.user,
        )

    # User email not found

    def test_get_user_by_email_not_found(self):
        result = UserService.get_user_by_email(
            "notfound@test.com"
        )

        self.assertIsNone(result)

    # Create user

    def test_create_user(self):
        result = UserService.create_user(
            {
                "email": "newuser@test.com",
                "password": "Test@12345",
            }
        )

        self.assertEqual(
            result.email,
            "newuser@test.com",
        )


# Saved service tests

class SavedServiceServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.customer = User.objects.create_user(
            email="saved@test.com",
            password="Test@12345",
        )

        self.service = Service.objects.create(
            name="Home Cleaning",
            description="Home cleaning service",
            price=Decimal("750.00"),
            duration=60,
            is_active=True,
        )

    # Save service

    def test_save_service(self):
        result = SavedServiceService.save_service(
            customer=self.customer,
            service=self.service,
        )

        self.assertEqual(
            result.customer,
            self.customer,
        )

        self.assertEqual(
            result.service,
            self.service,
        )

    # Duplicate saved service

    def test_duplicate_saved_service(self):
        SavedServiceService.save_service(
            customer=self.customer,
            service=self.service,
        )

        with self.assertRaises(ValueError):
            SavedServiceService.save_service(
                customer=self.customer,
                service=self.service,
            )

    # Get saved services

    def test_get_saved_services(self):
        SavedServiceService.save_service(
            customer=self.customer,
            service=self.service,
        )

        result = SavedServiceService.get_saved_services(
            self.customer
        )

        self.assertEqual(
            result.count(),
            1,
        )

    # Get empty saved services

    def test_get_saved_services_empty(self):
        result = SavedServiceService.get_saved_services(
            self.customer
        )

        self.assertEqual(
            result.count(),
            0,
        )

    # Delete saved service

    def test_delete_saved_service(self):
        saved_service = SavedServiceService.save_service(
            customer=self.customer,
            service=self.service,
        )

        SavedServiceService.delete_saved_service(
            customer=self.customer,
            saved_service=saved_service,
        )

        self.assertFalse(
            SavedService.objects.filter(
                id=saved_service.id
            ).exists()
        )

    # Delete other customer's service

    def test_delete_other_customer_saved_service(self):
        other_customer = User.objects.create_user(
            email="other@test.com",
            password="Test@12345",
        )

        saved_service = SavedServiceService.save_service(
            customer=self.customer,
            service=self.service,
        )

        with self.assertRaises(PermissionError):
            SavedServiceService.delete_saved_service(
                customer=other_customer,
                saved_service=saved_service,
            )


# Vehicle service tests

class VehicleServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.user = User.objects.create_user(
            email="vehicle@test.com",
            password="Test@12345",
        )

        self.driver = DriverProfile.objects.create(
            user=self.user,
            status=DriverProfile.DriverStatus.ACTIVE,
            license_number="DL223344556",
        )

    # Get driver

    def test_get_driver(self):
        result = VehicleService.get_driver(
            self.user
        )

        self.assertEqual(
            result,
            self.driver,
        )

    # Driver not found

    def test_get_driver_not_found(self):
        user = User.objects.create_user(
            email="nodriver@test.com",
            password="Test@12345",
        )

        with self.assertRaises(PermissionError):
            VehicleService.get_driver(user)

    # Get vehicle queryset

    def test_get_vehicle_queryset(self):
        result = VehicleService.get_vehicle_queryset(
            self.user
        )

        self.assertEqual(
            result.count(),
            0,
        )

    # Get vehicle queryset for staff

    def test_get_vehicle_queryset_staff(self):
        self.user.is_staff = True

        self.user.save(
            update_fields=["is_staff"]
        )

        result = VehicleService.get_vehicle_queryset(
            self.user
        )

        self.assertEqual(
            result.count(),
            0,
        )


# Ride service tests

class RideServiceTests(TestCase):

    # Setup

    def setUp(self):
        self.rider = User.objects.create_user(
            email="rider@test.com",
            password="Test@12345",
        )

        self.driver_user = User.objects.create_user(
            email="driver@test.com",
            password="Test@12345",
        )

        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            status=DriverProfile.DriverStatus.ACTIVE,
            license_number="DL556677889",
        )

        self.vehicle_type = VehicleType.objects.create(
            name="Sedan",
            base_fare=Decimal("50.00"),
            cost_per_km=Decimal("10.00"),
            cost_per_minute=Decimal("2.00"),
        )

        self.requested_status = RideStatus.objects.create(
            name=RideStatus.Status.REQUESTED
        )

        self.accepted_status = RideStatus.objects.create(
            name=RideStatus.Status.ACCEPTED
        )

    # Create test ride

    def create_ride(self, status=None):
        return Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            status=status or self.requested_status,
            fare=Decimal("100.00"),
            vehicle_type=self.vehicle_type,
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_latitude=17.4000,
            dropoff_longitude=78.5000,
        )

    # Create ride

    @patch("accounts.services.ride.async_to_sync")
    def test_create_ride(self, mock_async):
        validated_data = {
            "vehicle_type": self.vehicle_type,
            "pickup_latitude": 17.3850,
            "pickup_longitude": 78.4867,
            "dropoff_latitude": 17.4000,
            "dropoff_longitude": 78.5000,
        }

        ride = RideService.create_ride(
            rider=self.rider,
            validated_data=validated_data,
        )

        self.assertEqual(
            ride.rider,
            self.rider,
        )

        self.assertEqual(
            ride.status,
            self.requested_status,
        )

        self.assertGreater(
            ride.fare,
            Decimal("0"),
        )

    # Accept ride

    @patch("accounts.services.ride.async_to_sync")
    def test_accept_ride(self, mock_async):
        ride = self.create_ride(
            status=self.requested_status
        )

        ride.driver = None

        ride.save(
            update_fields=["driver"]
        )

        result = RideService.accept_ride(
            ride_id=ride.id,
            user=self.driver_user,
        )

        self.assertEqual(
            result.driver,
            self.driver,
        )

        self.assertEqual(
            result.status,
            self.accepted_status,
        )

    # Driver not found

    def test_accept_ride_driver_not_found(self):
        user = User.objects.create_user(
            email="notdriver@test.com",
            password="Test@12345",
        )

        ride = self.create_ride()

        ride.driver = None

        ride.save(
            update_fields=["driver"]
        )

        with self.assertRaises(PermissionError):
            RideService.accept_ride(
                ride_id=ride.id,
                user=user,
            )

    # Update ride status

    @patch("accounts.services.ride.async_to_sync")
    def test_update_status(self, mock_async):
        ride = self.create_ride(
            status=self.accepted_status
        )

        arriving_status = RideStatus.objects.create(
            name=RideStatus.Status.DRIVER_ARRIVING
        )

        result = RideService.update_status(
            ride_id=ride.id,
            driver=self.driver_user,
            new_status_name=RideStatus.Status.DRIVER_ARRIVING,
        )

        self.assertEqual(
            result.status,
            arriving_status,
        )

    # Wrong driver

    def test_update_status_wrong_driver(self):
        other_user = User.objects.create_user(
            email="otherdriver@test.com",
            password="Test@12345",
        )

        DriverProfile.objects.create(
            user=other_user,
            status=DriverProfile.DriverStatus.ACTIVE,
            license_number="DL987654321",
        )

        ride = self.create_ride(
            status=self.accepted_status
        )

        with self.assertRaises(PermissionError):
            RideService.update_status(
                ride_id=ride.id,
                driver=other_user,
                new_status_name=RideStatus.Status.DRIVER_ARRIVING,
            )

    # Cancel ride

    def test_cancel_ride(self):
        ride = self.create_ride(
            status=self.requested_status
        )

        cancelled_status = RideStatus.objects.create(
            name=RideStatus.Status.CANCELLED
        )

        result = RideService.cancel_ride(
            ride_id=ride.id,
            rider=self.rider,
        )

        self.assertEqual(
            result.status,
            cancelled_status,
        )

    # Wrong rider

    def test_cancel_ride_wrong_rider(self):
        other_user = User.objects.create_user(
            email="other-rider@test.com",
            password="Test@12345",
        )

        ride = self.create_ride(
            status=self.requested_status
        )

        with self.assertRaises(PermissionError):
            RideService.cancel_ride(
                ride_id=ride.id,
                rider=other_user,
            )
