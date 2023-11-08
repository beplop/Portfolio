from .models import Projects
from .filters import ProjectsFilter
from django_filters.views import FilterView
from .update_database import UpdateDB


class ProjectsFilterView(FilterView):
    model = Projects
    template_name = 'list/index.html'
    filterset_class = ProjectsFilter

    # Актуализируем БД и применяем сортировку
    def get_queryset(self):
        update_db = UpdateDB()
        update_db.update_database()
        queryset = super().get_queryset()

        order_direction = self.request.GET.get('order')

        if order_direction == 'asc':
            queryset = queryset.order_by('date')
        else:
            queryset = queryset.order_by('-date')

        return queryset

    # Передаем данные в index.html для отображения текущей сортировки в <select>
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_direction = self.request.GET.get('order')
        context['order_direction'] = order_direction
        return context
