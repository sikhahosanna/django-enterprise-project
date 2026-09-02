import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from django.test import Client
from django.db import connection, reset_queries

client = Client(HTTP_HOST="127.0.0.1")

reset_queries()

start = time.perf_counter()

response = client.post(
    "/api/v1/login/",
    data={
        "email": "passenger@test.com",
        "password": "Test@123456",
    },
    content_type="application/json",
    HTTP_ACCEPT="application/json",
)

end = time.perf_counter()

print("Status Code:", response.status_code)
print("Response Time:", round((end - start) * 1000, 2), "ms")
print("DB Queries:", len(connection.queries))
print("Content-Type:", response.get("Content-Type"))
print("Response:", response.content.decode())