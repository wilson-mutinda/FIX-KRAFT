from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import InquiryViewSet, requirements_api

router = DefaultRouter()

router.register(
    r'inquiries',
    InquiryViewSet,
    basename='inquiries'
)

urlpatterns = [
    path('', include(router.urls)),
    path('requirements/<str:token>/', requirements_api, name='requirements_api'),
]
