from django.contrib import admin
# Импортируем Categories, Products и вашу новую модель изображений ProductImages
from products.models import Categories, Products, ProductImages


# Регистрация модели Categories в админке
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # Автоматическое заполнение поля slug на основе name
    prepopulated_fields = {"slug": ("name",)}
    # Отображаемые поля в списке категорий
    list_display = ["name"]


# Настройка встроенного блока (Inline) для загрузки дополнительных картинок товара
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 3  # Количество пустых строк для загрузки фото по умолчанию
    verbose_name = "Дополнительное изображение"
    verbose_name_plural = "Дополнительная галерея изображений"


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
        "image",              # Главное изображение товара
        ("price", "discount"),# Цена и скидка — в одной строке
        "quantity",           # Количество на складе
    ]
    
    # Подключаем галерею картинок. Блок появится в самом низу формы редактирования товара
    inlines = [ProductImagesInline]
