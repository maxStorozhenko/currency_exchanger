from account.api.serializers import AccountSerializer, ContactSerializer
from account.models import Contact, User

from rest_framework import generics


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class UserReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
