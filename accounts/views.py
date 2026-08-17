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
from math import (
    radians,
    sin,
    cos,
    sqrt,
    atan2,
)
from django.db import connection, reset_queries

from django.db.models import (
    Count,
    Sum,
    Avg,
    Min,
    Max,
    Q,
    
)

 

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
    DriverLocation,
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
    DriverLocationSerializer,
    DriverLocation,
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

            "email": (
                driver_user.email
                if driver_user
                else None
            ),
        }

    return {
        "id": str(ride.id),

        "pickup_address":
            ride.pickup_address,

        "dropoff_address":
            ride.dropoff_address,

        "vehicle_type": (
            ride.vehicle_type.name
            if ride.vehicle_type
            else None
        ),

        "status": (
            ride.status.name
            if ride.status
            else None
        ),

        "fare":
            str(ride.fare),

        "driver":
            driver_data,

        "created_at":
            ride.created_at,

        "updated_at":
            ride.updated_at,
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
        .filter(
            is_deleted=False
        )
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

        queryset = (
            self.get_vehicle_queryset()
        )

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

    def perform_create(
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

        queryset = (
            self.get_vehicle_queryset()
        )

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

# =========================================================
# TASK 6 - ADVANCED RIDE FILTERING
# =========================================================

class RideListCreateView(
    generics.ListCreateAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CustomPagination

    def get_queryset(self):

        queryset = (
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
        )

        # =================================================
        # STATUS FILTER
        # =================================================

        status_value = self.request.query_params.get(
            "status"
        )

        if status_value:

            queryset = queryset.filter(
                status__name=status_value
            )

        # =================================================
        # DRIVER FILTER
        # =================================================

        driver_id = self.request.query_params.get(
            "driver"
        )

        if driver_id:

            queryset = queryset.filter(
                driver_id=driver_id
            )

        # =================================================
        # START DATE FILTER
        # =================================================

        start_date = self.request.query_params.get(
            "start_date"
        )

        if start_date:

            queryset = queryset.filter(
                created_at__date__gte=start_date
            )

        # =================================================
        # END DATE FILTER
        # =================================================

        end_date = self.request.query_params.get(
            "end_date"
        )

        if end_date:

            queryset = queryset.filter(
                created_at__date__lte=end_date
            )

        # =================================================
        # MIN FARE FILTER
        # =================================================

        min_fare = self.request.query_params.get(
            "min_fare"
        )

        if min_fare:

            queryset = queryset.filter(
                fare__gte=min_fare
            )

        # =================================================
        # MAX FARE FILTER
        # =================================================

        max_fare = self.request.query_params.get(
            "max_fare"
        )

        if max_fare:

            queryset = queryset.filter(
                fare__lte=max_fare
            )

        # =================================================
        # ORDERING
        # =================================================

        ordering = self.request.query_params.get(
            "ordering"
        )

        allowed_ordering = [
            "created_at",
            "-created_at",
            "fare",
            "-fare",
        ]

        if ordering in allowed_ordering:

            queryset = queryset.order_by(
                ordering
            )

        else:

            queryset = queryset.order_by(
                "-created_at"
            )

        return queryset

    def get_serializer_class(self):

        if self.request.method == "POST":

            return RideCreateSerializer

        return RideSerializer

    def perform_create(
        self,
        serializer
    ):

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

    def _validate_request_data(
        self,
        data
    ):

        for field in self.REQUIRED_FIELDS:

            if (
                field not in data
                or data.get(field) is None
            ):

                return (
                    f"{field} is required."
                )

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

    def post(
        self,
        request
    ):

        error = (
            self._validate_request_data(
                request.data
            )
        )

        if error:

            return error_response(
                message=error,

                error_code=(
                    "MISSING_REQUIRED_FIELD"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        vehicle_type = (
            self._get_vehicle_type(
                request.data.get(
                    "vehicle_type"
                )
            )
        )

        if vehicle_type is None:

            return error_response(
                message=(
                    "Vehicle type not found."
                ),

                error_code=(
                    "VEHICLE_TYPE_NOT_FOUND"
                ),

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        try:

            fare_details = (
                FareService.calculate_fare(

                    vehicle_type=vehicle_type,

                    pickup_latitude=(
                        request.data.get(
                            "pickup_latitude"
                        )
                    ),

                    pickup_longitude=(
                        request.data.get(
                            "pickup_longitude"
                        )
                    ),

                    dropoff_latitude=(
                        request.data.get(
                            "dropoff_latitude"
                        )
                    ),

                    dropoff_longitude=(
                        request.data.get(
                            "dropoff_longitude"
                        )
                    ),

                    duration_minutes=(
                        request.data.get(
                            "duration_minutes",
                            0,
                        )
                    ),
                )
            )

        except (
            ValueError,
            TypeError,
            KeyError,
        ) as e:

            return error_response(
                message=str(e),

                error_code=(
                    "FARE_CALCULATION_ERROR"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
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

    def post(
        self,
        request,
        pk
    ):

        try:

            ride = RideService.accept_ride(
                ride_id=pk,
                user=request.user,
            )

            return success_response(
                message="Ride accepted successfully.",

                data={
                    "ride_id": str(ride.id),

                    "driver_id": str(
                        ride.driver.id
                    ),

                    "driver_email":
                        ride.driver.user.email,

                    "status":
                        ride.status.name,
                },

                status_code=status.HTTP_200_OK,
            )

        except PermissionError as e:

            return error_response(
                message=str(e),

                error_code="PERMISSION_DENIED",

                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",

                error_code="RIDE_NOT_FOUND",

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        except ValueError as e:

            return error_response(
                message=str(e),

                error_code=(
                    "INVALID_RIDE_STATUS"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )


# =========================================================
# RIDE STATUS UPDATE
# =========================================================

class RideStatusUpdateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        pk
    ):

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

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
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

            updated_ride = (
                RideService.update_status(

                    ride_id=pk,

                    driver=request.user,

                    new_status_name=(
                        serializer.validated_data[
                            "status"
                        ]
                    ),
                )
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",

                error_code="RIDE_NOT_FOUND",

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        except PermissionError as e:

            return error_response(
                message=str(e),

                error_code="PERMISSION_DENIED",

                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
            )

        except ValueError as e:

            return error_response(
                message=str(e),

                error_code=(
                    "INVALID_RIDE_STATUS"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        return success_response(
            message="Ride status updated successfully.",

            data={
                "ride_id":
                    str(updated_ride.id),

                "status":
                    updated_ride.status.name,
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

    def post(
        self,
        request,
        pk
    ):

        try:

            ride = RideService.cancel_ride(
                ride_id=pk,
                rider=request.user,
            )

            return success_response(
                message="Ride cancelled successfully.",

                data={
                    "ride_id":
                        str(ride.id),

                    "status":
                        ride.status.name,
                },

                status_code=status.HTTP_200_OK,
            )

        except Ride.DoesNotExist:

            return error_response(
                message="Ride not found.",

                error_code="RIDE_NOT_FOUND",

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        except PermissionError as e:

            return error_response(
                message=str(e),

                error_code="PERMISSION_DENIED",

                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
            )

        except ValueError as e:

            return error_response(
                message=str(e),

                error_code=(
                    "INVALID_RIDE_STATUS"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
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

                status__name__in=(
                    active_statuses
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

        rides = (
            page
            if page is not None
            else queryset
        )

        data = []

        for ride in rides:

            profile = getattr(
                ride.rider,
                "profile",
                None
            )

            data.append(
                {
                    "id":
                        str(ride.id),

                    "passenger": {
                        "id":
                            str(ride.rider.id),

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

                "total_completed_rides":
                    total,
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
# TASK 3 - RIDE AGGREGATIONS
# =========================================================

class RideAggregationView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        # -------------------------------------------------
        # Rider rides
        # -------------------------------------------------

        rides = Ride.objects.filter(
            rider=request.user
        )

        completed_status = (
            RideStatus.Status.COMPLETED
        )

        cancelled_status = (
            RideStatus.Status.CANCELLED
        )

        # -------------------------------------------------
        # Rider aggregations
        # -------------------------------------------------

        result = rides.aggregate(

            total_rides=Count(
                "id"
            ),

            completed_rides=Count(
                "id",

                filter=Q(
                    status__name=(
                        completed_status
                    )
                ),
            ),

            cancelled_rides=Count(
                "id",

                filter=Q(
                    status__name=(
                        cancelled_status
                    )
                ),
            ),

            average_fare=Avg(
                "fare"
            ),

            maximum_fare=Max(
                "fare"
            ),

            minimum_fare=Min(
                "fare"
            ),
        )

        # -------------------------------------------------
        # Driver earnings
        # -------------------------------------------------

        driver_earnings = (
            Ride.objects
            .filter(
                driver__user=request.user,

                status__name=(
                    completed_status
                ),
            )
            .aggregate(
                total_driver_earnings=Sum(
                    "fare"
                )
            )
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return Response(
            {
                "success": True,

                "total_rides":
                    result["total_rides"],

                "completed_rides":
                    result["completed_rides"],

                "cancelled_rides":
                    result["cancelled_rides"],

                "average_fare": (
                    str(
                        result["average_fare"]
                    )
                    if result[
                        "average_fare"
                    ] is not None
                    else "0"
                ),

                "maximum_fare": (
                    str(
                        result["maximum_fare"]
                    )
                    if result[
                        "maximum_fare"
                    ] is not None
                    else "0"
                ),

                "minimum_fare": (
                    str(
                        result["minimum_fare"]
                    )
                    if result[
                        "minimum_fare"
                    ] is not None
                    else "0"
                ),

                "total_driver_earnings": (
                    str(
                        driver_earnings[
                            "total_driver_earnings"
                        ]
                    )
                    if driver_earnings[
                        "total_driver_earnings"
                    ] is not None
                    else "0"
                ),
            }
        )
 
    # =========================================================
# TASK 4 - SLOW RIDE HISTORY
# =========================================================

class SlowRideHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        reset_queries()

        rides = (
            Ride.objects
            .filter(rider=request.user)
            .order_by("-created_at")
        )

        data = []

        for ride in rides:

            # Deliberately accessing related objects
            # without select_related()
            driver = ride.driver

            driver_user = (
                driver.user
                if driver
                else None
            )

            vehicle_type = (
                ride.vehicle_type
                if ride.vehicle_type
                else None
            )

            data.append({
                "id": str(ride.id),

                "pickup_address":
                    ride.pickup_address,

                "dropoff_address":
                    ride.dropoff_address,

                "status": (
                    ride.status.name
                    if ride.status
                    else None
                ),

                "fare": str(ride.fare),

                "vehicle_type": (
                    vehicle_type.name
                    if vehicle_type
                    else None
                ),

                "driver": (
                    {
                        "id": str(driver.id),
                        "email": (
                            driver_user.email
                            if driver_user
                            else None
                        ),
                    }
                    if driver
                    else None
                ),
            })

        query_count = len(connection.queries)

        return Response({
            "success": True,
            "optimization": "slow",
            "query_count": query_count,
            "count": len(data),
            "results": data,
        })
# =========================================================
# TASK 4 - OPTIMIZED RIDE HISTORY
# =========================================================

class OptimizedRideHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        reset_queries()

        rides = (
            Ride.objects
            .filter(rider=request.user)
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

            driver_user = (
                driver.user
                if driver
                else None
            )

            vehicle_type = (
                ride.vehicle_type
                if ride.vehicle_type
                else None
            )

            data.append({
                "id": str(ride.id),

                "pickup_address":
                    ride.pickup_address,

                "dropoff_address":
                    ride.dropoff_address,

                "status": (
                    ride.status.name
                    if ride.status
                    else None
                ),

                "fare": str(ride.fare),

                "vehicle_type": (
                    vehicle_type.name
                    if vehicle_type
                    else None
                ),

                "driver": (
                    {
                        "id": str(driver.id),
                        "email": (
                            driver_user.email
                            if driver_user
                            else None
                        ),
                    }
                    if driver
                    else None
                ),
            })

        query_count = len(connection.queries)

        return Response({
            "success": True,
            "optimization": "optimized",
            "query_count": query_count,
            "count": len(data),
            "results": data,
        })
# =========================================================
# DRIVER LOCATION
# =========================================================

class DriverLocationView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        try:

            driver = request.user.driver_profile

        except DriverProfile.DoesNotExist:

            return error_response(
                message="You are not registered as a driver.",

                error_code="DRIVER_NOT_FOUND",

                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        serializer = DriverLocationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        location, created = (
            DriverLocation.objects.update_or_create(
                driver=driver,

                defaults={
                    "latitude":
                        serializer.validated_data[
                            "latitude"
                        ],

                    "longitude":
                        serializer.validated_data[
                            "longitude"
                        ],
                },
            )
        )

        return success_response(
            message="Driver location updated successfully.",

            data={
                "driver_id":
                    str(driver.id),

                "latitude":
                    location.latitude,

                "longitude":
                    location.longitude,

                "last_updated":
                    location.last_updated,

                "availability_status":
                    location.availability_status,
            },

            status_code=status.HTTP_200_OK,
        )
def calculate_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c
# =========================================================
# TASK 4 - NEARBY DRIVER API
# =========================================================

class NearbyDriverView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        latitude = request.query_params.get("latitude")
        longitude = request.query_params.get("longitude")
        radius = request.query_params.get("radius")

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not latitude or not longitude or not radius:

            return error_response(
                message="latitude, longitude and radius are required.",

                error_code="MISSING_REQUIRED_FIELD",

                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:

            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)

        except (ValueError, TypeError):

            return error_response(
                message="latitude, longitude and radius must be valid numbers.",

                error_code="INVALID_LOCATION_DATA",

                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not (-90 <= latitude <= 90):

            return error_response(
                message="Invalid latitude.",

                error_code="INVALID_LATITUDE",

                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not (-180 <= longitude <= 180):

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

        # -----------------------------------------
        # GET AVAILABLE DRIVERS
        # -----------------------------------------

        locations = (
            DriverLocation.objects
            .filter(
                availability_status=(
                    DriverLocation.AvailabilityStatus.ONLINE
                    
                ),
                driver__status=(
                    DriverProfile.DriverStatus.ACTIVE
                ),
            )
            .select_related(
                "driver",
                "driver__user",
            )
        )

        nearby_drivers = []

        # -----------------------------------------
        # DISTANCE CALCULATION
        # -----------------------------------------

        for location in locations:

            driver_latitude = float(
                location.latitude
            )

            driver_longitude = float(
                location.longitude
            )

            earth_radius_km = 6371.0

            lat1 = radians(latitude)
            lat2 = radians(driver_latitude)

            delta_lat = radians(
                driver_latitude - latitude
            )

            delta_lon = radians(
                driver_longitude - longitude
            )

            a = (
                sin(delta_lat / 2) ** 2
                +
                cos(lat1)
                * cos(lat2)
                * sin(delta_lon / 2) ** 2
            )

            c = 2 * atan2(
                sqrt(a),
                sqrt(1 - a)
            )

            distance_km = (
                earth_radius_km * c
            )

            if distance_km <= radius:

                nearby_drivers.append(
                    {
                        "driver_id": str(
                            location.driver.id
                        ),

                        "email":
                            location.driver.user.email,

                        "latitude":
                            float(location.latitude),

                        "longitude":
                            float(location.longitude),

                        "distance_km":
                            round(distance_km, 2),

                        "availability_status":
                            location.availability_status,

                        "last_updated":
                            location.last_updated,
                    }
                )

        # -----------------------------------------
        # SORT BY NEAREST
        # -----------------------------------------

        nearby_drivers.sort(
            key=lambda driver:
                driver["distance_km"]
        )

        return success_response(
            message="Nearby drivers retrieved successfully.",

            data={
                "latitude": latitude,

                "longitude": longitude,

                "radius_km": radius,

                "count": len(
                    nearby_drivers
                ),

                "drivers":
                    nearby_drivers,
            },

            status_code=status.HTTP_200_OK,
        )