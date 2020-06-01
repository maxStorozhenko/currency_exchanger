from django.views.generic import ListView

from rate.models import Rate


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate-list.html'
