from django.apps import AppConfig



# Определение класса конфигурации для приложения 'main'
class MainConfig(AppConfig):
    # Установка типа авто-поля по умолчанию для моделей в приложении (BigAutoField для больших целых чисел)
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения, соответствующее его папке в проекте
    name = 'main'
