from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для удаления всех пользователей"""

    def handle(self, *args, **options):
        User.objects.filter(is_superuser=False).delete()
