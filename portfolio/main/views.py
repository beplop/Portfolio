from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    data = {
        'title': 'Обо мне',
        'values': ['some', 'hello', '123']
    }
    return render(request, 'main/index.html', data)
