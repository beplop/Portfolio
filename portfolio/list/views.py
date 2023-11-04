from .models import Projects
from github import Github
from . import git_token

from django.core.cache import cache
from .filters import ProjectsFilter
from django_filters.views import FilterView


# def get_repos():
#     repos = user.get_repos()
#     for repo in repos:
#         # Если в БД уже есть запись с определенным репозиторием, то обновляем ее, тем самым делая актуальной
#         if Projects.objects.filter(repo_id=repo.id).exists():
#             Projects.objects.filter(repo_id=repo.id).update(name=repo.full_name[7:], descript=repo.description,
#                                                             date=repo.created_at,
#                                                             language=repo.language, url=repo.html_url)
#         else:
#             p = Projects(repo_id=repo.id, name=repo.full_name[7:], descript=repo.description, date=repo.created_at,
#                          language=repo.language, url=repo.html_url)
#             p.save()


class ProjectsFilterView(FilterView):
    model = Projects
    template_name = 'list/index.html'
    filterset_class = ProjectsFilter

    def get_github_data(self):
        username = 'beplop'

        # Проверяем, есть ли данные в кеше
        cached_data = cache.get('github_data')

        if cached_data:
            return cached_data, False
        else:
            # Если данных нет в кеше, выполняем запрос к API GitHub
            g = Github(git_token.my_token)
            user = g.get_user(username)
            repos = user.get_repos()
            data = []

            for repo in repos:
                data.append({
                    'repo_id': repo.id,
                    'name': repo.name,
                    'description': repo.description,
                    'language': repo.language,
                    'date': repo.created_at,
                    'html_url': repo.html_url,
                })

            # Сохраняем результаты запроса в кеше на заданное время
            cache.set('github_data', data, 60)

            return data, True

    def update_database(self):
        data, cache_is_updated = self.get_github_data()

        # Актуализируем БД только если кэш обновлялся
        if cache_is_updated:
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_direction = self.request.GET.get('order')
        context['order_direction'] = order_direction
        return context

# def list_git(request):
#     repos = user.get_repos()
#
#     for repo in repos:
#         # если в БД уже есть запись с определенным репозиторием, то обновляем ее, тем самым делая актуальной
#         if Projects.objects.filter(repo_id=repo.id).exists():
#             Projects.objects.filter(repo_id=repo.id).update(name=repo.full_name[7:], descript=repo.description,
#                                                             date=repo.created_at,
#                                                             language=repo.language, url=repo.html_url)
#         else:
#             p = Projects(repo_id=repo.id, name=repo.full_name[7:], descript=repo.description, date=repo.created_at,
#                          language=repo.language, url=repo.html_url)
#             p.save()
#
#     # gits = Projects.objects.all().order_by('date')
#     gits = Projects.objects.all()
#
#     # добавляем все используемые языки из репозиториев во множество, чтобы не было повторений
#     set_languages = set()
#     for el in gits:
#         set_languages.add(el.language)
#
#     return render(request, 'list/index.html', {'gits': gits, 'set_languages': set_languages})
