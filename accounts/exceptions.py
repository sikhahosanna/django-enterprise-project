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
                "error": response.data,
            },
            status=response.status_code,
        )

    # -----------------------------------------
    # UNHANDLED EXCEPTION
    # -----------------------------------------

    logger.exception(
        "Unhandled API Exception: %s",
        exc,
    )

    return Response(
        {
            "success": False,

            # TEMPORARY: actual error chudataniki
            "error": str(exc),

            "exception": exc.__class__.__name__,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )