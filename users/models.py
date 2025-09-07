# Создание моделей таблиц БД
from django.db import models
from django.contrib.auth.models import AbstractUser

#Добавление к стандартной таблице django user_auth поля image(изображение аватарки)
class User(AbstractUser):
    image=models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    #Класс для настройки таблицы
    class Meta:
        db_table='user' # Отображение таблицы в БД
        verbose_name='Пользователя' # Отображение таблицы в админке в единственном числе
        verbose_name_plural='Пользователи' # Отображение таблицы в админке в множественном числе
        
    def __str__(self):
        return self.username