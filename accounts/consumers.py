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


websocket_logger = logging.getLogger("websocket")


class DriverLocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.user = await self.get_user_from_token()

            if not self.user:
                websocket_logger.warning(
                    "WebSocket connection denied: user not found"
                )
                await self.close(code=4003)
                return

            if not self.user.is_authenticated:
                websocket_logger.warning(
                    "WebSocket connection denied: unauthorized user"
                )
                await self.close(code=4003)
                return

            await self.accept()

            websocket_logger.info(
                "Driver location WebSocket connected"
            )

        except Exception as e:
            websocket_logger.error(
                f"WebSocket connection error: {str(e)}"
            )
            await self.close(code=4003)

    async def disconnect(self, close_code):
        websocket_logger.info(
            f"Driver location WebSocket disconnected: {close_code}"
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude is None or longitude is None:
                websocket_logger.warning(
                    "Driver location update failed: latitude or longitude missing"
                )
                return

            websocket_logger.info(
                "Driver location update received"
            )

        except json.JSONDecodeError:
            websocket_logger.warning(
                "WebSocket received invalid JSON"
            )

        except Exception as e:
            websocket_logger.error(
                f"Driver location update error: {str(e)}"
            )

    async def get_user_from_token(self):
        try:
            token = self.scope.get("query_string", b"").decode()

            if not token:
                websocket_logger.warning(
                    "WebSocket authentication failed: token missing"
                )
                return None

            token_value = token.split("token=")[-1]

            validated_token = UntypedToken(token_value)

            user_id = validated_token.get("user_id")

            if not user_id:
                websocket_logger.warning(
                    "WebSocket authentication failed: user ID missing"
                )
                return None

            user = await self.get_user(user_id)

            if not user:
                websocket_logger.warning(
                    "WebSocket authentication failed: user not found"
                )
                return None

            return user

        except (InvalidToken, TokenError):
            websocket_logger.warning(
                "WebSocket authentication failed: invalid token"
            )
            return None

        except Exception as e:
            websocket_logger.error(
                f"WebSocket token processing error: {str(e)}"
            )
            return None

    async def get_user(self, user_id):
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return None


class RideConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.ride_id = self.scope["url_route"]["kwargs"]["ride_id"]

            self.user = await self.get_user_from_token()

            if not self.user:
                websocket_logger.warning(
                    "Ride WebSocket connection denied: user not found"
                )
                await self.close(code=4003)
                return

            self.room_group_name = f"ride_{self.ride_id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()

            websocket_logger.info(
                f"Ride WebSocket connected: ride={self.ride_id}"
            )

        except Exception as e:
            websocket_logger.error(
                f"Ride WebSocket connection error: {str(e)}"
            )
            await self.close(code=4003)

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "room_group_name"):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name,
                )

            websocket_logger.info(
                f"Ride WebSocket disconnected: ride={getattr(self, 'ride_id', None)}"
            )

        except Exception as e:
            websocket_logger.error(
                f"Ride WebSocket disconnect error: {str(e)}"
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            websocket_logger.info(
                f"Ride WebSocket message received: ride={self.ride_id}"
            )

        except json.JSONDecodeError:
            websocket_logger.warning(
                "Ride WebSocket received invalid JSON"
            )

        except Exception as e:
            websocket_logger.error(
                f"Ride WebSocket message processing error: {str(e)}"
            )

    async def ride_status_update(self, event):
        try:
            await self.send(
                text_data=json.dumps({
                    "type": "ride_status_update",
                    "ride_id": event.get("ride_id"),
                    "status": event.get("status"),
                })
            )

            websocket_logger.info(
                f"Ride status update sent: ride={self.ride_id}"
            )

        except Exception as e:
            websocket_logger.error(
                f"Ride status update error: {str(e)}"
            )

    async def get_user_from_token(self):
        try:
            token = self.scope.get("query_string", b"").decode()

            if not token:
                websocket_logger.warning(
                    "Ride WebSocket authentication failed: token missing"
                )
                return None

            token_value = token.split("token=")[-1]

            validated_token = UntypedToken(token_value)

            user_id = validated_token.get("user_id")

            if not user_id:
                websocket_logger.warning(
                    "Ride WebSocket authentication failed: user ID missing"
                )
                return None

            user = await self.get_user(user_id)

            if not user:
                websocket_logger.warning(
                    "Ride WebSocket authentication failed: user not found"
                )
                return None

            return user

        except (InvalidToken, TokenError):
            websocket_logger.warning(
                "Ride WebSocket authentication failed: invalid token"
            )
            return None

        except Exception as e:
            websocket_logger.error(
                f"Ride WebSocket token processing error: {str(e)}"
            )
            return None

    async def get_user(self, user_id):
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return None