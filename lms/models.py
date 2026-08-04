from django.db import models


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

    def __str__(self):
        return f"{self.name} {self.description} {self.course}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = [
            "name",
        ]
