import django_filters
from .models import *

class ClientFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Client
        fields = {
            'first_name': ['icontains'],
            'client_id': ['icontains'],
        }

    def filter_by_order(self,queryset, name, value):
        expression = 'date_created' if value == 'ascending' else '-date_created'
        return queryset.order_by(expression)
