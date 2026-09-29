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
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4Mzc1NDI3LCJpYXQiOjE3ODgzNzM2MjcsImp0aSI6IjgyZWNkNzc2NTdiYTRkOWQ5NjMwODI3Y2M0NGQxMGIzIiwidXNlcl9pZCI6Ijc4MmRhMDQxLWJmN2ItNDljMC1hYWVjLTE1Y2Y5OTA5M2I4ZiJ9.D2CPfXBeeFB7mX4JbkHDCbAtc9Z68FUHyCuYhqQKq6g"

# Create Ride response  Ride ID
ride_id = "c882f11f-6842-4b66-8014-44dc0d04b981"

# Previous queries 
reset_queries()

# API execution time start
start = time.perf_counter()

# Ride Details API call
response = client.get(
    f"/api/v1/rides/{ride_id}/",
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