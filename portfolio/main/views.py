from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import cache_page


@cache_page(60 * 30)
def index(request):
    data = {
        'title': 'Обо мне',
        'pdf_cv': settings.PDF_CV
    }
    return render(request, 'main/index.html', data)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404 Страница не найдена</h1>')
