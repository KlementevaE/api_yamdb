from rest_framework import permissions

ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ROLE_ADMIN
                     or request.user.is_staff))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == ROLE_ADMIN
                or request.user.role == ROLE_MODERATOR
                or obj.author == request.user)


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == ROLE_ADMIN)
