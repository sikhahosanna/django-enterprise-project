from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ProfileSerializer
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer



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



class ProfileView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


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


        serializer = ProfileSerializer(profile)

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


        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class ProfileListView(generics.ListAPIView):

    queryset = Profile.objects.all()

    serializer_class = ProfileSerializer


    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]


    # Search
    search_fields = [
        "first_name",
        "last_name",
        "phone",
    ]


    # Ordering
    ordering_fields = [
        "first_name",
        "last_name",
    ]


    # Filtering
    filterset_fields = [
        "first_name",
        "last_name",
    ]



class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]


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



class LogoutView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        try:

            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)

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