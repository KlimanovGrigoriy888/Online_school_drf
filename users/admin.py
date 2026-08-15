from django.contrib import admin
from .models import User, Payment


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Пишем exclude и указываем в нем только то, что не хотим видеть в админке, т.е. остальные поля будут видны
    exclude = ("password",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Поля, для отображения в таблице админки
    list_display = (
        "id",
        "user",
        "paid_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
    )

    # Боковая панель фильтрации по заданным полям
    list_filter = ("payment_method", "paid_date", "paid_course", "paid_lesson")

    # Поля, по которым можно вести поиск
    search_fields = ("user__email", "payment_amount")
