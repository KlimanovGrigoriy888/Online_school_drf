from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class UserTestCase(APITestCase):
    """Тестирование CRUD управления пользователями."""

    def test_user_registration(self):
        """Тест создания (регистрации) пользователя через CreateAPIView."""
        # Указываем путь для регистрации users - имя приложения, register - имя пути в urls для нужного view
        url = reverse("users:register")
        # Данные для создания пользователя через запрос client
        data = {"email": "new_student@test.ru", "password": "password123"}
        # Делаем POST-запрос
        response = self.client.post(url, data, format="json")
        # print(response.json()) # Для проверки ответа от HTTP запроса
        # Проверяем статус-код 201 CREATE
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что пользователь появился в базе данных
        self.assertTrue(User.objects.filter(email="new_student@test.ru").exists())

    def test_user_list_by_admin(self):
        """Тест: администратор успешно получает список пользователей."""
        # Создаем пользователя-администратора (is_staff=True)
        admin_user = User.objects.create(
            email="admin_staff@test.ru",
            password="password123",
            is_staff=True
        )
        # Авторизуем админа в клиенте
        self.client.force_authenticate(user=admin_user)
        # Делаем GET-запрос на ваш url (укажите правильное имя из urls.py)
        url = reverse("users:users")
        response = self.client.get(url)
        # Ожидаем статус 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_by_not_admin(self):
        """Тест: обычный пользователь получает ошибку 403 при попытке просмотреть список."""
        # Создаем обычного пользователя (не админа, is_staff=False)
        normal_user = User.objects.create(
            email="student@test.ru",
            password="password123"
        )
        # Авторизуем обычного пользователя
        self.client.force_authenticate(user=normal_user)
        # Делаем запрос
        url = reverse("users:users")
        response = self.client.get(url)
        # Ожидаем статус 403 Forbidden, так как сработал IsAdminUser
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserAndPaymentTestCase(APITestCase):
    """Комплексное тестирование профилей, удаления пользователей и платежей."""

    def setUp(self):
        """Подготовка данных: создаем обычного пользователя и администратора."""
        # Создаем обычного пользователя
        self.user = User.objects.create(email="student_profile@test.ru", password="password123")

        # Создаем администратора (is_staff=True)
        self.admin_user = User.objects.create(email="admin_profile@test.ru", password="password123", is_staff=True)

    def test_profile_update_by_owner(self):
        """Тест: пользователь может успешно обновить СВОЙ профиль."""
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # Берем name в users/urls.py ('user-profile')
        url = reverse("users:user-profile", args=(self.user.pk,))

        # Меняем поле first_name
        data = {"first_name": "Григорий"}
        response = self.client.patch(url, data, format="json")

        # Проверяем, что сервер ответил 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе пришло обновленное имя
        self.assertEqual(response.json().get("first_name"), "Григорий")

    def test_profile_update_by_not_owner(self):
        """Тест: пользователь НЕ может обновить ЧУЖОЙ профиль (IsProfileOwner)."""
        # Создаем чужого пользователя, но без предварительной авторизации
        stranger_user = User.objects.create(email="stranger@test.ru", password="password123")

        # Авторизуем нашего основного пользователя из setUp
        self.client.force_authenticate(user=self.user)

        # Берем name в users/urls.py ('user-profile')
        url = reverse("users:user-profile", args=(stranger_user.pk,))
        # Делаем запрос на обновление пользователя с новым именем пользователя
        data = {"first_name": "Георгий"}
        response = self.client.patch(url, data, format="json")
        # print(response.json()) # для проверки ответа HTTP запроса

        # Ожидаем 403 Forbidden, так как сработал кастомный IsProfileOwner
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_by_admin(self):
        """Тест: администратор может успешно удалить пользователя."""
        # Делаем авторизацию пользователя
        self.client.force_authenticate(user=self.admin_user)

        #  Берем name в users/urls.py ('user-delete')
        url = reverse("users:user-delete", args=(self.user.pk,))
        # Делаем запрос на удаление пользователя
        response = self.client.delete(url)
        # Проверяем, что сервер ответил 204 NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что пользователь с таким pk не существует или удален
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_payment_list_with_ordering(self):
        """Тест: получение списка платежей и проверка работы сортировки."""
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый платеж в базе данных для пользователя self.user
        Payment.objects.create(
            user=self.user,
            payment_amount=1000,
            payment_method="transfer",  # Указываем значение "cash" или "transfer" для способа оплаты т.к. поле choices
            paid_date=timezone.now()
        )
        # Берем name в users/urls.py ('payment_list') используя + можем добавить в запрос например "&paid_course=2",
        # "&payment_method=transfer" или "?ordering=paid_date"
        url = reverse("users:payment_list") + "?ordering=paid_date"
        # Делаем запрос получение payments для аутентифицированного пользователя
        response = self.client.get(url)
        # Проверяем, что сервер ответил 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Извлекаем данные (так как пагинации нет, data — это сразу список/list)
        data = response.json()
        print(data)
        # Проверяем, что это действительно список и в нём есть как минимум один элемент
        self.assertTrue(len(data) >= 1)
