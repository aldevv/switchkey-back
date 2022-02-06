from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path
from core.viewsets import ProductViewSet, UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("products", ProductViewSet, basename="products")
urlpatterns = [
    path("", include(router.urls)),
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/registration/", include("dj_rest_auth.registration.urls")),
]
