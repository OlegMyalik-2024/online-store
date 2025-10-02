import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser  
from django.http import HttpRequest
from django.urls import reverse
from carts.models import Cart
from products.models import Products, Categories  
from carts.utils import get_user_carts
from carts.views import CartAddView, CartChangeView, CartRemoveView
from users.models import User
import json



# Тесты для модели Cart и CartQueryset
class CartModelTestCase(TestCase):
   
    # Создаем данные 
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(name='Test Category')  
        cls.product = Products.objects.create(name='Test Product', price=10.00, category=cls.category) 
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.cart = Cart.objects.create(user=cls.user, product=cls.product, quantity=2)

    # Тест метода products_price
    def test_products_price(self):
        expected_price = round(self.product.price * self.cart.quantity, 2)
        self.assertEqual(self.cart.products_price(), expected_price)

    # Тест __str__ для аутентифицированного пользователя
    def test_str_authenticated_user(self):
        expected = f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.cart.quantity}'
        self.assertEqual(str(self.cart), expected)

    # Тест __str__ для анонимного пользователя
    def test_str_anonymous_user(self):
        category = Categories.objects.create(name='Another Category')  # Используем Categories
        product = Products.objects.create(name='Another Product', price=15.00, category=category)
        anonymous_cart = Cart.objects.create(session_key='test_session', product=product, quantity=1)
        expected = f'Анонимная корзина | Товар {product.name} | Количество {anonymous_cart.quantity}'
        self.assertEqual(str(anonymous_cart), expected)

    # Тест total_price для CartQueryset
    def test_cart_queryset_total_price(self):
        cart2 = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        queryset = Cart.objects.filter(user=self.user)
        expected_total = self.cart.products_price() + cart2.products_price()
        self.assertEqual(queryset.total_price(), expected_total)

    # Тест total_quantity для CartQueryset
    def test_cart_queryset_total_quantity(self):
        cart2 = Cart.objects.create(user=self.user, product=self.product, quantity=3)
        queryset = Cart.objects.filter(user=self.user)
        expected_quantity = self.cart.quantity + cart2.quantity
        self.assertEqual(queryset.total_quantity(), expected_quantity)

    # Тест total_quantity для пустого QuerySet
    def test_cart_queryset_total_quantity_empty(self):
        queryset = Cart.objects.filter(user__username='nonexistent')
        self.assertEqual(queryset.total_quantity(), 0)







# Тесты для utils.py
class CartUtilsTestCase(TestCase):

    # Создаем данные
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(name='Test Category')  
        cls.product = Products.objects.create(name='Test Product', price=10.00, category=cls.category)
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.cart = Cart.objects.create(user=cls.user, product=cls.product, quantity=1)

    # Тест get_user_carts для аутентифицированного пользователя
    def test_get_user_carts_authenticated(self):
        request = HttpRequest()
        request.user = self.user
        carts = get_user_carts(request)
        self.assertEqual(list(carts), [self.cart])
        self.assertTrue(hasattr(carts.first().product, 'name'))

    # Тест get_user_carts для анонимного пользователя
    def test_get_user_carts_anonymous(self):
        request = HttpRequest()
        request.user = AnonymousUser()
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        request.session.save()
        session_key = request.session.session_key
        category = Categories.objects.create(name='Anonymous Category')  
        product = Products.objects.create(name='Anonymous Product', price=20.00, category=category)
        anonymous_cart = Cart.objects.create(session_key=session_key, product=product, quantity=1)
        carts = get_user_carts(request)
        self.assertEqual(list(carts), [anonymous_cart])
        self.assertTrue(hasattr(carts.first().product, 'name'))







# Тесты для представлений (views.py)
class CartViewsTestCase(TestCase):

    # Создаем данные
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(name='Test Category')  # Используем Categories
        cls.product = Products.objects.create(name='Test Product', price=10.00, category=cls.category)

    # Подготовка данных
    def setUp(self):
        self.client = Client()
        self.add_url = reverse('carts:cart_add')
        self.change_url = reverse('carts:cart_change')
        self.remove_url = reverse('carts:cart_remove')

    # Тест добавления товара в корзину для аутентифицированного пользователя
    def test_cart_add_authenticated(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.add_url, {'product_id': self.product.id}, HTTP_REFERER='/some-url/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Товар добавлен в корзину')
        cart = Cart.objects.get(user=user, product=self.product)
        self.assertEqual(cart.quantity, 1)
        self.assertIn('cart_items_html', data)

    # Тест добавления товара в корзину для анонимного пользователя
    def test_cart_add_anonymous(self):
        self.client.session.save()
        response = self.client.post(self.add_url, {'product_id': self.product.id}, HTTP_REFERER='/some-url/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Товар добавлен в корзину')
        session_key = self.client.session.session_key
        cart = Cart.objects.get(session_key=session_key, product=self.product)
        self.assertEqual(cart.quantity, 1)

    # Тест добавления существующего товара (увеличение количества)
    def test_cart_add_existing_product(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.client.post(self.add_url, {'product_id': self.product.id}, HTTP_REFERER='/some-url/')
        response = self.client.post(self.add_url, {'product_id': self.product.id}, HTTP_REFERER='/some-url/')
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.get(user=user, product=self.product)
        self.assertEqual(cart.quantity, 2)

    # Тест изменения количества товара в корзине
    def test_cart_change_quantity(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=user, product=self.product, quantity=1)
        response = self.client.post(self.change_url, {'cart_id': cart.id, 'quantity': 5}, HTTP_REFERER='/some-url/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Количество изменено')
        self.assertEqual(data['quantity'], '5')
        cart.refresh_from_db()
        self.assertEqual(cart.quantity, 5)

    # Тест удаления товара из корзины
    def test_cart_remove(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=user, product=self.product, quantity=2)
        response = self.client.post(self.remove_url, {'cart_id': cart.id}, HTTP_REFERER='/some-url/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Товар удален из корзины')
        self.assertEqual(data['quantity_deleted'], 2)
        self.assertFalse(Cart.objects.filter(id=cart.id).exists())
