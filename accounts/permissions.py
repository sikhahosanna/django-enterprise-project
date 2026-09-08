from rest_framework.permissions import BasePermission
from .models import DriverProfile


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.is_staff:
            return True

        # User can access only own profile
        return obj.user == request.user


class IsAdminOrDriverOwner(BasePermission):

    def has_permission(self, request, view):
        # Must be logged in
        if not request.user.is_authenticated:
            return False

        # Admin can manage all vehicles
        if request.user.is_staff:
            return True

        # Driver must have DriverProfile
        return DriverProfile.objects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        # Admin can manage all vehicles
        if request.user.is_staff:
            return True

        # Driver can manage only own vehicle
        return obj.driver.user == request.user

class IsAdminOrDriver(BasePermission):
    """
    Admin and Driver can perform driver-specific actions.
    Passenger is denied.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return DriverProfile.objects.filter(user=request.user).exists()


class IsAdminOrPassenger(BasePermission):
    """
    Admin and Passenger can create rides.
    Driver is denied.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return not DriverProfile.objects.filter(user=request.user).exists()