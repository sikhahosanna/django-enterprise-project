import os

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application


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


application = get_wsgi_application()