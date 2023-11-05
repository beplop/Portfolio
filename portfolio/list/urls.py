from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectsFilterView.as_view(), name='list_git'),
]
