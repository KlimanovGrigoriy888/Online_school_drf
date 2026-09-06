from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Поля, для отображения в таблице админки
    list_display = (
        "id",
        "name",
        "description",
        "owner",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # Поля, для отображения в таблице админки
    list_display = (
        "id",
        "name",
        "description",
        "course",
        "owner",
    )
