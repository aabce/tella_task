from django.db.models import Q
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import Product
from .serializers import ProductSerializer
from .test_setups import MarketAPITestCaseSetUp, test_case_overview
from rest_framework.reverse import reverse as api_reverse
from faker import Factory
import uuid
import math
import random

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()
faker = Factory.create()

admin_user_password = uuid.uuid4()


class MarketAPITestCase( MarketAPITestCaseSetUp ):

    @test_case_overview
    def test_list_products( self ):
        url = api_reverse( 'products:product-list' )
        response = self.client.get( url, format='json' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    @test_case_overview
    def test_detail_product( self ):
        product = Product.objects.first()
        url = product.get_api_url()
        response = self.client.get( url, format='json' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )
        self.assertEqual( response.json()[ 'title' ], product.title )

    @test_case_overview
    def test_list_filter( self ):
        search_for = str( faker.word() )

        res = Product.objects.filter( title__icontains=search_for )
        print( f'RES={ len( list( res ) ) }' )

        url = api_reverse( 'products:product-list' )
        response = self.client.get( url, data={ 'title':search_for },format='json' )
        print( f'search_for={ search_for }' )
        # for _ in response.json():
        #     print( f'={ _.get( "id" ) }|{ _.get( "title" ) }' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    @test_case_overview
    def test_list_filter_with_misspell( self ):
        products = Product.objects.all()
        product = random.choice( list( products ) )
        search_for = str( product.title.split( ' ' )[ 0 ] )
        search_for = search_for.replace(  search_for[ math.floor( len( search_for )/2 ) ], '' )
        print( f'product={product}' )
        print( f'SearchFor={ search_for }' )

        res = Product.objects.filter( title__in=search_for )
        print( f'search output len={ len( list( res ) ) }' )

        url = api_reverse( 'products:product-list' )
        response = self.client.get( url, data={ 'title': search_for }, format='json' )
        for _ in response.json():
            print( f'={ _.get( "id" ) }|{ _.get( "title" ) }' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    @test_case_overview
    def test_patch_product_with_user(self):
        product = Product.objects.first()
        url = product.get_api_url()
        self.login_user()
        up_title = f'UPDATED TITLE  { product.title }'
        data = { 'title': up_title }
        serializer = ProductSerializer( product )
        response = self.client.patch( url, data, format='json' )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json()[ 'title' ], serializer.data[ 'title' ] )

    @test_case_overview
    def test_post_product_with_user(self):
        url = api_reverse( 'products:product-list' )
        self.login_user()
        data = {
            'title': faker.text(),
            'description': faker.text(),
        }
        response = self.client.post( url, data, format='json' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # data = {'img': super().generate_photo_file() }
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    @test_case_overview
    def test_delete_product_with_user(self):
        product = Product.objects.first()
        url = product.get_api_url()
        self.login_user()
        serializer = ProductSerializer( product )
        response = self.client.delete( url,  format='json' )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            Product.objects.get( pk=serializer.data[ 'id' ] )
            print( f'ERROR = { serializer.data }' )
        except Product.DoesNotExist:
            print( 'OK' )


