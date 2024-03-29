from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers import UserSerializer, MyTokenObtainPairSerializer
from .permissions import IsAuthenticatedAndIsOwner, IsProjectManager

User = get_user_model()

# Create your views here.


class ListCreateUser(ListCreateAPIView):
    queryset = User.objects.filter(
        is_active=True,
        deleted=False,
        is_superuser=False,
    )
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                IsProjectManager | permissions.IsAdminUser,
            ]
        elif self.request.method == "POST":
            self.permission_classes = [
                permissions.AllowAny,
            ]
        else:
            self.permission_classes = [
                permissions.IsAdminUser,
            ]
        return super().get_permissions()

    @method_decorator(cache_page(60 * 30, key_prefix="user"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RetrieveUpdateDestroyUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(
        is_active=True,
        deleted=False,
        is_superuser=False,
    )
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                permissions.IsAdminUser
                | IsAuthenticatedAndIsOwner
                | IsProjectManager,
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [
                permissions.IsAdminUser | IsAuthenticatedAndIsOwner,
            ]
        else:
            self.permission_classes = [
                permissions.IsAdminUser,
            ]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.is_active = False
        instance.save()
        return Response(
            {"Response": "User was successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ListProjectManagerUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(
        is_active=True, deleted=False, is_superuser=False, role="P"
    )
    permission_classes = [permissions.IsAdminUser | IsProjectManager]

    @method_decorator(cache_page(60 * 30, key_prefix="user"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ListDeveloperUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(
        is_active=True, deleted=False, is_superuser=False, role="D"
    )
    permission_classes = [permissions.IsAdminUser | IsProjectManager]

    @method_decorator(cache_page(60 * 30, key_prefix="user"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
