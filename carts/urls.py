from django.urls import path
from carts import views


# Имя приложения для namespace в URL (используется для обратных ссылок)
app_name = 'carts'

# Список URL-шаблонов для приложения carts
urlpatterns = [
    path('cart_add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_change/', views.CartChangeView.as_view(), name='cart_change'),
    path('cart_remove/', views.CartRemoveView.as_view(), name='cart_remove'),
]
