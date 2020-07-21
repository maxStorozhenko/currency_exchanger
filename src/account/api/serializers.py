from account.models import User, Contact

from rest_framework import serializers

from account.tasks import send_email_async


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
