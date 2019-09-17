from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework import permissions
from .documents import ProductDocument


class ProductViewSet( viewsets.ModelViewSet ):
    lookup_field        = 'id'
    serializer_class    = ProductSerializer
    permission_classes  = ( permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        t = self.request.query_params.get( 'title', None )
        f = self.request.query_params.get( 'features', None )
        d = self.request.query_params.get( 'description', None )
        products = []

        if t:
            search_result = ProductDocument.search().query( 'fuzzy', title=t )
            for hit in search_result:
                try:
                    p = Product.objects.get( pk=hit.id )
                    products.append( p )
                except Product.DoesNotExist:
                    print( f'Product with id={ hit.id } DoesNotExist ' )
            print(f'!!!NOTHING MATCH == { len( products ) } ')

        if f:
            search_result = ProductDocument.search().query( 'fuzzy', features=f )
            for hit in search_result:
                try:
                    p = Product.objects.get( pk=hit.id )
                    products.append( p )
                except Product.DoesNotExist:
                    print( f'Product with id={ hit.id } DoesNotExist ' )
            print(f'!!!NOTHING MATCH == { len( products ) } ')

        if d:
            search_result = ProductDocument.search().query( 'fuzzy', description=d )
            for hit in search_result:
                try:
                    p = Product.objects.get( pk=hit.id )
                    products.append( p )
                except Product.DoesNotExist:
                    print( f'Product with id={ hit.id } DoesNotExist ' )
            print(f'!!!NOTHING MATCH == { len( products ) } ')

            if ( len( products ) > 0 ):
                return set( products )

        return Product.objects.all()

    def get_serializer_context(self):
        request         = self.request
        current_user    = request.user if request.user else None

        return { 'request': request, 'user': current_user }

