from django.shortcuts import render


# Обработка авторизации пользователя
def login(request):
    context={
        'title': 'HelloMobile - Авторизация'
    }
    return render(request, 'users/login.html', context)



# Обработка регистрации пользователя
def registration(request):
    context={
        'title': 'HelloMobile - Регистрация'
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
    ...