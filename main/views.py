from django.http import HttpResponse
from django.shortcuts import render

#Импорт моделей таблиц из БД
from products.models import Categories

# Контроллер главной страницы index
def index(request):
    context={
        'title': 'HelloMobile - Главная',
        'content': 'Магазин по продаже мобильных телефонов HelloMobile',
    }
    return render(request, 'main/index.html', context)

#Контроллер страницы about 
def about(request):
    context={
        'title': 'HelloMobile - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том почему магазин такой классный'
    }
    return render(request, 'main/about.html', context)