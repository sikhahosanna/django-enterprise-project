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