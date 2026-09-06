from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс доступа, проверяет, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):
    """Класс доступа, проверяет, является ли пользователь владельцем 'IsOwner'."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
