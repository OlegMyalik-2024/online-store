from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


from users.forms import UserLoginForm, UserRegistrationForm


# Обработка авторизации пользователя
def login(request):
    #Обработка формы
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form=UserLoginForm()
    context={
        'title': 'HelloMobile - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)



# Обработка регистрации пользователя
def registration(request):
    #Обработка формы
    if request.method=='POST':
        form=UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user=form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form=UserRegistrationForm()
    context={
        'title': 'HelloMobile - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)



# Обработка кабинета пользователя
def profile(request):
    context={
        'title': 'HelloMobile - Кабинет'
    }
    return render(request, 'users/profile.html', context)


# Обработка выхода пользователя из системы
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))