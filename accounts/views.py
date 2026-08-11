
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .permissions import (
    IsAdminOrOwner,
    IsAdminOrDriverOwner
)

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User,
    Profile,
    DriverProfile,
    Vehicle
)

from .serializers import (
    DriverSerializer,
    DriverNestedSerializer,
    VehicleSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ProfileSerializer
)
class CustomPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

# =========================================
# REGISTER
# =========================================

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


# =========================================
# LOGIN
# =========================================

class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": str(user.id),
                    "email": user.email
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


# =========================================
# PROFILE
# =========================================

class ProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get(self, request):

        try:

            profile = request.user.profile

        except Profile.DoesNotExist:

            return Response(
                {
                    "message": "Profile not created"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(
            profile
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        try:

            profile = request.user.profile

            serializer = ProfileSerializer(
                profile,
                data=request.data,
                partial=True
            )

        except Profile.DoesNotExist:

            serializer = ProfileSerializer(
                data=request.data
            )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            user=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# =========================================
# PROFILE LIST - ADMIN
# =========================================

class ProfileListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    queryset = Profile.objects.select_related(
        "user"
    ).filter(
        is_deleted=False
    )

    serializer_class = ProfileSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]

    search_fields = [
        "first_name",
        "last_name",
        "phone"
    ]

    ordering_fields = [
        "first_name",
        "last_name"
    ]

    filterset_fields = [
        "first_name",
        "last_name"
    ]


# =========================================
# CHANGE PASSWORD
# =========================================

class ChangePasswordView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        request.user.set_password(
            serializer.validated_data["new_password"]
        )

        request.user.save()

        return Response(
            {
                "message": "Password changed successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================
# LOGOUT
# =========================================

class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        refresh_token = request.data.get(
            "refresh"
        )

        if not refresh_token:

            return Response(
                {
                    "error": "Refresh token is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            token = RefreshToken(
                refresh_token
            )

            token.blacklist()

            return Response(
                {
                    "message": "Logout successfully"
                },
                status=status.HTTP_200_OK
            )

        except Exception:

            return Response(
                {
                    "error": "Invalid refresh token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# =========================================
# DELETE PROFILE - SOFT DELETE
# =========================================

class DeleteProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(self, request):

        try:

            profile = request.user.profile

        except Profile.DoesNotExist:

            return Response(
                {
                    "message": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        profile.is_deleted = True

        profile.save(
            update_fields=["is_deleted"]
        )

        return Response(
            {
                "message": "Profile deleted successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================
# RESTORE PROFILE
# =========================================

class RestoreProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        try:

            profile = request.user.profile

        except Profile.DoesNotExist:

            return Response(
                {
                    "message": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        profile.is_deleted = False

        profile.save(
            update_fields=["is_deleted"]
        )

        return Response(
            {
                "message": "Profile restored successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================
# DRIVER LIST + CREATE
# ADMIN ONLY
# =========================================

class DriverListCreateView(
    generics.ListCreateAPIView
):

    queryset = DriverProfile.objects.select_related(
        "user",
        "user__profile"
    ).all()

    serializer_class = DriverSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]
    pagination_class = CustomPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]

    search_fields = [
        "license_number",
        "status",
        "user__email",
        "user__profile__first_name",
        "user__profile__last_name",
        "user__profile__phone"
    ]

    filterset_fields = [
        "status"
    ]

    ordering_fields = [
        "license_number",
        "status",
        "created_at",
        "updated_at"
    ]

    ordering = [
        "-created_at"
    ]


# =========================================
# DRIVER DETAIL
# ADMIN + DRIVER OWNER
# =========================================

class DriverDetailView(
    generics.RetrieveUpdateAPIView
):

    queryset = DriverProfile.objects.select_related(
        "user",
        "user__profile"
    ).all()

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDriverOwner
    ]

    def get_serializer_class(self):

        # GET
        # Returns nested driver response
        if self.request.method == "GET":

            return DriverNestedSerializer

        # PUT / PATCH
        # Uses normal driver serializer
        return DriverSerializer


# =========================================
# VEHICLE LIST + CREATE
# ADMIN + DRIVER OWNER
# =========================================

class VehicleListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = VehicleSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDriverOwner
    ]

    def get_queryset(self):

        user = self.request.user

        # ADMIN
        # Can see all vehicles

        if user.is_staff:

            return Vehicle.objects.select_related(
                "driver",
                "vehicle_type"
            ).all()

        # DRIVER
        # Can see only own vehicles

        return Vehicle.objects.select_related(
            "driver",
            "vehicle_type"
        ).filter(
            driver__user=user
        )


# =========================================
# VEHICLE DETAIL
# ADMIN + DRIVER OWNER
# =========================================

class VehicleDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = VehicleSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDriverOwner
    ]

    def get_queryset(self):

        user = self.request.user

        # ADMIN
        # Can GET / UPDATE / DELETE all vehicles

        if user.is_staff:

            return Vehicle.objects.select_related(
                "driver",
                "vehicle_type"
            ).all()

        # DRIVER
        # Can GET / UPDATE / DELETE only own vehicles

        return Vehicle.objects.select_related(
            "driver",
            "vehicle_type"
        ).filter(
            driver__user=user
        )

