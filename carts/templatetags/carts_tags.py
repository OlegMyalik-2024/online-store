# Файл для создания шаблонных тэгов
from django import template

from carts.models import Cart

register=template.Library() #регистрация шаблонного тэга

#Метод возвращающий все корзины определенного пользователя
@register.simple_tag()
def user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)