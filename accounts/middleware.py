import logging
import time
import uuid
from contextvars import ContextVar

request_id_context = ContextVar("request_id", default="-")
logger = logging.getLogger(__name__)


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()
        return True


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id
        token = request_id_context.set(request_id)
        start_time = time.perf_counter()

        try:
            response = self.get_response(request)
            response["X-Request-ID"] = request_id

            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "API request completed method=%s path=%s status_code=%s duration_ms=%.2f",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )

            return response

        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "API request failed method=%s path=%s duration_ms=%.2f",
                request.method,
                request.path,
                duration_ms,
            )
            raise

        finally:
            request_id_context.reset(token)
