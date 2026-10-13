
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse

from accounts.throttles import (
    LoginRateThrottle,
    RideCreationRateThrottle,
    SensitiveOperationThrottle,
)


class RateLimitTests(TestCase):

    def setUp(self):
        cache.clear()
        self.factory = APIRequestFactory()

        rates = {
            "login": "2/minute",
            "ride_creation": "2/minute",
            "sensitive": "2/minute",
        }

        LoginRateThrottle.THROTTLE_RATES = rates
        RideCreationRateThrottle.THROTTLE_RATES = rates
        SensitiveOperationThrottle.THROTTLE_RATES = rates

    def test_login_throttle(self):
        throttle = LoginRateThrottle()

        for _ in range(2):
            request = self.factory.post("/api/v1/auth/login/")
            request.META["REMOTE_ADDR"] = "10.0.0.1"
            self.assertTrue(throttle.allow_request(request, None))

        request = self.factory.post("/api/v1/auth/login/")
        request.META["REMOTE_ADDR"] = "10.0.0.1"
        self.assertFalse(throttle.allow_request(request, None))

    def test_ride_creation_throttle(self):
        throttle = RideCreationRateThrottle()

        user = type(
            "User",
            (),
            {"is_authenticated": True, "id": "test-user"},
        )()

        for _ in range(2):
            request = self.factory.post("/api/v1/rides/")
            request.user = user
            self.assertTrue(throttle.allow_request(request, None))

        request = self.factory.post("/api/v1/rides/")
        request.user = user
        self.assertFalse(throttle.allow_request(request, None))

    def test_sensitive_throttle(self):
        throttle = SensitiveOperationThrottle()

        user = type(
            "User",
            (),
            {
                "is_authenticated": True,
                "pk": "test-user",
            },
        )()

        for _ in range(2):
            request = self.factory.post(
                "/api/v1/auth/change-password/"
            )
            request.user = user
            self.assertTrue(throttle.allow_request(request, None))

        request = self.factory.post(
            "/api/v1/auth/change-password/"
        )
        request.user = user
        self.assertFalse(throttle.allow_request(request, None))

    def test_login_api_returns_429_after_limit(self):
        client = APIClient()

        url = "/api/v1/auth/login/"
        payload = {
            "email": "ratelimit-test@example.com",
            "password": "WrongPassword123!",
        }

        for _ in range(2):
            response = client.post(url, payload, format="json")
            self.assertNotEqual(response.status_code, 429)

        response = client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 429)
