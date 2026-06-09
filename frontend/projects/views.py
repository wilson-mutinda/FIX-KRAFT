from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Projects
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Projects.objects.all()

    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated]