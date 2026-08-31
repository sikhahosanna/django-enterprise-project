import time

from django.core.cache import cache
from django.db import connection, reset_queries
from django.db.models import Count, Sum, Avg, Min, Max, Q
from django.utils import timezone

from rest_framework import generics, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.tokens import RefreshToken

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .utils.helpers import calculate_distance_km
from rest_framework.permissions import AllowAny

from .services.notification_service import NotificationService
from .services.profile_service import ProfileService


from .permissions import IsAdminOrDriverOwner
from .throttles import LoginRateThrottle

from .models import (
    Ride,
    RideStatus,
    User,
    Profile,
    DriverProfile,
    DriverLocation,
    Vehicle,
    Notification,
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
    DriverLocationSerializer,
    NotificationSerializer,
)

from .services.fare_service import FareService
from .services.ride import RideService


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
# RIDE RESPONSE HELPER
# =========================================================


def build_ride_data(ride):

    driver_data = None

    if ride.driver:

        driver_user = getattr(
            ride.driver,
            "user",
            None,
        )

        driver_data = {
            "id": str(ride.driver.id),
            "email": (driver_user.email if driver_user else None),
        }

    return {
        "id": str(ride.id),
        "pickup_address": ride.pickup_address,
        "dropoff_address": ride.dropoff_address,
        "vehicle_type": (ride.vehicle_type.name if ride.vehicle_type else None),
        "status": (ride.status.name if ride.status else None),
        "fare": str(ride.fare),
        "driver": driver_data,
        "created_at": ride.created_at,
        "updated_at": ride.updated_at,
    }


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

    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return success_response(
            message="Login successful.",
            data={
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status_code=status.HTTP_200_OK,
        )
# =========================================================
# PROFILE
# =========================================================


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get(self, request):

        profile = ProfileService.get_profile(request.user)

        if profile is None:

            return error_response(
                message="Profile not created.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProfileSerializer(profile)

        return success_response(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = ProfileService.save_profile(
            user=request.user,
            data=request.data,
            serializer_class=ProfileSerializer,
        )

        return success_response(
            message="Profile saved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# PROFILE LIST - ADMIN
# =========================================================


class ProfileListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    queryset = Profile.objects.select_related("user").filter(is_deleted=False)

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

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["new_password"])

        request.user.save(update_fields=["password"])

        return success_response(
            message="Password changed successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# LOGOUT
# =========================================================


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:

            return error_response(
                message="Refresh token is required.",
                error_code="REFRESH_TOKEN_REQUIRED",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:

            token = RefreshToken(refresh_token)

            token.blacklist()

            return success_response(
                message="Logout successful.",
                data=None,
                status_code=status.HTTP_200_OK,
            )

        except Exception:

            return error_response(
                message="Invalid refresh token.",
                error_code="INVALID_REFRESH_TOKEN",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# DELETE PROFILE
# =========================================================


class DeleteProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        profile = ProfileService.delete_profile(request.user)

        if profile is None:

            return error_response(
                message="Profile not found.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
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

    permission_classes = [IsAuthenticated]

    def post(self, request):

        profile = ProfileService.restore_profile(request.user)

        if profile is None:

            return error_response(
                message="Profile not found.",
                error_code="PROFILE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
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


class DriverListCreateView(generics.ListCreateAPIView):

    queryset = DriverProfile.objects.select_related(
        "user",
        "user__profile",
    ).all()

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

    filterset_fields = ["status"]

    ordering_fields = [
        "license_number",
        "status",
        "created_at",
        "updated_at",
    ]

    ordering = ["-created_at"]


# =========================================================
# DRIVER DETAIL
# =========================================================


class DriverDetailView(generics.RetrieveUpdateAPIView):

    queryset = DriverProfile.objects.select_related(
        "user",
        "user__profile",
    ).all()

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

        return Vehicle.objects.select_related(
            "driver",
            "driver__user",
            "vehicle_type",
        )

    def get_driver(self):

        try:
            return self.request.user.driver_profile

        except DriverProfile.DoesNotExist:

            raise PermissionError("You are not registered as a driver.")


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

        return queryset.filter(driver__user=self.request.user)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:

            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

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

        serializer.save(driver=driver)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

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

        return queryset.filter(driver__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return success_response(
            message="Vehicle retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return success_response(
            message="Vehicle updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        self.perform_destroy(instance)

        return success_response(
            message="Vehicle deleted successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
        )

    def perform_update(self, serializer):

        if self.request.user.is_staff:
            serializer.save()
            return

        driver = self.get_driver()

        serializer.save(driver=driver)


# =========================================================
# TASK 6 - ADVANCED RIDE FILTERING
# =========================================================


class RideListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    def get_queryset(self):

        queryset = Ride.objects.select_related(
            "rider",
            "rider__profile",
            "status",
            "driver",
            "driver__user",
            "vehicle_type",
        ).filter(rider=self.request.user)

        status_value = self.request.query_params.get("status")

        if status_value:

            queryset = queryset.filter(status__name=status_value)

        driver_id = self.request.query_params.get("driver")

        if driver_id:

            queryset = queryset.filter(driver_id=driver_id)

        start_date = self.request.query_params.get("start_date")

        if start_date:

            queryset = queryset.filter(created_at__date__gte=start_date)

        end_date = self.request.query_params.get("end_date")

        if end_date:

            queryset = queryset.filter(created_at__date__lte=end_date)

        min_fare = self.request.query_params.get("min_fare")

        if min_fare:

            queryset = queryset.filter(fare__gte=min_fare)

        max_fare = self.request.query_params.get("max_fare")

        if max_fare:

            queryset = queryset.filter(fare__lte=max_fare)

        ordering = self.request.query_params.get("ordering")

        allowed_ordering = [
            "created_at",
            "-created_at",
            "fare",
            "-fare",
        ]

        if ordering in allowed_ordering:

            queryset = queryset.order_by(ordering)

        else:

            queryset = queryset.order_by("-created_at")

        return queryset

    def get_serializer_class(self):

        if self.request.method == "POST":

            return RideCreateSerializer

        return RideSerializer

    def perform_create(self, serializer):

        serializer.save(rider=self.request.user)


# =========================================================
# RIDE FARE
# =========================================================


class RideFareView(APIView):

    permission_classes = [IsAuthenticated]

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

                return f"{field} is required."

        return None

    def post(self, request):

        error = self._validate_request_data(request.data)

        if error:

            return error_response(
                message=error,
                error_code="MISSING_REQUIRED_FIELD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        vehicle_type = FareService.get_vehicle_type(request.data.get("vehicle_type"))

        if vehicle_type is None:

            return error_response(
                message="Vehicle type not found.",
                error_code="VEHICLE_TYPE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:

            fare_details = FareService.calculate_fare(
                vehicle_type=vehicle_type,
                pickup_latitude=request.data.get("pickup_latitude"),
                pickup_longitude=request.data.get("pickup_longitude"),
                dropoff_latitude=request.data.get("dropoff_latitude"),
                dropoff_longitude=request.data.get("dropoff_longitude"),
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
                "base_fare": fare_details["base_fare"],
                "distance_fare": fare_details["distance_fare"],
                "time_fare": fare_details["time_fare"],
                "surge": fare_details["surge"],
                "total": fare_details["total"],
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# RIDE DETAIL
# =========================================================


class RideDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = RideDetailSerializer

    def get_queryset(self):

        return Ride.objects.select_related(
            "rider",
            "rider__profile",
            "driver",
            "driver__user",
            "status",
            "vehicle_type",
        ).filter(rider=self.request.user)


# =========================================================
# ACCEPT RIDE
# =========================================================


class RideAcceptView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            ride = RideService.accept_ride(
                ride_id=pk,
                user=request.user,
            )

            NotificationService.ride_accepted(ride)

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

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        # -------------------------------------------------
        # GET RIDE
        # -------------------------------------------------

        try:

            ride = Ride.objects.select_related(
                "status",
                "driver",
                "driver__user",
                "rider",
            ).get(id=pk)

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",
                error_code="RIDE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # -------------------------------------------------
        # VALIDATE REQUEST
        # -------------------------------------------------

        serializer = RideStatusUpdateSerializer(
            data=request.data,
            context={
                "ride": ride,
                "request": request,
            },
        )

        serializer.is_valid(raise_exception=True)

        # -------------------------------------------------
        # UPDATE STATUS
        # -------------------------------------------------

        try:

            updated_ride = RideService.update_status(
                ride_id=pk,
                driver=request.user,
                new_status_name=(serializer.validated_data["status"]),
            )

            # -------------------------------------------------
            # NEW STATUS
            # -------------------------------------------------

            new_status = updated_ride.status.name

            # -------------------------------------------------
            # NOTIFICATIONS
            # -------------------------------------------------

            if new_status == RideStatus.Status.DRIVER_ARRIVING:

                NotificationService.driver_arriving(updated_ride)

            elif new_status == RideStatus.Status.STARTED:

                NotificationService.ride_started(updated_ride)

            elif new_status == RideStatus.Status.COMPLETED:

                NotificationService.ride_completed(updated_ride)
            # -------------------------------------------------
            # WEBSOCKET BROADCAST
            # -------------------------------------------------

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f"ride_{updated_ride.id}",
                {
                    "type": "ride_status_update",
                    "status": updated_ride.status.name,
                    "ride_id": str(updated_ride.id),
                },
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

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

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

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            ride = RideService.cancel_ride(
                ride_id=pk,
                rider=request.user,
            )

            # -------------------------------------------------
            # CANCELLATION NOTIFICATION
            # -------------------------------------------------

            NotificationService.ride_cancelled(ride)

            # -------------------------------------------------
            # WEBSOCKET
            # -------------------------------------------------

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f"ride_{ride.id}",
                {
                    "type": "ride_status_update",
                    "status": ride.status.name,
                    "ride_id": str(ride.id),
                },
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


class UserActiveRidesView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    def get_queryset(self):

        active_statuses = [
            RideStatus.Status.REQUESTED,
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
            RideStatus.Status.STARTED,
        ]

        return (
            Ride.objects.filter(
                rider=self.request.user,
                status__name__in=active_statuses,
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:

            data = [build_ride_data(ride) for ride in page]

            return self.get_paginated_response(data)

        data = [build_ride_data(ride) for ride in queryset]

        return success_response(
            message="Active rides retrieved successfully.",
            data={
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# USER COMPLETED RIDES
# =========================================================


class UserCompletedRidesView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects.filter(
                rider=self.request.user,
                status__name=RideStatus.Status.COMPLETED,
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:

            data = [build_ride_data(ride) for ride in page]

            return self.get_paginated_response(data)

        data = [build_ride_data(ride) for ride in queryset]

        return success_response(
            message="Completed rides retrieved successfully.",
            data={
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# USER CANCELLED RIDES
# =========================================================


class UserCancelledRidesView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects.filter(
                rider=self.request.user,
                status__name=RideStatus.Status.CANCELLED,
            )
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:

            data = [build_ride_data(ride) for ride in page]

            return self.get_paginated_response(data)

        data = [build_ride_data(ride) for ride in queryset]

        return success_response(
            message="Cancelled rides retrieved successfully.",
            data={
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# DRIVER RIDE HISTORY
# =========================================================


class DriverRideHistoryView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    def get_queryset(self):

        return (
            Ride.objects.filter(driver__user=self.request.user)
            .select_related(
                "rider",
                "rider__profile",
                "driver",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        rides = page if page is not None else queryset

        data = []

        for ride in rides:

            profile = getattr(ride.rider, "profile", None)

            data.append(
                {
                    "id": str(ride.id),
                    "passenger": {
                        "id": str(ride.rider.id),
                        "email": ride.rider.email,
                        "first_name": (profile.first_name if profile else ""),
                        "last_name": (profile.last_name if profile else ""),
                    },
                    "pickup_address": ride.pickup_address,
                    "dropoff_address": ride.dropoff_address,
                    "vehicle_type": (
                        ride.vehicle_type.name if ride.vehicle_type else None
                    ),
                    "status": ride.status.name,
                    "fare": str(ride.fare),
                    "created_at": ride.created_at,
                }
            )

        if page is not None:

            return self.get_paginated_response(data)

        return success_response(
            message="Driver ride history retrieved successfully.",
            data={
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# DAILY RIDE COUNT
# =========================================================


class DailyRideCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = timezone.localdate()

        count = Ride.objects.filter(
            rider=request.user,
            created_at__date=today,
        ).count()

        return success_response(
            message="Daily ride count retrieved successfully.",
            data={
                "date": today,
                "ride_count": count,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TOTAL COMPLETED RIDES
# =========================================================


class TotalCompletedRidesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total = Ride.objects.filter(
            rider=request.user,
            status__name=RideStatus.Status.COMPLETED,
        ).count()

        return success_response(
            message="Total completed rides retrieved successfully.",
            data={
                "total_completed_rides": total,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TOTAL FARE EARNED BY DRIVER
# =========================================================


class DriverTotalFareEarnedView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        result = Ride.objects.filter(
            driver__user=request.user,
            status__name=RideStatus.Status.COMPLETED,
        ).aggregate(total_fare=Sum("fare"))

        total_fare = result["total_fare"] if result["total_fare"] is not None else 0

        return success_response(
            message="Total fare earned retrieved successfully.",
            data={
                "total_fare_earned": str(total_fare),
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TASK 3 - RIDE AGGREGATIONS
# =========================================================


class RideAggregationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        rides = Ride.objects.filter(rider=request.user)

        completed_status = RideStatus.Status.COMPLETED

        cancelled_status = RideStatus.Status.CANCELLED

        result = rides.aggregate(
            total_rides=Count("id"),
            completed_rides=Count(
                "id",
                filter=Q(status__name=completed_status),
            ),
            cancelled_rides=Count(
                "id",
                filter=Q(status__name=cancelled_status),
            ),
            average_fare=Avg("fare"),
            maximum_fare=Max("fare"),
            minimum_fare=Min("fare"),
        )

        driver_earnings = Ride.objects.filter(
            driver__user=request.user,
            status__name=completed_status,
        ).aggregate(total_driver_earnings=Sum("fare"))

        return success_response(
            message="Ride aggregation retrieved successfully.",
            data={
                "total_rides": result["total_rides"],
                "completed_rides": result["completed_rides"],
                "cancelled_rides": result["cancelled_rides"],
                "average_fare": (
                    str(result["average_fare"])
                    if result["average_fare"] is not None
                    else "0"
                ),
                "maximum_fare": (
                    str(result["maximum_fare"])
                    if result["maximum_fare"] is not None
                    else "0"
                ),
                "minimum_fare": (
                    str(result["minimum_fare"])
                    if result["minimum_fare"] is not None
                    else "0"
                ),
                "total_driver_earnings": (
                    str(driver_earnings["total_driver_earnings"])
                    if driver_earnings["total_driver_earnings"] is not None
                    else "0"
                ),
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TASK 4 - SLOW RIDE HISTORY
# =========================================================


class SlowRideHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reset_queries()

        rides = Ride.objects.filter(rider=request.user).order_by("-created_at")

        data = []

        for ride in rides:

            driver = ride.driver

            driver_user = driver.user if driver else None

            vehicle_type = ride.vehicle_type if ride.vehicle_type else None

            data.append(
                {
                    "id": str(ride.id),
                    "pickup_address": ride.pickup_address,
                    "dropoff_address": ride.dropoff_address,
                    "status": (ride.status.name if ride.status else None),
                    "fare": str(ride.fare),
                    "vehicle_type": (vehicle_type.name if vehicle_type else None),
                    "driver": (
                        {
                            "id": str(driver.id),
                            "email": (driver_user.email if driver_user else None),
                        }
                        if driver
                        else None
                    ),
                }
            )

        query_count = len(connection.queries)

        return success_response(
            message="Ride history optimization retrieved successfully.",
            data={
                "optimization": "slow",
                "query_count": query_count,
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TASK 4 - OPTIMIZED RIDE HISTORY
# =========================================================


class OptimizedRideHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reset_queries()

        rides = (
            Ride.objects.filter(rider=request.user)
            .select_related(
                "driver",
                "driver__user",
                "vehicle_type",
                "status",
            )
            .order_by("-created_at")
        )

        data = []

        for ride in rides:

            driver = ride.driver

            driver_user = driver.user if driver else None

            vehicle_type = ride.vehicle_type if ride.vehicle_type else None

            data.append(
                {
                    "id": str(ride.id),
                    "pickup_address": ride.pickup_address,
                    "dropoff_address": ride.dropoff_address,
                    "status": (ride.status.name if ride.status else None),
                    "fare": str(ride.fare),
                    "vehicle_type": (vehicle_type.name if vehicle_type else None),
                    "driver": (
                        {
                            "id": str(driver.id),
                            "email": (driver_user.email if driver_user else None),
                        }
                        if driver
                        else None
                    ),
                }
            )

        query_count = len(connection.queries)

        return success_response(
            message="Optimized ride history retrieved successfully.",
            data={
                "optimization": "optimized",
                "query_count": query_count,
                "count": len(data),
                "results": data,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# DISTANCE CALCULATION
# =========================================================


# =========================================================
# DRIVER LOCATION
# =========================================================


class DriverLocationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            driver = request.user.driver_profile

        except DriverProfile.DoesNotExist:

            return error_response(
                message="You are not registered as a driver.",
                error_code="DRIVER_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = DriverLocationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        location, created = DriverLocation.objects.update_or_create(
            driver=driver,
            defaults={
                "latitude": serializer.validated_data["latitude"],
                "longitude": serializer.validated_data["longitude"],
                "availability_status": serializer.validated_data.get(
                    "availability_status", DriverLocation.AvailabilityStatus.OFFLINE
                ),
            },
        )

        # -------------------------------------------------
        # FIND ACTIVE RIDE
        # -------------------------------------------------

        ride = Ride.objects.filter(
            driver=driver,
            status__name__in=[
                RideStatus.Status.ACCEPTED,
                RideStatus.Status.DRIVER_ARRIVING,
                RideStatus.Status.STARTED,
            ],
        ).first()

        # -------------------------------------------------
        # WEBSOCKET LOCATION UPDATE
        # -------------------------------------------------

        if ride:

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f"ride_{ride.id}",
                {
                    "type": "driver_location_update",
                    "ride_id": str(ride.id),
                    "driver_id": str(driver.id),
                    "latitude": float(location.latitude),
                    "longitude": float(location.longitude),
                },
            )

        # -------------------------------------------------
        # CACHE INVALIDATION
        # -------------------------------------------------

        cache.clear()

        return success_response(
            message=("Driver location and availability " "updated successfully."),
            data={
                "driver_id": str(driver.id),
                "latitude": location.latitude,
                "longitude": location.longitude,
                "availability_status": location.availability_status,
                "last_updated": location.last_updated,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# DRIVER AVAILABILITY
# =========================================================


class DriverAvailabilityView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        try:

            driver = request.user.driver_profile

        except DriverProfile.DoesNotExist:

            return error_response(
                message="You are not registered as a driver.",
                error_code="DRIVER_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:

            location = DriverLocation.objects.get(driver=driver)

        except DriverLocation.DoesNotExist:

            return error_response(
                message="Driver location not found.",
                error_code="DRIVER_LOCATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        availability_status = request.data.get("availability_status")

        if not availability_status:

            return error_response(
                message="availability_status is required.",
                error_code="MISSING_AVAILABILITY_STATUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = [
            choice[0] for choice in (DriverLocation.AvailabilityStatus.choices)
        ]

        if availability_status not in valid_statuses:

            return error_response(
                message="Invalid availability status.",
                error_code="INVALID_AVAILABILITY_STATUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        location.availability_status = availability_status

        location.save(
            update_fields=[
                "availability_status",
                "last_updated",
            ]
        )

        cache.clear()

        return success_response(
            message=("Driver availability updated successfully."),
            data={
                "driver_id": str(driver.id),
                "availability_status": location.availability_status,
                "last_updated": location.last_updated,
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# TASK 5 - NEARBY DRIVER API WITH REDIS CACHE
# =========================================================


class NearbyDriverView(APIView):

    permission_classes = [IsAuthenticated]

    CACHE_TIMEOUT = 60

    def get(self, request):

        start_time = time.perf_counter()

        reset_queries()

        latitude = request.query_params.get("latitude")

        longitude = request.query_params.get("longitude")

        radius = request.query_params.get("radius")

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not latitude or not longitude or not radius:

            return error_response(
                message=("latitude, longitude and radius " "are required."),
                error_code="MISSING_REQUIRED_FIELD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:

            latitude = float(latitude)

            longitude = float(longitude)

            radius = float(radius)

        except (
            ValueError,
            TypeError,
        ):

            return error_response(
                message=("latitude, longitude and radius " "must be valid numbers."),
                error_code="INVALID_LOCATION_DATA",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not -90 <= latitude <= 90:

            return error_response(
                message="Invalid latitude.",
                error_code="INVALID_LATITUDE",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not -180 <= longitude <= 180:

            return error_response(
                message="Invalid longitude.",
                error_code="INVALID_LONGITUDE",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if radius <= 0:

            return error_response(
                message="Radius must be greater than 0.",
                error_code="INVALID_RADIUS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # CACHE KEY
        # -------------------------------------------------

        cache_key = (
            f"nearby_drivers:" f"{latitude:.4f}:" f"{longitude:.4f}:" f"{radius:.2f}"
        )

        cached_data = cache.get(cache_key)

        # -------------------------------------------------
        # CACHE HIT
        # -------------------------------------------------

        if isinstance(cached_data, dict):

            query_count = len(connection.queries)

            response_time = time.perf_counter() - start_time

            return success_response(
                message=("Nearby drivers retrieved " "from cache."),
                data={
                    **cached_data,
                    "cache_status": "HIT",
                    "query_count": query_count,
                    "response_time_ms": round(response_time * 1000, 2),
                },
                status_code=status.HTTP_200_OK,
            )

        # -------------------------------------------------
        # CACHE MISS
        # -------------------------------------------------

        locations = DriverLocation.objects.filter(
            availability_status=(DriverLocation.AvailabilityStatus.ONLINE),
            driver__status=(DriverProfile.DriverStatus.ACTIVE),
        ).select_related(
            "driver",
            "driver__user",
        )

        nearby_drivers = []

        # -------------------------------------------------
        # DISTANCE CALCULATION
        # -------------------------------------------------

        for location in locations:

            driver_latitude = float(location.latitude)

            driver_longitude = float(location.longitude)

            distance_km = calculate_distance_km(
                latitude,
                longitude,
                driver_latitude,
                driver_longitude,
            )

            if distance_km <= radius:

                nearby_drivers.append(
                    {
                        "driver_id": str(location.driver.id),
                        "email": location.driver.user.email,
                        "latitude": driver_latitude,
                        "longitude": driver_longitude,
                        "distance_km": round(distance_km, 2),
                        "availability_status": location.availability_status,
                        "last_updated": location.last_updated,
                    }
                )

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        nearby_drivers.sort(key=lambda driver: driver["distance_km"])

        # -------------------------------------------------
        # RESPONSE DATA
        # -------------------------------------------------

        response_data = {
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": radius,
            "count": len(nearby_drivers),
            "drivers": nearby_drivers,
        }

        # -------------------------------------------------
        # CACHE
        # -------------------------------------------------

        cache.set(
            cache_key,
            response_data,
            self.CACHE_TIMEOUT,
        )

        # -------------------------------------------------
        # PERFORMANCE
        # -------------------------------------------------

        query_count = len(connection.queries)

        response_time = time.perf_counter() - start_time

        return success_response(
            message=("Nearby drivers retrieved " "successfully."),
            data={
                **response_data,
                "cache_status": "MISS",
                "query_count": query_count,
                "response_time_ms": round(response_time * 1000, 2),
            },
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# NOTIFICATIONS
# =========================================================


class NotificationListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = NotificationSerializer

    pagination_class = CustomPagination

    def get_queryset(self):

        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


# =========================================================
# MARK NOTIFICATION READ
# =========================================================


class NotificationMarkReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:

            notification = Notification.objects.get(id=pk, user=request.user)

        except Notification.DoesNotExist:

            return error_response(
                message="Notification not found.",
                error_code="NOTIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True

        notification.save(update_fields=["is_read"])

        serializer = NotificationSerializer(notification)

        return success_response(
            message="Notification marked as read.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =========================================================
# MARK ALL NOTIFICATIONS READ
# =========================================================


class NotificationMarkAllReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True)

        return success_response(
            message="All notifications marked as read.",
            data={"updated_count": updated_count},
            status_code=status.HTTP_200_OK,
        )
