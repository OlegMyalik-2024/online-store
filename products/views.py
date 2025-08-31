from django.shortcuts import render

from products.models import Products

#Контроллер страницы catalog
def catalog(request):
    products_list=Products.objects.all()
    context = {
        'title': 'HelloMobile - Каталог',
        'products': products_list
    }
    return render(request, 'products/catalog.html', context)

#Контроллер страницы product
def product(request):
    return render(request, 'products/product.html')
    