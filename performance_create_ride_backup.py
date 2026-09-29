import os
import time

# Django settings 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

# Test client 
client = Client(HTTP_HOST="127.0.0.1")

# Passenger access token 
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4Mzc1MjI0LCJpYXQiOjE3ODgzNzM0MjQsImp0aSI6IjZiNGRmYTMxODkyYzRiNWM5MzAxM2UwYTAxOWIwNTc4IiwidXNlcl9pZCI6Ijc4MmRhMDQxLWJmN2ItNDljMC1hYWVjLTE1Y2Y5OTA5M2I4ZiJ9.jmcNcbE4Xv4w5czOgQ8_XyTgsrSy6gvyd3uDPkRvaI0"

# Previous queries 
reset_queries()

# API execution time start
start = time.perf_counter()

# Create Ride API call
response = client.post(
    "/api/v1/rides/",
    data={
        "pickup_latitude": 17.3850,
        "pickup_longitude": 78.4867,
        "pickup_address": "Hyderabad",
        "dropoff_latitude": 17.4000,
        "dropoff_longitude": 78.5000,
        "dropoff_address": "Secunderabad",
        "vehicle_type": "42101441-690b-496f-aad3-abdf30b9b8fc"
    },
    content_type="application/json",
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