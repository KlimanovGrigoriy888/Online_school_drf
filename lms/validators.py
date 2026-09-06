import re
from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    """Валидатор проверки обязательного наличия ссылки youtube.com"""

    # Выносим паттерн на уровень класса, чтобы он компилировался один раз, проверяет наличие названия youtube.com
    reg = re.compile(
        r"^(?:https?://)?(?:www\.|m\.)?youtube\.com(?:/.*)?$", re.IGNORECASE
    )

    def __init__(self, field: str):
        self.field = field

    def __call__(self, data):
        video_url = data.get(self.field)

        # Проверяем, что поле вообще заполнено и является строкой.
        if not video_url or not isinstance(video_url, str):
            raise ValidationError(f"Field '{self.field}' is missing or empty.")

        # Проверяем строку на соответствие регулярному выражению
        # т.е. если есть совпадение по компилированному выражению и выведет True иначе Validation error
        if not self.reg.match(video_url):
            raise ValidationError({self.field: "Video link must include youtube.com"})
