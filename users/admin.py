# Регистрация моделей таблиц БД для их отображения в админ панели
from django.contrib import admin

# Импорт моделей таблиц из приложений
from carts.admin import CartTabAdmin
from users.models import User

# Регистрация моделей таблиц в админке
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username', 'first_name', 'last_name', 'email']
    search_fields=['username', 'first_name', 'last_name', 'email']
    inlines=[CartTabAdmin]