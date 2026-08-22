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


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля пользователя и просмотра всех пользователей."""
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
            "is_staff",
            "is_superuser",
            "is_active",
            "groups"
        ]
        # ID и email делаем только для чтения.
        read_only_fields = ["id", "is_staff", "is_superuser"]


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
            "password"
        ]
        # ID и email делаем только для чтения.
        read_only_fields = ["id", "email"]

    def to_representation(self, instance):
        """Динамически скрывает конфиденциальные поля от чужих пользователей."""
        # переменной instance данные лежат в виде сложного объекта Python (экземпляра модели),
        # super().to_representation(instance) берет этот сложный объект и «переводит» (преобразует) его в обычный
        # Python-словарь {ключ: значение}
        data = super().to_representation(instance)

        # Получаем пользователя из контекста и находим там объект текущего HTTP-запроса ['request'], который делает
        # запрос к API и .user — посмотри на токен и скажи, какой именно пользователь (аккаунт) делает этот запрос
        # прямо сейчас.
        request_user = self.context['request'].user

        # Если профиль смотрит НЕ его владелец — стираем фамилию и платежи из JSON
        if instance != request_user:
            # .pop() — это стандартный метод для работы со словарями в Python, он находит в словаре ключ
            # (в данном случае 'last_name') и удаляет (стирает) его вместе со значением, None если ничего нет в словаре
            data.pop('last_name', None)
            data.pop('password', None)
            data.pop('payments_history', None)

        return data

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