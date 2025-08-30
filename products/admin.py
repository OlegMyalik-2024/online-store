# Регистрация моделей таблиц БД для их отображения в админ панели
from django.contrib import admin

# Импорт моделей таблиц из приложений
from products.models import Categories, Products

# Регистрация моделей таблиц в админке
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}