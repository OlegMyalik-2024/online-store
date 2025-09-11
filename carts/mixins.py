from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts




# Миксин для работы с корзиной, предоставляющий методы для получения и рендеринга корзины
class CartMixin:   
    
    # Возвращает объект Cart, соответствующий пользователю или сессии, с опциональными фильтрами по продукту или ID корзины.
    # Если пользователь авторизован, фильтрует по user.
    # Если анонимный, фильтрует по session_key.
    def get_cart(self, request, product=None, cart_id=None):
        # Определяем параметры фильтрации в зависимости от аутентификации пользователя
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}
        # Добавляем фильтр по продукту, если передан
        if product:
            query_kwargs["product"] = product
        # Добавляем фильтр по ID корзины, если передан
        if cart_id:
            query_kwargs["id"] = cart_id
        # Возвращаем первый объект Cart, соответствующий фильтрам (или None, если не найден)
        return Cart.objects.filter(**query_kwargs).first()
    
    
    
    # Рендерит HTML-шаблон корзины для текущего пользователя или сессии.
    # Добавляет флаг 'order' в контекст, если referer указывает на страницу создания заказа.
    # Возвращает строку с HTML.
    def render_cart(self, request):
        # Получаем корзину пользователя или сессии с помощью утилиты
        user_cart = get_user_carts(request)
        # Формируем базовый контекст с корзиной
        context = {"carts": user_cart}
        # Проверяем referer страницы (страницу, с которой пришел запрос)
        referer = request.META.get('HTTP_REFERER')
        # Если referer содержит URL страницы создания заказа, добавляем флаг order=True
        if reverse('orders:create_order') in referer:
            context["order"] = True
        # Рендерим шаблон корзины с контекстом и возвращаем HTML-строку
        return render_to_string(
            "carts/includes/included_cart.html", context, request=request
        )