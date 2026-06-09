from rest_framework.routers import DefaultRouter
from .views import MediahubViewSet

router = DefaultRouter()

router.register(
    r'mediahub',
    MediahubViewSet,
    basename='mediahub'
)

urlpatterns = router.urls
