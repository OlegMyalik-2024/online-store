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
        context['content'] = "О нас"
        context['text_on_page'] = "Текст о том почему этот магазин такой классный, и какой хороший товар."
        return context