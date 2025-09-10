from products.models import Products
from products.utils import q_search
from django.views.generic import DetailView, ListView
from django.http import Http404

#Контроллер страницы catalog
class CatalogView(ListView):
    model = Products
    template_name = "products/catalog.html"
    context_object_name = "products"
    paginate_by = 3
    allow_empty = False
    # чтоб удобно передать в методы
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all":
            products = super().get_queryset()
        elif query:
            products = q_search(query)
        else:
            products = super().get_queryset().filter(category__slug=category_slug)
            if not products.exists():
                raise Http404()

        if on_sale:
            products = products.filter(discount__gt=0)

        if order_by and order_by != "default":
            products = products.order_by(order_by)

        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HelloMobile - Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context



#Контроллер страницы product
class ProductView(DetailView):
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context