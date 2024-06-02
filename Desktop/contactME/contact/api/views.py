from rest_framework import generics, permissions
from .models import ContactUser
from .serializers import ContactUserSerializer

class ContactList(generics.ListCreateAPIView):
    queryset = ContactUser.objects.all()
    serializer_class = ContactUserSerializer
    permission_classes = (permissions.AllowAny,)


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUser.objects.all()
    serializer_class = ContactUserSerializer