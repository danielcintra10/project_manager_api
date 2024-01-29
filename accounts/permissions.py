from rest_framework import permissions


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated is not True:
            return False
        return request.user.is_project_manager()


class IsAuthenticatedAndIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user.email == obj.email
