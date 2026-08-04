from rest_framework.serializers import ModelSerializer
from users.models import User


class UserProfileSerializer(ModelSerializer):
    """Сериализатор для редактирования личных данных пользователя."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
        ]
        # ID и email делаем только для чтения.
        read_only_fields = ["id",]