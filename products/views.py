from rest_framework import viewsets
from .models import Product
from .search_manager import search_by_title, search_by_description, search_by_features
from .serializers import ProductSerializer
from rest_framework import permissions


class ProductViewSet( viewsets.ModelViewSet ):
    lookup_field        = 'id'
    serializer_class    = ProductSerializer
    permission_classes  = ( permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        if self.request.query_params:
            products = []

            products = [ *products, *search_by_title( self.request.query_params.get('title', None) ) ]
            products = [ *products, *search_by_description( self.request.query_params.get('description', None) ) ]
            products = [ *products, *search_by_features( self.request.query_params.get('features', None) ) ]

            return list( set( products ) )

        return Product.objects.all()

    def get_serializer_context(self):
        request         = self.request
        current_user    = request.user if request.user else None

        return { 'request': request, 'user': current_user }

