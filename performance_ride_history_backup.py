import os
import time

# Django settings 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

# Test client create 
client = Client(HTTP_HOST="127.0.0.1")

# Passenger access token 
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4Mzc1NjE1LCJpYXQiOjE3ODgzNzM4MTUsImp0aSI6IjA5NGJhOTZkY2Q1YzRjYTk5OWYwZjRkODU2YzI1ZjNhIiwidXNlcl9pZCI6Ijc4MmRhMDQxLWJmN2ItNDljMC1hYWVjLTE1Y2Y5OTA5M2I4ZiJ9.EaTtopuTIyIS-eEomWbQE_fXzmawqjaDyWMwFIGazhw"

# Previous queries 
reset_queries()

# API execution time start
start = time.perf_counter()

# Ride History API call
response = client.get(
    "/api/v1/rides/optimized-history/",
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