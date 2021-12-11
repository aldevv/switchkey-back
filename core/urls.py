from rest_framework.routers import DefaultRouter
from core.viewsets import BookmarkViewSet
from django.conf.urls import include
from django.urls import  path
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('bookmarks', BookmarkViewSet, basename='bookmarks')
urlpatterns = [
    path('', include(router.urls)),
    path('authtoken/', views.obtain_auth_token),
]
