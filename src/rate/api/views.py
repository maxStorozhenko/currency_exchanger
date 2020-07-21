from rate.api.serializers import RateSerializer
from rate.models import Rate

from rest_framework import generics

from rate.selectors import get_latest_rates


class RateListCreateView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class LatestRatesListView(generics.ListAPIView):
    queryset = get_latest_rates()
    serializer_class = RateSerializer
