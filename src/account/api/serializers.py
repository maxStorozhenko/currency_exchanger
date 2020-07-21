from account.models import Contact, User
from account.tasks import send_email_async

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('email_from', 'subject', 'message')

    def create(self, validated_data):
        obj = super().create(validated_data)
        send_email_async.delay(validated_data)
        return obj
