from rest_framework import (
    generics,
    status,
    filters,
)

from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from rest_framework.pagination import (
    PageNumberPagination,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from .permissions import (
    IsAdminOrDriverOwner,
)

from .models import (
    Ride,
    User,
    Profile,
    DriverProfile,
    Vehicle,
    VehicleType,
)

from .serializers import (
    DriverSerializer,
    DriverNestedSerializer,
    RideCreateSerializer,
    RideSerializer,
    RideDetailSerializer,
    RideStatusUpdateSerializer,
    VehicleSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)

from .services.fare_service import (
    FareService,
)

from .services.ride import (
    RideService,
)


# =========================================================
# PAGINATION
# =========================================================

class CustomPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


# =========================================================
# REGISTER
# =========================================================

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# =========================================================
# LOGIN
# =========================================================

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
                    "email": user.email,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# PROFILE
# =========================================================

class ProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get(self, request):

        try:
            profile = request.user.profile

        except Profile.DoesNotExist:

            return Response(
                {
                    "message": "Profile not created"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProfileSerializer(
            profile
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        try:

            profile = request.user.profile

            serializer = ProfileSerializer(
                profile,
                data=request.data,
                partial=True,
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
            status=status.HTTP_200_OK,
        )


# =========================================================
# PROFILE LIST - ADMIN
# =========================================================

class ProfileListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    queryset = (
        Profile.objects
        .select_related("user")
        .filter(is_deleted=False)
    )

    serializer_class = ProfileSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        "first_name",
        "last_name",
        "phone",
        "user__email",
    ]

    ordering_fields = [
        "first_name",
        "last_name",
    ]

    filterset_fields = [
        "first_name",
        "last_name",
    ]


# =========================================================
# CHANGE PASSWORD
# =========================================================

class ChangePasswordView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        request.user.set_password(
            serializer.validated_data["new_password"]
        )

        request.user.save(
            update_fields=["password"]
        )

        return Response(
            {
                "message": "Password changed successfully"
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# LOGOUT
# =========================================================

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
                status=status.HTTP_400_BAD_REQUEST,
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
                status=status.HTTP_200_OK,
            )

        except Exception:

            return Response(
                {
                    "error": "Invalid refresh token"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# DELETE PROFILE
# =========================================================

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
                status=status.HTTP_404_NOT_FOUND,
            )

        profile.is_deleted = True

        profile.save(
            update_fields=["is_deleted"]
        )

        return Response(
            {
                "message": "Profile deleted successfully"
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# RESTORE PROFILE
# =========================================================

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
                status=status.HTTP_404_NOT_FOUND,
            )

        profile.is_deleted = False

        profile.save(
            update_fields=["is_deleted"]
        )

        return Response(
            {
                "message": "Profile restored successfully"
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# DRIVER LIST + CREATE
# ADMIN ONLY
# =========================================================

class DriverListCreateView(
    generics.ListCreateAPIView
):

    queryset = (
        DriverProfile.objects
        .select_related(
            "user",
            "user__profile",
        )
        .all()
    )

    serializer_class = DriverSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    pagination_class = CustomPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        "license_number",
        "status",
        "user__email",
        "user__profile__first_name",
        "user__profile__last_name",
        "user__profile__phone",
    ]

    filterset_fields = [
        "status"
    ]

    ordering_fields = [
        "license_number",
        "status",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at"
    ]


# =========================================================
# DRIVER DETAIL
# =========================================================

class DriverDetailView(
    generics.RetrieveUpdateAPIView
):

    queryset = (
        DriverProfile.objects
        .select_related(
            "user",
            "user__profile",
        )
        .all()
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDriverOwner,
    ]

    def get_serializer_class(self):

        if self.request.method == "GET":
            return DriverNestedSerializer

        return DriverSerializer


# =========================================================
# VEHICLE BASE VIEW
# =========================================================
# Refactoring:
# Common vehicle queryset and driver lookup are centralized.
# =========================================================

class VehicleBaseView:

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDriverOwner,
    ]

    def get_vehicle_queryset(self):

        return (
            Vehicle.objects
            .select_related(
                "driver",
                "vehicle_type",
            )
        )

    def get_driver(self):

        try:

            return self.request.user.driver_profile

        except DriverProfile.DoesNotExist:

            raise PermissionError(
                "You are not registered as a driver."
            )


# =========================================================
# VEHICLE LIST + CREATE
# =========================================================

class VehicleListCreateView(
    VehicleBaseView,
    generics.ListCreateAPIView,
):

    serializer_class = VehicleSerializer

    def get_queryset(self):

        queryset = self.get_vehicle_queryset()

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            driver__user=self.request.user
        )

    def perform_create(self, serializer):

        if self.request.user.is_staff:

            serializer.save()
            return

        driver = self.get_driver()

        serializer.save(
            driver=driver
        )


# =========================================================
# VEHICLE DETAIL
# =========================================================

class VehicleDetailView(
    VehicleBaseView,
    generics.RetrieveUpdateDestroyAPIView,
):

    serializer_class = VehicleSerializer

    def get_queryset(self):

        queryset = self.get_vehicle_queryset()

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            driver__user=self.request.user
        )

    def perform_update(self, serializer):

        if self.request.user.is_staff:

            serializer.save()
            return

        driver = self.get_driver()

        serializer.save(
            driver=driver
        )


# =========================================================
# RIDE LIST + CREATE
# =========================================================

class RideListCreateView(
    generics.ListCreateAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects
            .select_related(
                "rider",
                "rider__profile",
                "status",
                "driver",
                "driver__user",
                "vehicle_type",
            )
            .filter(
                rider=self.request.user
            )
            .order_by(
                "-created_at"
            )
        )

    def get_serializer_class(self):

        if self.request.method == "POST":
            return RideCreateSerializer

        return RideSerializer

    def perform_create(self, serializer):

        serializer.save(
            rider=self.request.user
        )


# =========================================================
# RIDE FARE API
# =========================================================

class RideFareView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    REQUIRED_FIELDS = [
        "vehicle_type",
        "pickup_latitude",
        "pickup_longitude",
        "dropoff_latitude",
        "dropoff_longitude",
    ]

    def _validate_request_data(self, data):

        for field in self.REQUIRED_FIELDS:

            if field not in data or data.get(field) is None:

                return (
                    f"{field} is required."
                )

        return None

    def _get_vehicle_type(self, vehicle_type_id):

        try:

            return VehicleType.objects.get(
                id=vehicle_type_id
            )

        except VehicleType.DoesNotExist:

            return None

    def post(self, request):

        # -----------------------------------------------------
        # VALIDATE INPUT
        # -----------------------------------------------------

        error = self._validate_request_data(
            request.data
        )

        if error:

            return Response(
                {
                    "success": False,
                    "error": error,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------------------
        # GET VEHICLE TYPE
        # -----------------------------------------------------

        vehicle_type = self._get_vehicle_type(
            request.data.get("vehicle_type")
        )

        if vehicle_type is None:

            return Response(
                {
                    "success": False,
                    "error": "Vehicle type not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # -----------------------------------------------------
        # CALCULATE FARE
        # -----------------------------------------------------

        try:

            fare_details = FareService.calculate_fare(

                vehicle_type=vehicle_type,

                pickup_latitude=request.data.get(
                    "pickup_latitude"
                ),

                pickup_longitude=request.data.get(
                    "pickup_longitude"
                ),

                dropoff_latitude=request.data.get(
                    "dropoff_latitude"
                ),

                dropoff_longitude=request.data.get(
                    "dropoff_longitude"
                ),

                duration_minutes=request.data.get(
                    "duration_minutes",
                    0,
                ),
            )

        except (
            ValueError,
            TypeError,
            KeyError,
        ) as e:

            return Response(
                {
                    "success": False,
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return Response(
            {
                "base_fare": fare_details["base_fare"],
                "distance_fare": fare_details["distance_fare"],
                "time_fare": fare_details["time_fare"],
                "surge": fare_details["surge"],
                "total": fare_details["total"],
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# RIDE DETAIL
# =========================================================

class RideDetailView(
    generics.RetrieveAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = RideDetailSerializer

    def get_queryset(self):

        return (
            Ride.objects
            .select_related(
                "rider",
                "rider__profile",
                "driver",
                "driver__user",
                "status",
                "vehicle_type",
            )
            .filter(
                rider=self.request.user
            )
        )


# =========================================================
# ACCEPT RIDE
# =========================================================

class RideAcceptView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            ride = RideService.accept_ride(
                ride_id=pk,
                user=request.user,
            )

            return Response(
                {
                    "message": "Ride accepted successfully.",
                    "ride_id": str(ride.id),
                    "driver_id": str(ride.driver.id),
                    "driver_email": ride.driver.user.email,
                    "status": ride.status.name,
                },
                status=status.HTTP_200_OK,
            )

        except PermissionError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except Ride.DoesNotExist:

            return Response(
                {
                    "error": "Ride not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# RIDE STATUS UPDATE
# =========================================================

class RideStatusUpdateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, pk):

        serializer = RideStatusUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            ride = RideService.update_status(
                ride_id=pk,
                driver=request.user,
                new_status_name=serializer.validated_data[
                    "status"
                ],
            )

        except Ride.DoesNotExist:

            return Response(
                {
                    "error": "Ride not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except PermissionError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Ride status updated successfully.",
                "ride_id": str(ride.id),
                "status": ride.status.name,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# CANCEL RIDE
# =========================================================

class RideCancelView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            ride = RideService.cancel_ride(
                ride_id=pk,
                rider=request.user,
            )

            return Response(
                {
                    "message": "Ride cancelled successfully.",
                    "ride_id": str(ride.id),
                    "status": ride.status.name,
                },
                status=status.HTTP_200_OK,
            )

        except Ride.DoesNotExist:

            return Response(
                {
                    "error": "Ride not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )