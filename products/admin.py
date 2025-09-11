from django.contrib import admin
from products.models import Categories, Products


# Регистрация модели Categories в админке
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # Автоматическое заполнение поля slug на основе name
    prepopulated_fields = {"slug": ("name",)}
    # Отображаемые поля в списке категорий
    list_display = ["name"]



# Регистрация модели Products в админке
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # Автоматическое заполнение поля slug на основе name
    prepopulated_fields = {"slug": ("name",)}
    # Отображаемые поля в списке товаров
    list_display = ["name", "quantity", "price", "discount"]
    # Поля, доступные для редактирования прямо в списке
    list_editable = ["discount"]
    # Поля, по которым можно выполнять поиск
    search_fields = ["name", "description"]
    # Фильтры в правой панели админки
    list_filter = ["discount", "quantity", "category"]
    # Поля, отображаемые в форме редактирования товара
    fields = [
        "name",               # Название товара
        "category",           # Категория
        "slug",               # URL-идентификатор
        "description",        # Описание
        "image",              # Изображение
        ("price", "discount"),# Цена и скидка — в одной строке
        "quantity",           # Количество на складе
    ]