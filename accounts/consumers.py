import json
import logging

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


logger = logging.getLogger(__name__)


class DriverLocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # GET JWT TOKEN

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

        # JWT REQUIRED

        if not token:

            logger.warning(
                "Driver location WebSocket connection rejected: token missing"
            )

            await self.close(code=4001)
            return

        # VERIFY JWT

        try:

            validated_token = UntypedToken(token)

        except (
            InvalidToken,
            TokenError,
            Exception,
        ):

            logger.warning(
                "Driver location WebSocket connection rejected: invalid token"
            )

            await self.close(code=4003)
            return

        # GET USER ID FROM JWT

        user_id = validated_token.get("user_id")

        if not user_id:

            logger.warning(
                "Driver location WebSocket connection rejected: user ID missing"
            )

            await self.close(code=4003)
            return

        # GET USER

        try:

            self.user = await User.objects.aget(id=user_id)

        except User.DoesNotExist:

            logger.warning(
                "Driver location WebSocket connection rejected: user not found"
            )

            await self.close(code=4003)
            return

        # DRIVER AUTHORIZATION

        try:

            self.driver_profile = await self.user.driver_profile

        except Exception:

            logger.warning(
                "Driver location WebSocket authorization failed"
            )

            await self.close(code=4003)
            return

        # ACCEPT CONNECTION

        try:

            await self.accept()

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "message": (
                            "Driver location WebSocket "
                            "connected successfully."
                        ),
                        "user_id": str(self.user.id),
                        "driver_id": str(self.driver_profile.id),
                    }
                )
            )

            logger.info(
                "Driver location WebSocket connected successfully"
            )

        except Exception:

            logger.error(
                "Driver location WebSocket connection processing failed",
                exc_info=True,
            )

            raise

    async def disconnect(
        self,
        close_code,
    ):

        logger.info(
            "Driver location WebSocket disconnected | code=%s",
            close_code,
        )

    async def receive(
        self,
        text_data=None,
        bytes_data=None,
    ):

        try:

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "message": "Message received.",
                        "data": text_data,
                    }
                )
            )

        except Exception:

            logger.error(
                "Driver location WebSocket message processing failed",
                exc_info=True,
            )

            raise


class RideConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # GET RIDE ID

        self.ride_id = self.scope["url_route"]["kwargs"]["ride_id"]

        # GET JWT TOKEN

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

        # JWT REQUIRED

        if not token:

            logger.warning(
                "Ride WebSocket connection rejected: token missing | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4001)
            return

        # VERIFY JWT

        try:

            validated_token = UntypedToken(token)

        except (
            InvalidToken,
            TokenError,
            Exception,
        ):

            logger.warning(
                "Ride WebSocket connection rejected: invalid token | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4003)
            return

        # GET USER ID FROM JWT

        user_id = validated_token.get("user_id")

        if not user_id:

            logger.warning(
                "Ride WebSocket connection rejected: user ID missing | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4003)
            return

        # GET USER

        try:

            self.user = await User.objects.aget(id=user_id)

        except User.DoesNotExist:

            logger.warning(
                "Ride WebSocket connection rejected: user not found | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4003)
            return

        # GET RIDE

        try:

            self.ride = await Ride.objects.select_related(
                "rider",
                "driver__user",
            ).aget(id=self.ride_id)

        except Ride.DoesNotExist:

            logger.warning(
                "Ride WebSocket connection rejected: ride not found | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4004)
            return

        # RIDE OWNER CHECK

        is_ride_owner = self.ride.rider_id == self.user.id

        # DRIVER AUTHORIZATION

        is_assigned_driver = False

        if self.ride.driver:

            is_assigned_driver = (
                self.ride.driver.user_id == self.user.id
            )

        # AUTHORIZATION

        if not is_ride_owner and not is_assigned_driver:

            logger.warning(
                "Ride WebSocket authorization denied | ride_id=%s",
                self.ride_id,
            )

            await self.close(code=4003)
            return

        # GROUP

        self.group_name = f"ride_{self.ride_id}"

        try:

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name,
            )

            # ACCEPT CONNECTION

            await self.accept()

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "message": (
                            "Ride WebSocket connected "
                            "successfully."
                        ),
                        "ride_id": str(self.ride_id),
                        "user_id": str(self.user.id),
                    }
                )
            )

            logger.info(
                "Ride WebSocket connected successfully | ride_id=%s",
                self.ride_id,
            )

        except Exception:

            logger.error(
                "Ride WebSocket connection processing failed | ride_id=%s",
                self.ride_id,
                exc_info=True,
            )

            raise

    async def disconnect(
        self,
        close_code,
    ):

        # REMOVE FROM RIDE GROUP

        if hasattr(
            self,
            "group_name",
        ):

            try:

                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name,
                )

            except Exception:

                logger.error(
                    "Ride WebSocket group removal failed | ride_id=%s",
                    getattr(self, "ride_id", None),
                    exc_info=True,
                )

        # DISCONNECT LOG

        logger.info(
            "Ride WebSocket disconnected | ride_id=%s | code=%s",
            getattr(self, "ride_id", None),
            close_code,
        )

    async def ride_status_update(
        self,
        event,
    ):

        try:

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "message": "Ride status updated.",
                        "ride_id": str(self.ride_id),
                        "status": event["status"],
                    }
                )
            )

        except Exception:

            logger.error(
                "Ride status WebSocket update failed | ride_id=%s",
                self.ride_id,
                exc_info=True,
            )

            raise

    async def driver_location_update(
        self,
        event,
    ):

        try:

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "message": "Driver location updated.",
                        "type": "driver_location",
                        "ride_id": event["ride_id"],
                        "driver_id": event["driver_id"],
                        "latitude": event["latitude"],
                        "longitude": event["longitude"],
                    }
                )
            )

        except Exception:

            logger.error(
                "Driver location WebSocket update failed | ride_id=%s",
                self.ride_id,
                exc_info=True,
            )

            raise