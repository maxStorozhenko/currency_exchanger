import django_filters

from rate.models import Rate


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = ['source', 'currency_type', 'rate_type']
