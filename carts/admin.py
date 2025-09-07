from django.contrib import admin

# Импорт моделей таблиц из приложений
from carts.models import Cart

#Отображение корзины пользователя в админке
class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "quantity", "created_timestamp"
    search_fields = "product", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1
    
# Регистрация моделей таблиц в админке
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user', 'product__name', 'quantity', 'created_timestamp']
    list_filter=['created_timestamp', 'user', 'product__name']