from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Lesson, Course, Subscription


class LessonTestCase(APITestCase):
    """Тестирование функционала CRUD уроков (generics)."""

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        # Создаем тестового пользователя
        self.user = User.objects.create(email="admin@test.ru", password="password123")
        # Создаем тестовый курс, на который будем подписываться
        self.course = Course.objects.create(name="Первый курс", description="Начальный курс обучения")
        self.lesson = Lesson.objects.create(name="Математика", description="Базовая математика",
                                            course=self.course, owner=self.user)
        # Авторизуем нашего тестового пользователя
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест на проверку получения одной сущности из HTTP запроса."""
        # получаем через reverse путь url для запроса просмотра одного урока, lms-название приложения,
        # lessons_get - путь в urls из нужного View
        url = reverse("lms:lessons_get", args=(self.lesson.pk,))
        # HTTP клиент для выполнения запроса по адресу url
        response = self.client.get(url)
        # извлекаем json словарь из ответа клиента
        data = response.json()
        # Проверяем, что объект успешно получили (статус 200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверяем ответ от клиента с исходными данными при создании сущности из setUp
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тест на проверку создания одной сущности из HTTP запроса."""
        # получаем через reverse путь url для запроса создания одного урока, lms-название приложения,
        # lessons_create - путь в urls из нужного View
        url = reverse("lms:lessons_create")
        # подготовка данных для создания урока, передаем обязательное поле course (берём id курса, созданного в setUp)
        data = {
            "name": "русский язык",
            "course": self.course.id,
            "description": "Базовый русский язык",
            "video_link": "https://youtube.com"  # Добавляем обязательное поле ссылка, валидную ссылка для валидатора

        }
        # HTTP клиент для выполнения запроса создания сущности по адресу url
        response = self.client.post(url, data)
        print(response.json()) # на случай проверки ответа HTTP запроса
        # Проверяем, что объект успешно создался (статус 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем количество: 1 был в setUp + 1 создали сейчас = должно быть ровно 2
        self.assertEqual(Lesson.objects.all().count(), 2)
        # проверяем, что имя созданного урока совпадает с тем, что мы отправляли
        self.assertEqual(response.json().get("name"), "русский язык")

    def test_lesson_update(self):
        """Тест на проверку изменения созданной сущности из HTTP запроса."""
        # получаем через reverse путь url для запроса изменения одного урока, lms-название приложения,
        # lessons_update - путь в urls из нужного View, в args указываем id через созданную модель
        url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        # подготовка данных для создания урока, передаем обязательное поле course (берём id курса, созданного в setUp)
        data = {
            "name": "Алгебра",
            "description": "Алгебра для начинающих",
            "video_link": "https://youtube.com"  # Добавляем обязательное поле ссылка, валидную ссылка для валидатора
        }
        # HTTP клиент для выполнения запроса обновления сущности по адресу url
        response = self.client.patch(url, data)
        # print(response.json())  # на случай проверки ответа HTTP запроса

        # Проверяем, что объект успешно обновился (статус 200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем данные из ответа СЕРВЕРА
        response_data = response.json()
        self.assertEqual(response_data.get("name"), "Алгебра")
        self.assertEqual(response_data.get("description"), "Алгебра для начинающих")

        # Проверка посоветовал ИИ : проверяем, что данные изменились прямо в БД
        self.lesson.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(self.lesson.name, "Алгебра")

    def test_lesson_delete(self):
        """Тест на проверку удаления одной сущности из HTTP запроса."""
        # получаем через reverse путь url для запроса удаления одного урока, lms-название приложения,
        # lessons_delete - путь в urls из нужного View
        url = reverse("lms:lessons_delete", args=(self.lesson.pk,))
        # HTTP клиент для выполнения запроса по адресу url
        response = self.client.delete(url)
        # Проверяем, что объект успешно удалили (статус 204_NO_CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем количество: 1 был в setUp + его удалили = должно быть ровно 0
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест на проверку получения всех сущностей из HTTP запроса."""
        # получаем через reverse путь url для запроса просмотра уроков, lms-название приложения,
        # lessons_list - путь в urls из нужного View
        url = reverse("lms:lessons_list")
        # HTTP клиент для выполнения запроса по адресу url
        response = self.client.get(url)
        # извлекаем json словарь из ответа клиента
        data = response.json()
        # создаем результат для проверки в тесте
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_link": self.lesson.video_link,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        # Проверяем, что объект успешно получили (статус 200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверяем ответ от клиента response в виде json файла с желаемым результатом result
        self.assertEqual(data, result)

        # Проверяем структуру пагинации так посоветовал ИИ посмотрев на мой тест,
        # чтобы тесты не ломались при добавлении новых мелких полей в сериализатор:
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("next"), None)
        self.assertEqual(data.get("previous"), None)

        # Проверяем, что в списке результатов лежит именно созданная сущность
        first_lesson = data.get("results")[0]
        self.assertEqual(first_lesson.get("id"), self.lesson.pk)
        self.assertEqual(first_lesson.get("name"), self.lesson.name)


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписок на курсы."""

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        # Создаем тестового пользователя
        self.user = User.objects.create(email="sub_user@test.ru", password="password123")
        # Создаем тестовый курс, на который будем подписываться
        self.course = Course.objects.create(name="Тестовый курс для подписки", description="Описание")
        # Получаем URL подписки из urls.py по его name (укажите ваше имя из urls.py)
        # Если View лежит в приложении lms, имя будет "lms:course_subscribe"
        self.url = reverse("lms:course_subscribe")


    def test_subscribe_to_course(self):
        """Тест успешного создания подписки авторизованным пользователем."""
        # Авторизуем нашего пользователя
        self.client.force_authenticate(user=self.user)
        # Передаем ID курса в POST-запрос
        data = {"course": self.course.id}
        # Делаем POST-запрос
        response = self.client.post(self.url, data=data, format="json")
        print(response.json())
        # Проверяем статус-код 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем текст сообщения с ответом сервера
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        # Проверяем, что в базе данных действительно появилась запись подписки
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_to_course(self):
        """Тест успешного удаления подписки, если она уже существовала."""
        # Авторизуем нашего пользователя
        self.client.force_authenticate(user=self.user)
        # Имитируем, что пользователь уже был подписан — принудительно создаем запись в БД подписки пользователя
        Subscription.objects.create(user=self.user, course=self.course)
        # Передаем ID курса в POST-запрос
        data = {"course": self.course.id}
        # Делаем POST-запрос
        response = self.client.post(self.url, data=data, format="json")
        print(response.json())
        # Проверяем статус-код 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем текст сообщения с ответом сервера, что подписка удалена
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        # Проверяем, что в базе данных не осталось подписок
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_anonymous_user(self):
        """Тест: на незарегистрированного пользователя получает ошибку 401 при попытке подписаться."""
        # Клиента НЕ авторизуем (симулируем анонима)
        data = {"course": self.course.id}
        response = self.client.post(self.url, data=data, format="json")
        print(response.json())

        # Ожидаем статус 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseTestCase(APITestCase):
    """Тестирование функционала CRUD для курсов (ViewSet)."""

    def setUp(self):
        self.user = User.objects.create(email="course_admin@test.ru", password="password123")
        self.client.force_authenticate(user=self.user)

        # Создаем стартовый курс
        self.course = Course.objects.create(name="Базовый Django", description="Старый курс", owner=self.user)

        # Для ViewSet urls обычно формируются как 'lms:course-list' - для create, list(просмотр) и
        # 'lms:course-detail' - для retrieve, update, delete
        self.list_url = reverse("lms:course-list")
        self.detail_url = reverse("lms:course-detail", args=(self.course.pk,))

    def test_course_create(self):
        """Тест создания курса через ViewSet."""
        data = {
            "name": "Новый курс по DRF",
            "description": "Продвинутый уровень"
        }
        response = self.client.post(self.list_url, data, format="json")

        # Проверяем, что объект успешно создался (статус 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем количество: 1 был в setUp + 1 создали сейчас = должно быть ровно 2
        self.assertEqual(Course.objects.all().count(), 2)
        # проверяем, что имя созданного курса совпадает с тем, что мы отправляли
        self.assertEqual(response.json().get("name"), "Новый курс по DRF")

    def test_course_list(self):
        """Тест получения списка курсов с учетом пагинации."""
        response = self.client.get(self.list_url)
        data = response.json()

        # Проверяем, что объект успешно получили (статус 200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем структуру пагинации
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("next"), None)
        self.assertEqual(data.get("previous"), None)
        # Проверяем, что в списке результатов лежит именно созданная сущность
        first_lesson = data.get("results")[0]
        self.assertEqual(first_lesson.get("id"), self.course.pk)
        self.assertEqual(first_lesson.get("name"), self.course.name)
        self.assertEqual(data.get("count"), 1)