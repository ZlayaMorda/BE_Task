from rest_framework import permissions


class IsUserRole:
    @staticmethod
    def _is_user_role(request, user_role):
        return request.user.is_staff or request.user.role == user_role


class IsAdmin(permissions.BasePermission, IsUserRole):

    def has_permission(self, request, view):
        return self._is_user_role(request, request.user.Roles.ADMIN.value)

    def has_object_permission(self, request, view, obj):
        return self._is_user_role(request, request.user.Roles.ADMIN.value)


class IsModerator(permissions.BasePermission, IsUserRole):

    def has_permission(self, request, view):
        return self._is_user_role(request, request.user.Roles.MODERATOR.value)

    def has_object_permission(self, request, view, obj):
        return self._is_user_role(request, request.user.Roles.MODERATOR.value)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_blocked
