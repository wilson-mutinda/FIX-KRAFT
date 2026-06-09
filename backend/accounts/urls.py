from django.urls import path

from .views import (
    RegisterView,
    UserView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [

    # REGISTER
    path(
        'register/',
        RegisterView.as_view()
    ),

    # LOGIN
    path(
        'token/',
        TokenObtainPairView.as_view()
    ),

    # REFRESH
    path(
        'token/refresh/',
        TokenRefreshView.as_view()
    ),

    # CURRENT USER
    path(
        'me/',
        UserView.as_view()
    ),
]