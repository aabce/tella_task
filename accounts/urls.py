from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
    UserViewSet,
    # PermissionViewSet,
    # ProfileViewSet
)

router = DefaultRouter() 
router.register( r'profiles', UserViewSet )
# router.register(r'permissions', UserViewSet, base_name='permissions',)
# router.register(r'profiles', UserViewSet, base_name='profiles',)

urlpatterns = [
    path( r'login', obtain_jwt_token, name='login' ),
    path( r'', include( router.urls )  ),
]


