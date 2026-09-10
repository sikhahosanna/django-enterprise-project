import logging

from rest_framework.throttling import (
    SimpleRateThrottle,
    AnonRateThrottle,
    UserRateThrottle,
)


security_logger = logging.getLogger("security")


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        security_logger.info(
            "Login rate limit check performed"
        )
        return self.get_ident(request)


class RideCreationRateThrottle(SimpleRateThrottle):
    scope = "ride_creation"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            security_logger.info(
                "Ride creation rate limit check performed"
            )
            return f"ride_creation_{request.user.id}"

        security_logger.warning(
            "Ride creation rate limit check for anonymous user"
        )
        return self.get_ident(request)


class AnonymousRateThrottle(AnonRateThrottle):
    scope = "anonymous"


class AuthenticatedRateThrottle(UserRateThrottle):
    scope = "authenticated"


class SensitiveOperationThrottle(UserRateThrottle):
    scope = "sensitive"