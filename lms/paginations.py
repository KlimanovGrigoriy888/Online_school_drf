from rest_framework.pagination import PageNumberPagination


class CoursePageNumberPagination(PageNumberPagination):
    """Класс пагинатор для разбития данных получения курсов на странице"""

    page_size = 5  # Количество элементов на странице
    page_size_query_param = (
        "page_size"  # Параметр запроса для указания количества элементов на странице
    )
    max_page_size = 10  # Максимальное количество элементов на странице


class LessonPageNumberPagination(PageNumberPagination):
    """Класс пагинатор для разбития данных получения уроков на страницы"""

    page_size = 10  # Количество элементов на странице
    page_size_query_param = (
        "page_size"  # Параметр запроса для указания количества элементов на странице
    )
    max_page_size = 20  # Максимальное количество элементов на странице
