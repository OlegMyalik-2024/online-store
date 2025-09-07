from tabnanny import verbose
from django.db import models

from products.models import Products
from users.models import User


class CartQueryset(models.QuerySet):
    #Метод расчета полной стоимости всех корзин пользователей
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    #Метод количества товаров всех корзин пользователей
    def total_quantity(self):
      if self:
          return sum(cart.quantity for cart in self)
      return 0

#Модель таблицы корзина
class Cart(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product=models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity=models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key=models.CharField(max_length=32, blank=True)
    created_timestamp=models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')
    
    class Meta:
        db_table='cart'
        verbose_name='Корзина'
        verbose_name_plural='Корзины'
        
    objects=CartQueryset().as_manager()
     
    #метод расчета стоимости всех товаров находящихся в корзине пользователя   
    def products_price(self):
        return round(self.product.sell_price()*self.quantity, 2)
        
    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'