from django.core.cache import cache
from django.conf import settings
from github import Github
from ..models import Projects
from ..utils.database_utils import diff_db_and_cache


class GetGithubData:
    """Получение данных с GitHub, сохранение их в кэш и обновление БД"""

    @staticmethod
    def _data_caching() -> tuple:
        """
        Получает данные с GitHub и сохраняет их в кэш
        :return: кортеж данных из кэша и флага, который говорит обновлялся ли кэш
        """
        # username = 'BugBountyHuntr'
        username = 'beplop'

        # Проверяем, есть ли данные в кеше
        cached_data = cache.get('github_data')

        if cached_data:
            return cached_data, False
        else:
            # Если данных нет в кеше, выполняем запрос к API GitHub
            g = Github(settings.MY_GITHUB_TOKEN)
            # g = Github()
            user = g.get_user(username)
            repos = user.get_repos()
            data = []  # =[] если нет репозиториев

            # if repos.totalCount == 0:

            for repo in repos:
                data.append({
                    'repo_id': repo.id,
                    'name': repo.name,
                    'description': repo.description,
                    'language': repo.language,
                    'date': repo.created_at,
                    'html_url': repo.html_url,
                })

            # Сохраняем результаты запроса в кеше на 20 минут
            cache.set('github_data', data, 60 * 20)

            return data, True

    def update_database(self) -> None:
        """
        Обновляет БД, если кэш был обновлен
        :return:
        """
        data, cache_is_updated = self._data_caching()

        # Актуализируем БД только если кэш обновлялся
        if cache_is_updated:
            # Удаляем из БД неактуальные репозитории, которых уже нет на гитхабе (а значит нет в обновленном кэше)
            diff = diff_db_and_cache(data)
            for el in diff:
                Projects.objects.filter(repo_id=el).delete()

            for el in data:
                # Если в БД уже есть запись с определенным репозиторием, то обновляем ее, тем самым делая актуальной
                if Projects.objects.filter(repo_id=el['repo_id']).exists():
                    Projects.objects.filter(repo_id=el['repo_id']).update(name=el['name'], descript=el['description'],
                                                                          date=el['date'],
                                                                          language=el['language'], url=el['html_url'])
                else:
                    p = Projects(repo_id=el['repo_id'], name=el['name'], descript=el['description'],
                                 date=el['date'], language=el['language'], url=el['html_url'])
                    p.save()
