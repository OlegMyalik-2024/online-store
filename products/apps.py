from django.apps import AppConfig  


# Класс конфигурации приложения "products"
class ProductsConfig(AppConfig):
    # Указываем тип поля по умолчанию для моделей — BigAutoField (64-битный автоинкрементный ID)
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения — должно совпадать с названием директории приложения
    name = 'products'
    # Человекочитаемое имя приложения — отображается в админке Django
    verbose_name = 'Товары'  