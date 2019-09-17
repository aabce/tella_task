from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Permission, Profile, User
from accounts.filters import UserFilter 
from accounts.serializers import (
        PasswordSerializer,
        ProfileSerializer,
        UserSerializer,
        UserRegistrationSerializer,
)
from rest_framework import viewsets


class UserViewSet( viewsets.ModelViewSet ):
    lookup_field        = 'id'
    queryset            = User.objects.all()
    serializer_action_classes = {
        'list': UserRegistrationSerializer,
        'retrieve': UserRegistrationSerializer,
        'create': UserRegistrationSerializer,
        'update': UserRegistrationSerializer,
        'partial_update': UserRegistrationSerializer,
        'destroy': UserRegistrationSerializer,
        'set_password': PasswordSerializer,
    }
    filter_classes = ( UserFilter, )

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[ self.action ]
        except ( KeyError, AttributeError ):
            return super().get_serializer_class()

    def get_serializer_context(self):
        request = self.request
        return { 'request': request }

    @action( methods=['post'], detail=True, url_path='set-password', url_name='set-password', permission_classes=[] )
    def set_password( self, request, id=None ):
        user = self.get_object()
        serializer = self.get_serializer( data=request.data )
        if serializer.is_valid():
            user.set_password( serializer.data['password'] )
            user.save()
            return Response( status=status.HTTP_200_OK )
        else:
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )


    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)

