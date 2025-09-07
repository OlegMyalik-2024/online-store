# Создание моделей таблиц БД
from tabnanny import verbose
from django.db import models
from django.urls import reverse



# Модель таблицы категории товаров
class Categories(models.Model):
    name=models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    
    #Класс для настройки таблицы
    class Meta:
        db_table='category' # Отображение таблицы в БД
        verbose_name='Категорию' # Отображение таблицы в админке в единственном числе
        verbose_name_plural='Категории' # Отображение таблицы в админке в множественном числе
        
    def __str__(self):
        return self.name
  
  
  
        
# Модель таблицы товары
class Products(models.Model):
    name=models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description=models.TextField(blank=True, null=True, verbose_name='Описание')
    image=models.ImageField(upload_to='products_images', blank=True, null=True, verbose_name='Изображение')
    price=models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount=models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в процентах')
    quantity=models.PositiveIntegerField(default=0, verbose_name='Количество')  
    category=models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
      
    #Класс для настройки таблицы
    class Meta:
        db_table='product' # Отображение таблицы в БД
        verbose_name='Продукт' # Отображение таблицы в админке в единственном числе
        verbose_name_plural='Продукты' # Отображение таблицы в админке в множественном числе
        ordering=("id",)
    
    def __str__(self):
        return f"({self.name}) Количество - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    
    #Метод вывода пятизначного id продукта в шаблон
    def display_id(self):
        return f"{self.id:05}"
    
    # Метод расчета цены со скидкой
    def sell_price(self):
        if self.discount:
            return round(self.price-self.price*self.discount/100, 2)
        return self.price