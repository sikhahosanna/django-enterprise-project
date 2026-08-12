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
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Ride,
    User,
    Profile,
    DriverProfile,
    Vehicle,
    RideStatus,
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

        if self.request.method == "GET":
            return DriverNestedSerializer

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

        if user.is_staff:

            return Vehicle.objects.select_related(
                "driver",
                "vehicle_type"
            ).all()

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

        if user.is_staff:

            return Vehicle.objects.select_related(
                "driver",
                "vehicle_type"
            ).all()

        return Vehicle.objects.select_related(
            "driver",
            "vehicle_type"
        ).filter(
            driver__user=user
        )


# =========================================
# CREATE RIDE
# =========================================

class CreateRideView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = RideCreateSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        ride = serializer.save()

        return Response(
            {
                "message": "Ride created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# RIDE LIST + CREATE
# USER CAN SEE OWN RIDES
# =========================================

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
                "status",
                "driver",
                "driver__user",
                "vehicle_type"
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

        serializer.save()


# =========================================
# RIDE DETAIL
# TASK 4
# =========================================

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
                "vehicle_type"
            )
            .filter(
                rider=self.request.user
            )
        )


# =========================================
# RIDE STATUS UPDATE
# =========================================

class RideStatusUpdateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, pk):

        try:

            ride = Ride.objects.select_related(
                "status"
            ).get(
                pk=pk,
                rider=request.user
            )

        except Ride.DoesNotExist:

            return Response(
                {
                    "error": "Ride not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RideStatusUpdateSerializer(
            data=request.data,
            context={
                "ride": ride
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        new_status = RideStatus.objects.get(
            name=serializer.validated_data["status"]
        )

        ride.status = new_status

        ride.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return Response(
            {
                "message": "Ride status updated successfully.",
                "ride_id": str(ride.id),
                "status": ride.status.name
            },
            status=status.HTTP_200_OK
        )


# =========================================
# ACCEPT RIDE - DRIVER
# TASK 6
# =========================================

# =========================================
# ACCEPT RIDE - DRIVER
# TASK 6
# =========================================

# =========================================
# ACCEPT RIDE - DRIVER
# TASK 6
# =========================================

class RideAcceptView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        print("\n========== TASK 6 DEBUG ==========")
        print("USER:", request.user)
        print("USER ID:", request.user.id)

        # 1. DRIVER CHECK
        try:

            driver = DriverProfile.objects.get(
                user=request.user
            )

            print("DRIVER:", driver)
            print("DRIVER ID:", driver.id)
            print("DRIVER STATUS:", driver.status)

        except DriverProfile.DoesNotExist:

            return Response(
                {
                    "error": "You are not registered as a driver."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. DRIVER ACTIVE CHECK
        if driver.status != DriverProfile.DriverStatus.ACTIVE:

            return Response(
                {
                    "error": "Driver is not active."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. RIDE LOCK + VALIDATION
        try:

            with transaction.atomic():

                # IMPORTANT:
                # driver ni select_related lo include cheyyakudadhu
                # because driver nullable field.
                ride = (
                    Ride.objects
                    .select_for_update()
                    .select_related("status")
                    .get(
                        pk=pk
                    )
                )

                print("RIDE:", ride)
                print("RIDE ID:", ride.id)
                print("RIDE STATUS:", ride.status.name)

                # 4. RIDE MUST BE REQUESTED
                if ride.status.name != RideStatus.Status.REQUESTED:

                    return Response(
                        {
                            "error": (
                                "Ride is no longer available. "
                                f"Current status is "
                                f"'{ride.status.name}'."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 5. DRIVER CONFLICT CHECK
                conflicting_statuses = [
                    RideStatus.Status.ACCEPTED,
                    RideStatus.Status.DRIVER_ARRIVING,
                    RideStatus.Status.STARTED,
                ]

                conflicting_ride = (
                    Ride.objects
                    .filter(
                        driver=driver,
                        status__name__in=conflicting_statuses
                    )
                    .exclude(
                        id=ride.id
                    )
                    .exists()
                )

                print(
                    "CONFLICTING RIDE:",
                    conflicting_ride
                )

                if conflicting_ride:

                    return Response(
                        {
                            "error":
                                "Driver already has an active ride."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 6. GET ACCEPTED STATUS
                try:

                    accepted_status = RideStatus.objects.get(
                        name=RideStatus.Status.ACCEPTED
                    )

                except RideStatus.DoesNotExist:

                    return Response(
                        {
                            "error":
                                "Accepted ride status is not configured."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                # 7. ASSIGN DRIVER
                ride.driver = driver
                ride.status = accepted_status

                ride.save(
                    update_fields=[
                        "driver",
                        "status",
                        "updated_at"
                    ]
                )

                print("RIDE ACCEPTED SUCCESSFULLY")

            # 8. SUCCESS RESPONSE
            return Response(
                {
                    "message":
                        "Ride accepted successfully.",
                    "ride_id":
                        str(ride.id),
                    "driver_id":
                        str(driver.id),
                    "driver_email":
                        driver.user.email,
                    "status":
                        ride.status.name
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            import traceback

            print("\n========== TASK 6 ERROR ==========")
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR:", str(e))
            traceback.print_exc()
            print("==================================\n")

            return Response(
                {
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# =========================================
# CANCEL RIDE
# TASK 7
# =========================================
class RideCancelView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        print("\n========== TASK 7 DEBUG ==========")
        print("USER:", request.user)
        print("USER ID:", request.user.id)
        print("RIDE ID:", pk)

        try:

            with transaction.atomic():

                ride = (
                    Ride.objects
                    .select_for_update()
                    .select_related("status")
                    .get(
                        pk=pk,
                        rider=request.user
                    )
                )

                print("RIDE FOUND:", ride.id)
                print("CURRENT STATUS:", ride.status.name)

                # ---------------------------------
                # CHECK CANCELLATION STATUS
                # ---------------------------------

                allowed_statuses = [
                    RideStatus.Status.REQUESTED,
                    RideStatus.Status.ACCEPTED,
                ]

                if ride.status.name not in allowed_statuses:

                    return Response(
                        {
                            "error": (
                                "Ride cannot be cancelled when "
                                f"status is '{ride.status.name}'."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # ---------------------------------
                # GET CANCELLED STATUS
                # ---------------------------------

                try:

                    cancelled_status = RideStatus.objects.get(
                        name=RideStatus.Status.CANCELLED
                    )

                except RideStatus.DoesNotExist:

                    return Response(
                        {
                            "error":
                                "Cancelled ride status is not configured."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                # ---------------------------------
                # CANCEL RIDE
                # ---------------------------------

                ride.status = cancelled_status

                ride.save(
                    update_fields=[
                        "status",
                        "updated_at"
                    ]
                )

                print("RIDE CANCELLED SUCCESSFULLY")

            return Response(
                {
                    "message":
                        "Ride cancelled successfully.",
                    "ride_id":
                        str(ride.id),
                    "status":
                        ride.status.name
                },
                status=status.HTTP_200_OK
            )

        except Ride.DoesNotExist:

            print("ERROR: Ride not found")

            return Response(
                {
                    "error": "Ride not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:

            import traceback

            print("\n========== TASK 7 ERROR ==========")
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR:", str(e))
            traceback.print_exc()
            print("==================================")

            return Response(
                {
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )