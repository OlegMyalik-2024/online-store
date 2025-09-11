from django.db import models
from products.models import Products
from users.models import User


 
# Кастомный QuerySet для модели OrderItem с дополнительными методами подсчёта.   
class OrderitemQueryset(models.QuerySet):

    # Подсчитывает общую стоимость всех товаров в наборе.
    # Вызывает метод products_price() для каждого элемента и суммирует результаты. 
    def total_price(self):
        return sum(cart.products_price() for cart in self)


    # Подсчитывает общее количество товаров в наборе.
    # Если набор пуст, возвращает 0.
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0



# Модель заказа, содержащая информацию о пользователе, статусе, доставке и оплате.  
class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона"
    )
    requires_delivery = models.BooleanField(
        default=False,
        verbose_name="Требуется доставка"
    )
    delivery_address = models.TextField(
        null=True,
        blank=True,
        verbose_name="Адрес доставки"
    )
    payment_on_get = models.BooleanField(
        default=False,
        verbose_name="Оплата при получении"
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name="Оплачено"
    )
    status = models.CharField(
        max_length=50,
        default='В обработке',
        verbose_name="Статус заказа"
    )

    class Meta:
        db_table = "order"  # Название таблицы в базе данных
        verbose_name = "Заказ"  # Читаемое имя модели в единственном числе
        verbose_name_plural = "Заказы"  # Читаемое имя модели во множественном числе
        ordering = ("id",)  # Сортировка по умолчанию по возрастанию id

    # Читаемое строковое представление объекта заказа.
    # Показывает номер заказа и имя пользователя.
    def __str__(self):
        # Если пользователь не задан (None), избежать ошибки AttributeError
        if self.user:
            return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"
        return f"Заказ № {self.pk} | Покупатель: Гость"




# Модель товара в заказе — связывает конкретный продукт с конкретным заказом. 
class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество"
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата продажи"
    )

    class Meta:
        db_table = "order_item"  # Название таблицы в базе данных
        verbose_name = "Проданный товар"  # Читаемое имя модели в единственном числе
        verbose_name_plural = "Проданные товары"  # Читаемое имя модели во множественном числе
        ordering = ("id",)  # Сортировка по умолчанию по возрастанию id
    # Используем кастомный менеджер с дополнительными методами из OrderitemQueryset
    objects = OrderitemQueryset.as_manager()
 
    # Рассчитывает общую стоимость этого товара в заказе.
    # Умножает цену продажи продукта на количество.
    # Округляет результат до 2 знаков после запятой.   
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)


    # Читаемое строковое представление объекта товара в заказе.
    # Показывает название товара и номер заказа.
    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"