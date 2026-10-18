import uuid
from unittest.mock import Mock

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.middleware import RequestIDMiddleware, request_id_context


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
