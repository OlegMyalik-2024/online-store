from django.contrib import admin

from carts.models import Cart

# Регистрация моделей таблиц в админке
admin.site.register(Cart)
