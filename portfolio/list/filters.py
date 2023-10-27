from django_filters import FilterSet, ModelChoiceFilter

from .models import Projects


class ProjectsFilter(FilterSet):
    # gits = Projects.objects.all()
    # set_languages = set()
    # for el in gits:
    #     set_languages.add(el.language)
    # language = CharFilter(lookup_expr='in')
    # language = ModelChoiceFilter(queryset=Projects.)

    class Meta:
        model = Projects
        fields = ['language']
