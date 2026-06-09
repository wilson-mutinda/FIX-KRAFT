from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    UserSerializer
)


# REGISTER
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


# CURRENT USER
class UserView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get_object(self):

        return self.request.user