import logging

from ..models import Profile

database_logger = logging.getLogger("database")


class ProfileService:

    @staticmethod
    def get_profile(user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            database_logger.warning(
                "Profile not found for user"
            )
            return None

    @staticmethod
    def save_profile(user, data, serializer_class):
        profile = ProfileService.get_profile(user)

        if profile:
            serializer = serializer_class(
                profile,
                data=data,
                partial=True,
            )
        else:
            serializer = serializer_class(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=user)

        return serializer