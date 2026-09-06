from itertools import product

from django.utils import timezone
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

from users.services import create_stripe_product, create_stripe_price, create_stripe_session


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


class PaymentCreateAPIView(CreateAPIView):
    """Класс создания оплаты за курс через ресурс stripe.com."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated] # Ссылка доступна только для авторизованных пользователей

    def perform_create(self, serializer):
        """Переопределяем логику сохранения платежа, добавляя интеграцию со Stripe."""
        # Подставляем текущего пользователя и текущее время оплаты
        # (Пользователю не нужно передавать эти поля в POST-запросе)
        payment = serializer.save(user=self.request.user, paid_date=timezone.now())

        # Определяем, за что именно платит пользователь (курс или урок)
        # Извлекаем объект курса или урока из только что созданной записи платежа
        purchased_item = payment.paid_course if payment.paid_course else payment.paid_lesson

        if purchased_item:
            # Запускаем последовательную цепочку сервисных функций Stripe если платеж существует:

            # Создаем продукт в Stripe (передаем id, имя и описание), получаем id продукта Stripe
            stripe_product_id = create_stripe_product(
                id_product=purchased_item.id,
                name=purchased_item.name,
                description=getattr(purchased_item, 'description', 'Оплата обучения')
            )

            # Создаем цену в Stripe для этого продукта (передаем id созданного продукта Stripe, сумму и имя), получаем
            # id созданного платежа
            stripe_price_id = create_stripe_price(
                product_id=stripe_product_id,
                amount=payment.payment_amount,
                product_name=purchased_item.name
            )

            # Создаем сессию оплаты в Stripe, передавая объект цены (или словарь с id)
            # Так как ваша функция ожидает price.get("id"), мы можем упаковать строку в словарь
            stripe_session_id, stripe_payment_url = create_stripe_session(price_id=stripe_price_id)

            # Сохраняем полученные от Stripe данные обратно в нашу модель платежа Django
            payment.session_id = stripe_session_id
            payment.payment_link = stripe_payment_url
            payment.save()
