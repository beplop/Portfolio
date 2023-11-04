from django_filters import FilterSet, ChoiceFilter

from .models import Projects


# Берем уникальные значения из поля language (за исключением None) и возвращаем список этих значений
def get_choices(model, field):
    choices = []
    for k in model.objects.values_list(field).distinct():
        if k[0] != None:
            choices.append((k[0], k[0]))
    return choices


# Используем ChoiceFilter, т.к. ModelChoiceFilter работает только с уникальными значениями
class ProjectsFilter(FilterSet):
    language = ChoiceFilter(choices=get_choices(Projects, 'language'))

    class Meta:
        model = Projects
        fields = ['language']
