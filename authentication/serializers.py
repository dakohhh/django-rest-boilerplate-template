from rest_framework import serializers
from common.exceptions import BadRequestException
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("incorrect email or password")}

    @classmethod
    def get_token(cls, user):
        # Custom validation to ensure the user is verified before issuing a token
        if not user.is_verified:
            raise BadRequestException("User is not verified")

        # Return the token if the user is verified
        return super().get_token(user)


class RequestTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value: str):
        try:
            refresh_token = RefreshToken(value)  # noqa: F841
            return value
        except TokenError:
            raise serializers.ValidationError(
                "invalid or expired token"
            )  # This token can also be blacklisted, but for security reasons, we would not describe further
