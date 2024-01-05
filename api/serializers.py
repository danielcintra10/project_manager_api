from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_type = 'Bearer'

    def validate(self, attrs):
        data = super().validate(attrs)
        new_data_representation = {
            'user': {'id': self.user.id,
                     'first_name': self.user.first_name,
                     'last_name': self.user.last_name,
                     'email': self.user.email,
                     'mobile_phone': self.user.mobile_phone,
                     'role': self.user.get_role_display(),
                     'is_admin_user': self.user.is_superuser},
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'token_type': self.token_type
        }
        return new_data_representation
