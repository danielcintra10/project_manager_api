from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile_phone",
            "role",
            "password",
            "is_active",
            "creation_date",
            "last_update",
        )
        read_only_fields = ("id", "is_active", "creation_date", "last_update", )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        validate_password(password)
        return password

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
