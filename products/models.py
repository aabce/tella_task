from django.db import models
from rest_framework.reverse import reverse
from django.conf import settings


class Product( models.Model ):
    title           = models.TextField( blank=False )
    description     = models.TextField( blank=False )
    features         = models.TextField( blank=True, null=True )
    user            = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='product', on_delete=models.CASCADE )
    img             = models.ImageField( upload_to='products', blank=True, null=True )

    def __str__( self ):
        return str( self.title )

    def get_api_url( self, request=None ):
        return reverse( 'products:product-detail', kwargs={ 'id': self.id  }, request=request )

