from django.core.cache import cache
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView





# Класс для обработки формы авторизации пользователя
class UserLoginView(LoginView):
    template_name = 'users/login.html'  # Шаблон страницы входа
    form_class = UserLoginForm  # Форма для входа

    # Определение URL для успешного входа
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)  # Получаем URL из параметра next
        if redirect_page and redirect_page != reverse('user:logout'):  # Проверяем, что это не logout
            return redirect_page  # Перенаправляем на исходную страницу
        return reverse_lazy('main:index')  # Иначе на главную страницу
    
    # Обработка валидной формы входа
    def form_valid(self, form):
        session_key = self.request.session.session_key  # Получаем ключ сессии
        user = form.get_user()  # Получаем пользователя из формы
        if user:
            auth.login(self.request, user)  # Логиним пользователя
            if session_key:
                # Удаляем старые корзины пользователя, если есть
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # Привязываем корзину из сессии к пользователю
                Cart.objects.filter(session_key=session_key).update(user=user)
                # Показываем сообщение об успешном входе
                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт!")
                # Перенаправляем на нужный URL
                return HttpResponseRedirect(self.get_success_url())

    # Добавление заголовка страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Авторизация'
        return context






# Класс для обработки регистрации нового пользователя
class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'  # Шаблон регистрации
    form_class = UserRegistrationForm  # Форма регистрации
    success_url = reverse_lazy('users:profile')  # URL после успешной регистрации

    # Обработка валидной формы регистрации
    def form_valid(self, form):
        session_key = self.request.session.session_key  # Ключ сессии
        user = form.instance  # Новый пользователь (экземпляр модели)
        if user:
            form.save()  # Сохраняем пользователя
            auth.login(self.request, user)  # Логиним нового пользователя
        if session_key:
            # Переносим корзину из сессии на пользователя
            Cart.objects.filter(session_key=session_key).update(user=user)
        # Сообщение об успешной регистрации и входе
        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт!")
        return HttpResponseRedirect(self.success_url)

    # Добавление заголовка страницы в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Регистрация'
        return context





# Класс для отображения и редактирования личного кабинета пользователя
class UserProfileView(LoginRequiredMixin, UpdateView, CacheMixin):
    template_name = 'users/profile.html'  # Шаблон профиля
    form_class = ProfileForm  # Форма редактирования профиля
    success_url = reverse_lazy('users:profile')  # URL после успешного обновления

    # Получаем объект пользователя для редактирования (текущий пользователь)
    def get_object(self, queryset=None):
        return self.request.user
    
    # Обработка успешного обновления профиля
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)
    
    # Обработка ошибок при обновлении профиля
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка!")
        return super().form_invalid(form)
    
    # Добавляем в контекст данные для шаблона, включая заказы пользователя
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Кабинет'
      
        # Получаем заказы пользователя с предзагрузкой товаров для оптимизации запросов
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
          
        # Используем кеширование заказов на 2 минуты для повышения производительности
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60*2)
        return context





# Класс для отображения корзины пользователя
class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'  # Шаблон корзины

    # Добавляем заголовок страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Корзина'
        return context






# Функция для выхода пользователя из системы
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта!")  # Сообщение об выходе
    auth.logout(request)  # Выход пользователя
    return redirect(reverse("main:index"))  # Перенаправление на главную страницу






# Класс для обработки запроса на сброс пароля (ввод email)
class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset/password_reset.html'  # Шаблон формы сброса пароля
    email_template_name = 'users/password_reset/password_reset_email.html'  # Шаблон email для сброса
    success_url = reverse_lazy('users:password_reset_done')  # URL после отправки письма
    subject_template_name = 'users/password_reset/password_reset_subject.txt'  # Тема письма

    # Добавляем заголовок страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Сброс пароля'
        return context







# Класс для отображения страницы подтверждения отправки email для сброса пароля
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset/password_reset_done.html'  # Шаблон страницы

    # Добавляем заголовок страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Сброс пароля отправлен'
        return context







# Класс для подтверждения сброса пароля (ввод нового пароля)
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset/password_reset_confirm.html'  # Шаблон формы нового пароля
    success_url = reverse_lazy('users:password_reset_complete')  # URL после успешного сброса

    # Добавляем заголовок страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Новый пароль'
        return context






# Класс для отображения страницы успешного сброса пароля
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset/password_reset_complete.html'  # Шаблон страницы успеха

    # Добавляем заголовок страницы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Пароль изменен'
        return context
