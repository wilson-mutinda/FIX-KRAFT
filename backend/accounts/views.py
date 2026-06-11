from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    UserSerializer
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from inquiry.models import Inquiry
from clients.models import Client
from quotation.models import Quotation
from payment.models import Payment

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

@api_view(['GET'])
def get_counts(request):
    return Response({
        'inquiries_new': Inquiry.objects.filter(status='new').count(),
        'clients_total': Client.objects.count(),
        'quotations_pending': Quotation.objects.filter(status='pending').count(),
        'payments_total': Payment.objects.count(),
    })    
