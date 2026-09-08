from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class RideCreationRateThrottle(SimpleRateThrottle):
    scope = "ride_creation"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"ride_creation_{request.user.id}"
        return self.get_ident(request)
from rest_framework.throttling import (
    SimpleRateThrottle,
    AnonRateThrottle,
    UserRateThrottle,
)


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class RideCreationRateThrottle(SimpleRateThrottle):
    scope = "ride_creation"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"ride_creation_{request.user.id}"
        return self.get_ident(request)


class AnonymousRateThrottle(AnonRateThrottle):
    scope = "anonymous"


class AuthenticatedRateThrottle(UserRateThrottle):
    scope = "authenticated"


class SensitiveOperationThrottle(UserRateThrottle):
    scope = "sensitive"