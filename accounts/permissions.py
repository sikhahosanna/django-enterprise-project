from rest_framework.permissions import BasePermission
from .models import DriverProfile


class IsAdminOrOwner(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        # Admin can access everything
        if request.user.is_staff:
            return True

        # User can access only own profile
        return obj.user == request.user


class IsAdminOrDriverOwner(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):
        # Must be logged in
        if not request.user.is_authenticated:
            return False

        # Admin can manage all vehicles
        if request.user.is_staff:
            return True

        # Driver must have DriverProfile
        return DriverProfile.objects.filter(
            user=request.user
        ).exists()

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        # Admin can manage all vehicles
        if request.user.is_staff:
            return True

        # Driver can manage only own vehicle
        return obj.driver.user == request.user