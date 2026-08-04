from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Модель класса ModelViewSet организующая CRUD операции."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Класс создания объекта класса Lesson, т.к. из БД ничего не получаем нужен только сериализатор.
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


# Класс чтения все объектов класса Lesson
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


# Класс чтения одного объекта класса Lesson
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


# Класс обновления одного объекта класса Lesson, поддерживает команду PUT и PATH
class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


# Класс удаления одного объекта класса Lesson, т.к. ничего не отправляем нужен только queryset для отправки id
# для удаления
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
