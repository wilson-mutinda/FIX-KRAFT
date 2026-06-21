from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Projects
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Projects.objects.all().order_by('-created_at')

    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]