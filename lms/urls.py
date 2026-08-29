from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView, SubscriptionAPIView,
)
from lms.apps import LmsConfig

app_name = LmsConfig.name

# SimpleRouter в нем уже созданы методы CRUD операций взаимосвязи с БД
router = SimpleRouter()
# маршрутизация для router
router.register("", CourseViewSet, basename="course")

# маршрутизация путей для приложения, необходимо зарегистрировать путь приложения в основном settings/urls.py
urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_get"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(),name="lessons_delete"),
    path("course/subscribe/", SubscriptionAPIView.as_view(),name="course_subscribe"),
]

urlpatterns += router.urls
