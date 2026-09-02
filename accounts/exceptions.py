from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger("accounts")


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

 
    # DRF HANDLED EXCEPTIONS
  

    if response is not None:

        logger.error(
            "API Exception: %s",
            exc,
            exc_info=True,
        )

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            error_code = "VALIDATION_ERROR"

        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            error_code = "AUTHENTICATION_REQUIRED"

        elif response.status_code == status.HTTP_403_FORBIDDEN:
            error_code = "PERMISSION_DENIED"

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            error_code = "NOT_FOUND"

        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            error_code = "METHOD_NOT_ALLOWED"

        else:
            error_code = "API_ERROR"

        if isinstance(response.data, dict):

            if "detail" in response.data:
                message = str(response.data["detail"])
            else:
                message = "Validation error."

        else:
            message = str(response.data)

        return Response(
            {
                "success": False,
                "message": message,
                "error_code": error_code,
                "data": None,
            },
            status=response.status_code,
        )

    # UNHANDLED EXCEPTION
   

    logger.exception(
        "Unhandled API Exception: %s",
        exc,
    )

    return Response(
        {
            "success": False,
            "message": "Internal server error.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "data": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
