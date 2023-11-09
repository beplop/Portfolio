from django.http import JsonResponse, HttpResponse
from django.views import View
from github import GithubException


class BaseView(View):
    """Базовый класс для всех View, обрабатывает исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except GithubException as g_e:
            return HttpResponse(f'<h1>Что-то не так c подключением к GitHub... ({g_e})</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Что-то пошло не так... ({e})</h1>')

        return response
