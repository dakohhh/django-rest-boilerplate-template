from rest_framework import serializers


class UserPublicSerializers(serializers.Serializer):
    user_id = serializers.CharField(source='pk', read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
