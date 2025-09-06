# Регистрация моделей таблиц БД для их отображения в админ панели
from django.contrib import admin

#Импорт модели таблицы User из приложения users
from users.models import User

#Регистрация модели таблицы User
admin.site.register(User)