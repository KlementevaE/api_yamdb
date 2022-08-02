from rest_framework import permissions
from users.models import MODERATOR, ADMIN


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN or request.user.is_staff)


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == ADMIN
                or request.user.role == MODERATOR
                or obj.author == request.user)


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == ADMIN):
            return True
        return False
