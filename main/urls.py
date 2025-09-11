from django.urls import path
from main import views
from django.views.decorators.cache import cache_page

app_name = 'main'  # Инициализация пространства имен main для уникальности имен маршрутов

# Список маршрутов URL для приложения
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', cache_page(60)(views.AboutView.as_view()), name='about'),
    path('contacts/', cache_page(60)(views.ContactsView.as_view()), name='contacts'),
    path('delivery_and_payment/', cache_page(60)(views.Delivery_and_paymentView.as_view()), name='delivery_and_payment'),
]
