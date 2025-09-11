from django.urls import path  
from products import views     

# Пространство имён для URL — используется при обратном разрешении (reverse) и шаблонах
app_name = 'products'  

# Список маршрутов для приложения products
urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
