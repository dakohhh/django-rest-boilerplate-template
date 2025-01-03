from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from common.exceptions import BadRequestException
from user.serializers import UserSerializer, UserPublicSerializers
from common.response import CustomResponse as Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomTokenObtainPairSerializer, RequestTokenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):

        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        # TODO: Setup mail for registration email sending

        # TODO: Setup aws for image upload


        return Response("Signup Successfully", serializer.data)


class SessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        serializer_class = UserPublicSerializers(request.user)

        return Response("Get session info for user", serializer_class.data)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):

        refresh_token_serializer = RequestTokenSerializer(data=request.data)

        # Validate the input
        if not refresh_token_serializer.is_valid():
            raise BadRequestException(refresh_token_serializer.errors)

        refresh_token = RefreshToken(refresh_token_serializer.validated_data["refresh"])

        refresh_token.blacklist()

        return Response("Logout Successfully", status_code=status.HTTP_205_RESET_CONTENT)
