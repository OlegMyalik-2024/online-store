# Файл для сохранения рандомных дополнительных функций

from products.models import Products
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)


# Функция поиска товаров по запросу
def q_search(query):
    # Если запрос состоит только из цифр и его длина не превышает 5 символов, то ищем товар по id
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    # Создаем вектор поиска, указывающий, в каких полях модели Products искать
    vector = SearchVector("name", "description")
    # Преобразуем поисковый запрос в объект SearchQuery
    query = SearchQuery(query)
    # Выполняем поиск, аннотируем результаты рангом соответствия и фильтруем
    # товары с рангом больше 0 (то есть те, которые соответствуют запросу)
    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank") # Сортируем по убыванию релевантности
    )
    # Подсвечиваем найденные слова в названии товара
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color:yellow;">',
            stop_sel="</span>",
        )
    )
    # Подсвечиваем найденные слова в описании товара
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color:yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.filter(image__isnull=False)  # Исключаем товары без изображений
    return result