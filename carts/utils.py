from carts.models import Cart



# Возвращает QuerySet объектов Cart, соответствующих текущему пользователю или сессии.
# Если пользователь аутентифицирован, возвращает корзины, связанные с пользователем.
# Если пользователь анонимный, возвращает корзины, связанные с текущей сессией.
def get_user_carts(request):
    
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Возвращаем корзины пользователя с подгрузкой связанных товаров (оптимизация запросов)
        return Cart.objects.filter(user=request.user).select_related('product')
    
    # Если сессия еще не создана, создаем новую сессию
    if not request.session.session_key:
        request.session.create()
    # Возвращаем корзины, связанные с текущим session_key, с подгрузкой связанных товаров
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
