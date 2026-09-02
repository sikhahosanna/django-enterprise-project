import os
import time

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

# Create test client
client = Client(HTTP_HOST="127.0.0.1")

# Paste the passenger access token here
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4Mzc2MDc3LCJpYXQiOjE3ODgzNzQyNzcsImp0aSI6ImM5ZjZkMTJmMjE2YzRlYjJiMWYxNDVkMWNlY2E4MWU5IiwidXNlcl9pZCI6Ijc4MmRhMDQxLWJmN2ItNDljMC1hYWVjLTE1Y2Y5OTA5M2I4ZiJ9.dzImxnLG_DJIm23aR2sJOqg3PE-lh8HwXGIVNVQaceA"

# Reset previous database queries
reset_queries()

# Start API execution timer
start = time.perf_counter()

# Call Notifications API
response = client.get(
    "/api/v1/notifications/",
    HTTP_ACCEPT="application/json",
    HTTP_AUTHORIZATION=f"Bearer {access_token}",
)

# Stop API execution timer
end = time.perf_counter()

# Calculate response time
response_time = (end - start) * 1000

# Print performance results
print("Status Code:", response.status_code)
print("Response Time:", round(response_time, 2), "ms")
print("DB Queries:", len(connection.queries))
print("Content-Type:", response.get("Content-Type"))
print("Response:", response.content.decode())