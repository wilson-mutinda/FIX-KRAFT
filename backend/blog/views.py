from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import BlogPost
from .serializers import BlogPostSerializer

from django.http import HttpResponse
from django.template import loader
from django.urls import reverse

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_at')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = BlogPost.objects.all().order_by('-published_at')
        status_param = self.request.query_params.get('status')
        slug_param = self.request.query_params.get('slug')
        if status_param == 'published':
            qs = qs.filter(status='published')
        if slug_param:
            qs = qs.filter(slug=slug_param)
        return qs
    
    def sitemap(request):
        static_pages = [
            {'url': '/', 'priority': '1.0', 'changefreq': 'monthly'},
            {'url': '/services', 'priority': '0.8', 'changefreq': 'monthly'},
            {'url': '/projects', 'priority': '0.8', 'changefreq': 'monthly'},
            {'url': '/contact', 'priority': '0.9', 'changefreq': 'monthly'},
            {'url': '/blog', 'priority': '0.9', 'changefreq': 'weekly'},
        ]
        blog_posts = BlogPost.objects.filter(status='published').order_by('-published_at')
        context = {
            'static_pages': static_pages,
            'blog_posts': blog_posts,
            'site_url': 'https://fixkraftdigital.co.ke',
        }
        template = loader.get_template('sitemap.xml')
        return HttpResponse(template.render(context, request), content_type='application/xml')
