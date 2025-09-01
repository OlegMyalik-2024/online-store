from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from products.models import Products

#Контроллер страницы catalog
def catalog(request, category_slug):
    page=request.GET.get('page', 1)
    on_sale=request.GET.get('on_sale', None)
    order_by=request.GET.get('order_by', None)
    
    if category_slug=='all':
        products_list=Products.objects.all()
    else:
        products_list=get_list_or_404(Products.objects.filter(category__slug=category_slug))
    
    if on_sale:
        products_list = products_list.filter(discount__gt=0)
   
    if order_by and order_by != 'default':
        products_list=products_list.order_by(order_by)
        
    paginator=Paginator(products_list, 3)
    current_page=paginator.page(int(page))
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
    