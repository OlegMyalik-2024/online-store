from django.db import models
from django.contrib.auth.models import AbstractUser



# Создание модели User, наследующей от AbstractUser, для добавления дополнительных полей
class User(AbstractUser):
    # Поле для загрузки изображения аватарки пользователя (опциональное)
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    # Поле для хранения номера телефона пользователя (опциональное, максимум 10 символов)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Внутренний класс Meta для настройки поведения модели в базе данных и админке
    class Meta:
        # Указание имени таблицы в базе данных
        db_table = 'user'
        # Отображение названия модели в админке в единственном числе
        verbose_name = 'Пользователя'
        # Отображение названия модели в админке во множественном числе
        verbose_name_plural = 'Пользователи'
        
    # Метод для строкового представления объекта модели (возвращает username)
    def __str__(self):
        return self.username