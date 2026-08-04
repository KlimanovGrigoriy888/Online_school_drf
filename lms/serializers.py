from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Класс, используется для сериализации данных модели Course в БД"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Класс, используется для сериализации данных модели Lesson в БД"""

    class Meta:
        model = Lesson
        fields = "__all__"
