#Связь формы которая находится в HTML-разметке с определенной таблицей БД и проверка данных на валидность
#В основоном это все требуется при передаче данных при POST-запросе
from django import forms
#Импорт уже готовых форм django для регистрации и авторизации 
from django.contrib.auth.forms import AuthenticationForm

from users.models import User

class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username', 'password']
        