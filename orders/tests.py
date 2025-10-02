import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()


from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.core.exceptions import ValidationError
from django.db import transaction
from unittest.mock import patch
from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm
from orders.views import CreateOrderView
from products.models import Products, Categories  
from users.models import User

User = get_user_model()




# Функция для добавления middleware к request (для RequestFactory)
def add_middleware_to_request(request):
    mw_session = SessionMiddleware(lambda r: None)
    mw_session.process_request(request)
    request.session.save()
    mw_message = MessageMiddleware(lambda r: None)
    mw_message.process_request(request)
    mw_auth = AuthenticationMiddleware(lambda r: None)
    mw_auth.process_request(request)






# Тесты для модели Order
class OrderModelTest(TestCase):
    
    # Подготовка данных
    def setUp(self):
         # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        # Создаем категорию для продукта (используем правильное имя модели Categories)
        self.category = Categories.objects.create(name='Test Category')
        # Создаем продукт с обязательным полем category
        self.product = Products.objects.create(
            name='Test Product',
            price=100.00,
            quantity=10,
            category=self.category
        )

    # Тестируем создание заказа с базовыми полями
    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            phone_number='375291234567',
            requires_delivery=True,
            delivery_address='Test Address',
            payment_on_get=False
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'В обработке')
        self.assertFalse(order.is_paid)

    # Тестируем строковое представление заказа для авторизованного пользователя
    def test_order_str(self):
        order = Order.objects.create(user=self.user, phone_number='375291234567')
        self.assertEqual(str(order), f"Заказ № {order.pk} | Покупатель {self.user.first_name} {self.user.last_name}")

    # Тестируем строковое представление заказа для гостя (без пользователя)
    def test_order_str_guest(self):
        order = Order.objects.create(phone_number='375291234567')
        self.assertEqual(str(order), f"Заказ № {order.pk} | Покупатель: Гость")






# Тесты для модели OrderItem
class OrderItemModelTest(TestCase):
    
    # Подготовка данных
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        # Создаем категорию для продукта
        self.category = Categories.objects.create(name='Test Category')
        # Создаем продукт с category
        self.product = Products.objects.create(
            name='Test Product',
            price=50.00,
            quantity=10,
            category=self.category
        )
        # Создаем заказ для тестов
        self.order = Order.objects.create(
            user=self.user,
            phone_number='375291234567'
        )

    # Тестируем создание элемента заказа и расчет цены
    def test_orderitem_creation(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,  
            quantity=2
        )
        self.assertEqual(item.products_price(), 100.00)  

    # Тестируем строковое представление элемента заказа
    def test_orderitem_str(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=1
        )
        self.assertEqual(str(item), f"Товар {self.product.name} | Заказ № {self.order.pk}")

    # Тестируем расчет общей цены для queryset элементов заказа
    def test_orderitem_queryset_total_price(self):
        item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=2
        )
        item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=1
        )
        queryset = OrderItem.objects.filter(order=self.order)
        self.assertEqual(queryset.total_price(), 150.00)  

    # Тестируем расчет общего количества для queryset элементов заказа
    def test_orderitem_queryset_total_quantity(self):
        item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=2
        )
        item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=1
        )
        queryset = OrderItem.objects.filter(order=self.order)
        self.assertEqual(queryset.total_quantity(), 3)

    # Тестируем расчет общего количества для пустого queryset
    def test_orderitem_queryset_empty_total_quantity(self):
        queryset = OrderItem.objects.filter(order=self.order)
        self.assertEqual(queryset.total_quantity(), 0)







# Тесты для формы CreateOrderForm
class CreateOrderFormTest(TestCase):
    
     # Тестируем валидные данные формы
    def test_form_valid_data(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375291234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        form = CreateOrderForm(data=data)
        self.assertTrue(form.is_valid())

    # Тестируем невалидный номер телефона (содержит буквы)
    def test_form_invalid_phone_number_not_digits(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375abc1234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        form = CreateOrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ['Номер телефона должен содержать только цифры'])

    # Тестируем невалидный номер телефона (неправильный формат)
    def test_form_invalid_phone_number_wrong_format(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '123456789',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        form = CreateOrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ['Неверный формат номера. Ожидается 375(код оператора)(номер)'])

    # Тестируем валидный номер телефона и очистку данных
    def test_form_valid_phone_number(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375291234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        form = CreateOrderForm(data=data)
        self.assertTrue(form.is_valid())
        cleaned_phone = form.clean_phone_number()
        self.assertEqual(cleaned_phone, '375291234567')








# Тесты для представления CreateOrderView
class CreateOrderViewTest(TestCase):
    
    # Подготовка данных
    def setUp(self):
        # Инициализируем клиент и фабрику запросов
        self.client = Client()
        self.factory = RequestFactory()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        # Создаем категорию для продукта
        self.category = Categories.objects.create(name='Test Category')
        # Создаем продукт с category
        self.product = Products.objects.create(
            name='Test Product',
            price=100.00,
            quantity=10,
            category=self.category
        )
        # Создаем элемент корзины для пользователя
        self.cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

    # Тестируем, что GET-запрос требует авторизации (редирект на логин)
    def test_get_view_requires_login(self):
        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    # Тестируем GET-запрос для авторизованного пользователя
    def test_get_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Оформление заказа')

    # Тестируем начальные данные формы (имя и фамилия пользователя)
    def test_get_initial_data(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial['first_name'], self.user.first_name)
        self.assertEqual(form.initial['last_name'], self.user.last_name)

    # Тестируем успешное создание заказа с валидной формой
    def test_post_valid_form(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375291234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        response = self.client.post(reverse('orders:create_order'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        # Проверяем создание заказа и элементов заказа
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.get(user=self.user)
        self.assertTrue(OrderItem.objects.filter(order=order).exists())
        # Проверяем уменьшение количества товара
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)  
        # Проверяем очистку корзины
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    # Тестируем POST-запрос с невалидной формой (неправильный номер телефона)
    def test_post_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 'invalid',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        response = self.client.post(reverse('orders:create_order'), data)
        self.assertEqual(response.status_code, 302)  
        # Проверяем, что заказ не создан
        self.assertFalse(Order.objects.filter(user=self.user).exists())

    # Тестируем POST-запрос при недостатке товара на складе
    def test_post_insufficient_stock(self):
        self.client.login(username='testuser', password='password123')
        # Устанавливаем количество в корзине больше, чем на складе
        self.cart_item.quantity = 15
        self.cart_item.save()
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375291234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        response = self.client.post(reverse('orders:create_order'), data)
        self.assertEqual(response.status_code, 302)  # Redirect back
        # Проверяем, что заказ не создан
        self.assertFalse(Order.objects.filter(user=self.user).exists())
        # Проверяем, что количество товара не изменилось
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)

     # Тестируем POST-запрос при пустой корзине
    def test_post_empty_cart(self):
        self.client.login(username='testuser', password='password123')
        Cart.objects.filter(user=self.user).delete()  # Очищаем корзину
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '375291234567',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0'
        }
        response = self.client.post(reverse('orders:create_order'), data)
        self.assertEqual(response.status_code, 302)  # Redirect back
        # Проверяем, что заказ не создан
        self.assertFalse(Order.objects.filter(user=self.user).exists())
