from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static


# Основной список маршрутов URL проекта
urlpatterns = [
    path('admin/', admin.site.urls),  # Путь к административной панели Django
    # Главная страница сайта и маршруты приложения main, namespace позволяет использовать имена URL с префиксом 'main'
    path('', include('main.urls', namespace='main')),  
    # Маршруты каталога товаров из приложения products
    path('catalog/', include('products.urls', namespace='catalog')),  
    # Маршруты управления пользователями из приложения users
    path('user/', include('users.urls', namespace='user')),  
    # Маршруты корзины из приложения carts
    path('cart/', include('carts.urls', namespace='cart')),  
     # Маршруты оформления заказов из приложения orders
    path('orders/', include('orders.urls', namespace='orders')),  
]

# Дополнительные настройки URL для режима отладки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()  # Добавляем URL-ы для панели отладки Django Debug Toolbar
    # Позволяет серверу разработки отдавать статические файлы (CSS, JS и т.п.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
    # Позволяет серверу разработки отдавать загружаемые медиа-файлы (картинки, документы)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  