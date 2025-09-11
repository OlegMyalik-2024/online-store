from products.models import Products
from products.utils import q_search
from django.views.generic import DetailView, ListView
from django.http import Http404





# Контроллер страницы каталога товаров
class CatalogView(ListView):
    model = Products  # Используемая модель данных - товары
    template_name = "products/catalog.html"  # Шаблон для отображения каталога
    context_object_name = "products"  # Имя переменной, в которой товары будут переданы в шаблон
    paginate_by = 3  # Количество товаров на странице
    allow_empty = False # Вызывает 404 ошибку, если страница пустая
    # Для удобной передачи аргумента из URL в методы класса.
    slug_url_kwarg = "category_slug"

    # Получает набор товаров для отображения в каталоге.
    # Фильтрует товары по категории, наличию скидки, сортирует по выбранному параметру, а также осуществляет поиск по запросу.
    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg) # Получаем слаг категории из URL
        on_sale = self.request.GET.get("on_sale") # Получаем параметр "on_sale" из GET запроса
        order_by = self.request.GET.get("order_by") # Получаем параметр "order_by" из GET запроса
        query = self.request.GET.get("q") # Получаем поисковой запрос "q" из GET запроса
        if category_slug == "all": # Если категория "all", получаем все товары
            products = super().get_queryset()
        elif query: # Если есть поисковой запрос
            products = q_search(query) # Используем функцию q_search для поиска товаров
        else: # Если категория указана
            products = super().get_queryset().filter(category__slug=category_slug) # Фильтруем товары по слагу категории
            if not products.exists(): # Если товаров в категории не найдено
                raise Http404() # Возвращаем ошибку 404
        if on_sale: # Если указан параметр "on_sale"
            products = products.filter(discount__gt=0) # Фильтруем товары со скидкой больше 0
        if order_by and order_by != "default": # Если указан параметр "order_by" и он не "default"
            products = products.order_by(order_by) # Сортировка товаров
        return products # Возвращаем отфильтрованный и отсортированный набор товаров

    # Добавляет данные в контекст шаблона.    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HelloMobile - Каталог" # Задаем заголовок страницы
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg) # Добавляем слаг текущей категории в контекст
        return context



# Контроллер страницы товара
class ProductView(DetailView):
    template_name = "products/product.html" # Шаблон для отображения страницы товара
    slug_url_kwarg = "product_slug" # Имя параметра слаг товара в URL
    context_object_name = "product" # Имя переменной в шаблоне, содержащей информацию о товаре

    # Получает объект товара по его слагу.
    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg)) # Получаем товар по слагу из URL
        return product

    # Добавляет данные в контекст шаблона страницы товара.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name # Задаем заголовок страницы равным имени товара
        return context