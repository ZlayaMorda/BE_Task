from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    @staticmethod
    def _is_admin(request):
        return request.user.is_staff or request.user.role == request.user.Roles.ADMIN.value

    def has_permission(self, request, view):
        return self._is_admin(request)

    def has_object_permission(self, request, view, obj):
        return self._is_admin(request)
