from rate.api.serializers import RateSerializer
from rate.models import Rate
from rate.selectors import get_latest_rates

from rest_framework import generics


class RateListCreateView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class LatestRatesListView(generics.ListAPIView):
    queryset = get_latest_rates()
    serializer_class = RateSerializer
