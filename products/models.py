from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVector


# Модель категории товаров
class Categories(models.Model):
    # Название категории (уникальное)
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название'
    )
    # URL-идентификатор категории (slug), может быть пустым
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name='URL'
    )
    class Meta:
        db_table = 'category'  # Имя таблицы в БД
        verbose_name = 'Категорию'  # Название в админке (единственное число)
        verbose_name_plural = 'Категории'  # Название в админке (множественное число)
        # Добавляем индексы для оптимизации запросов
        indexes = [
            # Индекс по slug для фильтров по category__slug (ускоряет CatalogView)
            models.Index(fields=['slug'], name='categories_slug_idx'),
        ]

    # Представление категории в интерфейсах
    def __str__(self):
        return self.name




# Модель товара
class Products(models.Model):
    # Название товара (уникальное)
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название'
    )
    # URL-идентификатор товара (slug), может быть пустым
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name='URL'
    )
    # Описание товара (необязательное)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    # Изображение товара (загружается в папку products_images)
    image = models.ImageField(
        upload_to='products_images',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    # Цена товара
    price = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        verbose_name='Цена'
    )
    # Скидка в процентах (например, 15.00 означает 15%)
    discount = models.DecimalField(
        default=0.00,
        max_digits=4,
        decimal_places=2,
        verbose_name='Скидка в процентах'
    )
    # Количество товара на складе
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество'
    )
    # Связь с категорией товара
    category = models.ForeignKey(
        to=Categories,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    class Meta:
        db_table = 'product'  # Имя таблицы в БД
        verbose_name = 'Продукт'  # Название в админке (единственное число)
        verbose_name_plural = 'Продукты'  # Название в админке (множественное число)
        ordering = ("id",)  # Сортировка по ID
        # Добавляем индексы для оптимизации запросов
        indexes = [
            # Индекс по slug для быстрого поиска товара (ProductView)
            models.Index(fields=['slug'], name='products_slug_idx'),
            # Индекс по category (FK) для фильтров по категории (CatalogView)
            models.Index(fields=['category'], name='products_category_idx'),
            # Индекс по discount для фильтров товаров со скидкой
            models.Index(fields=['discount'], name='products_discount_idx'),
            # Индекс по price для сортировки по цене (если часто используется order_by="price")
            models.Index(fields=['price'], name='products_price_idx'),
        ]

    # Представление товара в интерфейсах
    def __str__(self):
        return f"({self.name}) Количество - {self.quantity}"

    # Метод для получения абсолютного URL товара (используется в шаблонах и ссылках)
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    # Метод для отображения ID товара в виде 5-значного числа (например, 00042)
    def display_id(self):
        return f"{self.id:05}"

    # Метод для расчёта цены с учётом скидки
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price