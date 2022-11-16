from rest_framework import permissions


class IsPageFollower(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.followers


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.is_blocked)
        return not obj.is_blocked
