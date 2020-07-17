from account.api.serializers import AccountSerializer
from account.models import User

from rest_framework import generics


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class UserReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
