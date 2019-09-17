from .models import Product
from .documents import ProductDocument


def search_by_title( query_value ):
    print( f'>> search_by_title:{ query_value }' )
    if query_value:
        return get_models( ProductDocument.search().query( 'fuzzy', title=query_value ) )
    return []


def search_by_description( query_value ):
    print(f'>> search_by_descriptions:{query_value}')
    if query_value:
        return get_models( ProductDocument.search().query( 'fuzzy', description=query_value ) )
    return []


def search_by_features( query_value ):
    print(f'>> search_by_features:{query_value}')
    if query_value:
        return get_models( ProductDocument.search().query( 'fuzzy', features=query_value ) )
    return []


def get_models( documents_found ):
    print( f'FOUND == { len( list( documents_found ) ) }' )
    products = []

    if documents_found is None or len( list( documents_found ) ) == 0:
        return products

    for hit in documents_found:
        try:
            p = Product.objects.get( pk=hit.id )
            products.append( p )
        except Product.DoesNotExist:
            print( f'Product with id={ hit.id } DoesNotExist ' )
    return products
