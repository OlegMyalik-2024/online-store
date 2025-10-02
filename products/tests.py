import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()


import json
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import Http404
from django.core.files.base import ContentFile  
from products.models import Categories, Products
from products.utils import q_search
from products.views import CatalogView, ProductView

User = get_user_model()




# Unit-тесты для моделей
# Тесты для моделей Categories и Products
# Проверяют строковые представления, методы и свойства моделей
class ProductsModelTestCase(TestCase):
    
    # Подготовка данных 
    def setUp(self):
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=100.0,
            discount=0.0,  
            quantity=5,
            category=self.category
        )
        # Добавляем фейковое изображение для тестов поиска
        self.product.image.save('test.jpg', ContentFile(b'fake image data'))
        self.product.save()

    # Тест строкового представления категории
    def test_categories_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    # Тест строкового представления продукта
    def test_products_str(self):
        expected_str = "(Test Product) Количество - 5"
        self.assertEqual(str(self.product), expected_str)

    # Тест метода get_absolute_url продукта
    def test_products_get_absolute_url(self):
        expected_url = reverse("catalog:product", kwargs={"product_slug": self.product.slug})
        self.assertEqual(self.product.get_absolute_url(), expected_url)

    # Тест метода display_id продукта
    def test_products_display_id(self):
        # Создаем продукт для проверки display_id
        product = Products.objects.create(
            name='Test Product 2',
            slug='test-product-2',
            category=self.category
        )
        self.assertEqual(product.display_id(), f"{product.id:05}")

    # Тест метода sell_price с скидкой
    def test_products_sell_price_with_discount(self):
        product_discount = Products.objects.create(
            name='Discount Product',
            slug='discount-product',
            price=100.0,
            discount=10.0,
            quantity=1,
            category=self.category
        )
        expected_price = round(100.0 - 100.0 * 10.0 / 100, 2)  
        self.assertEqual(product_discount.sell_price(), expected_price)

    # Тест метода sell_price без скидки
    def test_products_sell_price_without_discount(self):
        self.assertEqual(self.product.sell_price(), 100.0)

    # Тест свойства has_image, когда изображение есть
    def test_products_has_image_true(self):
        self.assertTrue(self.product.has_image)





# Unit-тесты для utils
# Тесты для функций утилит, таких как q_search
# Проверяют поиск по различным критериям
class UtilsTestCase(TestCase):
    
    # Подготовка данных
    def setUp(self):
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=100.0,
            quantity=5,
            category=self.category
        )
        # Добавляем изображение
        self.product.image.save('test.jpg', ContentFile(b'fake image data'))
        self.product.save()

    # Тест поиска по ID продукта
    def test_q_search_by_id(self):
        result = q_search(str(self.product.id))  
        self.assertIn(self.product, result)








# Unit-тесты для представлений
# Тесты для представлений CatalogView и ProductView
# Проверяют методы get_queryset, get_object и get_context_data
class ProductsViewTestCase(TestCase):
    
    # Подготовка данных
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=100.0,
            discount=0.0,
            quantity=5,
            category=self.category
        )
        self.product.image.save('test.jpg', ContentFile(b'fake image data'))
        self.product.save()
        self.product2 = Products.objects.create(
            name='Test Product 2',
            slug='test-product-2',
            price=200.0,
            quantity=3,
            category=self.category
        )
        self.product2.image.save('test2.jpg', ContentFile(b'fake image data'))
        self.product2.save()

    # Тест get_queryset для CatalogView с category_slug
    def test_catalog_view_get_queryset_category_slug(self):
        request = self.factory.get(reverse('catalog:index', kwargs={'category_slug': 'test-category'}))
        view = CatalogView()
        view.request = request
        view.kwargs = {'category_slug': 'test-category'}
        queryset = view.get_queryset()
        self.assertIn(self.product, queryset)
        self.assertIn(self.product2, queryset)

    # Тест get_queryset для CatalogView с фильтром on_sale
    def test_catalog_view_get_queryset_on_sale(self):
        # Создать продукт со скидкой
        product_discount = Products.objects.create(
            name='Discount Product',
            slug='discount-product',
            price=100.0,
            discount=5.0,
            quantity=1,
            category=self.category
        )
        product_discount.image.save('discount.jpg', ContentFile(b'fake image data'))
        product_discount.save()
        request = self.factory.get(reverse('catalog:index', kwargs={'category_slug': 'test-category'}), {'on_sale': 'on'})
        view = CatalogView()
        view.request = request
        view.kwargs = {'category_slug': 'test-category'}
        queryset = view.get_queryset()
        self.assertIn(product_discount, queryset)
        self.assertNotIn(self.product, queryset)  

    # Тест get_queryset для CatalogView с order_by price
    def test_catalog_view_get_queryset_order_by_price(self):
        request = self.factory.get(reverse('catalog:index', kwargs={'category_slug': 'test-category'}), {'order_by': 'price'})
        view = CatalogView()
        view.request = request
        view.kwargs = {'category_slug': 'test-category'}
        queryset = view.get_queryset()
        # Проверяем порядок: product (100) перед product2 (200)
        products_list = list(queryset)
        self.assertEqual(products_list[0], self.product)
        self.assertEqual(products_list[1], self.product2)

    # Тест get_context_data для CatalogView
    def test_catalog_view_get_context_data(self):
        request = self.factory.get(reverse('catalog:index', kwargs={'category_slug': 'test-category'}))
        view = CatalogView()
        view.request = request
        view.kwargs = {'category_slug': 'test-category'}
        view.object_list = view.get_queryset()  # Устанавливаем object_list перед get_context_data
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Каталог')
        self.assertEqual(context['slug_url'], 'test-category')

    # Тест get_object для ProductView с валидным slug
    def test_product_view_get_object_valid(self):
        request = self.factory.get(reverse('catalog:product', kwargs={'product_slug': 'test-product'}))
        view = ProductView()
        view.request = request
        view.kwargs = {'product_slug': 'test-product'}
        obj = view.get_object()
        self.assertEqual(obj, self.product)

    # Тест get_object для ProductView с quantity=0 (должен вызвать Http404)
    def test_product_view_get_object_quantity_zero(self):
        product_zero = Products.objects.create(
            name='Zero Quantity',
            slug='zero-quantity',
            quantity=0,
            category=self.category
        )
        request = self.factory.get(reverse('catalog:product', kwargs={'product_slug': 'zero-quantity'}))
        view = ProductView()
        view.request = request
        view.kwargs = {'product_slug': 'zero-quantity'}
        with self.assertRaises(Http404):
            view.get_object()

    # Тест get_context_data для ProductView
    def test_product_view_get_context_data(self):
        request = self.factory.get(reverse('catalog:product', kwargs={'product_slug': 'test-product'}))
        view = ProductView()
        view.request = request
        view.kwargs = {'product_slug': 'test-product'}
        view.object = view.get_object()  # Устанавливаем object перед get_context_data
        context = view.get_context_data()
        self.assertEqual(context['title'], self.product.name)
