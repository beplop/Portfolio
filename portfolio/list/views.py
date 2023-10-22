from django.shortcuts import render
from .models import Projects
from github import Github

username = 'beplop'
g = Github()
user = g.get_user(username)


def list_git(request):
    repos = user.get_repos()

    for repo in repos:
        if Projects.objects.filter(name=repo.full_name[7:]).exists():
            pass  # надо апдейтить
        else:
            p = Projects(name=repo.full_name[7:], descript=repo.description, date=repo.created_at,
                         language=repo.language)
            p.save()

    gits = Projects.objects.all().order_by('date')
    return render(request, 'list/index.html', {'gits': gits})
