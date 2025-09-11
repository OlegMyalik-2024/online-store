from django.views.generic import TemplateView




# Контроллер главной страницы index
class IndexView(TemplateView):
    # Указание имени шаблона для рендеринга страницы
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        # Получение базового контекста от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавление заголовка страницы в контекст
        context['title'] = 'HelloMobile - Главная'
        # Добавление основного содержимого страницы в контекст
        context['content'] = "Интернет-магазин HelloMobile"
        # Возврат обновленного контекста
        return context
   
   
   
    
# Контроллер страницы about 
class AboutView(TemplateView):
    # Указание имени шаблона для страницы "О нас"
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        # Получение базового контекста от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавление заголовка страницы в контекст
        context['title'] = 'HelloMobile - О нас'
        # Добавление основного содержимого страницы в контекст
        context['content'] = "Почему HelloMobile — ваш идеальный магазин для мобильных устройств?"
       
        # Определение HTML-кода для содержимого страницы "О нас"
        about_html = """
            <div class="about-highlight">
                <p><strong>HelloMobile</strong> — это магазин, которому доверяют тысячи покупателей. 
                    Мы предлагаем лучшие смартфоны и гаджеты по ценам ниже рыночных, сохраняя высокое 
                    качество и надежность.</p>
                <p>Быстрая доставка, удобные форматы покупки — онлайн, через приложение или в магазинах 
                    — делают процесс максимально комфортным.</p>
                <p>Наша команда экспертов всегда готова помочь с выбором, настройкой и любыми вопросами, 
                    чтобы вы остались довольны каждой покупкой.</p>
            </div>
        """
        # Добавление HTML-содержимого в контекст и удаление лишних пробелов
        context['text_on_page'] = about_html.strip()  
        # Возврат обновленного контекста
        return context
    
  
  
  
    
# Контроллер страницы contacts 
class ContactsView(TemplateView):
    # Указание имени шаблона для страницы контактов
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        # Получение базового контекста от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавление заголовка страницы в контекст
        context['title'] = 'HelloMobile - Контакты'
        # Добавление основного содержимого страницы в контекст
        context['content'] = "Наши контакты"
       
        # Определение HTML-кода для содержимого страницы контактов
        contacts_html = """
            <div class="contact-page">
                <h3>Связаться с нами</h3>
                <p>У вас есть вопрос, нужна помощь с заказом или хотите узнать больше о товарах? 
                    Мы всегда на связи!</p>
                <p><strong>Телефон:</strong> +375 (29) 123-45-67<br>
                <strong>Email:</strong> support@hellomobile.by<br>
                <strong>Часы работы:</strong> Пн–Вс, 9:00–21:00</p>
                <p><strong>Адрес офиса:</strong> г. Минск, ул. Филимонова, 10</p>
                <p>Подписывайтесь на нас в соцсетях, чтобы быть в курсе акций и новинок!</p>
            </div>
        """
        # Добавление HTML-содержимого в контекст и удаление лишних пробелов
        context['text_on_page'] = contacts_html.strip()  
        # Возврат обновленного контекста
        return context  
   
   
   
    
# Контроллер страницы delivery_and_payment 
class Delivery_and_paymentView(TemplateView):
    # Указание имени шаблона для страницы доставки и оплаты
    template_name = 'main/delivery_and_payment.html'

    def get_context_data(self, **kwargs):
        # Получение базового контекста от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавление заголовка страницы в контекст
        context['title'] = 'HelloMobile - Доставка и оплата'
        # Добавление основного содержимого страницы в контекст
        context['content'] = "Доставка и оплата"
       
        # Определение HTML-кода для содержимого страницы доставки и оплаты
        delivery_and_payment_html = """
            <div class="delivery-payment">
                <h3>Доставка и оплата</h3>
                <p><strong>Доставка по всей Беларуси:</strong> Курьером, почтой или в пункты самовывоза. 
                    Срок — от 1 до 3 дней.</p>
                <p><strong>Бесплатная доставка:</strong> При заказе от 500 BYN — мы доставим бесплатно.</p>
                <p><strong>Способы оплаты:</strong> Онлайн-картой, наличными при получении или при 
                    получении картой.</p>
                <p>Все заказы сопровождаются гарантией, а возврат возможен в течение 14 дней. Покупать у нас 
                    — просто и безопасно.</p>
            </div>
        """
        # Добавление HTML-содержимого в контекст и удаление лишних пробелов
        context['text_on_page'] = delivery_and_payment_html.strip()  
        # Возврат обновленного контекста
        return context