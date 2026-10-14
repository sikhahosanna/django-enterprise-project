
from django.test import TestCase, TransactionTestCase, override_settings
from asgiref.sync import sync_to_async
from unittest.mock import patch

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.testing import WebsocketCommunicator

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import (
    User,
    DriverProfile,
    DriverLocation,
    VehicleType,
    RideStatus,
    Ride,
    Notification,
)

from accounts.routing import websocket_urlpatterns

from accounts.tasks import (
    ride_notification,
    retry_test_task,
)


@override_settings(
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }
)
class WebSocketTest(TransactionTestCase):

    application = ProtocolTypeRouter(
        {
            "websocket": URLRouter(websocket_urlpatterns),
        }
    )

    def setUp(self):
        self.rider = User.objects.create_user(
            email="rider@test.com",
            password="Test@12345",
        )

        self.driver = User.objects.create_user(
            email="driver@test.com",
            password="Test@12345",
        )

        self.driver_profile = DriverProfile.objects.create(
            user=self.driver,
            license_number="TEST-LICENSE-001",
            status=DriverProfile.DriverStatus.ACTIVE,
        )

        self.driver_location = DriverLocation.objects.create(
            driver=self.driver_profile,
            latitude=17.3850,
            longitude=78.4867,
            availability_status=(
                DriverLocation.AvailabilityStatus.ONLINE
            ),
        )

        self.vehicle_type, _ = VehicleType.objects.get_or_create(
            name="CAR"
        )

        self.ride_status, _ = RideStatus.objects.get_or_create(
            name=RideStatus.Status.REQUESTED
        )

        self.ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver_profile,
            vehicle_type=self.vehicle_type,
            status=self.ride_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=100,
        )

    @sync_to_async
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    async def test_driver_websocket_valid_token(self):
        token = await self.get_token(self.driver)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/driver/location/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_driver_websocket_without_token(self):
        communicator = WebsocketCommunicator(
            self.application,
            "/ws/driver/location/",
        )

        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_ride_websocket_rider_connection(self):
        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()
        self.assertTrue(response["success"])
        self.assertEqual(response["ride_id"], str(self.ride.id))

        await communicator.disconnect()

    async def test_ride_websocket_unauthorized_user(self):
        unauthorized_user = await sync_to_async(
            User.objects.create_user
        )(
            email="unauthorized@test.com",
            password="Test@12345",
        )

        token = await self.get_token(unauthorized_user)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        await communicator.disconnect()

    async def test_ride_status_event(self):
        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_json_from()

        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            f"ride_{self.ride.id}",
            {
                "type": "ride_status_update",
                "status": "ACCEPTED",
            },
        )

        response = await communicator.receive_json_from()

        self.assertTrue(response["success"])
        self.assertEqual(response["message"], "Ride status updated.")
        self.assertEqual(response["ride_id"], str(self.ride.id))
        self.assertEqual(response["status"], "ACCEPTED")

        await communicator.disconnect()

    async def test_api_status_update_broadcasts_websocket_event(self):
        from rest_framework.test import APIClient

        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_json_from()

        @sync_to_async
        def update_status_via_api():
            accepted_status, _ = RideStatus.objects.get_or_create(
                name=RideStatus.Status.ACCEPTED
            )
            self.ride.status = accepted_status
            self.ride.save(update_fields=["status"])

            RideStatus.objects.get_or_create(
                name=RideStatus.Status.STARTED
            )

            client = APIClient()
            client.force_authenticate(user=self.driver)

            return client.patch(
                f"/api/v1/rides/{self.ride.id}/status/",
                {"status": RideStatus.Status.STARTED},
                format="json",
            )

        response = await update_status_via_api()

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data["data"]["status"],
            RideStatus.Status.STARTED,
        )

        event = await communicator.receive_json_from(timeout=3)

        self.assertTrue(event["success"])
        self.assertEqual(event["ride_id"], str(self.ride.id))
        self.assertEqual(event["status"], RideStatus.Status.STARTED)

        await communicator.disconnect()

    async def test_driver_location_event(self):
        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_json_from()

        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            f"ride_{self.ride.id}",
            {
                "type": "driver_location_update",
                "ride_id": str(self.ride.id),
                "driver_id": str(self.driver_profile.id),
                "latitude": 17.3850,
                "longitude": 78.4867,
            },
        )

        response = await communicator.receive_json_from()

        self.assertTrue(response["success"])
        self.assertEqual(response["type"], "driver_location")
        self.assertEqual(response["ride_id"], str(self.ride.id))
        self.assertEqual(
            response["driver_id"],
            str(self.driver_profile.id),
        )
        self.assertEqual(response["latitude"], 17.3850)
        self.assertEqual(response["longitude"], 78.4867)

        await communicator.disconnect()


