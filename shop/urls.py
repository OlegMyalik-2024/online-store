from venv import logger
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render

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

# Временное обслуживание файлов для тестирования с DEBUG=False (НЕ ДЛЯ ПРОДАКШЕНА!)
# В продакшене настройте nginx/apache для раздачи /static/ и /media/
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Дополнительные настройки URL для режима отладки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()  # Добавляем URL-ы для панели отладки Django Debug Toolbar
    # Позволяет серверу разработки отдавать статические файлы (CSS, JS и т.п.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
    # Позволяет серверу разработки отдавать загружаемые медиа-файлы (картинки, документы)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


# Функция-обработчик для 404 ошибок (страница не найдена)
# Django вызывает эту функцию, когда не может найти маршрут для запроса
def custom_404(request, exception):
    # Логируем информацию о 404 ошибке: путь запроса и исключение
    logger.error(f"404 error for {request.path}: {exception}")
    # Попытка рендерить шаблон 404.html
    try:
        # Возвращаем рендеренный шаблон с кодом статуса 404
        return render(request, '404.html', status=404)
    except Exception as e:
        # Если рендеринг шаблона вызывает исключение (например, шаблон не найден),
        # логируем эту ошибку
        logger.error(f"Error rendering 404 template: {e}")
        # Возвращаем рендеренный шаблон снова (или можно заменить на простой текст,
        # например: return HttpResponse("404 - Page not found", status=404))
        return render(request, '404.html', status=404)  # Или простой текст, если шаблон сломан

# Назначаем нашу функцию как обработчик 404 ошибок в Django
handler404 = custom_404