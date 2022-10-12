from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    @staticmethod
    def _is_admin(request):
        return request.user.is_staff or request.user.role == request.user.Roles.ADMIN.value

    def has_permission(self, request, view):
        return self._is_admin(request)

    def has_object_permission(self, request, view, obj):
        return self._is_admin(request)


class IsModerator(permissions.BasePermission):
    @staticmethod
    def _is_moderator(request):
        return request.user.role == request.user.Roles.MODERATOR.value

    def has_permission(self, request, view):
        return self._is_moderator(request)

    def has_object_permission(self, request, view, obj):
        return self._is_moderator(request)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_blocked
