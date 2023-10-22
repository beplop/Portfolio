from django.shortcuts import render
from .models import Projects


def list_git(request):
    gits = Projects.objects.all().order_by('title')
    return render(request, 'list/index.html', {'gits': gits})
