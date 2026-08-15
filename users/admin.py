from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Пишем exclude и указываем в нем только то, что не хотим видеть в админке, т.е. остальные поля будут видны
    exclude = ('password',)
