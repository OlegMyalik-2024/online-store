from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from products.models import Products

#Контроллер страницы catalog
def catalog(request, category_slug, page=1):
    if category_slug=='all':
        products_list=Products.objects.all()
    else:
        products_list=get_list_or_404(Products.objects.filter(category__slug=category_slug))
    paginator=Paginator(products_list, 3)
    current_page=paginator.page(page)
    context = {
        'title': 'HelloMobile - Каталог',
        'products': current_page,
        'slug_url': category_slug
    }
    return render(request, 'products/catalog.html', context)

#Контроллер страницы product
def product(request, product_slug):
    product=Products.objects.get(slug=product_slug)
    context={
        'product': product
    }
    return render(request, 'products/product.html', context=context)
    