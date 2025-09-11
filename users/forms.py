from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User




# Форма для авторизации пользователя, наследующая от AuthenticationForm
class UserLoginForm(AuthenticationForm):
    # Внутренний класс Meta для указания модели и полей формы
    class Meta:
        model = User  # Связь с моделью User
        fields = ['username', 'password']  # Поля, используемые в форме (имя пользователя и пароль)
  
  
  
  
        
# Форма для регистрации нового пользователя, наследующая от UserCreationForm
class UserRegistrationForm(UserCreationForm):
    # Внутренний класс Meta для указания модели и полей формы
    class Meta:
        model = User  # Связь с моделью User
        fields = (  # Кортеж полей, включенных в форму
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )
    # Определение полей формы как CharField (хотя в Meta они уже указаны, это может быть избыточно)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
   
   
   
   
   
                
# Форма для редактирования профиля пользователя, наследующая от UserChangeForm
class ProfileForm(UserChangeForm):
    # Внутренний класс Meta для указания модели и полей формы
    class Meta:
        model = User  # Связь с моделью User
        fields = (  # Кортеж полей для редактирования профиля
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
        )
    # Определение полей формы (image как ImageField, остальные как CharField)
    image = forms.ImageField(required=False)  # Поле для загрузки изображения, необязательное
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()