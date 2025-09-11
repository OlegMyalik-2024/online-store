from django.contrib import admin
from carts.admin import CartTabAdmin 
from orders.admin import OrderTabulareAdmin  
from users.models import User  




# Регистрация моделей таблиц в админке
@admin.register(User)  # Декоратор для автоматической регистрации модели User в админке
class UserAdmin(admin.ModelAdmin):
    # Список полей, отображаемых в списке объектов в админке
    list_display = ['username', 'first_name', 'last_name', 'email']
    # Поля, по которым можно выполнять поиск в админке
    search_fields = ['username', 'first_name', 'last_name', 'email']
    # Встроенные (inline) админ-классы для отображения связанных объектов (корзина и заказы) на странице пользователя
    inlines = [CartTabAdmin, OrderTabulareAdmin]
