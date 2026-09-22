from django.urls import re_path

from .consumers import (
    DriverLocationConsumer,
    RideConsumer,
    BookingConsumer,
)

websocket_urlpatterns = [
    re_path(
        r"ws/driver/location/$",
        DriverLocationConsumer.as_asgi(),
    ),
    re_path(
        r"ws/ride/(?P<ride_id>[0-9a-f-]+)/$",
        RideConsumer.as_asgi(),
    ),
    re_path(
    r"ws/booking/(?P<booking_id>[0-9a-f-]+)/$",
    BookingConsumer.as_asgi(),
),
]
