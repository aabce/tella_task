from django.db.models import Q
from rest_framework import status
from rest_framework.test import APITestCase
import json
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from accounts.models import Profile
from accounts.serializers import UserSerializer, UserRegistrationSerializer
from rest_framework.reverse import reverse as api_reverse

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserAPITestCase( APITestCase ):
    def setUp(self):
        user_obj = User( username='Alice', email='alice_test@test.com', first_name='Alice' )
        user_obj.set_password( "somerandopassword" )
        user_obj.save()

        data = { 'rank': 'astronaut' }

        profile = Profile( user=user_obj, **data )
        profile.save()

    def test_user_login( self ):
        url = api_reverse( 'accounts:login' )
        data = {
            'email': 'alice_test@test.com',
            'password': "somerandopassword"
        }

        response = self.client.post( url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual( user_count, 1 )

    def test_post_user_wthout_user(self):
        # test the get list
        data = {"title": "Some random title", "content": "some more content"}
        url = api_reverse("accounts:user-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_user_with_user(self):
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials( HTTP_AUTHORIZATION='JWT ' + token_rsp )

        data = {
                'first_name': 'Marwin', 
                'last_name': 'Android',
                'email': 'marwin@galaxy.com',
                'username': 'Dont tell me abput life',
                'password': 'FREEZE?',
                'permissions': [],
                'profile':{
                    'rank': 'Paranoid Android'
                }
            }
        
        url = api_reverse("accounts:user-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_patch_user_with_user(self):
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials( HTTP_AUTHORIZATION='JWT ' + token_rsp )

        data_case_1 = {
                'id': 1,
                'url': user_obj.get_api_url(),
                'first_name': 'Marwin', 
            }

        url = user_obj.get_api_url()
        response = self.client.patch(url, data_case_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_user_password_by_user(self):
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials( HTTP_AUTHORIZATION='JWT ' + token_rsp )

        data_case_2 = {
                'id': 1,
                # 'url': user_obj.get_api_url(),
                'password': 'DontPanicAndCarryATowel',
            }

        user_obj = User.objects.first()
        url = user_obj.get_api_url()
        url += f'set-password/'
        print( f'url = { url }' )
        response = self.client.post( url, data_case_2, format='json' )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = api_reverse( 'accounts:login' )
        data = {
            'email': user_obj.email,
            'password': 'DontPanicAndCarryATowel'
        }

        response = self.client.post( url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list( self ):
        search_for = 'lice'
        res = User.objects.filter(
                Q(first_name__icontains=search_for)|
                Q(last_name__icontains=search_for)
            ).distinct()

        serializer = UserRegistrationSerializer( res, many=True )

        url = api_reverse( 'accounts:user-list' ) + f'?first_name={ search_for }'
        response = self.client.get( url, format='json' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )
        self.assertEqual( response.json()[ 0 ][ "first_name" ], serializer.data[ 0 ][ "first_name" ] )

    def test_get_item( self ):
        user = User.objects.first()
        data={}
        url = user.get_api_url()
        response = self.client.get( url, data, format='json' )
        self.assertEqual( response.status_code, status.HTTP_200_OK )
