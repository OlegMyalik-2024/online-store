import re
from django import forms




class CreateOrderForm(forms.Form):
    # Поле для ввода имени — обязательное текстовое поле
    first_name = forms.CharField()
    # Поле для ввода фамилии — обязательное текстовое поле
    last_name = forms.CharField()
    # Поле для ввода номера телефона — обязательное текстовое поле
    phone_number = forms.CharField()
    # Поле выбора необходимости доставки — выбор из двух вариантов: "0" (False) или "1" (True)
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),  # Самовывоз
            ("1", True),   # Нужна доставка
        ],
    )
    # Поле для ввода адреса доставки — необязательное текстовое поле (требуется только если доставка нужна)
    delivery_address = forms.CharField(required=False)
    # Поле выбора способа оплаты — два варианта: "0" (False) и "1" (True)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),  # Оплата картой онлайн
            ("1", 'True'),   # Оплата при получении (наличными или картой)
        ],
    )

    # Метод для валидации поля phone_number.
    # Проверяет, что номер состоит только из цифр и соответствует формату белорусского номера. 
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        # Проверяем, что номер содержит только цифры
        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        # Проверяем, что номер начинается с '375' и далее идут ровно 9 цифр
        pattern = re.compile(r'^375\d{9}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера. Ожидается 375(код оператора)(номер)")
        # Если все проверки пройдены, возвращаем очищенное значение
        return data
