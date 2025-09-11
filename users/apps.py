from django.apps import AppConfig



# Определение конфигурации приложения 'users'
class UsersConfig(AppConfig):
    # Установка типа авто-поля по умолчанию для первичных ключей в моделях
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения (должно соответствовать названию папки приложения)
    name = 'users'
    # Человеко-читаемое название приложения для отображения в админке Django
    verbose_name = 'Пользователи'
