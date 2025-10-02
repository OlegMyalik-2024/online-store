import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse, resolve
from main.views import IndexView, AboutView, ContactsView, Delivery_and_paymentView




# Unit-тесты для представлений (views) приложения main
class MainViewsTestCase(TestCase):

    # Подготовка данных
    def setUp(self):
        self.client = Client()

    # Тест представления IndexView: проверка шаблона и контекста
    def test_index_view_template_and_context(self):
        view = IndexView()
        context = view.get_context_data()
        # Проверка шаблона
        self.assertEqual(view.template_name, 'main/index.html')
        # Проверка контекста
        self.assertEqual(context['title'], 'HelloMobile - Главная')
        self.assertEqual(context['content'], 'Интернет-магазин HelloMobile')
        self.assertNotIn('text_on_page', context)  # В IndexView нет text_on_page

    # Тест представления AboutView: проверка шаблона и контекста
    def test_about_view_template_and_context(self):
        view = AboutView()
        context = view.get_context_data()
        # Проверка шаблона
        self.assertEqual(view.template_name, 'main/about.html')
        # Проверка контекста
        self.assertEqual(context['title'], 'HelloMobile - О нас')
        self.assertEqual(context['content'], 'Почему HelloMobile — ваш идеальный магазин для мобильных устройств?')
        self.assertIn('text_on_page', context)
        self.assertIn('<div class="about-highlight">', context['text_on_page'])  # Проверка наличия HTML

    # Тест представления ContactsView: проверка шаблона и контекста
    def test_contacts_view_template_and_context(self):
        view = ContactsView()
        context = view.get_context_data()
        # Проверка шаблона
        self.assertEqual(view.template_name, 'main/contacts.html')
        # Проверка контекста
        self.assertEqual(context['title'], 'HelloMobile - Контакты')
        self.assertEqual(context['content'], 'Наши контакты')
        self.assertIn('text_on_page', context)
        self.assertIn('<div class="contact-page">', context['text_on_page'])  # Проверка наличия HTML

    # Тест представления Delivery_and_paymentView: проверка шаблона и контекста
    def test_delivery_and_payment_view_template_and_context(self):
        view = Delivery_and_paymentView()
        context = view.get_context_data()
        # Проверка шаблона
        self.assertEqual(view.template_name, 'main/delivery_and_payment.html')
        # Проверка контекста
        self.assertEqual(context['title'], 'HelloMobile - Доставка и оплата')
        self.assertEqual(context['content'], 'Доставка и оплата')
        self.assertIn('text_on_page', context)
        self.assertIn('<div class="delivery-payment">', context['text_on_page'])  # Проверка наличия HTML





# Unit-тесты для URL-маршрутов приложения main
class MainUrlsTestCase(TestCase):
    
    # Тест разрешения URL для главной страницы
    def test_index_url_resolves(self):
        url = reverse('main:index')
        self.assertEqual(url, '/')
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, IndexView)

    # Тест разрешения URL для страницы 'О нас'
    def test_about_url_resolves(self):
        url = reverse('main:about')
        self.assertEqual(url, '/about/')
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, AboutView)

    # Тест разрешения URL для страницы контактов
    def test_contacts_url_resolves(self):
        url = reverse('main:contacts')
        self.assertEqual(url, '/contacts/')
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, ContactsView)

    # Тест разрешения URL для страницы доставки и оплаты
    def test_delivery_and_payment_url_resolves(self):
        url = reverse('main:delivery_and_payment')
        self.assertEqual(url, '/delivery_and_payment/')
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, Delivery_and_paymentView)






# Интеграционные тесты для проверки HTTP-ответов 
class MainIntegrationTestCase(TestCase):

    # Подготовка данных
    def setUp(self):
        self.client = Client()

    # Тест GET-запроса к главной странице
    def test_index_page_get(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, 'HelloMobile - Главная')

    # Тест GET-запроса к странице 'О нас'
    def test_about_page_get(self):
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'HelloMobile - О нас')

    # Тест GET-запроса к странице контактов
    def test_contacts_page_get(self):
        response = self.client.get(reverse('main:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contacts.html')
        self.assertContains(response, 'HelloMobile - Контакты')

    # Тест GET-запроса к странице доставки и оплаты
    def test_delivery_and_payment_page_get(self):
        response = self.client.get(reverse('main:delivery_and_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delivery_and_payment.html')
        self.assertContains(response, 'HelloMobile - Доставка и оплата')

