from users.models import User
from .serializers import UserProfileSerializer
from rest_framework.generics import RetrieveUpdateAPIView

class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """Generic-класс для просмотра и редактирования профиля любого пользователя по ID."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer