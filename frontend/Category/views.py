from django.shortcuts import render
from rest_framework import viewsets
from .models import MediaCategory
from .serializers import MediaCategorySerializer

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class MediaCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MediaCategorySerializer

    queryset = MediaCategory.objects.filter(
        is_deleted=False
    ).order_by('name')

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):

        category = MediaCategory.objects.get(pk=pk)

        category.restore()

        return Response({
            'message': 'Category restored successfully',
            'info': category.name
        })
    