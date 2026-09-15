from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def blocked_inactive_users():
    """Функция используется проверки активности пользователей в течении 1 месяца,
     необходимо запустить две команды для запуска:
    первая команда - celery -A config worker -l INFO -P eventlet,
    вторая команда - celery -A config beat --scheduler django -l INFO."""

    # Получаем дату 30 дней назад, как точку отсчета от текущей даты
    data_one_month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей которые не логинились более 30 дней назад
    inactive_users = User.objects.filter(
        is_active=True,
        # Получаем время последнего логирования пользователя при условии если логирование было месяц назад
        last_login__lt=data_one_month_ago,
    )
    # Считаем неактивных пользователей
    count = inactive_users.count()

    if count > 0:
        # У всех не активных пользователей обновляем флаг is_active в False (блокируем) за 1 запрос к базе
        inactive_users.update(is_active=False)
        print(f"Celery Beat: Успешно заблокировано {count} неактивных пользователей.")
    else:
        print("Celery Beat: Неактивных пользователей для блокировки не найдено.")

    return f"Проверка завершена. Заблокировано: {count}"
