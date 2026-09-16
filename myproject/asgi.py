import os

from dotenv import load_dotenv

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


# Load environment variables
load_dotenv()

# Get current environment
environment = os.getenv(
    "DJANGO_ENV",
    "development"
).lower()

# Select Django settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"myproject.settings.{environment}"
)


django_asgi_app = get_asgi_application()


from accounts.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,

        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)