from django.shortcuts import render

#Контроллер страницы catalog
def catalog(request):
    return render(request, 'products/catalog.html')

#Контроллер страницы product
def product(request):
    return render(request, 'products/product.html')
    