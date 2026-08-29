from dataclasses import field

from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
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
    # Объявляем метод для выборки информации подписании текущего пользователя на курс или нет
    user_subscribes = serializers.SerializerMethodField()
    # Вывод списка самих уроков через LessonSerializer, указываем many=True, так как уроков в курсе много
    lessons = LessonSerializer(source="lesson", many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lesson_count", "lessons", "user_subscribes", "owner")

    def get_lesson_count(self, obj):
        """Метод для динамического подсчета уроков курса. obj — это конкретный экземпляр модели Course."""
        # 'lesson' — это related_name из ForeignKey в модели Lesson.
        # Если related_name не задан, Django по умолчанию использует 'lesson_set'.
        return obj.lesson.count()

    def get_user_subscribes(self, obj):
        """ Метод для получения данных, подписан ли текущий пользователь на данный курс.
        obj — это текущий объект курса (Course).
        """

        # Достаем объект запроса (request) из контекста сериализатора. self.context — это внутренний мессенджер
        # между View и Serializer,
        request = self.context.get('request')

        # Если запроса нет (например, сериализатор вызван в тестах без контекста)
        # или пользователь не авторизован (анонимный), возвращаем False
        if not request or not request.user or request.user.is_anonymous:
            return False

        # Проверяем в базе данных, существует ли подписка этого юзера на этот курс
        # Метод .exists() вернет True, если запись есть, и False, если её нет.
        return Subscription.objects.filter(user=request.user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Класс, используется для сериализации данных модели Subscription в БД"""

    class Meta:
        model = Subscription
        fields = ["course"] # Передаем только ID курса