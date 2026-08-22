from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    # Способы оплаты из задания
    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = [(CASH, "Наличные"), (TRANSFER, "Перевод на счет")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
        help_text="Укажите пользователя",
    )
    paid_date = models.DateTimeField(
        verbose_name="Дата оплаты",
        help_text="Укажите дату и время оплаты",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
        help_text="Напишите оплаченный курс, если применим",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
        help_text="Напишите оплаченный урок, если применим",
    )
    payment_amount = models.IntegerField(
        default=0,
        verbose_name="Сумма оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=TRANSFER,
        verbose_name="Способ оплаты",
        help_text="Укажите способ оплаты (наличные или перевод)",
    )

    def __str__(self):
        # Отображаем, за что именно был платеж
        item = self.paid_course if self.paid_course else self.paid_lesson
        return f"{self.user} - {item}: {self.payment_amount} руб. ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-paid_date"]
