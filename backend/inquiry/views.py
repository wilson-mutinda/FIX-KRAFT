from django.shortcuts import render
from rest_framework import viewsets

from .models import Inquiry
from .serializers import InquirySerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

class InquiryViewSet(viewsets.ModelViewSet):
    
    queryset = Inquiry.objects.all().order_by('-created_at')

    serializer_class = InquirySerializer

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        # Count inquiries with status 'new'
        count = self.get_queryset().filter(status='new').count()
        return Response({'count': count})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_inquiries(self, request):
        # get client linked to the logged-in user
        try:
            client = request.user.client
        except AttributeError:
            return Response({"detail": "Client profile not found."}, status=404)
        
        inquiries = self.get_queryset().filter(client=client)
        serializer = self.get_serializer(inquiries, many=True)
        return Response(serializer.data)
