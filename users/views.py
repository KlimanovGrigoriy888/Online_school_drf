from users.models import User, Payment
from .serializers import UserProfileSerializer, PaymentSerializer
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """Generic-класс для просмотра и редактирования профиля любого пользователя по ID."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class PaymentListAPIView(ListAPIView):
    """Класс просмотра объекта класса Payment через фильтрацию и сортировку, пример GET запроса в postman:
    http://127.0.0.1:8000/users/payments/?ordering=paid_date, в запрос можно добавить &paid_course=2 или
    &payment_method=transfer"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    #  Подключаем бэкенды для фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    #  Настраиваем фильтрацию по курсу, уроку и способу оплаты
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    #  Настраиваем сортировку по дате оплаты
    ordering_fields = ("paid_date",)
