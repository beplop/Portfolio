from django.urls import path
from . import views

urlpatterns = [
    # path('', views.list_git, name='list_git'),
    path('', views.ProjectsFilterView.as_view(), name='list_git'),
]
