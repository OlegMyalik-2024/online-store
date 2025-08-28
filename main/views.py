from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context={
        'title': 'HelloMobile - Главная',
        'content': 'Магазин по продаже мобильных телефонов HelloMobile'
    }
    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('About page')