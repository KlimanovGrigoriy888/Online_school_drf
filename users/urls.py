from django.urls import path

from users.apps import UsersConfig
from users.views import UserProfileUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

# маршрутизация путей для приложения, необходимо зарегистрировать путь приложения в основном settings/urls.py
urlpatterns = [
    # <int:pk> — это ID пользователя, профиль которого мы хотим посмотреть или изменить
    path("users/<int:pk>/", UserProfileUpdateAPIView.as_view(), name="user-profile"),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
