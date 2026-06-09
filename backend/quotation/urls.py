from rest_framework.routers import DefaultRouter

from .views import QuotationViewSet

router = DefaultRouter()

router.register(
    'quotation',
    QuotationViewSet,
    basename='qoutation'
)

urlpatterns = router.urls
