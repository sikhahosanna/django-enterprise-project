import os
import time

# Django settings ni configure
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

# Test client create 
client = Client(HTTP_HOST="127.0.0.1")

# Postman lo driver login response 
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4MzczNDkwLCJpYXQiOjE3ODgzNzE2OTAsImp0aSI6IjcxMzMwZjA0MzU2ODRkM2FhOTIxNTE0OTMzMDQzM2VhIiwidXNlcl9pZCI6IjE1ODE1YjY2LWQzZTQtNDU3NC1hNDI4LWFjNjhlM2U0OTFjMSJ9.2EFhcLdq3USFlMKUosAuOpd0DqLNP98lDu5uqVGgBrA"

# Previous queries ni reset 
reset_queries()

# API execution time start
start = time.perf_counter()

# Driver Location API call
response = client.post(
    "/api/v1/drivers/location/",
    data={
        "latitude": 17.3850,
        "longitude": 78.4867,
        "availability_status": "ONLINE"
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