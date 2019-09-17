from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import ProductViewSet

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter() 
router.register( r'', ProductViewSet, basename='product' )

urlpatterns = [
    path( r'', include( router.urls )  ),
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )


