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
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4Mzc0Mzc3LCJpYXQiOjE3ODgzNzI1NzcsImp0aSI6IjI1NTUyY2JiYTczYzQ5ZDM5MzAyYjFjOTg3OGQ0OGNmIiwidXNlcl9pZCI6IjkzMWVlYTdlLTdjMGYtNGUwNy1iNWI3LTIwNzI3NzZiOWFmNCJ9.D_byjVqfzNEOzi-BQ_Ns8zP84QLFBgBiEvS7qRauI5M"

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