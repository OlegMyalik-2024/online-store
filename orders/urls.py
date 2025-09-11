from django.urls import path  
from orders import views  

app_name = 'orders'  # Пространство имён для маршрутов данного приложения.

# Определение маршрута для создания заказа
urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
]
