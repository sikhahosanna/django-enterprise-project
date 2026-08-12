from django.urls import path


from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
    ProfileListView,
    DeleteProfileView,
    RestoreProfileView,

    DriverListCreateView,
    DriverDetailView,

    VehicleListCreateView,
    VehicleDetailView,

    RideListCreateView,
    RideDetailView,
    RideStatusUpdateView,
    RideAcceptView,
    RideCancelView,

    RideFareView,
)


urlpatterns = [

    # =========================================
    # AUTH
    # =========================================

    path(
        "register/",
        RegisterView.as_view()
    ),

    path(
        "login/",
        LoginView.as_view()
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
    ),


    # =========================================
    # PROFILE
    # =========================================

    path(
        "profile/",
        ProfileView.as_view()
    ),

    path(
        "profiles/",
        ProfileListView.as_view()
    ),

    path(
        "profile/delete/",
        DeleteProfileView.as_view()
    ),

    path(
        "profile/restore/",
        RestoreProfileView.as_view()
    ),


    # =========================================
    # DRIVER
    # =========================================

    path(
        "drivers/",
        DriverListCreateView.as_view()
    ),

    path(
        "drivers/<uuid:pk>/",
        DriverDetailView.as_view()
    ),


    # =========================================
    # VEHICLE
    # =========================================

    path(
        "vehicles/",
        VehicleListCreateView.as_view()
    ),

    path(
        "vehicles/<uuid:pk>/",
        VehicleDetailView.as_view()
    ),


    # =========================================
    # RIDES
    # =========================================

    # TASK 4 - FARE
    # =========================================
# RIDES
# =========================================

# TASK 4 - FARE
path(
    "rides/fare/",
    RideFareView.as_view(),
    name="ride-fare"
),

path(
    "rides/",
    RideListCreateView.as_view()
),

path(
    "rides/<uuid:pk>/",
    RideDetailView.as_view()
),

path(
    "rides/<uuid:pk>/status/",
    RideStatusUpdateView.as_view()
),

# TASK 6 - ACCEPT RIDE
path(
    "rides/<uuid:pk>/accept/",
    RideAcceptView.as_view()
),

# TASK 7 - CANCEL RIDE
path(
    "rides/<uuid:pk>/cancel/",
    RideCancelView.as_view(),
    name="ride-cancel"
)
]