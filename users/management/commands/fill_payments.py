from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Заполнение базы данных тестовыми платежами"

    def handle(self, *args, **options):
        # Очищаем старые платежи, чтобы не дублировать при повторном запуске
        Payment.objects.all().delete()

        # Находим тестовые объекты из существующих в БД
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(
                self.style.ERROR("Сначала создайте хотя бы одного пользователя!")
            )
            return

        # Создаем платеж за курс
        if course:
            Payment.objects.create(
                user=user,
                paid_date="2025-08-09",
                paid_course=course,
                payment_amount=25000,
                payment_method=Payment.TRANSFER,
            )

        # Создаем платеж за отдельный урок
        if lesson:
            Payment.objects.create(
                user=user,
                paid_date="2026-08-09",
                paid_lesson=lesson,
                payment_amount=1200,
                payment_method=Payment.CASH,
            )

        self.stdout.write(self.style.SUCCESS("Тестовые платежи успешно созданы!"))
