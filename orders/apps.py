from django.apps import AppConfig



# Конфигурация приложения "orders"
class OrdersConfig(AppConfig):
    # Указываем тип поля по умолчанию для моделей — BigAutoField (64-битный автоинкрементный ID)
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения, должно совпадать с именем директории (важно для Django)
    name = 'orders'
    # Человекочитаемое имя приложения, отображается в админке
    verbose_name = 'Заказы'