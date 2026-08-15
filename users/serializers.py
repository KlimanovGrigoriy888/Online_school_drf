from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка платежей с фильтрацией для эндпоинта вывода списка платежей с возможностями:
    - менять порядок сортировки по дате оплаты
    - фильтровать по курсу или уроку
    - фильтровать по способу оплаты."""

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "paid_date",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_method",
        ]
        # ID делаем только для чтения.
        read_only_fields = [
            "id",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с историей его платежей."""

    payments_history = PaymentSerializer(source="payments", many=True, read_only=True)

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
            "payments_history",
        ]
        # ID и email делаем только для чтения.
        read_only_fields = ["id", "email"]

    # # Метод получения последнего платежа с использованием метода get_last_payment
    # # last_payment в этом случае необходимо включить в поля сериализатора user
    # last_payment = serializers.SerializerMethodField()
    #
    # def get_last_payment(self, instance):
    #     # instance — это текущий User.
    #     # ordering=['-paid_date'] в модели уже сортирует от новых к старым.
    #     # Берем самый свежий платеж пользователя:
    #     latest_payment = instance.payments.first()
    #
    #     if latest_payment:
    #         # Возвращаем информацию в виде удобного словаря
    #         return {
    #             "amount": latest_payment.payment_amount,
    #             "date": latest_payment.paid_date,
    #             "method": latest_payment.get_payment_method_display()  # Красивое название метода
    #         }
    #     return "Нет платежей"