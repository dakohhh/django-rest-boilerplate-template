from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from user.serializers import UserPublicSerializers
from rest_framework.permissions import IsAuthenticated
from common.response import CustomResponse as Response
from .serializers import CustomTokenObtainPairSerializer, RequestTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from common.exceptions import BadRequestException


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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
