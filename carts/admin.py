from django.contrib import admin
from carts.models import Cart




# Класс для встроенной (inline) формы в админ-панели, использует TabularInline для отображения корзины в табличном виде
class CartTabAdmin(admin.TabularInline):
    # Указываем модель, с которой работает этот inline
    model = Cart
    # Поля, отображаемые в inline-форме
    fields = "product", "quantity", "created_timestamp"
    # Поля, по которым можно искать в inline
    search_fields = "product", "quantity", "created_timestamp"
    # Поля, доступные только для чтения (нельзя редактировать)
    readonly_fields = ("created_timestamp",)
    # Количество дополнительных пустых форм для добавления новых записей
    extra = 1




# Регистрация модели Cart в админ-панели с кастомными настройками
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке объектов в админ-панели
    list_display = ["user_display", "product_display", "quantity", "created_timestamp"]
    # Фильтры для списка объектов
    list_filter = ["created_timestamp", "user", "product__name"]

    # Метод для отображения пользователя (возвращает строку пользователя или "Анонимный пользователь" если нет)
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    # Метод для отображения названия товара
    def product_display(self, obj):
        return str(obj.product.name)

    # Установка описания для столбцов в админ-панели (для улучшения читаемости)
    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"