from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_at')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = BlogPost.objects.all().order_by('-published_at')
        status_param = self.request.query_params.get('status')
        slug_param = self.request.query_params.get('slug')
        if status_param == 'published':
            qs = qs.filter(status='published')
        if slug_param:
            qs = qs.filter(slug=slug_param)
        return qs
