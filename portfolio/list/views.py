from .models import Projects
from github import Github
from . import git_token

from django.core.cache import cache
from .filters import ProjectsFilter
from django_filters.views import FilterView


def repo_id_in_database() -> list[int]:
    ids_in_db = list()
    for el in Projects.objects.values_list('repo_id'):
        ids_in_db.append(el[0])
    return ids_in_db


def repo_id_in_cache(data: list[dict]) -> list[int]:
    ids_in_cache = list()
    for el in data:
        ids_in_cache.append(el['repo_id'])
    return ids_in_cache


def diff_db_and_cache(ids_in_db: list[int], ids_in_cache: list[int]) -> list[int]:
    diff_db_and_cache = list()
    for el in ids_in_db:
        if el not in ids_in_cache:
            diff_db_and_cache.append(el)
    return diff_db_and_cache


class ProjectsFilterView(FilterView):
    model = Projects
    template_name = 'list/index.html'
    filterset_class = ProjectsFilter

    def get_github_data(self) -> tuple:
        # username = 'BugBountyHuntr'
        username = 'beplop'

        # Проверяем, есть ли данные в кеше
        cached_data = cache.get('github_data')

        if cached_data:
            return cached_data, False
        else:
            # Если данных нет в кеше, выполняем запрос к API GitHub
            g = Github(git_token.my_token)
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
            cache.set('github_data', data, 5)

            return data, True

    def update_database(self):
        data, cache_is_updated = self.get_github_data()

        # Актуализируем БД только если кэш обновлялся
        if cache_is_updated:
            # Удаляем из БД неактуальные репозитории, которых уже нет на гитхабе (а значит нет в обновленном кэше)
            ids_in_db = repo_id_in_database()
            ids_in_cache = repo_id_in_cache(data)
            diff = diff_db_and_cache(ids_in_db, ids_in_cache)
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

    # Актуализируем БД и применяем сортировку
    def get_queryset(self):
        self.update_database()
        queryset = super().get_queryset()

        order_direction = self.request.GET.get('order')

        if order_direction == 'asc':
            queryset = queryset.order_by('date')
        else:
            queryset = queryset.order_by('-date')

        return queryset

    # Передаем данные в index.html для отображения текущей сортировки в <select>
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_direction = self.request.GET.get('order')
        context['order_direction'] = order_direction
        return context
