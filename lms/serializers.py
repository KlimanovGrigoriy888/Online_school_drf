from dataclasses import field

from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Класс, используется для сериализации данных модели Lesson в БД"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field='video_link')] # Кастомный валидатор см. # validators.py


class CourseSerializer(serializers.ModelSerializer):
    """Класс, используется для сериализации данных модели Course в БД"""

    # Объявляем метод для подсчета количества уроков
    lesson_count = serializers.SerializerMethodField()
    # Вывод списка самих уроков через LessonSerializer, указываем many=True, так как уроков в курсе много
    lessons = LessonSerializer(source="lesson", many=True, read_only=True)


    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lesson_count", "lessons", "owner")

    def get_lesson_count(self, obj):
        """Метод для динамического подсчета уроков курса. obj — это конкретный экземпляр модели Course."""
        # 'lesson' — это related_name из ForeignKey в модели Lesson.
        # Если related_name не задан, Django по умолчанию использует 'lesson_set'.
        return obj.lesson.count()
