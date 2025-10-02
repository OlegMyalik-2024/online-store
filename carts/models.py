# Импорт модулей для работы с моделями Django
from django.db import models
from products.models import Products
from users.models import User



# Кастомный QuerySet для модели Cart, расширяющий стандартный QuerySet дополнительными методами
class CartQueryset(models.QuerySet):
    
    # Метод для расчета общей цены всех товаров в QuerySet
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    # Метод для расчета общего количества товаров в QuerySet (возвращает 0, если QuerySet пустой)
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    

# Модель Cart для представления корзины покупок в базе данных
class Cart(models.Model):
    # Поле для связи с пользователем (может быть пустым для анонимных пользователей)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    # Поле для связи с товаром
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    # Поле для количества товара в корзине
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    # Поле для ключа сессии (для анонимных пользователей)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    # Поле для даты и времени создания записи (автоматически устанавливается при создании)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    # Внутренний класс для метаданных модели
    class Meta:
        # Название таблицы в базе данных
        db_table = 'cart'
        # Человеко-читаемое название модели в единственном числе
        verbose_name = "Корзина"
        # Человеко-читаемое название модели во множественном числе
        verbose_name_plural = "Корзина"
        # Порядок сортировки по умолчанию
        ordering = ("id",)
        # Добавляем индексы для оптимизации запросов
        indexes = [
            # Составной индекс для фильтров по user + product
            models.Index(fields=['user', 'product'], name='cart_user_product_idx'),
            # Составной индекс для фильтров по session_key + product
            models.Index(fields=['session_key', 'product'], name='cart_session_product_idx'),
            # Отдельный индекс для фильтров только по user
            models.Index(fields=['user'], name='cart_user_idx'),
            # Отдельный индекс для фильтров только по session_key
            models.Index(fields=['session_key'], name='cart_session_key_idx'),
            # Индекс по product (FK) для select_related и фильтров по товару
            models.Index(fields=['product'], name='cart_product_idx'),
        ]

    # Использование кастомного менеджера на основе CartQueryset
    objects = CartQueryset().as_manager()

    # Метод для расчета цены товара в корзине (цена за единицу * количество, округленная до 2 знаков)
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    # Метод для строкового представления объекта (используется в админ-панели и отладке)
    def __str__(self):
        if self.user:
            # Для авторизованного пользователя
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
            
        # Для анонимного пользователя
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'
    