from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_about_subscription(email):# email пользователя подписавшегося на рассылку курсов
    """Функция отправки сообщения пользователю об обновлении курса чрез функционал Celery отложенные задачи,
     для работы Celery на Windows так же необходимо установить eventlet, команда для запуска
     celery -A config worker -l INFO -P eventlet"""
    send_mail("Курс обновился!",
              "Ваши подписанные курсы обновились",
              EMAIL_HOST_USER,
              [email]
    )