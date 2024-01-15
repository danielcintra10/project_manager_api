from django.contrib.auth import get_user_model
from rest_framework import permissions


User = get_user_model()


class IsRequestedDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        developer_id = view.kwargs['developer_id']
        developer = User.objects.filter(id=developer_id).first()
        return developer == request.user


class IsTaskDeveloper(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.developer == request.user
