from django.shortcuts import render

#Обработка создания заказа
def create_order(request):
    return render(request, 'orders/create_order.html')
