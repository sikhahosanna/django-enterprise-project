from django.urls import path

from .views import (
    DeleteProfileView,
    RegisterView,
  
    LoginView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
    ProfileListView,
    RestoreProfileView,
    
)


urlpatterns = [

    path("register/", RegisterView.as_view()),

    path("login/", LoginView.as_view()),

    path("profile/", ProfileView.as_view()),

    path(
        "change-password/",
        ChangePasswordView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
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

]