#Связь формы которая находится в HTML-разметке с определенной таблицей БД и проверка данных на валидность
#В основоном это все требуется при передаче данных при POST-запросе
from django import forms
#Импорт уже готовых форм django для регистрации и авторизации 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User

#Форма авторизации пользователя
class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username', 'password']
        
#Форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=(
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )
        first_name=forms.CharField()
        last_name=forms.CharField()
        username=forms.CharField()
        email=forms.CharField()
        password1=forms.CharField()
        password2=forms.CharField()
        