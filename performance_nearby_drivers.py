import os
import time

# Django settings ni configure cheyyadaniki
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

# Test client create 
client = Client(HTTP_HOST="127.0.0.1")

# Passenger access token
login_response = client.post(
    "/api/v1/auth/login/",
    data={
        "email": "passenger@test.com",
        "password": "Test@123456",
    },
    content_type="application/json",
)

access_token = login_response.json()["data"]["access"]

# Previous queries 
reset_queries()

# API execution time start
start = time.perf_counter()

# Nearby Drivers API call
response = client.get(
    "/api/v1/drivers/nearby/",
    data={
        "latitude": 17.3850,
        "longitude": 78.4867,
        "radius": 5
    },
    HTTP_ACCEPT="application/json",
    HTTP_AUTHORIZATION=f"Bearer {access_token}",
)

# API execution time end
end = time.perf_counter()

# Results print 
print("Status Code:", response.status_code)
print("Response Time:", round((end - start) * 1000, 2), "ms")
print("DB Queries:", len(connection.queries))
print("Content-Type:", response.get("Content-Type"))
print("Response:", response.content.decode())
