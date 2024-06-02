from rest_framework import serializers
from .models import ContactUser


class ContactUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUser
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone', )