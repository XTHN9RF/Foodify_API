from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsReadOnly(permissions.BasePermission):
    """Custom permission to only allow read-only access to an object."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
