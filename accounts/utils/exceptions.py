from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger("accounts")


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        logger.error(
            "API Exception: %s",
            exc,
            exc_info=True,
        )

        return Response(
            {
                "success": False,
                "message": str(response.data),
                "error_code": "API_ERROR",
                "data": None,
            },
            status=response.status_code,
        )

    logger.exception(
        "Unhandled API Exception: %s",
        exc,
    )

    return Response(
        {
            "success": False,
            "message": str(exc),
            "error_code": "INTERNAL_SERVER_ERROR",
            "data": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
