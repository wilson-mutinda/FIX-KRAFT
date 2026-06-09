from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Mediahub
from .serializers import MediahubSerializer

class MediahubViewSet(viewsets.ModelViewSet):

    serializer_class = MediahubSerializer

    queryset = Mediahub.objects.filter(
        is_deleted=False
    ).order_by('-uploaded_at')

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):

        media = Mediahub.objects.get(pk=pk)

        media.restore()

        return Response({
            'message': 'Media restored successfully'
        })