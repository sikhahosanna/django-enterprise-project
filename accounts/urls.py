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
    DriverTotalFareEarnedView,
    DriverRideHistoryView,
    DriverLocationView,

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

    # RIDE HISTORY
    UserActiveRidesView,
    UserCompletedRidesView,
    UserCancelledRidesView,
    DailyRideCountView,
    TotalCompletedRidesView,

    # DATABASE OPTIMIZATION
    DriverRideHistoryView,
    OptimizedRideHistoryView,
    SlowRideHistoryView,
    RideAggregationView,
    NearbyDriverView,
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
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

    path(
        "driver/ride-history/",
        DriverRideHistoryView.as_view(),
        name="driver-ride-history",
    ),

    path(
        "driver/total-fare/",
        DriverTotalFareEarnedView.as_view(),
        name="driver-total-fare",
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

    # Active rides
    path(
        "rides/active/",
        UserActiveRidesView.as_view(),
        name="user-active-rides",
    ),

    # Completed rides
    path(
        "rides/completed/",
        UserCompletedRidesView.as_view(),
        name="user-completed-rides",
    ),

    # Cancelled rides
    path(
        "rides/cancelled/",
        UserCancelledRidesView.as_view(),
        name="user-cancelled-rides",
    ),

    # Daily ride count
    path(
        "rides/daily-count/",
        DailyRideCountView.as_view(),
        name="daily-ride-count",
    ),

    # Total completed rides
    path(
        "rides/total-completed/",
        TotalCompletedRidesView.as_view(),
        name="total-completed-rides",
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


    # =====================================================
    # DATABASE OPTIMIZATION
    # =====================================================

    path(
        "rides/slow-history/",
        SlowRideHistoryView.as_view(),
        name="slow-ride-history",
    ),

    path(
        "rides/optimized-history/",
        OptimizedRideHistoryView.as_view(),
        name="optimized-ride-history",
    ),
    path(
    "rides/aggregations/",
    RideAggregationView.as_view(),
    name="ride-aggregations",
),
path(
    "rides/driver/history/",
    DriverRideHistoryView.as_view(),
    name="driver-ride-history",
),
path(
    "drivers/location/",
    DriverLocationView.as_view(),
    name="driver-location",
),
path(
    "drivers/nearby/",
    NearbyDriverView.as_view(),
    name="nearby-drivers",
),
path(
    "notifications/",
    NotificationListView.as_view(),
    name="notifications",
),

path(
    "notifications/<uuid:pk>/read/",
    NotificationMarkReadView.as_view(),
    name="notification-read",
),
path(
    "notifications/read-all/",
    NotificationMarkAllReadView.as_view(),
    name="notification-read-all",
),
]