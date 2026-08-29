from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwner(BasePermission):
    """Разрешает просмотр всем, но редактирование — только владельцу профиля."""

    def has_object_permission(self, request, view, obj):
        # Если это безопасный запрос (GET, HEAD, OPTIONS) — разрешаем всем авторизованным пользователям
        if request.method in SAFE_METHODS:
            return True

        # Если пытаются изменить профиль (PUT, PATCH) — проверяем, хозяин ли это
        return obj == request.user
