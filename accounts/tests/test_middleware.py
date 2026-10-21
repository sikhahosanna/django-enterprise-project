import uuid
from unittest.mock import Mock

from django.http import HttpResponse
import logging

from django.test import RequestFactory, SimpleTestCase

from accounts.middleware import RequestIDFilter, RequestIDMiddleware, request_id_context


class RequestIDMiddlewareTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_preserves_supplied_request_id(self):
        request_id = "test-correlation-id"
        request = self.factory.get(
            "/",
            HTTP_X_REQUEST_ID=request_id,
        )
        seen = {}

        def get_response(req):
            seen["request_id"] = request_id_context.get()
            return HttpResponse("OK")

        middleware = RequestIDMiddleware(get_response)

        with self.assertLogs("accounts.middleware", level="INFO") as logs:
            response = middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Request-ID"], request_id)
        self.assertEqual(request.request_id, request_id)
        self.assertEqual(seen["request_id"], request_id)
        self.assertTrue(any("duration_ms=" in line for line in logs.output))
        self.assertEqual(request_id_context.get(), "-")

    def test_generates_request_id_when_header_missing(self):
        request = self.factory.get("/")
        middleware = RequestIDMiddleware(lambda req: HttpResponse("OK"))

        response = middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Request-ID"], request.request_id)
        uuid.UUID(request.request_id)

    def test_resets_context_when_request_raises_exception(self):
        request_id = "failing-request-id"
        request = self.factory.get("/", HTTP_X_REQUEST_ID=request_id)

        def get_response(req):
            raise RuntimeError("simulated failure")

        middleware = RequestIDMiddleware(get_response)

        with self.assertLogs("accounts.middleware", level="ERROR"):
            with self.assertRaises(RuntimeError):
                middleware(request)

        self.assertEqual(request_id_context.get(), "-")

    def test_server_error_response_includes_request_id_and_logs_status(self):
        request_id = "server-error-test-123"
        request = self.factory.get("/", HTTP_X_REQUEST_ID=request_id)
        middleware = RequestIDMiddleware(
            lambda req: HttpResponse("Server error", status=500)
        )

        with self.assertLogs("accounts.middleware", level="INFO") as logs:
            response = middleware(request)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response["X-Request-ID"], request_id)
        self.assertTrue(any("status_code=500" in line for line in logs.output))

    def test_exception_log_contains_correlation_id(self):
        request_id = "exception-trace-123"
        request = self.factory.get("/", HTTP_X_REQUEST_ID=request_id)

        def raise_error(req):
            raise RuntimeError("simulated server failure")

        middleware = RequestIDMiddleware(raise_error)

        with self.assertLogs("accounts.middleware", level="ERROR") as logs:
            with self.assertRaisesRegex(RuntimeError, "simulated server failure"):
                middleware(request)

        self.assertTrue(
            any("API request failed" in record.getMessage()
                for record in logs.records)
        )
        self.assertEqual(request_id_context.get(), "-")
