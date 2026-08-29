from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.models import User, Payment
from .permissions import IsProfileOwner
from .serializers import UserProfileSerializer, PaymentSerializer, UserSerializer
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    DestroyAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserListAPIView(ListAPIView):
    """Класс представления для просмотра всех пользователей."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    # Могут видеть только администраторы
    permission_classes = [IsAdminUser]


class UserCreateAPIView(CreateAPIView):
    """Класс представления для создания нового пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    # Устанавливаем класс доступа AllowAny для всех незарегистрированных пользователй
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # сохраняем пользователя и делаем его активным
        user = serializer.save(is_active=True)
        # кешируем пароль с помощью команды set_password в которой вызываем пароль пользователя
        user.set_password(user.password)
        user.save()


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """Generic-класс для просмотра и редактирования профиля любого пользователя по ID."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    # permission IsAuthenticated закроет от гостей, а IsProfileOwner запретит чужой PUT/PATCH
    permission_classes = [IsAuthenticated, IsProfileOwner]


# Класс удаления одного объекта класса User, т.к. ничего не отправляем нужен только queryset для отправки id
# для удаления
class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    # Могут удалять только администраторы
    permission_classes = [IsAdminUser]


class PaymentListAPIView(ListAPIView):
    """Класс просмотра объекта класса Payment через фильтрацию и сортировку, пример GET запроса в postman:
    http://127.0.0.1:8000/users/payments/?ordering=paid_date, в запрос можно добавить &paid_course=2 или
    &payment_method=transfer."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    #  Подключаем бэкенды для фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    #  Настраиваем фильтрацию по курсу, уроку и способу оплаты
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    #  Настраиваем сортировку по дате оплаты
    ordering_fields = ("paid_date",)
