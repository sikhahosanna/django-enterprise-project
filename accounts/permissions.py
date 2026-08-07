from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Admin can access everything
        if request.user.is_staff:
            return True

        # User can access only own profile
        return obj.user == request.user