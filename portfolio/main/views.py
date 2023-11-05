from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 30)
def index(request):
    data = {
        'title': 'Обо мне',
    }
    return render(request, 'main/index.html', data)
