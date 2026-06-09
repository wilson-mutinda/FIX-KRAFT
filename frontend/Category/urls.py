from rest_framework.routers import DefaultRouter
from .views import MediaCategoryViewSet

router = DefaultRouter()

router.register(
    r'media-categories',
    MediaCategoryViewSet,
    basename='media-categories'
)

urlpatterns = router.urls
