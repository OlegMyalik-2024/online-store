# Файл для создания шаблонных тэгов
from django import template

from carts.models import Cart
from carts.utils import get_user_carts

register=template.Library() #регистрация шаблонного тэга

#Метод возвращающий все корзины определенного пользователя
@register.simple_tag()
def user_carts(request):
    return get_user_carts(request)