class CeleryTest(TestCase):

    def create_ride_and_user(self, email):
        user = User.objects.create_user(
            email=email,
            password="Test@12345",
        )

        vehicle_type, _ = VehicleType.objects.get_or_create(
            name="CAR"
        )

        ride_status, _ = RideStatus.objects.get_or_create(
            name=RideStatus.Status.REQUESTED
        )

        ride = Ride.objects.create(
            rider=user,
            vehicle_type=vehicle_type,
            status=ride_status,
            pickup_address="Hyderabad",
            pickup_latitude=17.3850,
            pickup_longitude=78.4867,
            dropoff_address="Secunderabad",
            dropoff_latitude=17.4399,
            dropoff_longitude=78.4983,
            fare=100,
        )

        return user, ride

    def test_celery_task_execution(self):
        user, ride = self.create_ride_and_user("celery@test.com")

        result = ride_notification.apply(
            args=[str(ride.id), str(user.id), "Test notification"]
        )

        self.assertEqual(result.status, "SUCCESS")
        self.assertTrue(result.result["notification_id"])

    def test_celery_duplicate_notification(self):
        user, ride = self.create_ride_and_user("duplicate@test.com")

        args = [str(ride.id), str(user.id), "Test notification"]

        first_result = ride_notification.apply(args=args)
        second_result = ride_notification.apply(args=args)

        self.assertEqual(first_result.status, "SUCCESS")
        self.assertEqual(second_result.status, "SUCCESS")
        self.assertTrue(first_result.result["created"])
        self.assertFalse(second_result.result["created"])

        self.assertEqual(
            Notification.objects.filter(
                user=user,
                ride=ride,
                notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            ).count(),
            1,
        )

    @patch("accounts.tasks.Notification.objects.get_or_create")
    def test_notification_recovers_after_transient_failure(
        self, mock_get_or_create
    ):
        user, ride = self.create_ride_and_user("recovery@test.com")

        notification = Notification(
            user=user,
            ride=ride,
            notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            message="Recovery notification",
        )

        mock_get_or_create.side_effect = [
            Exception("Temporary database failure"),
            (notification, True),
        ]

        result = ride_notification.apply(
            args=[
                str(ride.id),
                str(user.id),
                "Recovery notification",
            ],
            throw=False,
        )

        self.assertEqual(result.status, "SUCCESS")
        self.assertTrue(result.result["created"])
        self.assertEqual(mock_get_or_create.call_count, 2)

    @patch("accounts.tasks.Notification.objects.get_or_create")
    def test_notification_recovers_after_timeout(self, mock_get_or_create):
        user, ride = self.create_ride_and_user("timeout@test.com")

        notification = Notification(
            user=user,
            ride=ride,
            notification_type=Notification.NotificationType.RIDE_ACCEPTED,
            message="Timeout recovery notification",
        )

        mock_get_or_create.side_effect = [
            TimeoutError("Notification database timed out"),
            (notification, True),
        ]

        result = ride_notification.apply(
            args=[
                str(ride.id),
                str(user.id),
                "Timeout recovery notification",
            ],
            throw=False,
        )

        self.assertEqual(result.status, "SUCCESS")
        self.assertTrue(result.result["created"])
        self.assertEqual(mock_get_or_create.call_count, 2)

    def test_celery_retry(self):
        result = retry_test_task.apply()

        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.result, "Retry test successful")