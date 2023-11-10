from ..models import Projects


def diff_db_and_cache(data: list[dict]) -> list[int]:
    """
    Находит различающиеся данные в БД и кэше по repo_id. Эти данные больше неактуальны для БД.
    :param data: кэш (список словарей) с актуальными данными
    :return: список с неактуальными repo_id в БД, которые следует удалить
    """
    diff_db_and_cache = list()
    cache = [x['repo_id'] for x in data]
    db = Projects.objects.values_list('repo_id')
    for el in db:
        if el[0] not in cache:
            diff_db_and_cache.append(el[0])
    return diff_db_and_cache
