from django.shortcuts import render
from django.views.generic import TemplateView

# Контроллер главной страницы index
class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Главная'
        context['content'] = "Интернет-магазин HelloMobile"
        return context
    
#Контроллер страницы about 
class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - О нас'
        context['content'] = "Почему HelloMobile — ваш идеальный магазин для мобильных устройств?"
       
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
        context['text_on_page'] = about_html.strip()  
        return context
    
    
#Контроллер страницы contacts 
class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Контакты'
        context['content'] = "Наши контакты"
       
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
        context['text_on_page'] = contacts_html.strip()  
        return context  
    
#Контроллер страницы delivery_and_payment 
class Delivery_and_paymentView(TemplateView):
    template_name = 'main/delivery_and_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HelloMobile - Доставка и оплата'
        context['content'] = "Доставка и оплата"
       
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
        context['text_on_page'] = delivery_and_payment_html.strip()  
        return context  