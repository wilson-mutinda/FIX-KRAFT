from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename='blog')
urlpatterns = [
    # path('sitemap.xml', sitemap, name='sitemap'),
] + router.urls
