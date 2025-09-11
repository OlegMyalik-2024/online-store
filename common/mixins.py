from django.core.cache import cache  




# Миксин для добавления функциональности кэширования в классы.
# Позволяет кэшировать результаты запросов или данных, чтобы избежать повторных вычислений.
class CacheMixin:
    
    # Метод для получения данных из кэша или выполнения запроса и кэширования результата. 
    def set_get_cache(self, query, cache_name, cache_time):
        # Попытка получить данные из кэша по ключу cache_name
        data = cache.get(cache_name)
        # Если данных в кэше нет (data равно None)
        if not data:
            # Присваиваем данные из query (здесь предполагается, что query - это результат)
            data = query
            # Сохраняем данные в кэш с указанным временем жизни
            cache.set(cache_name, data, cache_time)
        # Возвращаем данные (из кэша или новые)
        return data