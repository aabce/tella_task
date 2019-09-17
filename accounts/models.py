from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.reverse import reverse


class User( AbstractUser ):
    username = models.CharField( max_length=200, blank=True, null=True )
    email = models.EmailField( unique=True )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__( self ):
        return str( self.email )

    def get_api_url( self, request=None ):
        return reverse( 'accounts:user-detail', kwargs={ 'id':self.id  }, request=request )

  
class Profile( models.Model ):
    rank = models.CharField( max_length=250, blank=True, null=True )
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile' )

    def __str__( self ):
        return str( self.rank )

    def get_api_url( self, request ):
        return reverse( 'api-users:profile', kwargs={ 'id':self.id  }, request=request )


class Permission( models.Model ):
    user = models.ManyToManyField( settings.AUTH_USER_MODEL, related_name='permissions' )
    
    name = models.CharField( max_length=200 )
    level = models.PositiveIntegerField( default=0 ) 

    def __str__( self ):
        return str( self.name )

    def get_api_url( self, request=None ):
        return reverse( 'accounts:permissions', kwargs={ 'id':self.id  }, request=request )

