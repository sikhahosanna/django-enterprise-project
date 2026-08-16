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

from django.db import connection

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from django.db.models import Sum
from django.utils import timezone

from .permissions import (
    IsAdminOrDriverOwner,
)

from .models import (
    Ride,
    RideStatus,
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

from .utils.responses import (
    success_response,
    error_response,
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
                "access": str(
                    refresh.access_token
                ),
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

            return error_response(
                message="Profile not created.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProfileSerializer(
            profile
        )

        return success_response(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
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

        return success_response(
            message="Profile saved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# PROFILE LIST - ADMIN
# =========================================================

class ProfileListView(
    generics.ListAPIView
):

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
    pagination_class = CustomPagination

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
            serializer.validated_data[
                "new_password"
            ]
        )

        request.user.save(
            update_fields=["password"]
        )

        return Response(
            {
                "message":
                    "Password changed successfully"
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
                    "error":
                        "Refresh token is required"
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
                    "message":
                        "Logout successfully"
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            return Response(
                {
                    "error":
                        "Invalid refresh token"
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

            return error_response(
                message="Profile not found.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        profile.is_deleted = True

        profile.save(
            update_fields=["is_deleted"]
        )

        return success_response(
            message="Profile deleted successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
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

            return error_response(
                message="Profile not found.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        profile.is_deleted = False

        profile.save(
            update_fields=["is_deleted"]
        )

        return success_response(
            message="Profile restored successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
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
                "driver__user",
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

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:

            serializer = self.get_serializer(
                page,
                many=True
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return success_response(
            message="Vehicles retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):

        if self.request.user.is_staff:

            serializer.save()

            return

        driver = self.get_driver()

        serializer.save(
            driver=driver
        )

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_create(
            serializer
        )

        return success_response(
            message="Vehicle created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
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

    def retrieve(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return success_response(
            message="Vehicle retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_update(
            serializer
        )

        return success_response(
            message="Vehicle updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        self.perform_destroy(
            instance
        )

        return success_response(
            message="Vehicle deleted successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
        )

    def perform_update(
        self,
        serializer
    ):

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

    # IMPORTANT:
    # RideCreateSerializer already handles rider.
    # Do NOT pass rider=self.request.user here.
    def perform_create(self, serializer):

        serializer.save()


# =========================================================
# RIDE FARE
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

            if (
                field not in data
                or data.get(field) is None
            ):

                return f"{field} is required."

        return None

    def _get_vehicle_type(
        self,
        vehicle_type_id
    ):

        try:

            return VehicleType.objects.get(
                id=vehicle_type_id
            )

        except VehicleType.DoesNotExist:

            return None

    def post(self, request):

        error = self._validate_request_data(
            request.data
        )

        if error:

            return error_response(
                message=error,
                error_code="MISSING_REQUIRED_FIELD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        vehicle_type = self._get_vehicle_type(
            request.data.get("vehicle_type")
        )

        if vehicle_type is None:

            return error_response(
                message="Vehicle type not found.",
                error_code="VEHICLE_TYPE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

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

            return error_response(
                message=str(e),
                error_code="FARE_CALCULATION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Fare calculated successfully.",
            data={
                "base_fare":
                    fare_details["base_fare"],

                "distance_fare":
                    fare_details["distance_fare"],

                "time_fare":
                    fare_details["time_fare"],

                "surge":
                    fare_details["surge"],

                "total":
                    fare_details["total"],
            },
            status_code=status.HTTP_200_OK,
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

            return success_response(
                message="Ride accepted successfully.",
                data={
                    "ride_id": str(ride.id),
                    "driver_id": str(ride.driver.id),
                    "driver_email": ride.driver.user.email,
                    "status": ride.status.name,
                },
                status_code=status.HTTP_200_OK,
            )

        except PermissionError as e:

            return error_response(
                message=str(e),
                error_code="PERMISSION_DENIED",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",
                error_code="RIDE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:

            return error_response(
                message=str(e),
                error_code="INVALID_RIDE_STATUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# RIDE STATUS UPDATE
# =========================================================

class RideStatusUpdateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, pk):

        try:

            ride = (
                Ride.objects
                .select_related(
                    "status",
                    "driver",
                    "driver__user",
                )
                .get(id=pk)
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",
                error_code="RIDE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = RideStatusUpdateSerializer(
            data=request.data,
            context={
                "ride": ride,
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            updated_ride = RideService.update_status(
                ride_id=pk,
                driver=request.user,
                new_status_name=(
                    serializer.validated_data["status"]
                ),
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",
                error_code="RIDE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except PermissionError as e:

            return error_response(
                message=str(e),
                error_code="PERMISSION_DENIED",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        except ValueError as e:

            return error_response(
                message=str(e),
                error_code="INVALID_RIDE_STATUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Ride status updated successfully.",
            data={
                "ride_id": str(updated_ride.id),
                "status": updated_ride.status.name,
            },
            status_code=status.HTTP_200_OK,
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

            return success_response(
                message="Ride cancelled successfully.",
                data={
                    "ride_id": str(ride.id),
                    "status": ride.status.name,
                },
                status_code=status.HTTP_200_OK,
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",
                error_code="RIDE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except PermissionError as e:

            return error_response(
                message=str(e),
                error_code="PERMISSION_DENIED",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        except ValueError as e:

            return error_response(
                message=str(e),
                error_code="INVALID_RIDE_STATUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# USER ACTIVE RIDES
# =========================================================

class UserActiveRidesView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        active_statuses = [
            RideStatus.Status.REQUESTED,
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
            RideStatus.Status.STARTED,
        ]

        return (
            Ride.objects
            .filter(
                rider=self.request.user,
                status__name__in=active_statuses,
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by(
                "-created_at"
            )
        )

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:

            data = [
                build_ride_data(ride)
                for ride in page
            ]

            return self.get_paginated_response(
                data
            )

        data = [
            build_ride_data(ride)
            for ride in queryset
        ]

        return Response(
            {
                "success": True,
                "count": len(data),
                "results": data,
            }
        )


# =========================================================
# USER COMPLETED RIDES
# =========================================================

class UserCompletedRidesView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects
            .filter(
                rider=self.request.user,
                status__name=(
                    RideStatus.Status.COMPLETED
                ),
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by(
                "-created_at"
            )
        )

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:

            data = [
                build_ride_data(ride)
                for ride in page
            ]

            return self.get_paginated_response(
                data
            )

        data = [
            build_ride_data(ride)
            for ride in queryset
        ]

        return Response(
            {
                "success": True,
                "count": len(data),
                "results": data,
            }
        )


# =========================================================
# USER CANCELLED RIDES
# =========================================================

class UserCancelledRidesView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects
            .filter(
                rider=self.request.user,
                status__name=(
                    RideStatus.Status.CANCELLED
                ),
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by(
                "-created_at"
            )
        )

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:

            data = [
                build_ride_data(ride)
                for ride in page
            ]

            return self.get_paginated_response(
                data
            )

        data = [
            build_ride_data(ride)
            for ride in queryset
        ]

        return Response(
            {
                "success": True,
                "count": len(data),
                "results": data,
            }
        )


# =========================================================
# DRIVER RIDE HISTORY
# =========================================================

class DriverRideHistoryView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects
            .filter(
                driver__user=self.request.user
            )
            .select_related(
                "rider",
                "rider__profile",
                "driver",
                "vehicle_type",
                "status",
            )
            .order_by(
                "-created_at"
            )
        )

    def list(
        self,
        request,
        *args,
        **kwargs
    ):

        queryset = self.get_queryset()

        page = self.paginate_queryset(
            queryset
        )

        rides = page if page is not None else queryset

        data = []

        for ride in rides:

            profile = getattr(
                ride.rider,
                "profile",
                None
            )

            data.append(
                {
                    "id": str(ride.id),

                    "passenger": {
                        "id": str(
                            ride.rider.id
                        ),

                        "email":
                            ride.rider.email,

                        "first_name": (
                            profile.first_name
                            if profile
                            else ""
                        ),

                        "last_name": (
                            profile.last_name
                            if profile
                            else ""
                        ),
                    },

                    "pickup_address":
                        ride.pickup_address,

                    "dropoff_address":
                        ride.dropoff_address,

                    "vehicle_type": (
                        ride.vehicle_type.name
                        if ride.vehicle_type
                        else None
                    ),

                    "status":
                        ride.status.name,

                    "fare":
                        str(ride.fare),

                    "created_at":
                        ride.created_at,
                }
            )

        if page is not None:

            return self.get_paginated_response(
                data
            )

        return Response(
            {
                "success": True,
                "count": len(data),
                "results": data,
            }
        )


# =========================================================
# DAILY RIDE COUNT
# =========================================================

class DailyRideCountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        today = timezone.localdate()

        count = (
            Ride.objects
            .filter(
                rider=request.user,
                created_at__date=today,
            )
            .count()
        )

        return Response(
            {
                "success": True,
                "date": today,
                "ride_count": count,
            }
        )


# =========================================================
# TOTAL COMPLETED RIDES
# =========================================================

class TotalCompletedRidesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        total = (
            Ride.objects
            .filter(
                rider=request.user,
                status__name=(
                    RideStatus.Status.COMPLETED
                ),
            )
            .count()
        )

        return Response(
            {
                "success": True,
                "total_completed_rides": total,
            }
        )


# =========================================================
# TOTAL FARE EARNED BY DRIVER
# =========================================================

class DriverTotalFareEarnedView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        result = (
            Ride.objects
            .filter(
                driver__user=request.user,
                status__name=(
                    RideStatus.Status.COMPLETED
                ),
            )
            .aggregate(
                total_fare=Sum("fare")
            )
        )

        total_fare = (
            result["total_fare"]
            if result["total_fare"] is not None
            else 0
        )

        return Response(
            {
                "success": True,
                "total_fare_earned":
                    str(total_fare),
            }
        )


# =========================================================
# TASK 5 - DATABASE OPTIMIZATION
# =========================================================

class SlowRideHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        rides = (
            Ride.objects
            .filter(
                rider=request.user
            )
            .order_by("-created_at")
        )

        data = []

        for ride in rides:

            data.append(
                {
                    "id": str(ride.id),

                    "pickup_address":
                        ride.pickup_address,

                    "dropoff_address":
                        ride.dropoff_address,

                    "rider_email":
                        ride.rider.email,

                    "vehicle_type": (
                        ride.vehicle_type.name
                        if ride.vehicle_type
                        else None
                    ),

                    "status":
                        ride.status.name,

                    "fare":
                        str(ride.fare),
                }
            )

        return success_response(
            message="Slow ride history fetched successfully.",
            data={
                "query_count":
                    len(connection.queries),

                "results":
                    data,
            },
            status_code=status.HTTP_200_OK,
        )


class OptimizedRideHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        rides = (
            Ride.objects
            .filter(
                rider=request.user
            )
            .select_related(
                "rider",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

        data = []

        for ride in rides:

            data.append(
                {
                    "id": str(ride.id),

                    "pickup_address":
                        ride.pickup_address,

                    "dropoff_address":
                        ride.dropoff_address,

                    "rider_email":
                        ride.rider.email,

                    "vehicle_type": (
                        ride.vehicle_type.name
                        if ride.vehicle_type
                        else None
                    ),

                    "status":
                        ride.status.name,

                    "fare":
                        str(ride.fare),
                }
            )

        return success_response(
            message="Optimized ride history fetched successfully.",
            data={
                "query_count":
                    len(connection.queries),

                "results":
                    data,
            },
            status_code=status.HTTP_200_OK,
        )