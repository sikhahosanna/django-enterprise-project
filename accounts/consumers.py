import json

from channels.generic.websocket import AsyncWebsocketConsumer

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)

from accounts.models import (
    User,
    Ride,
)


class DriverLocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # -----------------------------------------
        # GET JWT TOKEN
        # -----------------------------------------

        query_string = self.scope.get(
            "query_string",
            b"",
        ).decode()

        token = None

        for item in query_string.split("&"):

            if item.startswith("token="):

                token = item.split(
                    "=",
                    1,
                )[1]

                break

        # -----------------------------------------
        # JWT REQUIRED
        # -----------------------------------------

        if not token:

            await self.close(
                code=4001
            )

            return

        # -----------------------------------------
        # VERIFY JWT
        # -----------------------------------------

        try:

            validated_token = UntypedToken(
                token
            )

        except (
            InvalidToken,
            TokenError,
            Exception,
        ):

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GET USER ID FROM JWT
        # -----------------------------------------

        user_id = validated_token.get(
            "user_id"
        )

        if not user_id:

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GET USER
        # -----------------------------------------

        try:

            self.user = await User.objects.aget(
                id=user_id
            )

        except User.DoesNotExist:

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # DRIVER AUTHORIZATION
        # -----------------------------------------

        try:

            self.driver_profile = (
                await self.user.driver_profile
            )

        except Exception:

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # ACCEPT CONNECTION
        # -----------------------------------------

        await self.accept()

        await self.send(
            text_data=json.dumps({
                "success": True,
                "message": (
                    "Driver location WebSocket "
                    "connected successfully."
                ),
                "user_id": str(
                    self.user.id
                ),
                "driver_id": str(
                    self.driver_profile.id
                ),
            })
        )

    async def disconnect(
        self,
        close_code,
    ):

        # -----------------------------------------
        # DISCONNECT LOG
        # -----------------------------------------

        user_id = getattr(
            getattr(
                self,
                "user",
                None,
            ),
            "id",
            None,
        )

        driver_id = getattr(
            getattr(
                self,
                "driver_profile",
                None,
            ),
            "id",
            None,
        )

        print(
            "Driver location WebSocket "
            "disconnected | "
            f"user={user_id} | "
            f"driver={driver_id} | "
            f"code={close_code}"
        )

    async def receive(
        self,
        text_data=None,
        bytes_data=None,
    ):

        await self.send(
            text_data=json.dumps({
                "success": True,
                "message": "Message received.",
                "data": text_data,
            })
        )


class RideConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # -----------------------------------------
        # GET RIDE ID
        # -----------------------------------------

        self.ride_id = self.scope[
            "url_route"
        ]["kwargs"]["ride_id"]

        # -----------------------------------------
        # GET JWT TOKEN
        # -----------------------------------------

        query_string = self.scope.get(
            "query_string",
            b"",
        ).decode()

        token = None

        for item in query_string.split("&"):

            if item.startswith("token="):

                token = item.split(
                    "=",
                    1,
                )[1]

                break

        # -----------------------------------------
        # JWT REQUIRED
        # -----------------------------------------

        if not token:

            await self.close(
                code=4001
            )

            return

        # -----------------------------------------
        # VERIFY JWT
        # -----------------------------------------

        try:

            validated_token = UntypedToken(
                token
            )

        except (
            InvalidToken,
            TokenError,
            Exception,
        ):

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GET USER ID FROM JWT
        # -----------------------------------------

        user_id = validated_token.get(
            "user_id"
        )

        if not user_id:

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GET USER
        # -----------------------------------------

        try:

            self.user = await User.objects.aget(
                id=user_id
            )

        except User.DoesNotExist:

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GET RIDE
        # -----------------------------------------

        try:

            self.ride = await Ride.objects.select_related(
                "rider",
                "driver__user",
            ).aget(
                id=self.ride_id
            )

        except Ride.DoesNotExist:

            await self.close(
                code=4004
            )

            return

        # -----------------------------------------
        # RIDE OWNER CHECK
        # -----------------------------------------

        is_ride_owner = (
            self.ride.rider_id
            == self.user.id
        )

        # -----------------------------------------
        # DRIVER AUTHORIZATION
        # -----------------------------------------

        is_assigned_driver = False

        if self.ride.driver:

            is_assigned_driver = (
                self.ride.driver.user_id
                == self.user.id
            )

        # -----------------------------------------
        # AUTHORIZATION
        # -----------------------------------------

        if (
            not is_ride_owner
            and not is_assigned_driver
        ):

            await self.close(
                code=4003
            )

            return

        # -----------------------------------------
        # GROUP
        # -----------------------------------------

        self.group_name = (
            f"ride_{self.ride_id}"
        )

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        # -----------------------------------------
        # ACCEPT CONNECTION
        # -----------------------------------------

        await self.accept()

        await self.send(
            text_data=json.dumps({
                "success": True,
                "message": (
                    "Ride WebSocket connected "
                    "successfully."
                ),
                "ride_id": str(
                    self.ride_id
                ),
                "user_id": str(
                    self.user.id
                ),
            })
        )

    async def disconnect(
        self,
        close_code,
    ):

        # -----------------------------------------
        # REMOVE FROM RIDE GROUP
        # -----------------------------------------

        if hasattr(
            self,
            "group_name",
        ):

            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

        # -----------------------------------------
        # DISCONNECT LOG
        # -----------------------------------------

        user_id = getattr(
            getattr(
                self,
                "user",
                None,
            ),
            "id",
            None,
        )

        ride_id = getattr(
            self,
            "ride_id",
            None,
        )

        print(
            "Ride WebSocket disconnected | "
            f"ride={ride_id} | "
            f"user={user_id} | "
            f"code={close_code}"
        )

    async def ride_status_update(
        self,
        event,
    ):

        await self.send(
            text_data=json.dumps({
                "success": True,
                "message": "Ride status updated.",
                "ride_id": str(
                    self.ride_id
                ),
                "status": event["status"],
            })
        )