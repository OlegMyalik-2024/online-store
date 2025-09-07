from django.shortcuts import render

#Контроллер обработки добавления товара в корзину
def cart_add(request, product_id):
    ...

#Контроллер обработки изменения количества товара в корзине    
def cart_change(request, product_id):
    ...
    
#Контроллер обработки удаления товара из корзины
def cart_remove(request, product_id):
    ...