# Файл для создания шаблонных тэгов
from django import template
from django.utils.http import urlencode
from products.models import Categories

register=template.Library() #регистрация шаблонного тэга

#Метод возвращающий категорию товара
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query=context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)