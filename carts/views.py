from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from products.models import Products






# Представление для добавления товара в корзину.
# Позволяет добавлять товары в корзину, обрабатывая POST-запросы.
# Если пользователь аутентифицирован, товар добавляется в корзину пользователя.
# Если пользователь не аутентифицирован, товар добавляется в корзину сессии.
# Возвращает JSON-ответ с сообщением об успехе и обновленным HTML-фрагментом корзины.

class CartAddView(CartMixin, View):
    
    # Обрабатывает POST-запрос для добавления товара в корзину.
    # JsonResponse: JSON-ответ с сообщением об успехе и обновленным HTML-фрагментом корзины.
    def post(self, request):
        product_id = request.POST.get("product_id")  # Получаем ID товара из POST-запроса
        product = Products.objects.get(id=product_id)  # Получаем объект товара по ID
        cart = self.get_cart(request, product=product) # Получаем корзину для данного товара.
        if cart:
            # Если товар уже есть в корзине, увеличиваем количество
            cart.quantity += 1
            cart.save()
        else:
            # Если товара нет в корзине, создаем новую запись
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)
        response_data = {
            "message": "Товар добавлен в корзину",
            'cart_items_html': self.render_cart(request) # Обновляем отображение корзины
        }
        return JsonResponse(response_data)




# Представление для изменения количества товара в корзине.
# Позволяет изменять количество товара в корзине, обрабатывая POST-запросы.
# Возвращает JSON-ответ с сообщением об успехе, новым количеством товара и обновленным HTML-фрагментом корзины.
class CartChangeView(CartMixin, View):
    
    # Обрабатывает POST-запрос для изменения количества товара в корзине.
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get("quantity") # Получаем новое количество товара из POST-запроса
        cart.save()
        quantity = cart.quantity
        response_data = {
            "message": "Количество изменено",
            "quantity": quantity,
            'cart_items_html': self.render_cart(request) # Обновляем отображение корзины
        }
        return JsonResponse(response_data)




# Представление для удаления товара из корзины.
# Позволяет удалять товар из корзины, обрабатывая POST-запросы.
# Возвращает JSON-ответ с сообщением об успехе, количеством удаленных товаров и обновленным HTML-фрагментом корзины.
class CartRemoveView(CartMixin, View):
    
    # Обрабатывает POST-запрос для удаления товара из корзины.
    # JsonResponse: JSON-ответ с сообщением об успехе, количеством удалённых товаров и обновленным HTML-фрагментом корзины.
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete() # Удаляем товар из корзины
        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request) # Обновляем отображение корзины
        }
        return JsonResponse(response_data)