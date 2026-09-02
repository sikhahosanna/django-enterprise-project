import json

from django.test import TestCase, TransactionTestCase, override_settings
from asgiref.sync import sync_to_async

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
)

from accounts.routing import websocket_urlpatterns

from accounts.tasks import (
    ride_notification,
    driver_assignment_notification,
    ride_completion_notification,
    reminder_notification,
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

    # CHANNELS APPLICATION

    application = ProtocolTypeRouter(
        {
            "websocket": URLRouter(websocket_urlpatterns),
        }
    )

    # SETUP

    def setUp(self):

        # Rider

        self.rider = User.objects.create_user(
            email="rider@test.com",
            password="Test@12345",
        )

       
        # Driver


        self.driver = User.objects.create_user(
            email="driver@test.com",
            password="Test@12345",
        )

        self.driver_profile = DriverProfile.objects.create(
            user=self.driver,
            license_number="TEST-LICENSE-001",
            status=DriverProfile.DriverStatus.ACTIVE,
        )

        # Driver Location
        

        self.driver_location = DriverLocation.objects.create(
            driver=self.driver_profile,
            latitude=17.3850,
            longitude=78.4867,
            availability_status=(
                DriverLocation.AvailabilityStatus.ONLINE
            ),
        )

       
        # Vehicle Type
        

        self.vehicle_type, _ = VehicleType.objects.get_or_create(
            name="CAR"
        )

        # Ride Status
       

        self.ride_status, _ = RideStatus.objects.get_or_create(
            name=RideStatus.Status.REQUESTED
        )

        # Ride
        

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

    # JWT TOKEN HELPER
   
    @sync_to_async
    def get_token(self, user):

        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)

    # 1. DRIVER WEBSOCKET - VALID TOKEN
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

    # 2. DRIVER WEBSOCKET - WITHOUT TOKEN
   

    async def test_driver_websocket_without_token(self):

        communicator = WebsocketCommunicator(
            self.application,
            "/ws/driver/location/",
        )

        connected, _ = await communicator.connect()

        self.assertFalse(connected)

    
    # 3. RIDE WEBSOCKET - RIDER CONNECTION
    

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
        self.assertEqual(
            response["ride_id"],
            str(self.ride.id),
        )

        await communicator.disconnect()

 
    # 4. RIDE WEBSOCKET - UNAUTHORIZED USER
  

        async def test_ride_websocket_unauthorized_user(self):

           unauthorized_user = await sync_to_async(
            User.objects.create_user
        )(
            email="unauthorized@test.com",
            password="Test@12345",
        )

        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

    # 5. RIDE STATUS EVENT
   

    async def test_ride_status_event(self):

        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        # First message = connection success
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

        self.assertEqual(
            response["message"],
            "Ride status updated.",
        )

        self.assertEqual(
            response["ride_id"],
            str(self.ride.id),
        )

        self.assertEqual(
            response["status"],
            "ACCEPTED",
        )

        await communicator.disconnect()

    # 6. DRIVER LOCATION EVENT
    

    async def test_driver_location_event(self):

        token = await self.get_token(self.rider)

        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/ride/{self.ride.id}/?token={token}",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        # First message = connection success
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

        self.assertEqual(
            response["type"],
            "driver_location",
        )

        self.assertEqual(
            response["ride_id"],
            str(self.ride.id),
        )

        self.assertEqual(
            response["driver_id"],
            str(self.driver_profile.id),
        )

        self.assertEqual(
            response["latitude"],
            17.3850,
        )

        self.assertEqual(
            response["longitude"],
            78.4867,
        )

        await communicator.disconnect()


# CELERY TESTS
class CeleryTest(TestCase):

    # CELERY TASK EXECUTION
   

    def test_celery_task_execution(self):

        user = User.objects.create_user(
            email="celery@test.com",
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

        result = ride_notification.apply(
            args=[
                str(ride.id),
                str(user.id),
                "Test notification",
            ]
        )

        self.assertEqual(
            result.status,
            "SUCCESS",
        )

        self.assertTrue(
            result.result["notification_id"]
        )

    # CELERY DUPLICATE NOTIFICATION
    

    def test_celery_duplicate_notification(self):

        user = User.objects.create_user(
            email="duplicate@test.com",
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

        first_result = ride_notification.apply(
            args=[
                str(ride.id),
                str(user.id),
                "Test notification",
            ]
        )

        second_result = ride_notification.apply(
            args=[
                str(ride.id),
                str(user.id),
                "Test notification",
            ]
        )

        self.assertEqual(
            first_result.status,
            "SUCCESS",
        )

        self.assertEqual(
            second_result.status,
            "SUCCESS",
        )

        self.assertFalse(
            second_result.result["created"]
        )

    # CELERY RETRY

    def test_celery_retry(self):

        result = retry_test_task.apply()

        self.assertEqual(
            result.status,
            "SUCCESS",
        )

        self.assertEqual(
            result.result,
            "Retry test successful",
        )