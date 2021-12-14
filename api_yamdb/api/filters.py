from django_filters import FilterSet, filters

from reviews.models import Title


class TitlesFilter(FilterSet):
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains')
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains')
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains')
    year = filters.NumberFilter()

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
