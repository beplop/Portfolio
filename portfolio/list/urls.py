from django.urls import path
from . import views

urlpatterns = [
    # path('', views.list_git, name='list_git'),
    path('', views.ProjectsListView.as_view(), name='list_git'),
]
