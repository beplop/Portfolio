from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter

from .models import Projects


def get_choices(model, field):
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


class ProjectsFilter(FilterSet):
    language = ChoiceFilter(choices=get_choices(Projects, 'language'))

    class Meta:
        model = Projects
        fields = ['language']
