from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from lms.models import Course, Lesson, Subscription
from lms.paginations import CoursePageNumberPagination, LessonPageNumberPagination
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Модель класса ModelViewSet организующая CRUD операции с курсами."""

    # Использовали prefetch_related, чтобы уроки для всех курсов подгрузились за 1 дополнительный запрос.
    queryset = Course.objects.prefetch_related("lesson").all()
    serializer_class = CourseSerializer
    # Подключаем пагинацию для курсов
    pagination_class = CoursePageNumberPagination

    def perform_create(self, serializer):
        """Метод привязки владельца к создателю курса."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Метод динамически определяет права доступа для каждого действия."""

        # Для создания — запрещаем доступ модераторам
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]

        # Для просмотра одного курса и редактирования — разрешаем модераторам или владельцам
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        # Для удаления одного курса — разрешаем владельцу, но блокируем модератора
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]

        return super().get_permissions()



# Класс создания объекта класса Lesson, т.к. из БД ничего не получаем нужен только сериализатор.
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # Могут создавать только зарегистрированные пользователи и не модераторы
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Метод привязки владельца к создателю курса."""
        new_course = serializer.save(owner=self.request.user)


# Класс чтения все объектов класса Lesson
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Подключаем пагинацию для уроков
    pagination_class = LessonPageNumberPagination
    # Могут просматривать только модераторы и владельцы
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


# Класс чтения одного объекта класса Lesson
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Могут просматривать один объект только зарегистрированные пользователи и модераторы или владельцы
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


# Класс обновления одного объекта класса Lesson, поддерживает команду PUT и PATH
class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Могут обновлять объект только зарегистрированные пользователи и модераторы или владельцы
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


# Класс удаления одного объекта класса Lesson, т.к. ничего не отправляем нужен только queryset для отправки id
# для удаления
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # Могут удалять объект только зарегистрированные пользователи и не модераторы или владельцы
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscriptionAPIView(APIView):
    """APIView - эндпойнт-переключатель для установки и удаления подписки пользователя на курс, работает только
    на POST запросе."""
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        # Получаем пользователя из request из БД, после проверки его через токен т.е. после авторизации
        user = self.request.user
        # Получаем id курса из request.data, то что отправил пользователь через POST при создании курса {'course': 5}
        course_id = self.request.data.get('course')
        # Получаем объект курса из базы данных с помощью get_object_or_404
        course_item = get_object_or_404(Course, id=course_id)
        # Получаем объекты подписок по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(user=user, course=course_item)


        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})