from django.db import models
from config import settings


class Course(models.Model):
    """Класс создания модели курс"""

    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Напишите описание курса",
    )
    preview = models.ImageField(
        upload_to="lms/photos/",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Самый безопасный способ сослаться на кастомного пользователя
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = [
            "name",
        ]


class Lesson(models.Model):
    """Класс создания модели урок"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Напишите описание урока",
    )
    preview = models.ImageField(
        upload_to="lms/photos",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите картинку урока",
    )
    video_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lesson",
        help_text="Укажите курс",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} {self.description} {self.course}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = [
            "name",
        ]


class Subscription(models.Model):
    """Модель создания подписки на обновления курса для пользователя."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Пользователь',
        blank=True,
        null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscription",
        help_text="Курс",
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        # Запрещаем повторную подписку пользователя на тот же самый курс подсказал ИИ
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course_subscription')
        ]

    def __str__(self):
        return f"{self.user} - {self.course.name}"