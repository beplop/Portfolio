from django.shortcuts import render
from .models import Projects
from github import Github

from .filters import ProjectsFilter
from django_filters.views import FilterView

username = 'beplop'
g = Github()
user = g.get_user(username)


def get_repos():
    repos = user.get_repos()
    for repo in repos:
        # если в БД уже есть запись с определенным репозиторием, то обновляем ее, тем самым делая актуальной
        if Projects.objects.filter(repo_id=repo.id).exists():
            Projects.objects.filter(repo_id=repo.id).update(name=repo.full_name[7:], descript=repo.description,
                                                            date=repo.created_at,
                                                            language=repo.language, url=repo.html_url)
        else:
            p = Projects(repo_id=repo.id, name=repo.full_name[7:], descript=repo.description, date=repo.created_at,
                         language=repo.language, url=repo.html_url)
            p.save()


class ProjectsListView(FilterView):
    model = Projects
    template_name = 'list/index.html'
    filterset_class = ProjectsFilter

    # context_object_name = 'filter'

    def get_queryset(self):
        get_repos()
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date')
        return queryset


def list_git(request):
    repos = user.get_repos()

    for repo in repos:
        # если в БД уже есть запись с определенным репозиторием, то обновляем ее, тем самым делая актуальной
        if Projects.objects.filter(repo_id=repo.id).exists():
            Projects.objects.filter(repo_id=repo.id).update(name=repo.full_name[7:], descript=repo.description,
                                                            date=repo.created_at,
                                                            language=repo.language, url=repo.html_url)
        else:
            p = Projects(repo_id=repo.id, name=repo.full_name[7:], descript=repo.description, date=repo.created_at,
                         language=repo.language, url=repo.html_url)
            p.save()

    # gits = Projects.objects.all().order_by('date')
    gits = Projects.objects.all()

    # добавляем все используемые языки из репозиториев во множество, чтобы не было повторений
    set_languages = set()
    for el in gits:
        set_languages.add(el.language)

    return render(request, 'list/index.html', {'gits': gits, 'set_languages': set_languages})
