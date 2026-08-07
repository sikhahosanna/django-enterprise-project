from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging


logger = logging.getLogger("accounts")


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        logger.error(str(exc))

        return Response(
            {
                "success": False,
                "error": response.data
            },
            status=response.status_code
        )


    logger.error(str(exc))

    return Response(
        {
            "success": False,
            "error": "Internal Server Error"
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )