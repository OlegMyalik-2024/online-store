from django.contrib.auth.mixins import LoginRequiredMixin  
from django.contrib import messages  
from django.core.mail import send_mail
from django.db import transaction  
from django.forms import ValidationError  
from django.shortcuts import redirect
from django.urls import reverse_lazy  
from django.views.generic import FormView  
from carts.models import Cart  
from orders.forms import CreateOrderForm  
from orders.models import Order, OrderItem, OrderitemQueryset
from users.models import User
from django.conf import settings  



# Представление для создания заказа.
# Доступно только авторизованным пользователям (LoginRequiredMixin).
# Использует форму CreateOrderForm и шаблон create_order.html.
class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'  # Шаблон для отображения формы
    form_class = CreateOrderForm  # Класс формы для создания заказа
    success_url = reverse_lazy('users:profile')  # URL для перенаправления после успешной отправки формы

    # Метод для заполнения начальных данных формы.
    # Автоматически подставляет имя и фамилию текущего пользователя. 
    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

 
    # Обработка валидной формы.
    # Создаёт заказ и связанные с ним товары в рамках атомарной транзакции.
    # Проверяет наличие товаров в корзине и их количество на складе.
    # После успешного создания заказа очищает корзину.  
    def form_valid(self, form):
        # Проверка пустой корзины
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            messages.warning(self.request, 'Ваша корзина пуста')
            return redirect('users:profile')
        try:
            with transaction.atomic():  # Гарантирует, что все операции будут выполнены как одна транзакция
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)  # Получаем все товары в корзине пользователя
                if cart_items.exists():
                    # Создаём объект заказа с данными из формы
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    # Создаём объекты заказанных товаров на основе элементов корзины
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = product.name
                        price = product.sell_price()
                        quantity = cart_item.quantity
                        # Проверяем, достаточно ли товара на складе
                        if product.quantity < quantity:
                            raise ValidationError(
                                f'Недостаточное количество товара {name} на складе. '
                                f'В наличии - {product.quantity}'
                            )
                        # Создаём запись OrderItem
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        # Уменьшаем количество товара на складе
                        product.quantity -= quantity
                        product.save()
                    # Очищаем корзину пользователя после оформления заказа
                    cart_items.delete()
                    
                    
                    # Отправка email-уведомления сотрудникам о новом заказе
                    # Получаем список email всех сотрудников (включая текущего, если он сотрудник)
                    staff_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
                    
                    # Формируем тему и тело письма
                    subject = f"Новый заказ №{order.id} от {user.first_name} {user.last_name}"
                    message = (
                        f"Пользователь {user.first_name} {user.last_name} сделал новый заказ.\n"
                        f"Номер заказа: {order.id}\n"
                        f"Телефон: {order.phone_number}\n"
                        f"Статус: {order.status}\n"
                        f"Дата: {order.created_timestamp.strftime('%d.%m.%Y %H:%M')}\n"
                        f"Адрес доставки: {order.delivery_address if order.requires_delivery else 'Самовывоз'}\n"
                        # f"Сумма заказа: {OrderitemQueryset.get_total_cost()} руб.\n"  # Предполагаем, что у модели Order есть метод get_total_cost
                    )
                    
                    if staff_emails:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            staff_emails,
                            fail_silently=False,
                        )
                    
                    
                    # Отправляем сообщение об успешном оформлении заказа
                    messages.success(self.request, 'Заказ оформлен!')
                    # Перенаправляем пользователя на страницу профиля
                    return redirect('users:profile')
        except ValidationError as e:
            # Если возникла ошибка валидации (например, недостаток товара),
            # выводим сообщение об ошибке и возвращаем пользователя обратно к форме
            messages.error(self.request, str(e))
            return redirect('orders:create_order')

 
    # Обработка случая, когда форма не прошла валидацию.
    # Выводит сообщение об ошибке и перенаправляет обратно к форме.   
    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect('orders:create_order')

 
    # Добавляет дополнительные данные в контекст шаблона.
    # В данном случае — заголовок страницы и флаг, что это страница оформления заказа.    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context
    