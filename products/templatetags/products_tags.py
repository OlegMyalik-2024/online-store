# Файл для создания шаблонных тэгов
from django import template
from products.models import Categories

register=template.Library() #регистрация шаблонного тэга

#Метод возвращающий категорию товара
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()