from django.contrib import admin
from orders.models import Order, OrderItem


# Встраиваемый (inline) админ-класс для отображения и редактирования элементов заказа (OrderItem)
class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem  # Модель, для которой создается inline
    fields = "product", "name", "price", "quantity"  # Поля, отображаемые в таблице inline
    search_fields = (
        "product",  # Поле для поиска по связанному продукту (скорее всего FK)
        "name",     # Поле для поиска по имени товара
    )
    extra = 0  # Количество пустых форм для добавления новых элементов заказа по умолчанию — 0




# Отдельный админ-класс для модели OrderItem — позволяет управлять элементами заказа напрямую
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"  # Колонки, отображаемые в списке объектов
    search_fields = (
        "order",    # Поле для поиска по связанному заказу
        "product",  # Поиск по продукту
        "name",     # Поиск по имени товара
    )




# Встраиваемый (inline) админ-класс для отображения и редактирования заказов (Order)
class OrderTabulareAdmin(admin.TabularInline):
    model = Order  # Модель заказа
    fields = (
        "requires_delivery",   # Требуется ли доставка
        "status",             # Статус заказа
        "payment_on_get",     # Способ оплаты (при получении или нет)
        "is_paid",            # Оплачен ли заказ
        "created_timestamp",  # Дата и время создания заказа
    )
    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)  # Поле только для чтения — нельзя редактировать вручную
    extra = 0  # Количество пустых форм для добавления новых заказов — 0




# Основной админ-класс для модели Order — настройка отображения и поиска заказов в админке
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",                 # ID заказа
        "user",               # Пользователь, сделавший заказ
        "requires_delivery",  # Требуется ли доставка
        "status",             # Статус заказа
        "payment_on_get",     # Способ оплаты
        "is_paid",            # Оплачен ли заказ
        "created_timestamp",  # Дата и время создания заказа
    )
    search_fields = (
        "id",  # Поиск по ID заказа
    )
    readonly_fields = ("created_timestamp",)  # Дата создания только для чтения
    list_filter = (
        "requires_delivery",  # Фильтр по доставке
        "status",            # Фильтр по статусу
        "payment_on_get",    # Фильтр по способу оплаты
        "is_paid",           # Фильтр по оплате
    )
    inlines = (OrderItemTabulareAdmin,)  # Встраиваемые элементы — отображение товаров заказа внутри заказа
