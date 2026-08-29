from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    UserProfileUpdateAPIView,
    PaymentListAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

# маршрутизация путей для приложения, необходимо зарегистрировать путь приложения в основном settings/urls.py
urlpatterns = [
    # путь просмотра всех зарегистрированных пользователей
    path("users/", UserListAPIView.as_view(), name="users"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    # <int:pk> — это ID пользователя, профиль которого мы хотим посмотреть или изменить
    path("users/<int:pk>/", UserProfileUpdateAPIView.as_view(), name="user-profile"),
    # путь для удаления пользователя по его id
    path("users/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    # путь для просмотра пользователя
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    # пути для получения токенов авторизации, получаем путем ввода email и пароля в запросе по этому пути для не
    # авторизованных пользователей, далее токен используем в запросах путей требующих авторизации в теле запроса Headers
    # выбираем Authorization и пишем Bearer и добавляем токен
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
