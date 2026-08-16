from django.urls import path

from .views import (
    # AUTH
    RegisterView,
    LoginView,
    ChangePasswordView,
    LogoutView,

    # PROFILE
    ProfileView,
    ProfileListView,
    DeleteProfileView,
    RestoreProfileView,

    # DRIVER
    DriverListCreateView,
    DriverDetailView,

    # VEHICLE
    VehicleListCreateView,
    VehicleDetailView,

    # RIDES
    RideListCreateView,
    RideDetailView,
    RideStatusUpdateView,
    RideAcceptView,
    RideCancelView,
    RideFareView,
    SlowRideHistoryView,
    OptimizedRideHistoryView,
)



urlpatterns = [

    # =====================================================
    # AUTH
    # =====================================================

    path(
        "register/",
        RegisterView.as_view(),
    ),

    path(
        "login/",
        LoginView.as_view(),
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
    ),

    path(
        "logout/",
        LogoutView.as_view(),
    ),


    # =====================================================
    # PROFILE
    # =====================================================

    path(
        "profile/",
        ProfileView.as_view(),
    ),

    path(
        "profiles/",
        ProfileListView.as_view(),
    ),

    path(
        "profile/delete/",
        DeleteProfileView.as_view(),
    ),

    path(
        "profile/restore/",
        RestoreProfileView.as_view(),
    ),


    # =====================================================
    # DRIVER
    # =====================================================

    path(
        "drivers/",
        DriverListCreateView.as_view(),
    ),

    path(
        "drivers/<uuid:pk>/",
        DriverDetailView.as_view(),
    ),


    # =====================================================
    # VEHICLE
    # =====================================================

    path(
        "vehicles/",
        VehicleListCreateView.as_view(),
    ),

    path(
        "vehicles/<uuid:pk>/",
        VehicleDetailView.as_view(),
    ),


    # =====================================================
    # RIDES
    # =====================================================

    # Fare calculation
    path(
        "rides/fare/",
        RideFareView.as_view(),
        name="ride-fare",
    ),

    # Create / list rides
    path(
        "rides/",
        RideListCreateView.as_view(),
    ),

    # Ride detail
    path(
        "rides/<uuid:pk>/",
        RideDetailView.as_view(),
    ),

    # Update ride status
    path(
        "rides/<uuid:pk>/status/",
        RideStatusUpdateView.as_view(),
    ),

    # Accept ride
    path(
        "rides/<uuid:pk>/accept/",
        RideAcceptView.as_view(),
    ),

    # Cancel ride
    path(
        "rides/<uuid:pk>/cancel/",
        RideCancelView.as_view(),
        name="ride-cancel",
    ),
    path(
    "rides/slow-history/",
    SlowRideHistoryView.as_view(),
),

path(
    "rides/optimized-history/",
    OptimizedRideHistoryView.as_view(),
),
]