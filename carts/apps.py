from django.apps import AppConfig



# Класс конфигурации приложения "carts", наследуется от AppConfig для настройки параметров приложения
class CartsConfig(AppConfig):
    # Установка типа поля автоинкремента по умолчанию для моделей в этом приложении
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения (должно совпадать с именем папки приложения)
    name = 'carts'
    # Человеко-читаемое название приложения, отображаемое в админ-панели Django
    verbose_name = 'Корзины'
