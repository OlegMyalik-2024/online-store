import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()



import json
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile  # Для фейкового изображения
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from users.views import (
    UserLoginView, UserRegistrationView, UserProfileView, UserCartView,
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView,
    logout
)
from carts.models import Cart  # Предполагаем, что модель Cart существует
from orders.models import Order  # Предполагаем, что модель Order существует 

User = get_user_model()


# Функция для добавления middleware к request в тестах
def add_middleware_to_request(request):
    def get_response(r):
        return None
    session_middleware = SessionMiddleware(get_response)
    session_middleware.process_request(request)
    request.session.save()
    message_middleware = MessageMiddleware(get_response)
    message_middleware.process_request(request)
    request.session.save()






# Unit-тесты для модели User
# Проверяют строковое представление и другие методы модели
class UserModelTestCase(TestCase):
   
    # Подготовка данных
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
    
    # Тест строкового представления пользователя
    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')






# Unit-тесты для форм пользователей
# Проверяют валидацию и сохранение форм
class UserFormsTestCase(TestCase):
    
    # Подготовка данных
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
    
    # Тест валидной формы входа
    def test_user_login_form_valid(self):
        form_data = {'username': 'testuser', 'password': 'testpass123'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    # Тест валидной формы регистрации
    def test_user_registration_form_valid(self):
        form_data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newuser')
    
    # Тест валидной формы профиля
    def test_profile_form_valid(self):
        form_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'updated@example.com'
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')






# Unit-тесты для представлений пользователей
# Проверяют методы представлений, контекст и формы
class UserViewsTestCase(TestCase):
    
    # Подготовка данных
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.user.image.save('test.jpg', ContentFile(b'fake image data'))  # Фейковое изображение для профиля
        self.user.save()
        # Создаем заказ для тестов профиля 
        self.order = Order.objects.create(user=self.user, phone_number='1234567890')
    
    # Тест get_context_data для UserLoginView
    def test_user_login_view_get_context_data(self):
        request = self.factory.get(reverse('users:login'))
        view = UserLoginView()
        view.request = request
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Авторизация')
    
    # Тест form_valid для UserLoginView
    def test_user_login_view_form_valid(self):
        request = self.factory.post(reverse('users:login'), {'username': 'testuser', 'password': 'testpass123'})
        add_middleware_to_request(request)  # Используем функцию для middleware
        view = UserLoginView()
        view.request = request
        form = UserLoginForm(data={'username': 'testuser', 'password': 'testpass123'})
        self.assertTrue(form.is_valid())
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)  # Redirect
    
    # Тест get_context_data для UserRegistrationView
    def test_user_registration_view_get_context_data(self):
        request = self.factory.get(reverse('users:registration'))
        view = UserRegistrationView()
        view.request = request
        view.object = None  # Устанавливаем object (для DetailView/UpdateView)
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Регистрация')
    
    # Тест form_valid для UserRegistrationView
    def test_user_registration_view_form_valid(self):
        request = self.factory.post(reverse('users:registration'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        add_middleware_to_request(request)  # Используем функцию для middleware
        view = UserRegistrationView()
        view.request = request
        form = UserRegistrationForm(data={
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertTrue(form.is_valid())
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)
    
    # Тест get_object для UserProfileView
    def test_user_profile_view_get_object(self):
        request = self.factory.get(reverse('users:profile'))
        request.user = self.user
        view = UserProfileView()
        view.request = request
        obj = view.get_object()
        self.assertEqual(obj, self.user)
    
    # Тест get_context_data для UserProfileView
    def test_user_profile_view_get_context_data(self):
        request = self.factory.get(reverse('users:profile'))
        request.user = self.user
        view = UserProfileView()
        view.request = request
        view.object = view.get_object()  # Устанавливаем object перед get_context_data
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Кабинет')
        self.assertIn('orders', context)
    
    # Тест form_valid для UserProfileView
    def test_user_profile_view_form_valid(self):
        request = self.factory.post(reverse('users:profile'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'updated@example.com'
        })
        request.user = self.user
        add_middleware_to_request(request)  # Используем функцию для middleware
        view = UserProfileView()
        view.request = request
        form = ProfileForm(data={
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'updated@example.com'
        }, instance=self.user)
        self.assertTrue(form.is_valid())
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)
    
    # Тест get_context_data для UserCartView
    def test_user_cart_view_get_context_data(self):
        request = self.factory.get(reverse('users:users_cart'))
        view = UserCartView()
        view.request = request
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Корзина')
    
    # Тест функции logout
    def test_logout_function(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
    
    # Тест get_context_data для UserPasswordResetView
    def test_user_password_reset_view_get_context_data(self):
        request = self.factory.get(reverse('users:password_reset'))
        view = UserPasswordResetView()
        view.request = request
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Сброс пароля')
    
    # Тест get_context_data для UserPasswordResetDoneView
    def test_user_password_reset_done_view_get_context_data(self):
        request = self.factory.get(reverse('users:password_reset_done'))
        view = UserPasswordResetDoneView()
        view.request = request
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Сброс пароля отправлен')
    
    # Тест get_context_data для UserPasswordResetConfirmView
    def test_user_password_reset_confirm_view_get_context_data(self):
        request = self.factory.get(reverse('users:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test'}))
        view = UserPasswordResetConfirmView()
        view.request = request
        view.user = None  # Устанавливаем user 
        view.validlink = False  # Устанавливаем validlink 
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Новый пароль')
    
    # Тест get_context_data для UserPasswordResetCompleteView
    def test_user_password_reset_complete_view_get_context_data(self):
        request = self.factory.get(reverse('users:password_reset_complete'))
        view = UserPasswordResetCompleteView()
        view.request = request
        context = view.get_context_data()
        self.assertEqual(context['title'], 'HelloMobile - Пароль изменен')
